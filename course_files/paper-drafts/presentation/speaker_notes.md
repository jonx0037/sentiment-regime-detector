# Speaker Notes — Cross-Asset Sentiment Regime Detector
**Target: ~11 minutes total (~60 seconds per slide)**

---

## Slide 1 — Title (30 seconds)

Good [morning/afternoon]. My name is Jonathan Rocha, and today I'm presenting my capstone project: the Cross-Asset Sentiment Regime Detector — a system that automates market psychology analysis using multi-source NLP.

The core idea is simple: can we use natural language processing on financial text to detect when market regimes are about to shift?

---

## Slide 2 — Problem & Motivation (60 seconds)

Financial markets generate enormous amounts of unstructured text every day — news articles, social media posts, analyst reports, and central bank communications.

Research shows that sentiment shifts across asset classes often precede regime transitions — the moments when markets move from calm to crisis, or vice versa. But monitoring this manually across multiple markets at scale is impossible.

The research gap here is significant: existing approaches focus on single-asset sentiment analysis. No one has built a unified framework that integrates NLP sentiment signals across multiple asset classes with volatility regime models.

That's the goal of this project — build an automated cross-asset sentiment regime detection system.

---

## Slide 3 — Data & NLP Pipeline (75 seconds)

The study uses a multi-source financial text corpus of approximately 33 million documents spanning January 2005 through August 2025, producing 4,490 market-aligned daily observations.

The corpus covers four asset classes: equities via SPY-related news, crypto via Bitcoin social media and news, forex via EUR/USD central bank communications, and commodities via gold-related reports.

For sentiment extraction, I use an ensemble transformer model — a domain-specific architecture fine-tuned on financial text. This produces daily aggregated sentiment scores, including compound polarity and cross-asset components.

On the right you can see the live sentiment dashboard showing actual daily sentiment scores across all four asset classes — this is what the system produces in real time.

The feature engineering pipeline produces 22 engineered features per daily observation, organized into four categories: sentiment level and polarity, dispersion and divergence metrics, market risk indicators, and temporal dynamics.

---

## Slide 4 — Two-Layer Architecture (75 seconds)

The detection system uses a two-layer architecture.

Layer 1 is GARCH(1,1) volatility modeling — applied independently to each asset. This captures time-varying volatility clustering and extracts features of conditional variance, shock magnitude, and persistence.

Layer 2 is a Statistical Jump Model with a jump penalty selected through data-driven cross-validation. This model detects regime transitions in the combined feature space by identifying structural breaks in the multivariate time series.

The system classifies each day into one of four regime states: Low Volatility for calm, stable markets, Normal for typical conditions, Elevated for increasing uncertainty, and High Volatility for crisis or extreme stress periods.

On the right you can see the GARCH and regime dashboard from the production system, showing real-time volatility estimates and regime classifications.

An additional network layer computes Transfer Entropy between sentiment streams to measure cross-asset information flow, which feeds into our third hypothesis.

---

## Slide 5 — Validation Framework (60 seconds)

For validation, I use walk-forward cross-validation with a 756-day training window, 63-day test window, and a 5-day purge gap to prevent look-ahead bias.

The study tests three pre-registered hypotheses. H1 asks whether sentiment leads regime transitions. H2 tests if cross-asset sentiment divergence increases before transitions. And H3 examines whether network connectedness rises during pre-crisis periods.

The figure on the right shows our regime labels overlaid on the VIX during the COVID period — you can see the system correctly identifies the transition to high volatility in March 2020.

---

## Slide 6 — Classification Performance (60 seconds)

The classification results are strong. Overall accuracy is 92.84% with a weighted F1 of 0.9236.

My primary metric is the Matthews Correlation Coefficient (MCC) because it properly accounts for class imbalance across four regime states. We achieve an MCC of 0.8279, which indicates excellent classification performance.

