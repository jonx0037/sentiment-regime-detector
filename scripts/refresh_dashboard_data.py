#!/usr/bin/env python3
"""
Refresh dashboard data: collect recent news via NewsAPI, score sentiment,
aggregate daily, and push to Railway PostgreSQL.

Also updates CISS (ECB API) and VIX (yfinance) market indicators.

Usage:
    python scripts/refresh_dashboard_data.py
"""

import os
import sys
import uuid
import json
from datetime import datetime, timedelta
from collections import defaultdict

import requests
import psycopg2
from psycopg2.extras import execute_values
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# ── Configuration ──────────────────────────────────────────────────────────────

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:rUxfHXftLGrOpqvQTbQynXfHXfnQrJOV@yamabiko.proxy.rlwy.net:19328/railway",
)
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "296ce429-3a4c-4abc-a71e-cb4486fb6bd3")
FINNHUB_API_KEY = os.environ.get(
    "FINNHUB_API_KEY", "d5vq0a9r01qihi8nc2i0d5vq0a9r01qihi8nc2ig"
)

# Queries per asset class for NewsAPI
ASSET_QUERIES = {
    "equity": ["stock market", "S&P 500", "Wall Street", "NASDAQ", "equity markets"],
    "crypto": ["cryptocurrency", "bitcoin", "ethereum", "crypto market"],
    "forex": ["forex", "currency exchange", "US dollar", "EUR USD"],
    "commodity": ["gold price", "oil market", "commodities", "crude oil"],
}

# ── Sentiment Scoring ──────────────────────────────────────────────────────────

vader = SentimentIntensityAnalyzer()


def score_text(text: str) -> dict:
    """Score a text using VADER + TextBlob, return compound metrics."""
    try:
        vs = vader.polarity_scores(str(text))
        vader_compound = vs["compound"]
        vader_pos = vs["pos"]
        vader_neg = vs["neg"]
        vader_neu = vs["neu"]
    except Exception:
        vader_compound, vader_pos, vader_neg, vader_neu = 0.0, 0.0, 0.0, 1.0

    try:
        tb = TextBlob(str(text)).sentiment
        tb_polarity = tb.polarity
    except Exception:
        tb_polarity = 0.0

    # Ensemble: weight VADER more heavily (better for financial text)
    ensemble = 0.6 * vader_compound + 0.4 * tb_polarity

    return {
        "compound": ensemble,
        "positive": vader_pos,
        "negative": vader_neg,
        "neutral": vader_neu,
    }


# ── News Collection via NewsAPI ────────────────────────────────────────────────


def collect_newsapi(asset_class: str, from_date: str, to_date: str) -> list[dict]:
    """Fetch articles from NewsAPI for an asset class."""
    queries = ASSET_QUERIES.get(asset_class, [])
    articles = []
    seen_urls = set()

    for query in queries:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "from": from_date,
                    "to": to_date,
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": 100,
                    "apiKey": NEWS_API_KEY,
                },
                timeout=15,
            )
            if resp.status_code != 200:
                print(
                    f"    NewsAPI error for '{query}': {resp.status_code} {resp.text[:200]}"
                )
                continue

            data = resp.json()
            for art in data.get("articles", []):
                url = art.get("url", "")
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                title = art.get("title") or ""
                desc = art.get("description") or ""
                text = f"{title}. {desc}".strip()
                if len(text) < 20:
                    continue

                published = art.get("publishedAt", "")
                try:
                    pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                except Exception:
                    pub_dt = datetime.utcnow()

                articles.append(
                    {
                        "text": text,
                        "published": pub_dt,
                        "asset_class": asset_class,
                        "source": "newsapi",
                    }
                )
        except Exception as e:
            print(f"    Error fetching '{query}': {e}")

    return articles


# ── Finnhub News Collection ────────────────────────────────────────────────────


