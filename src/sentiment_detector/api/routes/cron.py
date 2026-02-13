"""Automated data refresh endpoint for scheduled cron execution.

This endpoint is called by Railway's cron service daily to keep
sentiment data, VIX, and GARCH results up-to-date automatically.
"""

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from sentiment_detector.core.database import get_session

logger = logging.getLogger(__name__)

router = APIRouter()

FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "d5vq0a9r01qihi8nc2i0d5vq0a9r01qihi8nc2ig")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "296ce429-3a4c-4abc-a71e-cb4486fb6bd3")


async def _fetch_finnhub_news() -> list[dict[str, Any]]:
    """Fetch recent financial news from Finnhub."""
    import httpx

    articles = []
    today = datetime.now(timezone.utc)
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    categories = ["general", "forex", "crypto"]
    async with httpx.AsyncClient(timeout=15) as client:
        for cat in categories:
            try:
                resp = await client.get(
                    "https://finnhub.io/api/v1/news",
                    params={"category": cat, "minId": 0, "token": FINNHUB_API_KEY},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data[:50]:
                        articles.append(
                            {
                                "headline": item.get("headline", ""),
                                "summary": item.get("summary", ""),
                                "source": "finnhub",
                                "category": item.get("category", cat),
                                "datetime": datetime.fromtimestamp(
                                    item.get("datetime", 0), tz=timezone.utc
                                ),
                            }
                        )
            except Exception as e:
                logger.warning(f"Finnhub {cat} error: {e}")

    return articles


async def _fetch_newsapi_news() -> list[dict[str, Any]]:
    """Fetch recent news from NewsAPI."""
    import httpx

    articles = []
    today = datetime.now(timezone.utc)
    from_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    queries = [
        "stock market OR S&P 500 OR Wall Street",
        "bitcoin OR ethereum OR cryptocurrency",
        "oil price OR gold price OR commodities",
        "forex OR currency OR US dollar",
    ]
    asset_map = ["equity", "crypto", "commodity", "forex"]

    async with httpx.AsyncClient(timeout=15) as client:
        for query, asset in zip(queries, asset_map):
            try:
                resp = await client.get(
                    "https://newsapi.org/v2/everything",
                    params={
                        "q": query,
                        "from": from_date,
                        "sortBy": "publishedAt",
                        "pageSize": 25,
                        "apiKey": NEWS_API_KEY,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("articles", []):
                        articles.append(
                            {
                                "headline": item.get("title", ""),
                                "summary": item.get("description", ""),
                                "source": "newsapi",
                                "category": asset,
                                "datetime": datetime.fromisoformat(
                                    item.get("publishedAt", "").replace("Z", "+00:00")
                                )
                                if item.get("publishedAt")
                                else today,
                            }
                        )
            except Exception as e:
                logger.warning(f"NewsAPI {asset} error: {e}")

    return articles


def _score_text(text: str) -> dict[str, float]:
    """Score a text using VADER (fast, no GPU required)."""
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        return {
            "compound": scores["compound"],
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"],
        }
    except ImportError:
        # Fallback: simple keyword-based scoring
        text_lower = text.lower()
        pos_words = ["gain", "rise", "bull", "surge", "rally", "up", "high", "growth", "profit"]
        neg_words = ["loss", "fall", "bear", "crash", "drop", "down", "low", "decline", "risk"]
        pos_count = sum(1 for w in pos_words if w in text_lower)
        neg_count = sum(1 for w in neg_words if w in text_lower)
        total = pos_count + neg_count + 1
        compound = (pos_count - neg_count) / total
        return {
            "compound": compound,
            "positive": pos_count / total,
            "negative": neg_count / total,
            "neutral": 1 - (pos_count + neg_count) / total,
        }


def _classify_asset(category: str) -> str:
    """Map article category to asset class."""
    cat = category.lower()
    if cat in ("crypto", "cryptocurrency", "bitcoin"):
        return "crypto"
    elif cat in ("forex", "currency"):
        return "forex"
    elif cat in ("commodity", "commodities", "oil", "gold"):
        return "commodity"
    else:
        return "equity"


@router.post("/refresh")
async def refresh_sentiment_data() -> dict:
    """
    Automated daily data refresh endpoint.

    Fetches news from Finnhub and NewsAPI, scores with VADER,
    and inserts aggregated daily sentiment into the database.
    Called by Railway cron service.
    """
    import uuid

    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")

    # Step 1: Fetch news
    logger.info("Cron refresh: fetching news...")
    finnhub_articles = await _fetch_finnhub_news()
    newsapi_articles = await _fetch_newsapi_news()
    all_articles = finnhub_articles + newsapi_articles
    logger.info(
        f"Cron refresh: {len(finnhub_articles)} Finnhub + {len(newsapi_articles)} NewsAPI = {len(all_articles)} total"
    )

    if not all_articles:
        return {"status": "no_articles", "message": "No articles fetched", "timestamp": today_str}

    # Step 2: Score and aggregate by asset class and date
    from collections import defaultdict

    daily_scores: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    for article in all_articles:
        text_content = f"{article['headline']} {article.get('summary', '')}"
        if len(text_content.strip()) < 10:
            continue

        scores = _score_text(text_content)
        asset = _classify_asset(article.get("category", "general"))
        date_key = article["datetime"].strftime("%Y-%m-%d")

        daily_scores[date_key][asset].append(scores)

    # Step 3: Insert into database
    inserted = 0
    async for session in get_session():
        for date_str, asset_data in daily_scores.items():
            for asset_class, scores_list in asset_data.items():
                if not scores_list:
                    continue

                compounds = [s["compound"] for s in scores_list]
                positives = [s["positive"] for s in scores_list]
                negatives = [s["negative"] for s in scores_list]

                mean_compound = sum(compounds) / len(compounds)
                std_compound = (
                    (sum((c - mean_compound) ** 2 for c in compounds) / len(compounds)) ** 0.5
                    if len(compounds) > 1
                    else 0.0
                )

                # Check if row already exists for this date/asset
                existing = await session.execute(
                    text("""
                        SELECT COUNT(*) FROM sentiment_indices
                        WHERE asset_class = :ac AND source IS NULL
                        AND DATE(period_start) = :dt
                    """),
                    {"ac": asset_class, "dt": date_str},
                )
                if existing.scalar() > 0:
                    # Update existing row
                    await session.execute(
                        text("""
                            UPDATE sentiment_indices
                            SET mean_compound = :mc, std_compound = :sc,
                                sample_count = :cnt, positive_ratio = :pr,
                                negative_ratio = :nr, updated_at = :now
                            WHERE asset_class = :ac AND source IS NULL
                            AND DATE(period_start) = :dt
                        """),
                        {
                            "mc": mean_compound,
                            "sc": std_compound,
                            "cnt": len(scores_list),
                            "pr": sum(positives) / len(positives),
                            "nr": sum(negatives) / len(negatives),
                            "now": now.isoformat(),
                            "ac": asset_class,
                            "dt": date_str,
                        },
                    )
                else:
                    # Insert new row
                    period_start = f"{date_str}T00:00:00+00:00"
                    next_day = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
                    period_end = f"{next_day.strftime('%Y-%m-%d')}T00:00:00+00:00"

                    await session.execute(
                        text("""
                            INSERT INTO sentiment_indices (
                                id, asset_class, source, period_start, period_end,
                                granularity, mean_compound, std_compound, sample_count,
                                positive_ratio, negative_ratio, created_at, updated_at
                            ) VALUES (
                                :id, :ac, NULL, :ps, :pe, 'daily', :mc, :sc, :cnt,
                                :pr, :nr, :now, :now
                            )
                        """),
                        {
                            "id": str(uuid.uuid4()),
                            "ac": asset_class,
                            "ps": period_start,
                            "pe": period_end,
                            "mc": mean_compound,
                            "sc": std_compound,
                            "cnt": len(scores_list),
                            "pr": sum(positives) / len(positives),
                            "nr": sum(negatives) / len(negatives),
                            "now": now.isoformat(),
                        },
                    )

                inserted += 1

        await session.commit()

    logger.info(f"Cron refresh: inserted/updated {inserted} rows")

    return {
        "status": "success",
        "timestamp": today_str,
        "articles_fetched": len(all_articles),
        "rows_upserted": inserted,
        "sources": {
            "finnhub": len(finnhub_articles),
            "newsapi": len(newsapi_articles),
        },
    }
