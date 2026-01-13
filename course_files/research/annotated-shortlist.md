# Annotated Shortlist: Sentiment-Enhanced Regime Detection and Spillover Analysis

## Overview

This document provides an annotated shortlist of academic papers relevant to the development of a cross-asset sentiment regime detection system. Each entry summarizes the data sources, models used, regime/spillover insights, and backtesting or practical impact relevant to your project.

The goal is to identify key methodologies and findings that can inform your approach to building a robust sentiment-based regime detector.

## Tabular Summary

| Paper | Data | Sentiment model | Regime/Spillover method | Key finding | Reuse in pipeline |
| --- | --- | --- | --- | --- | --- |
| Caferra 2022 (Physica A) | S&P 500, Bitcoin; sentiment series | Not specified (sentiment series) | Wavelet + Transfer Entropy | Sentiment mediates crypto–equity spillovers, episodic across frequencies | Feature for cross-asset spillover and directionality checks |
| Cao et al. 2025 (Entropy) | S&P 500 firm sentiment network | Sentiment network metrics | Network connectedness → crash risk regression | High connectedness, especially negative, raises crash risk | Use connectedness as risk overlay for regime signals |
| Nyakurukwa & Seetharam 2025 (Financial Innovation) | DJIA news + social sentiment | Sentiment by polarity and horizon | Frequency/asymmetric connectedness | Negative news sentiment transmits more strongly | Engineer pos/neg and horizon-specific sentiment factors |
| Liu et al. 2024 (IEEE Access) | China market indicators + internet text | Text-derived signals | HMM composite risk index | Text + market signals improve systemic risk regimes | Template for HMM with sentiment exogenous inputs |
| Shu et al. 2024 (Journal of Asset Management) | US/DE/JP indices (1990–2023) | Market features (add sentiment as exogenous) | Jump-penalized regime switching (JM) | More persistent regimes; better drawdown control | Candidate core regime detector with sentiment inputs |
| Zhang et al. 2020 (IEEE BigData) | Macro + market (with mood swings) | Mood/sentiment features | Hierarchical clustering | Identifies unusual regimes; interpretable factors | Use for explainability and feature importance |
| Huang et al. 2021 (DASFAA) | Weibo sentiment + crypto prices | LSTM with crypto lexicon | Predictive modeling, no explicit regimes | Social sentiment boosts short-term crypto prediction | Justifies multi-language/social ingestion |
| Peivandizadeh et al. 2023 (IEEE Access) | Social sentiment + stocks | TLSTM + PPO for imbalance | Temporal sentiment alignment | Better alignment of sentiment with price moves | Techniques for class imbalance and temporal weighting |
| Araci 2019; Mishev 2020 | FiQA/FPB, financial news | FinBERT; benchmarks vs lexicons/encoders | N/A (sentiment accuracy focus) | Domain-specific BERT outperforms lexicons | Baseline sentiment encoder |
| FinSoSent 2024 | Financial news + social corpora | Domain-specific LLM | N/A (sentiment focus) | Outperforms other FSA models | Richer sentiment features than FinBERT |
| FinLlama 2024 | Financial news | LoRA-tuned Llama2-7B | N/A (sentiment focus) | Efficient graded sentiment via parameter-efficient tuning | Lightweight custom sentiment for your stack |

## Annotated Paper Summaries

### Caferra 2022, Physica A (crypto–equity spillovers with transfer entropy)

Data: S&P 500, Bitcoin; sentiment series; wavelet + TE.
Model: Transfer Entropy to capture directionality.
Regime/Spillover: Episodic interconnectedness across frequencies; sentiment mediates crypto–equity link.
Backtest/Impact: Motivates cross-asset sentiment features; shows sentiment as a transmission channel.

### Cao et al. 2025, Entropy (sentiment connectedness → crash risk)

Data: S&P 500 firm-level sentiment network.
Model: Network connectedness of sentiment; crash risk regression.
Regime/Spillover: High connectedness → higher crash risk; negative sentiment dominates.
Backtest/Impact: Use connectedness as a risk overlay in regime signals.

### Nyakurukwa & Seetharam 2025, Financial Innovation (DJIA sentiment networks)

Data: News + social sentiment, DJIA constituents.
Model: Frequency and asymmetric sentiment connectedness.
Regime/Spillover: Negative news sentiment transmits more strongly; consistent across horizons.
Backtest/Impact: Feature engineer separate positive/negative and horizon-specific sentiment factors.

