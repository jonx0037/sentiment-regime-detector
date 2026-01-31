"""
Evaluation Metrics for Sentiment-Regime Detection.

This module implements evaluation metrics for assessing:
1. Sentiment classification accuracy
2. Regime prediction performance
3. Model calibration

Key metrics per Dakalbab et al. (2024):
- Directional Accuracy (DA): Accuracy of regime direction
- Matthews Correlation Coefficient (MCC): Robust classification metric
- F1 Score: Balanced precision/recall
- Calibration Error: Confidence reliability
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
import numpy as np
from collections import Counter


@dataclass
class ClassificationMetrics:
    """
    Classification performance metrics.
    
    Attributes:
        accuracy: Overall accuracy
        precision: Precision per class
        recall: Recall per class
        f1_score: F1 score per class
        mcc: Matthews Correlation Coefficient
        confusion_matrix: Confusion matrix as dict
    """
    accuracy: float
    precision: dict[str, float]
    recall: dict[str, float]
    f1_score: dict[str, float]
    mcc: float
    confusion_matrix: dict[str, dict[str, int]]
    support: dict[str, int] = field(default_factory=dict)
    
    @property
    def macro_f1(self) -> float:
        """Calculate macro-averaged F1 score."""
        return np.mean(list(self.f1_score.values()))
    
    @property
    def weighted_f1(self) -> float:
        """Calculate support-weighted F1 score."""
        if not self.support:
            return self.macro_f1
        total = sum(self.support.values())
        return sum(
            self.f1_score[k] * self.support.get(k, 0) / total 
            for k in self.f1_score
        )


@dataclass
class DirectionalMetrics:
    """
    Directional accuracy metrics for regime prediction.
    
    Attributes:
        directional_accuracy: Correct direction (up/down/neutral)
        up_precision: Precision for bullish predictions
        down_precision: Precision for bearish predictions
        regime_transitions: Accuracy on transition periods
    """
    directional_accuracy: float
    up_precision: float
    down_precision: float
    neutral_precision: float
    regime_transitions: float
    total_predictions: int


@dataclass
class CalibrationMetrics:
    """
    Calibration metrics for confidence reliability.
    
    Attributes:
        expected_calibration_error: ECE
        maximum_calibration_error: MCE
        reliability_diagram: Binned accuracy vs confidence
    """
    expected_calibration_error: float
    maximum_calibration_error: float
    reliability_diagram: dict[str, tuple[float, float]]
    brier_score: float


class EvaluationMetrics:
    """
    Evaluation metrics calculator for sentiment-regime detection.
    
    Implements metrics from Dakalbab et al. (2024):
    - Directional Accuracy for regime alignment
    - MCC for imbalanced classification
    - Calibration analysis
    """
    
    @staticmethod
    def calculate_mcc(
        y_true: list[int],
        y_pred: list[int],
        num_classes: int = 3
    ) -> float:
        """
        Calculate Matthews Correlation Coefficient.
        
        MCC is a robust metric for imbalanced classification,
        returning values in [-1, 1] where 1 is perfect prediction.
        
        For multi-class, uses the generalized MCC formula.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            num_classes: Number of classes
            
        Returns:
            MCC value in [-1, 1]
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and labels must have same length")
        
        n = len(y_true)
        if n == 0:
            return 0.0
        
        # Build confusion matrix
        cm = np.zeros((num_classes, num_classes), dtype=np.int64)
        for t, p in zip(y_true, y_pred):
            if 0 <= t < num_classes and 0 <= p < num_classes:
                cm[t][p] += 1
        
        # Calculate MCC for multi-class
        # Using the RK correlation formula
        correct = np.trace(cm)
        total = np.sum(cm)
        
        if total == 0:
            return 0.0
        
        # Sum of squares of row sums
        row_sums = np.sum(cm, axis=1)
        col_sums = np.sum(cm, axis=0)
        
        # Numerator
        cov_xy = correct * total - np.dot(row_sums, col_sums)
        
        # Denominator
        cov_xx = total ** 2 - np.dot(row_sums, row_sums)
        cov_yy = total ** 2 - np.dot(col_sums, col_sums)
        
        denom = np.sqrt(cov_xx * cov_yy)
        
        if denom == 0:
            return 0.0
        
        return float(cov_xy / denom)
    
    @staticmethod
    def calculate_directional_accuracy(
        y_true: list[int],
        y_pred: list[int],
        positive_label: int = 1,
        negative_label: int = -1,
        neutral_label: int = 0
    ) -> DirectionalMetrics:
        """
        Calculate directional accuracy for regime predictions.
        
        Measures how often the model correctly predicts:
        - Bullish regime (positive sentiment)
        - Bearish regime (negative sentiment)  
        - Neutral regime
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            positive_label: Label for positive/bullish
            negative_label: Label for negative/bearish
            neutral_label: Label for neutral
            
        Returns:
            DirectionalMetrics with detailed accuracy breakdown
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and labels must have same length")
        
        n = len(y_true)
        if n == 0:
            return DirectionalMetrics(
                directional_accuracy=0.0,
                up_precision=0.0,
                down_precision=0.0,
                neutral_precision=0.0,
                regime_transitions=0.0,
                total_predictions=0
            )
        
        correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        directional_accuracy = correct / n
        
        # Per-direction precision
        def precision_for_class(label):
            predicted_positive = sum(1 for p in y_pred if p == label)
            true_positive = sum(
                1 for t, p in zip(y_true, y_pred) 
                if p == label and t == label
            )
            return true_positive / predicted_positive if predicted_positive > 0 else 0.0
        
        up_precision = precision_for_class(positive_label)
        down_precision = precision_for_class(negative_label)
        neutral_precision = precision_for_class(neutral_label)
        
        # Transition accuracy (when true regime changes)
        transitions = 0
        transition_correct = 0
        for i in range(1, len(y_true)):
            if y_true[i] != y_true[i-1]:
                transitions += 1
                if y_pred[i] == y_true[i]:
                    transition_correct += 1
        
        regime_transitions = (
            transition_correct / transitions if transitions > 0 else 0.0
        )
        
        return DirectionalMetrics(
            directional_accuracy=directional_accuracy,
            up_precision=up_precision,
            down_precision=down_precision,
            neutral_precision=neutral_precision,
            regime_transitions=regime_transitions,
            total_predictions=n
        )
    
    @staticmethod
    def calculate_classification_metrics(
        y_true: list,
        y_pred: list,
        labels: Optional[list] = None
    ) -> ClassificationMetrics:
        """
        Calculate comprehensive classification metrics.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            labels: Optional list of label names
            
        Returns:
            ClassificationMetrics with all metrics
        """
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and labels must have same length")
        
        n = len(y_true)
        if n == 0:
            return ClassificationMetrics(
                accuracy=0.0,
                precision={},
                recall={},
                f1_score={},
                mcc=0.0,
                confusion_matrix={},
                support={}
            )
        
        # Get unique labels
        all_labels = sorted(set(y_true) | set(y_pred))
        if labels:
            label_names = {l: labels[i] if i < len(labels) else str(l) 
                         for i, l in enumerate(all_labels)}
        else:
            label_names = {l: str(l) for l in all_labels}
        
        # Calculate confusion matrix
        confusion = {
            label_names[t]: {label_names[p]: 0 for p in all_labels}
            for t in all_labels
        }
        for t, p in zip(y_true, y_pred):
            confusion[label_names[t]][label_names[p]] += 1
        
        # Calculate support (count per true class)
        support = Counter(y_true)
        support_named = {label_names[k]: v for k, v in support.items()}
        
        # Calculate per-class metrics
        precision = {}
        recall = {}
        f1_score = {}
        
        for label in all_labels:
            name = label_names[label]
            
            # True positives
            tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
            
            # False positives (predicted as this class but wrong)
            fp = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
            
            # False negatives (is this class but predicted wrong)
            fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)
            
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            
            precision[name] = prec
            recall[name] = rec
            f1_score[name] = f1
        
        # Overall accuracy
        accuracy = sum(1 for t, p in zip(y_true, y_pred) if t == p) / n
        
        # MCC
        y_true_int = [all_labels.index(t) for t in y_true]
        y_pred_int = [all_labels.index(p) for p in y_pred]
        mcc = EvaluationMetrics.calculate_mcc(
            y_true_int, y_pred_int, len(all_labels)
        )
        
        return ClassificationMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            mcc=mcc,
            confusion_matrix=confusion,
            support=support_named
        )
    
    @staticmethod
    def calculate_calibration(
        y_true: list[int],
        y_pred: list[int],
        confidences: list[float],
        n_bins: int = 10
    ) -> CalibrationMetrics:
        """
        Calculate calibration metrics.
        
        Measures how well confidence scores correlate with accuracy.
        A well-calibrated model has confidence ≈ accuracy.
        
        Args:
            y_true: Ground truth labels
            y_pred: Predicted labels
            confidences: Confidence scores [0, 1]
            n_bins: Number of bins for calibration analysis
            
        Returns:
            CalibrationMetrics with ECE, MCE, and reliability diagram
        """
        if len(y_true) != len(y_pred) or len(y_true) != len(confidences):
            raise ValueError("All inputs must have same length")
        
        n = len(y_true)
        if n == 0:
            return CalibrationMetrics(
                expected_calibration_error=0.0,
                maximum_calibration_error=0.0,
                reliability_diagram={},
                brier_score=0.0
            )
        
        # Bin predictions by confidence
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        reliability_diagram = {}
        calibration_errors = []
        
        for i in range(n_bins):
            lower, upper = bin_boundaries[i], bin_boundaries[i + 1]
            bin_name = f"{lower:.1f}-{upper:.1f}"
            
            # Find predictions in this bin
            in_bin = [
                j for j, c in enumerate(confidences) 
                if lower <= c < upper or (i == n_bins - 1 and c == upper)
            ]
            
            if len(in_bin) > 0:
                # Accuracy in this bin
                bin_accuracy = sum(
                    1 for j in in_bin if y_true[j] == y_pred[j]
                ) / len(in_bin)
                
                # Average confidence in this bin
                bin_confidence = sum(confidences[j] for j in in_bin) / len(in_bin)
                
                reliability_diagram[bin_name] = (bin_confidence, bin_accuracy)
                
                # Weighted calibration error
                calibration_errors.append(
                    (abs(bin_accuracy - bin_confidence), len(in_bin))
                )
        
        # Expected Calibration Error (weighted average)
        if calibration_errors:
            total_samples = sum(w for _, w in calibration_errors)
            ece = sum(e * w for e, w in calibration_errors) / total_samples
            mce = max(e for e, _ in calibration_errors)
        else:
            ece, mce = 0.0, 0.0
        
        # Brier score (mean squared error of confidence)
        correct = [1.0 if y_true[i] == y_pred[i] else 0.0 for i in range(n)]
        brier = sum((c - correct[i]) ** 2 for i, c in enumerate(confidences)) / n
        
        return CalibrationMetrics(
            expected_calibration_error=ece,
            maximum_calibration_error=mce,
            reliability_diagram=reliability_diagram,
            brier_score=brier
        )
    
    @staticmethod
    def evaluate_sentiment_model(
        y_true: list,
        y_pred: list,
        confidences: Optional[list[float]] = None,
        label_names: Optional[list[str]] = None
    ) -> dict:
        """
        Comprehensive evaluation of a sentiment model.
        
        Args:
            y_true: Ground truth sentiment labels
            y_pred: Predicted sentiment labels
            confidences: Optional confidence scores
            label_names: Optional names for labels
            
        Returns:
            Dictionary with all evaluation metrics
        """
        # Classification metrics
        cls_metrics = EvaluationMetrics.calculate_classification_metrics(
            y_true, y_pred, label_names
        )
        
        # Directional metrics (assuming -1=negative, 0=neutral, 1=positive)
        y_true_int = [
            -1 if str(y).lower() in ('negative', '-1') else
            1 if str(y).lower() in ('positive', '1') else 0
            for y in y_true
        ]
        y_pred_int = [
            -1 if str(y).lower() in ('negative', '-1') else
            1 if str(y).lower() in ('positive', '1') else 0
            for y in y_pred
        ]
        
        dir_metrics = EvaluationMetrics.calculate_directional_accuracy(
            y_true_int, y_pred_int
        )
        
        result = {
            "classification": {
                "accuracy": cls_metrics.accuracy,
                "precision": cls_metrics.precision,
                "recall": cls_metrics.recall,
                "f1_score": cls_metrics.f1_score,
                "macro_f1": cls_metrics.macro_f1,
                "weighted_f1": cls_metrics.weighted_f1,
                "mcc": cls_metrics.mcc,
                "confusion_matrix": cls_metrics.confusion_matrix,
                "support": cls_metrics.support
            },
            "directional": {
                "accuracy": dir_metrics.directional_accuracy,
                "up_precision": dir_metrics.up_precision,
                "down_precision": dir_metrics.down_precision,
                "neutral_precision": dir_metrics.neutral_precision,
                "transition_accuracy": dir_metrics.regime_transitions,
                "total_predictions": dir_metrics.total_predictions
            }
        }
        
        # Calibration if confidences provided
        if confidences:
            cal_metrics = EvaluationMetrics.calculate_calibration(
                y_true_int, y_pred_int, confidences
            )
            result["calibration"] = {
                "ece": cal_metrics.expected_calibration_error,
                "mce": cal_metrics.maximum_calibration_error,
                "brier_score": cal_metrics.brier_score,
                "reliability_diagram": cal_metrics.reliability_diagram
            }
        
        return result