def collect_finnhub_news(from_date: str, to_date: str) -> list[dict]:
    """Fetch general market news from Finnhub."""
    articles = []
    try:
        resp = requests.get(
            "https://finnhub.io/api/v1/news",
            params={"category": "general", "token": FINNHUB_API_KEY},
            timeout=15,
        )
        if resp.status_code != 200:
            print(f"    Finnhub error: {resp.status_code}")
            return []

        for art in resp.json():
            headline = art.get("headline", "")
            summary = art.get("summary", "")
            text = f"{headline}. {summary}".strip()
            if len(text) < 20:
                continue

            ts = art.get("datetime", 0)
            pub_dt = datetime.utcfromtimestamp(ts) if ts else datetime.utcnow()

            # Classify by keywords
            text_lower = text.lower()
            if any(
                k in text_lower for k in ["crypto", "bitcoin", "ethereum", "blockchain"]
            ):
                ac = "crypto"
            elif any(
                k in text_lower
                for k in ["forex", "currency", "dollar", "yen", "euro exchange"]
            ):
                ac = "forex"
            elif any(
                k in text_lower for k in ["gold", "oil", "commodity", "crude", "metal"]
            ):
                ac = "commodity"
            else:
                ac = "equity"

            articles.append(
                {
                    "text": text,
                    "published": pub_dt,
                    "asset_class": ac,
                    "source": "finnhub",
                }
            )
    except Exception as e:
        print(f"    Finnhub error: {e}")

    return articles


# ── Daily Aggregation ──────────────────────────────────────────────────────────


def aggregate_to_daily(scored_articles: list[dict]) -> list[tuple]:
    """Aggregate scored articles into daily sentiment_indices rows."""
    # Group by (date, asset_class)
    buckets = defaultdict(list)
    for art in scored_articles:
        day = art["published"].strftime("%Y-%m-%d")
        buckets[(day, art["asset_class"])].append(art["scores"])

    rows = []
    now = datetime.utcnow().isoformat() + "+00:00"

    for (day, ac), scores_list in sorted(buckets.items()):
        n = len(scores_list)
        mean_compound = sum(s["compound"] for s in scores_list) / n
        mean_pos = sum(s["positive"] for s in scores_list) / n
        mean_neg = sum(s["negative"] for s in scores_list) / n
        std_compound = (
            (
                sum((s["compound"] - mean_compound) ** 2 for s in scores_list)
                / max(n - 1, 1)
            )
            ** 0.5
            if n > 1
            else 0.0
        )

        dt = datetime.strptime(day, "%Y-%m-%d")
        period_start = dt.isoformat() + "+00:00"
        period_end = (dt + timedelta(days=1)).isoformat() + "+00:00"

        rows.append(
            (
                str(uuid.uuid4()),  # id
                ac,  # asset_class
                None,  # source (NULL = aggregated)
                period_start,  # period_start
                period_end,  # period_end
                "daily",  # granularity
                mean_compound,  # mean_compound
                std_compound,  # std_compound
                n,  # sample_count
                mean_pos,  # positive_ratio
                mean_neg,  # negative_ratio
                None,  # sentiment_momentum
                None,  # sentiment_acceleration
                now,  # created_at
                now,  # updated_at
            )
        )

    return rows


# ── VIX Update via yfinance ────────────────────────────────────────────────────