Transition accuracy — how well the model detects the actual regime change points — is 80.10%, which is particularly important because transitions are where the most actionable information lies.

The confusion matrix on the right shows strong diagonal performance, with most misclassifications occurring between adjacent regime states, which makes intuitive sense since neighboring regimes share similar characteristics.

---

## Slide 7 — H1: Sentiment Lead Time (60 seconds)

Now let's look at the hypothesis results individually, starting with H1.

H1 asked whether individual sentiment leads regime transitions by one to five days. This was NOT confirmed. The strongest lead-lag alignment was at lag 0, indicating no meaningful 1-to-5-day lead was detected globally.

Only 1 event window — the COVID-19 crash — showed localized lead behavior, but project-level confirmation required at least 2 event windows.

The figure on the right shows the lead-time analysis summary, visualizing the lag distribution across event windows. You can see the concentration at lag 0.

The takeaway: standalone sentiment is not a reliable leading indicator across all market contexts. But as we'll see in the next slide, that's not the whole story.

---

## Slide 8 — H2 & H3: Divergence & Network Effects (75 seconds)

This is the core contribution of the project.

H2 IS supported. Cross-asset sentiment divergence — when different assets' sentiment signals disagree — is significantly higher before regime transitions. The divergence ratio is 1.19 times, with a t-statistic of 18.73, p-value below 0.001, and a Cohen's d of 0.58. The top figure on the right shows the divergence distribution comparing stable and transition periods.

This is the project's strongest finding: it's the disagreement between markets that signals trouble, not sentiment alone.

H3 is also supported. Network connectedness, measured through Transfer Entropy, shows significant separation between stable and transition regimes — TCI of 0.5402 for stable periods versus 0.4569 during transitions. The ANOVA F-statistic is 427.44 with p below 0.001. The bottom figure shows this connectedness comparison across regime states.

Together, H2 and H3 confirm that cross-asset dynamics — divergence and information flow — are the key predictive signals.

---

## Slide 9 — Live Production Dashboard (60 seconds)

To make this research actionable, I built a production dashboard that runs daily automated updates.

The backend is FastAPI with Python, connected to a PostgreSQL database hosted on Railway, with a daily CRON job that refreshes sentiment data, GARCH estimates, and regime classifications.

The frontend is built with Next.js and TypeScript using Recharts for visualization, deployed on Vercel.

What you see on the right is the live dashboard showing the regime overview — current regime state, historical regime classifications, and the underlying metrics. This is publicly accessible and updated daily.

---

## Slide 10 — Discussion & Limitations (60 seconds)

To summarize the key findings: cross-asset divergence is the strongest signal. When markets disagree on sentiment, regime transitions are more likely. Network effects confirm that information cascades during transitions. But individual sentiment-to-regime lag is not reliable on its own.

There are important limitations. Computationally, repeated cross-validation tuning and rolling validation are expensive, and transformer inference latency may limit near-real-time operation on large data streams. Mixed-frequency alignment between irregular text arrivals and regular market bars introduces noise, especially during periods of sparse news. Data quality is also a concern — bots, sarcasm, and selection bias in public discourse affect representativeness. And the design is fundamentally correlational, so observed relationships may not be causal.

---

## Slide 11 — Conclusion & Future Work (45 seconds)

In terms of contributions, this is the first unified framework that combines NLP sentiment analysis with volatility-regime detection across multiple asset classes. The novel cross-asset divergence metric is a genuine contribution to the field. The production dashboard demonstrates real-world deployment, and we achieve 92.84% accuracy with strong MCC on a 4-class problem.

Future directions include adaptive model weighting, such as IMCA-style recalibration; incorporating multimodal signals, such as earnings-call audio; high-frequency decomposition to test whether lead-time effects persist at intraday levels; expanding to additional asset classes, such as bonds and REITs; extending to multilingual financial discourse; and pursuing more rigorous causal identification.

Thank you. I'm happy to take any questions.