### Liu et al. 2024, IEEE Access (HMM + text for systemic risk)

Data: China market indicators + internet text signals.
Model: HMM composite index with text-derived signals.
Regime: Regime classification for systemic risk; medium-high risk identified.
Backtest/Impact: Blueprint for blending market data with text sentiment into HMM regimes.

### Shu et al. 2024, Journal of Asset Management (jump-penalized regime switching)

Data: Major equity indices (US/DE/JP), 1990–2023.
Model: Statistical Jump Model with jump penalty for regime persistence.
Regime: More robust, persistent regime identification; improves drawdown control.
Backtest/Impact: Candidate for your regime detector; add sentiment as exogenous signals.

### Zhang et al. 2020, IEEE BigData (explainable clustering for regimes)

Data: Macro + market; uses sentiment/mood swings.
Model: Hierarchical clustering for regimes; interpretable factors.
Regime: Detects unusual regimes (e.g., 2015–2016 spike).
Backtest/Impact: Useful for feature importance and explainability.

### Huang et al. 2021, DASFAA (Weibo LSTM for crypto)

Data: Chinese social sentiment (Weibo) + crypto prices.
Model: LSTM with crypto-specific sentiment lexicon.
Regime/Spillover: Social sentiment improves short-term crypto prediction.
Backtest/Impact: Shows value of non-English/social streams; supports multi-source ingestion.

### Peivandizadeh et al. 2023, IEEE Access (TLSTM + sentiment, class-imbalance aware)

Data: Social sentiment + stock prices.
Model: Transductive LSTM; PPO to handle class imbalance in sentiment.
Regime/Spillover: Better temporal alignment of sentiment with price moves.
Backtest/Impact: Techniques for handling label skew and temporal weighting.

### Araci 2019 FinBERT + Mishev et al. 2020 (finance sentiment evaluation)

Data: FiQA/Financial PhraseBank and financial news.
Model: FinBERT; benchmarking vs lexicons/encoders.
Regime/Spillover: Higher sentiment accuracy → better downstream signals.
Backtest/Impact: Baseline sentiment encoder for your pipeline; strong starting point.

### FinSoSent 2024, Delgadillo et al. (financial LLM pretrained on news + social)

Data: Financial news + social media corpora; many hyperparameter sweeps.
Model: Domain-specific LLM, outperforms other FSA models; ensemble option.
Regime/Spillover: Captures subtle financial terminology; better sentiment granularity.
Backtest/Impact: Candidate upgrade over FinBERT for richer sentiment features.

### FinLlama 2024, Konstantinidis et al. (LoRA-tuned Llama2-7B for finance)

Data: Financial news; few-shot/LoRA fine-tune.
Model: Parameter-efficient finetune; generator-classifier for sentiment strength.
Regime/Spillover: Provides graded sentiment useful for transition probability tweaks.
Backtest/Impact: Efficient path to custom sentiment with low compute.

## Pipeline mapping (how these plug into your flow)

### Data sources

Social/news: Caferra 2022; Huang 2021; Peivandizadeh 2023; FinSoSent/FinLlama (pretraining corpora).
Cross-asset prices: Caferra 2022; Cao 2025; Li 2021; Shu 2024.

### Sentiment models (stack)

Baseline: FinBERT (Araci 2019).
Enhanced: FinSoSent 2024 (domain-pretrained), FinLlama 2024 (LoRA for efficiency), Peivandizadeh TLSTM (temporal + imbalance handling).
Topic/entity: FinEntity (2023) from the same CSV if you need entity-level scores.

### Regime detection

HMM/JM: Li 2021 (HMM with text), Shu 2024 (jump-penalized regimes).
Clustering: Zhang 2020 (interpretable clustering).
Network/spillover: Caferra 2022; Cao 2025; Nyakurukwa 2025 (connectedness).

### Backtest & evaluation hooks

Risk overlays: crash risk from sentiment connectedness (Cao 2025).
Spillover/risk control: Caferra 2022 (TE), Nyakurukwa 2025 (asymmetric sentiment).
Performance metrics to mirror: crash-risk regressions, transfer entropy significance, Sharpe/drawdown improvements (Shu 2024), predictive lift vs baselines (Huang 2021, Peivandizadeh 2023)