def update_vix(conn, from_date: str):
    """Fetch and insert recent VIX data via yfinance."""
    try:
        conn.rollback()  # Clear any failed transaction state
        import yfinance as yf

        vix = yf.download("^VIX", start=from_date, progress=False)
        if vix.empty:
            print("  No VIX data returned")
            return 0

        cur = conn.cursor()

        # Get existing dates to avoid duplicates
        cur.execute(
            "SELECT DISTINCT date::date FROM market_data WHERE symbol = '^VIX' AND date >= %s",
            (from_date,),
        )
        existing = {str(r[0]) for r in cur.fetchall()}

        now = datetime.utcnow().isoformat() + "+00:00"
        rows = []
        for idx, row in vix.iterrows():
            day = (
                idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)[:10]
            )
            if day in existing:
                continue
            # Handle both single and multi-level columns
            try:
                close_val = (
                    float(row["Close"].iloc[0])
                    if hasattr(row["Close"], "iloc")
                    else float(row["Close"])
                )
                open_val = (
                    float(row["Open"].iloc[0])
                    if hasattr(row["Open"], "iloc")
                    else float(row["Open"])
                )
                high_val = (
                    float(row["High"].iloc[0])
                    if hasattr(row["High"], "iloc")
                    else float(row["High"])
                )
                low_val = (
                    float(row["Low"].iloc[0])
                    if hasattr(row["Low"], "iloc")
                    else float(row["Low"])
                )
                vol_val = (
                    float(row["Volume"].iloc[0])
                    if hasattr(row["Volume"], "iloc")
                    else float(row["Volume"])
                )
            except Exception:
                close_val = float(row.iloc[0]) if len(row) > 0 else 0
                open_val = close_val
                high_val = close_val
                low_val = close_val
                vol_val = 0

            # market_data schema requires: id, symbol, asset_type, date, open, high, low, close, volume, source, created_at, updated_at
            rows.append(
                (
                    str(uuid.uuid4()),
                    "^VIX",
                    "volatility_index",
                    day,
                    open_val,
                    high_val,
                    low_val,
                    close_val,
                    int(vol_val),
                    "yfinance",
                    now,
                    now,
                )
            )

        if rows:
            execute_values(
                cur,
                """INSERT INTO market_data (id, symbol, asset_type, date, open, high, low, close, volume, source, created_at, updated_at)
                   VALUES %s ON CONFLICT DO NOTHING""",
                rows,
            )
            conn.commit()
            print(f"  ✅ Inserted {len(rows)} new VIX rows")
        else:
            print(f"  ℹ️  VIX already up to date")
        return len(rows)
    except Exception as e:
        print(f"  ❌ VIX update failed: {e}")
        return 0


# ── CISS Update via ECB ────────────────────────────────────────────────────────


def update_ciss(conn, from_date: str):
    """Fetch and insert recent CISS data from ECB Statistical Data Warehouse."""
    try:
        conn.rollback()  # Clear any failed transaction state
        # ECB SDMX REST API for CISS composite indicator (EU aggregate)
        url = (
            f"https://data-api.ecb.europa.eu/service/data/CISS/D.EU.CISS_CI?"
            f"startPeriod={from_date}&format=csvdata"
        )
        resp = requests.get(url, timeout=30, headers={"Accept": "text/csv"})
        if resp.status_code != 200:
            print(
                f"  ⚠️  ECB CISS API returned {resp.status_code}, trying alternate URL..."
            )
            # Try alternate SDMX endpoint
            url2 = f"https://sdw-wsrest.ecb.europa.eu/service/data/CISS/D.EU.CISS_CI?startPeriod={from_date}&format=csvdata"
            resp = requests.get(url2, timeout=30)
            if resp.status_code != 200:
                print(f"  ❌ ECB CISS API error: {resp.status_code}")
                return 0

        import csv
        from io import StringIO

        reader = csv.DictReader(StringIO(resp.text))

        cur = conn.cursor()
        cur.execute(
            "SELECT DISTINCT date::date FROM stress_indices WHERE date >= %s",
            (from_date,),
        )
        existing = {str(r[0]) for r in cur.fetchall()}

        now = datetime.utcnow().isoformat() + "+00:00"
        rows = []
        for record in reader:
            day = record.get("TIME_PERIOD", "")
            val = record.get("OBS_VALUE", "")
            if not day or not val or day in existing:
                continue
            try:
                ciss_val = float(val)
            except ValueError:
                continue

            # stress_indices schema: id, source, date, region, value, created_at, updated_at
            rows.append(
                (
                    str(uuid.uuid4()),
                    "ecb_ciss",
                    day,
                    "EU",
                    ciss_val,
                    now,
                    now,
                )
            )

        if rows:
            execute_values(
                cur,
                """INSERT INTO stress_indices (id, source, date, region, value, created_at, updated_at)
                   VALUES %s ON CONFLICT DO NOTHING""",
                rows,
            )
            conn.commit()
            print(f"  ✅ Inserted {len(rows)} new CISS rows")
        else:
            print(f"  ℹ️  CISS already up to date")
        return len(rows)
    except Exception as e:
        print(f"  ❌ CISS update failed: {e}")
        return 0


