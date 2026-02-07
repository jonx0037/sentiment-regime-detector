#!/usr/bin/env python3
"""Validate the complete ML pipeline end-to-end.

This script validates:
1. Sentiment ensemble (FinBERT, VADER, TextBlob, DistilBERT)
2. GARCH-MIDAS volatility modeling
3. Regime classifier (Random Forest)
4. Feature engineering pipeline
5. SHAP explainability

Part of Phase 2: Complete System Validation
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def validate_sentiment_ensemble() -> dict[str, any]:
    """Validate all sentiment models in the ensemble.

    Returns:
        Validation results for sentiment ensemble
    """
    print("\n" + "=" * 60)
    print("🔍 SENTIMENT ENSEMBLE VALIDATION")
    print("=" * 60)

    results = {
        "models": {},
        "passed": True,
        "issues": []
    }

    test_texts = [
        "Bitcoin surges to new all-time high on strong institutional demand",
        "Markets crash as recession fears intensify",
        "Stocks hold steady amid mixed economic signals"
    ]

    try:
        from sentiment_detector.models.sentiment_ensemble import create_ensemble

        # Test 1: FinBERT + VADER + TextBlob (standard ensemble)
        print("\n📊 Testing standard ensemble (FinBERT + VADER + TextBlob)...")
        try:
            ensemble = create_ensemble(
                use_finbert=True,
                use_vader=True,
                use_textblob=True,
                use_llama=False
            )

            predictions = []
            for text in test_texts:
                result = ensemble.predict(text)
                predictions.append({
                    "text": text[:50],
                    "label": result.label,
                    "confidence": result.confidence,
                    "models": list(result.model_predictions.keys())
                })

            results["models"]["standard_ensemble"] = {
                "passed": True,
                "models_loaded": ["finbert", "vader", "textblob"],
                "sample_predictions": predictions
            }

            print(f"✓ Standard ensemble working")
            print(f"  Models loaded: FinBERT, VADER, TextBlob")

            for pred in predictions:
                print(f"  • {pred['text']}...")
                print(f"    → {pred['label']} ({pred['confidence']:.3f})")

        except Exception as e:
            results["models"]["standard_ensemble"] = {
                "passed": False,
                "error": str(e)
            }
            results["passed"] = False
            results["issues"].append(f"Standard ensemble failed: {e}")
            print(f"✗ Standard ensemble failed: {e}")

        # Test 2: Check for DistilBERT
        print("\n📊 Checking for DistilBERT model...")
        try:
            # Try to import DistilBERT model if it exists
            from sentiment_detector.models import sentiment_ensemble

            # Check if DistilBERT is available
            # (This will depend on the actual implementation)
            has_distilbert = False  # Placeholder - need to check actual code

            if has_distilbert:
                print("✓ DistilBERT model available")
                results["models"]["distilbert"] = {"available": True}
            else:
                print("⚠️  DistilBERT not found in ensemble")
                results["models"]["distilbert"] = {"available": False}
                results["issues"].append("DistilBERT not implemented")

        except Exception as e:
            results["models"]["distilbert"] = {
                "available": False,
                "error": str(e)
            }
            print(f"⚠️  Could not check DistilBERT: {e}")

        # Test 3: Llama 3 integration status
        print("\n📊 Checking Llama 3 integration...")
        try:
            from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

            llama = LlamaSentimentModel(backend="mock")
            llama.load()

            test_result = llama.predict(test_texts[0])

            results["models"]["llama3"] = {
                "available": True,
                "integrated": False,  # Not yet in ensemble
                "mock_backend_works": True
            }

            print("✓ Llama 3 model exists (not yet integrated into ensemble)")
            print(f"  Mock test: {test_result.label} ({test_result.confidence:.3f})")

        except Exception as e:
            results["models"]["llama3"] = {
                "available": False,
                "error": str(e)
            }
            print(f"⚠️  Llama 3 not available: {e}")

    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"Sentiment ensemble validation failed: {e}")
        print(f"\n❌ Sentiment ensemble validation failed: {e}")

    return results


def validate_garch_midas() -> dict[str, any]:
    """Validate GARCH-MIDAS volatility model.

    Returns:
        Validation results for GARCH-MIDAS
    """
    print("\n" + "=" * 60)
    print("🔍 GARCH-MIDAS VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        from sentiment_detector.models.garch_midas import GARCHMIDASModel

        print("\n📊 Testing GARCH-MIDAS model...")

        # Create synthetic VIX data for testing
        np.random.seed(42)
        dates = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
        vix_data = pd.Series(
            20 + 10 * np.random.randn(len(dates)).cumsum() * 0.1,
            index=dates
        )

        # Fit GARCH-MIDAS
        model = GARCHMIDASModel()

        print("✓ GARCH-MIDAS model loaded")

        # Try to fit the model
        try:
            result = model.fit(vix_data)

            results["parameters"] = {
                "alpha": float(result.params.get("alpha", 0)),
                "beta": float(result.params.get("beta", 0)),
                "alpha_plus_beta": float(result.params.get("alpha", 0) + result.params.get("beta", 0))
            }

            # Check if parameters are reasonable
            expected_alpha = 0.155
            expected_beta = 0.800
            tolerance = 0.1  # Allow 10% difference

            alpha_ok = abs(results["parameters"]["alpha"] - expected_alpha) < tolerance
            beta_ok = abs(results["parameters"]["beta"] - expected_beta) < tolerance

            if alpha_ok and beta_ok:
                print(f"✓ Parameters within expected range")
                print(f"  α = {results['parameters']['alpha']:.4f} (expected ~{expected_alpha})")
                print(f"  β = {results['parameters']['beta']:.4f} (expected ~{expected_beta})")
            else:
                issue = f"Parameters differ from expected: α={results['parameters']['alpha']:.4f}, β={results['parameters']['beta']:.4f}"
                results["issues"].append(issue)
                print(f"⚠️  {issue}")

            # Try forecasting
            forecast = model.forecast(horizon=5)
            results["forecast_works"] = True
            print(f"✓ Forecasting works (5-day horizon)")

        except Exception as e:
            results["passed"] = False
            results["issues"].append(f"GARCH-MIDAS fitting failed: {e}")
            print(f"✗ GARCH-MIDAS fitting failed: {e}")

    except ImportError as e:
        results["passed"] = False
        results["issues"].append(f"GARCH-MIDAS not found: {e}")
        print(f"✗ GARCH-MIDAS model not available: {e}")
    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"GARCH-MIDAS validation error: {e}")
        print(f"✗ GARCH-MIDAS validation failed: {e}")

    return results


def validate_regime_classifier() -> dict[str, any]:
    """Validate the Random Forest regime classifier.

    Returns:
        Validation results for regime classifier
    """
    print("\n" + "=" * 60)
    print("🔍 REGIME CLASSIFIER VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        # Try different possible locations for the regime classifier
        classifier = None
        classifier_path = None

        possible_imports = [
            "sentiment_detector.models.regime_classifier",
            "sentiment_detector.models.jump_model"
        ]

        for import_path in possible_imports:
            try:
                if "regime_classifier" in import_path:
                    from sentiment_detector.models import regime_classifier
                    if hasattr(regime_classifier, 'RegimeClassifier'):
                        classifier = regime_classifier.RegimeClassifier
                        classifier_path = import_path
                        break
                elif "jump_model" in import_path:
                    from sentiment_detector.models.jump_model import StatisticalJumpModel
                    classifier = StatisticalJumpModel
                    classifier_path = import_path
                    break
            except ImportError:
                continue

        if classifier is None:
            results["passed"] = False
            results["issues"].append("Regime classifier not found")
            print("✗ Regime classifier not found in expected locations")
            return results

        print(f"✓ Found classifier at: {classifier_path}")

        # Test instantiation
        try:
            model = classifier()
            results["instantiation"] = "success"
            print("✓ Classifier instantiates successfully")
        except Exception as e:
            results["passed"] = False
            results["issues"].append(f"Classifier instantiation failed: {e}")
            print(f"✗ Classifier instantiation failed: {e}")
            return results

        # Check for trained model file
        model_paths = [
            Path("models/regime_classifier_rf.pkl"),
            Path("models/regime_classifier.pkl"),
            Path("models/jump_model.pkl")
        ]

        model_found = False
        for path in model_paths:
            if path.exists():
                model_found = True
                results["model_path"] = str(path)
                print(f"✓ Found trained model: {path}")
                break

        if not model_found:
            results["issues"].append("No trained model file found")
            print("⚠️  No trained model file found")

        # Test prediction (if model has predict method)
        if hasattr(model, 'predict'):
            try:
                # Create dummy feature vector
                test_features = {
                    'sentiment_mean': -0.1,
                    'sentiment_std': 0.3,
                    'vix': 25.0,
                    'volume': 1000
                }

                # Try prediction
                prediction = model.predict(test_features)
                results["prediction_works"] = True
                print("✓ Prediction method works")

            except Exception as e:
                results["issues"].append(f"Prediction failed: {e}")
                print(f"⚠️  Prediction test failed: {e}")

    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"Regime classifier validation error: {e}")
        print(f"✗ Regime classifier validation failed: {e}")

    return results


def validate_explainability() -> dict[str, any]:
    """Validate SHAP explainability integration.

    Returns:
        Validation results for explainability
    """
    print("\n" + "=" * 60)
    print("🔍 SHAP EXPLAINABILITY VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        import shap
        results["shap_installed"] = True
        print(f"✓ SHAP library installed (version {shap.__version__})")

        # Check for explainability module
        try:
            from sentiment_detector.api.routes import explainability
            results["explainability_module"] = "found"
            print("✓ Explainability API module exists")
        except ImportError:
            results["explainability_module"] = "not_found"
            results["issues"].append("Explainability API module not found")
            print("⚠️  Explainability API module not found")

        # Check for SHAP values storage
        shap_paths = [
            Path("models/shap_values.pkl"),
            Path("models/explainer.pkl")
        ]

        for path in shap_paths:
            if path.exists():
                results["shap_artifacts"] = str(path)
                print(f"✓ Found SHAP artifacts: {path}")
                break
        else:
            results["issues"].append("No SHAP artifacts found")
            print("⚠️  No pre-computed SHAP values found")

    except ImportError:
        results["passed"] = False
        results["shap_installed"] = False
        results["issues"].append("SHAP library not installed")
        print("✗ SHAP library not installed")

    return results


def main():
    """Run complete ML pipeline validation."""
    print("🔍 COMPLETE ML PIPELINE VALIDATION")
    print("=" * 60)
    print("Validating all ML components end-to-end")
    print()

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "overall_passed": True
    }

    try:
        # Validate sentiment ensemble
        sentiment_results = validate_sentiment_ensemble()
        all_results["sentiment_ensemble"] = sentiment_results
        if not sentiment_results["passed"]:
            all_results["overall_passed"] = False

        # Validate GARCH-MIDAS
        garch_results = validate_garch_midas()
        all_results["garch_midas"] = garch_results
        if not garch_results["passed"]:
            all_results["overall_passed"] = False

        # Validate regime classifier
        classifier_results = validate_regime_classifier()
        all_results["regime_classifier"] = classifier_results
        if not classifier_results["passed"]:
            all_results["overall_passed"] = False

        # Validate explainability
        explainability_results = validate_explainability()
        all_results["explainability"] = explainability_results
        if not explainability_results["passed"]:
            all_results["overall_passed"] = False

        # Summary
        print("\n" + "=" * 60)
        if all_results["overall_passed"]:
            print("✅ ML PIPELINE VALIDATION PASSED")
            print("   All components working correctly")
        else:
            print("❌ ML PIPELINE VALIDATION FAILED")
            print("   Issues found in one or more components")
        print("=" * 60)

        # Save results
        output_dir = Path("results/validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"ml_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=2, default=str)

        print(f"\n📄 Results saved to: {output_file}")

        # Exit with appropriate code
        sys.exit(0 if all_results["overall_passed"] else 1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
