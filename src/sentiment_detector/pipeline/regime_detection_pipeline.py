"""
End-to-End Regime Detection Pipeline.

This module integrates all components of the regime detection system:
1. TimeAligner: Align irregular sentiment to trading days
2. Feature Engineering: Transfer Entropy, Connectedness, Granger Causality
3. GARCH-MIDAS: Layer 1 volatility decomposition
4. Statistical Jump Model: Layer 2 regime classification

The pipeline follows the methodology from Draft-1.md Section 2.

References:
- Shu et al. (2024): Statistical Jump Model for regime detection
- Cao et al. (2025): Entropy-based connectedness measures
- Engle et al. (2013): GARCH-MIDAS decomposition
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any, Literal
from enum import Enum
from datetime import datetime, timedelta
import logging

import numpy as np
import pandas as pd

import sys
import os

# Ensure the package is importable
_pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _pkg_root not in sys.path:
    sys.path.insert(0, os.path.dirname(_pkg_root))

from src.sentiment_detector.preprocessing.time_alignment import TimeAligner, AlignmentResult
from src.sentiment_detector.preprocessing.timezone_handler import MarketTimezone
from src.sentiment_detector.features.transfer_entropy import TransferEntropyAnalyzer
from src.sentiment_detector.features.connectedness import ConnectednessAnalyzer
from src.sentiment_detector.features.granger_causality import GrangerCausalityAnalyzer
from src.sentiment_detector.models.garch_midas import GARCHMIDASModel, GARCHMIDASResult
from src.sentiment_detector.models.jump_model import (
    StatisticalJumpModel, 
    JumpModelConfig, 
    JumpModelResult,
    RegimeState,
    create_feature_matrix,
)

logger = logging.getLogger(__name__)


class PipelineStage(str, Enum):
    """Pipeline processing stages."""
    TIME_ALIGNMENT = "time_alignment"
    FEATURE_ENGINEERING = "feature_engineering"
    GARCH_MIDAS = "garch_midas"
    JUMP_MODEL = "jump_model"
    COMPLETE = "complete"


@dataclass
class PipelineConfig:
    """Configuration for the end-to-end pipeline."""
    
    # Time alignment settings
    target_timezone: MarketTimezone = MarketTimezone.EST
    max_forward_fill_days: int = 5
    
    # Feature engineering settings
    transfer_entropy_bins: int = 6
    transfer_entropy_lag: int = 1
    connectedness_window: int = 22  # Trading days
    connectedness_h: int = 10  # Forecast horizon
    granger_max_lag: int = 5
    
    # GARCH-MIDAS settings
    garch_p: int = 1
    garch_q: int = 1
    midas_lags: int = 22
    garch_distribution: Literal["normal", "t", "skewt"] = "t"
    
    # Jump model settings
    n_regimes: int = 4
    jump_penalty: float = 0.5
    min_regime_duration: int = 5
    
    # Feature weights for Jump Model
    volatility_weight: float = 0.30
    sentiment_weight: float = 0.25
    entropy_weight: float = 0.20
    connectedness_weight: float = 0.15
    granger_weight: float = 0.10
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'target_timezone': self.target_timezone.value,
            'max_forward_fill_days': self.max_forward_fill_days,
            'transfer_entropy_bins': self.transfer_entropy_bins,
            'connectedness_window': self.connectedness_window,
            'garch_p': self.garch_p,
            'garch_q': self.garch_q,
            'midas_lags': self.midas_lags,
            'n_regimes': self.n_regimes,
            'jump_penalty': self.jump_penalty,
        }


@dataclass
class PipelineResult:
    """Complete result from the pipeline."""
    
    # Timestamps
    start_time: datetime
    end_time: datetime
    processing_duration_seconds: float
    
    # Configuration used
    config: PipelineConfig
    
    # Data dimensions
    n_trading_days: int
    n_sentiment_records: int
    date_range: Tuple[datetime, datetime]
    
    # Stage results
    alignment_results: Optional[List[AlignmentResult]] = None
    garch_midas_result: Optional[GARCHMIDASResult] = None
    jump_model_result: Optional[JumpModelResult] = None
    
    # Feature matrix
    feature_matrix: Optional[pd.DataFrame] = None
    
    # Final output
    regime_series: Optional[pd.Series] = None
    transition_probability: Optional[pd.Series] = None
    
    # Metrics
    regime_distribution: Dict[str, float] = field(default_factory=dict)
    n_transitions: int = 0
    avg_regime_duration: float = 0
    
    def summary(self) -> str:
        """Generate summary report."""
        lines = [
            "=" * 60,
            "REGIME DETECTION PIPELINE RESULTS",
            "=" * 60,
            "",
            f"Processing Time: {self.processing_duration_seconds:.2f} seconds",
            f"Date Range: {self.date_range[0].date()} to {self.date_range[1].date()}",
            f"Trading Days: {self.n_trading_days}",
            f"Sentiment Records: {self.n_sentiment_records}",
            "",
            "GARCH-MIDAS (Layer 1):",
        ]
        
        if self.garch_midas_result:
            lines.extend([
                f"  Omega: {self.garch_midas_result.params.get('omega', 'N/A')}",
                f"  Alpha: {self.garch_midas_result.params.get('alpha', 'N/A')}",
                f"  Beta: {self.garch_midas_result.params.get('beta', 'N/A')}",
                f"  Log-Likelihood: {self.garch_midas_result.log_likelihood}",
            ])
        
        lines.extend([
            "",
            "Jump Model (Layer 2):",
            f"  Number of Regimes: {self.config.n_regimes}",
            f"  Jump Penalty: {self.config.jump_penalty}",
            f"  Transitions: {self.n_transitions}",
            f"  Avg Regime Duration: {self.avg_regime_duration:.1f} days",
        ])
        
        if self.regime_distribution:
            lines.append("")
            lines.append("Regime Distribution:")
            for regime, pct in sorted(self.regime_distribution.items()):
                lines.append(f"  {regime}: {pct:.1%}")
        
        return "\n".join(lines)


class RegimeDetectionPipeline:
    """
    End-to-end pipeline for regime detection.
    
    Integrates:
    1. Time Alignment (Kengmegni, 2024)
    2. Feature Engineering (Transfer Entropy, Connectedness, Granger)
    3. GARCH-MIDAS volatility decomposition (Layer 1)
    4. Statistical Jump Model regime classification (Layer 2)
    
    Example:
        >>> pipeline = RegimeDetectionPipeline()
        >>> result = pipeline.run(
        ...     sentiment_data=sentiment_df,
        ...     market_data=market_df,
        ...     trading_dates=trading_dates
        ... )
        >>> print(result.regime_series)
        >>> print(result.summary())
    """
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize the pipeline.
        
        Args:
            config: Pipeline configuration (uses defaults if None)
        """
        self.config = config or PipelineConfig()
        
        # Initialize components
        self.time_aligner = TimeAligner(
            target_timezone=self.config.target_timezone,
            max_forward_fill_days=self.config.max_forward_fill_days,
        )
        
        self.transfer_entropy = TransferEntropyAnalyzer(
            n_bins=self.config.transfer_entropy_bins,
            history_length=self.config.transfer_entropy_lag,
        )
        
        self.connectedness = ConnectednessAnalyzer(
            var_lag=self.config.granger_max_lag,
            forecast_horizon=self.config.connectedness_h,
        )
        
        self.granger_tester = GrangerCausalityAnalyzer(
            max_lag=self.config.granger_max_lag,
        )
        
        self.garch_midas = GARCHMIDASModel(
            p=self.config.garch_p,
            q=self.config.garch_q,
            midas_lags=self.config.midas_lags,
            distribution=self.config.garch_distribution,
        )
        
        self.jump_model = StatisticalJumpModel(
            config=JumpModelConfig(
                n_regimes=self.config.n_regimes,
                jump_penalty=self.config.jump_penalty,
                min_regime_duration=self.config.min_regime_duration,
            )
        )
        
        self._current_stage = PipelineStage.TIME_ALIGNMENT
        
        logger.info(f"RegimeDetectionPipeline initialized with config: {self.config.to_dict()}")
    
    def run(
        self,
        sentiment_data: pd.DataFrame,
        market_data: pd.DataFrame,
        trading_dates: Optional[List[datetime]] = None,
        vix_data: Optional[pd.DataFrame] = None,
    ) -> PipelineResult:
        """
        Run the complete pipeline.
        
        Args:
            sentiment_data: DataFrame with sentiment scores and timestamps
            market_data: DataFrame with market returns/prices
            trading_dates: List of trading dates (inferred if None)
            vix_data: Optional VIX data for ground truth comparison
            
        Returns:
            PipelineResult with regime classifications
        """
        start_time = datetime.now()
        
        logger.info("=" * 60)
        logger.info("STARTING REGIME DETECTION PIPELINE")
        logger.info("=" * 60)
        
        # Infer trading dates if not provided
        if trading_dates is None:
            trading_dates = market_data.index.tolist()
        
        # Stage 1: Time Alignment
        self._current_stage = PipelineStage.TIME_ALIGNMENT
        logger.info(f"Stage 1: {self._current_stage.value}")
        
        aligned_sentiment, alignment_results = self._align_sentiment(
            sentiment_data, trading_dates
        )
        
        # Stage 2: Feature Engineering
        self._current_stage = PipelineStage.FEATURE_ENGINEERING
        logger.info(f"Stage 2: {self._current_stage.value}")
        
        feature_matrix = self._engineer_features(
            aligned_sentiment, market_data, vix_data
        )
        
        # Stage 3: GARCH-MIDAS
        self._current_stage = PipelineStage.GARCH_MIDAS
        logger.info(f"Stage 3: {self._current_stage.value}")
        
        garch_result = self._fit_garch_midas(market_data, aligned_sentiment)
        
        # Add GARCH-MIDAS volatility to features
        if garch_result and garch_result.conditional_volatility is not None:
            feature_matrix['garch_volatility'] = garch_result.conditional_volatility
            feature_matrix['long_run_volatility'] = garch_result.long_run_volatility
        
        # Stage 4: Jump Model
        self._current_stage = PipelineStage.JUMP_MODEL
        logger.info(f"Stage 4: {self._current_stage.value}")
        
        jump_result = self._fit_jump_model(feature_matrix)
        
        # Map integer regimes to meaningful labels
        # Using VIX-based regime naming (matches 4-regime configuration)
        regime_labels = ['low_volatility', 'normal', 'elevated', 'high_volatility']
        
        # Create regime series with mapped labels
        regime_series = pd.Series(
            [regime_labels[int(r) % len(regime_labels)] for r in jump_result.regimes],
            index=feature_matrix.index,
            name='regime'
        )
        
        # Calculate metrics
        regime_counts = regime_series.value_counts()
        regime_distribution = (regime_counts / len(regime_series)).to_dict()
        
        # Count transitions
        transitions = (regime_series != regime_series.shift(1)).sum() - 1
        avg_duration = len(regime_series) / (transitions + 1) if transitions >= 0 else len(regime_series)
        
        self._current_stage = PipelineStage.COMPLETE
        end_time = datetime.now()
        
        logger.info(f"Pipeline completed in {(end_time - start_time).total_seconds():.2f}s")
        
        return PipelineResult(
            start_time=start_time,
            end_time=end_time,
            processing_duration_seconds=(end_time - start_time).total_seconds(),
            config=self.config,
            n_trading_days=len(trading_dates),
            n_sentiment_records=len(sentiment_data),
            date_range=(min(trading_dates), max(trading_dates)),
            alignment_results=alignment_results,
            garch_midas_result=garch_result,
            jump_model_result=jump_result,
            feature_matrix=feature_matrix,
            regime_series=regime_series,
            transition_probability=None,  # TODO: Add transition probabilities
            regime_distribution=regime_distribution,
            n_transitions=int(transitions),
            avg_regime_duration=avg_duration,
        )
    
    def _align_sentiment(
        self,
        sentiment_data: pd.DataFrame,
        trading_dates: List[datetime],
    ) -> Tuple[pd.DataFrame, List[AlignmentResult]]:
        """
        Align irregular sentiment to trading days.
        
        Implements three-case alignment (Dakalbab et al., 2025):
        - Case 1: Perfect match
        - Case 2: Forward-fill for sparse data
        - Case 3: Aggregation for high velocity
        """
        logger.info(f"Aligning {len(sentiment_data)} sentiment records to {len(trading_dates)} trading days")
        
        # Use time aligner
        results = self.time_aligner.align_to_daily(
            sentiment_data=sentiment_data,
            trading_dates=trading_dates,
        )
        
        # Convert to DataFrame
        aligned_data = {
            'compound': [],
            'positive': [],
            'negative': [],
            'neutral': [],
            'document_count': [],
            'alignment_case': [],
        }
        dates = []
        
        for result in results:
            dates.append(result.trading_date)
            aligned_data['compound'].append(result.sentiment_score)
            aligned_data['positive'].append(result.positive_score)
            aligned_data['negative'].append(result.negative_score)
            aligned_data['neutral'].append(result.neutral_score)
            aligned_data['document_count'].append(result.document_count)
            aligned_data['alignment_case'].append(result.case)
        
        aligned_df = pd.DataFrame(aligned_data, index=pd.DatetimeIndex(dates))
        
        # Log alignment statistics
        case_counts = aligned_df['alignment_case'].value_counts()
        logger.info(f"Alignment cases: {case_counts.to_dict()}")
        
        return aligned_df, results
    
    def _engineer_features(
        self,
        aligned_sentiment: pd.DataFrame,
        market_data: pd.DataFrame,
        vix_data: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        Engineer features for regime detection.
        
        Features:
        1. Sentiment scores (compound, positive, negative)
        2. Transfer Entropy (sentiment → VIX)
        3. Connectedness (Total Connectedness Index)
        4. Granger causality scores
        5. Market volatility
        """
        logger.info("Engineering features for regime detection")
        
        # Start with aligned sentiment
        features = aligned_sentiment[['compound', 'positive', 'negative']].copy()
        
        # Add market data
        if 'returns' in market_data.columns:
            features['returns'] = market_data['returns']
            features['realized_vol'] = market_data['returns'].rolling(22).std() * np.sqrt(252)
        
        # Add VIX if available
        if vix_data is not None and 'close' in vix_data.columns:
            vix_aligned = vix_data['close'].reindex(features.index, method='ffill')
            features['vix'] = vix_aligned
            features['vix_change'] = vix_aligned.pct_change()
        
        # Calculate rolling transfer entropy
        if 'vix' in features.columns:
            te_values = []
            for i in range(len(features)):
                if i < 22:
                    te_values.append(0)
                else:
                    window_sent = features['compound'].iloc[i-22:i].values
                    window_vix = features['vix'].iloc[i-22:i].values
                    try:
                        te = self.transfer_entropy.compute(
                            source=window_sent,
                            target=window_vix,
                        )
                        te_values.append(te.transfer_entropy)
                    except:
                        te_values.append(0)
            features['transfer_entropy'] = te_values
        
        # Calculate connectedness (rolling TCI)
        # Simplified version - full implementation would use VAR model
        if len(features) >= self.config.connectedness_window:
            tci_values = []
            for i in range(len(features)):
                if i < self.config.connectedness_window:
                    tci_values.append(0.5)  # Default TCI
                else:
                    # Use correlation as proxy for connectedness
                    window = features.iloc[i-self.config.connectedness_window:i]
                    if 'vix' in window.columns:
                        corr = abs(window['compound'].corr(window['vix']))
                        tci_values.append(corr if not np.isnan(corr) else 0.5)
                    else:
                        tci_values.append(0.5)
            features['tci'] = tci_values
        
        # Fill NaN values
        features = features.fillna(method='ffill').fillna(0)
        
        logger.info(f"Engineered {len(features.columns)} features over {len(features)} days")
        
        return features
    
    def _fit_garch_midas(
        self,
        market_data: pd.DataFrame,
        aligned_sentiment: pd.DataFrame,
    ) -> Optional[GARCHMIDASResult]:
        """
        Fit GARCH-MIDAS model for volatility decomposition.
        """
        logger.info("Fitting GARCH-MIDAS model")
        
        # Get returns
        if 'returns' in market_data.columns:
            returns = market_data['returns']
        elif 'close' in market_data.columns:
            returns = market_data['close'].pct_change().dropna()
        else:
            logger.warning("No returns data available for GARCH-MIDAS")
            return None
        
        # Get sentiment index
        sentiment = aligned_sentiment['compound']
        
        # Fit model
        try:
            result = self.garch_midas.fit(
                returns=returns,
                sentiment=sentiment,
            )
            logger.info(f"GARCH-MIDAS fitted: LL={result.log_likelihood:.2f}")
            return result
        except Exception as e:
            logger.warning(f"GARCH-MIDAS fitting failed: {e}")
            return None
    
    def _fit_jump_model(
        self,
        feature_matrix: pd.DataFrame,
    ) -> JumpModelResult:
        """
        Fit Statistical Jump Model for regime classification.
        """
        logger.info("Fitting Statistical Jump Model")
        
        # Select features for jump model
        feature_cols = [
            col for col in feature_matrix.columns 
            if col not in ['alignment_case', 'document_count']
        ]
        
        X = feature_matrix[feature_cols].values
        
        # Standardize features
        X_mean = np.nanmean(X, axis=0)
        X_std = np.nanstd(X, axis=0)
        X_std[X_std == 0] = 1  # Avoid division by zero
        X_normalized = (X - X_mean) / X_std
        
        # Handle any remaining NaN
        X_normalized = np.nan_to_num(X_normalized, nan=0)
        
        # Fit jump model
        result = self.jump_model.fit_predict(X_normalized)
        
        logger.info(f"Jump Model fitted: {self.config.n_regimes} regimes detected")
        logger.info(f"Regime distribution: {pd.Series(result.regimes).value_counts().to_dict()}")
        
        return result
    
    def predict(
        self,
        new_sentiment: pd.DataFrame,
        new_market_data: pd.DataFrame,
    ) -> pd.Series:
        """
        Predict regimes for new data using fitted models.
        
        Args:
            new_sentiment: New sentiment data
            new_market_data: New market data
            
        Returns:
            Regime predictions
        """
        if not self.jump_model._fitted:
            raise ValueError("Pipeline has not been fitted. Call run() first.")
        
        # Align sentiment
        trading_dates = new_market_data.index.tolist()
        aligned_sentiment, _ = self._align_sentiment(new_sentiment, trading_dates)
        
        # Engineer features
        features = self._engineer_features(aligned_sentiment, new_market_data)
        
        # Select and normalize features
        feature_cols = [
            col for col in features.columns 
            if col not in ['alignment_case', 'document_count']
        ]
        X = features[feature_cols].values
        X_normalized = (X - np.nanmean(X, axis=0)) / (np.nanstd(X, axis=0) + 1e-8)
        X_normalized = np.nan_to_num(X_normalized, nan=0)
        
        # Predict
        result = self.jump_model.predict(X_normalized)
        
        return pd.Series(
            [RegimeState(r).value for r in result.regimes],
            index=features.index,
            name='regime'
        )


def run_pipeline(
    sentiment_path: str,
    market_path: str,
    vix_path: Optional[str] = None,
    output_path: Optional[str] = None,
    config: Optional[PipelineConfig] = None,
) -> PipelineResult:
    """
    Convenience function to run the pipeline from file paths.
    
    Args:
        sentiment_path: Path to sentiment CSV
        market_path: Path to market data CSV
        vix_path: Optional path to VIX data CSV
        output_path: Optional path to save results
        config: Pipeline configuration
        
    Returns:
        PipelineResult
    """
    # Load data
    sentiment_data = pd.read_csv(sentiment_path, parse_dates=['created_at'])
    market_data = pd.read_csv(market_path, parse_dates=['date'], index_col='date')
    
    vix_data = None
    if vix_path:
        vix_data = pd.read_csv(vix_path, parse_dates=['date'], index_col='date')
    
    # Run pipeline
    pipeline = RegimeDetectionPipeline(config)
    result = pipeline.run(
        sentiment_data=sentiment_data,
        market_data=market_data,
        vix_data=vix_data,
    )
    
    # Save results
    if output_path and result.regime_series is not None:
        result.regime_series.to_csv(output_path)
        logger.info(f"Results saved to {output_path}")
    
    return result