# ── Main ───────────────────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print("DASHBOARD DATA REFRESH")
    print("=" * 60)

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Find the latest date in sentiment_indices
    cur.execute(
        "SELECT MAX(period_start)::date FROM sentiment_indices WHERE source IS NULL"
    )
    latest = cur.fetchone()[0]
    if latest:
        from_date = (latest + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        from_date = "2026-01-01"

    to_date = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"\n📅 Filling gap: {from_date} → {to_date}")

    if from_date >= to_date:
        print("✅ Sentiment data is already up to date!")
    else:
        # ── Step 1: Collect news ──────────────────────────────────────────
        print(f"\n📰 Step 1: Collecting news articles...")
        all_articles = []

        for ac in ["equity", "crypto", "forex", "commodity"]:
            print(f"  Collecting {ac}...")
            articles = collect_newsapi(ac, from_date, to_date)
            print(f"    → {len(articles)} articles")
            all_articles.extend(articles)

        print(f"  Collecting Finnhub general news...")
        finnhub = collect_finnhub_news(from_date, to_date)
        print(f"    → {len(finnhub)} articles")
        all_articles.extend(finnhub)

        print(f"\n  Total articles collected: {len(all_articles)}")

        # ── Step 2: Score sentiment ───────────────────────────────────────
        print(f"\n📊 Step 2: Scoring sentiment...")
        for i, art in enumerate(all_articles):
            art["scores"] = score_text(art["text"])
            if (i + 1) % 200 == 0:
                print(f"    Scored {i + 1}/{len(all_articles)}...")
        print(f"    ✅ Scored all {len(all_articles)} articles")

        # ── Step 3: Aggregate to daily ────────────────────────────────────
        print(f"\n📈 Step 3: Aggregating to daily indices...")
        daily_rows = aggregate_to_daily(all_articles)
        print(f"    Generated {len(daily_rows)} daily index rows")

        # Show breakdown
        from collections import Counter

        ac_counts = Counter(r[1] for r in daily_rows)
        for ac, count in sorted(ac_counts.items()):
            dates = [r[3][:10] for r in daily_rows if r[1] == ac]
            print(f"    {ac}: {count} days ({min(dates)} → {max(dates)})")

        # ── Step 4: Insert into Railway DB ────────────────────────────────
        print(f"\n💾 Step 4: Inserting into Railway PostgreSQL...")
        execute_values(
            cur,
            """INSERT INTO sentiment_indices (
                id, asset_class, source, period_start, period_end, granularity,
                mean_compound, std_compound, sample_count, positive_ratio,
                negative_ratio, sentiment_momentum, sentiment_acceleration,
                created_at, updated_at
            ) VALUES %s""",
            daily_rows,
            page_size=500,
        )
        conn.commit()
        print(f"    ✅ Inserted {len(daily_rows)} rows")

    # ── Step 5: Update market indicators ──────────────────────────────
    print(f"\n📉 Step 5: Updating VIX...")
    update_vix(conn, from_date)

    print(f"\n🏛️  Step 6: Updating CISS...")
    update_ciss(conn, from_date)

    # ── Step 7: Verify ────────────────────────────────────────────────
    conn.rollback()  # Clear any failed transaction state before verify
    cur = conn.cursor()
    print(f"\n{'=' * 60}")
    print("VERIFICATION")
    print(f"{'=' * 60}")

    cur.execute("""
        SELECT asset_class, COUNT(*), MIN(period_start)::date, MAX(period_start)::date
        FROM sentiment_indices WHERE source IS NULL
        GROUP BY asset_class ORDER BY asset_class
    """)
    print("\nSentiment indices:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]} days ({row[2]} → {row[3]})")

    cur.execute(
        "SELECT COUNT(*), MAX(date)::date FROM market_data WHERE symbol = '^VIX'"
    )
    vix_row = cur.fetchone()
    print(f"\nVIX: {vix_row[0]} rows, latest = {vix_row[1]}")

    cur.execute("SELECT COUNT(*), MAX(date)::date FROM stress_indices")
    ciss_row = cur.fetchone()
    print(f"CISS: {ciss_row[0]} rows, latest = {ciss_row[1]}")

    cur.close()
    conn.close()
    print(f"\n🎉 Dashboard data refresh complete!")


if __name__ == "__main__":
    main()
