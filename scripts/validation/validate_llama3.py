#!/usr/bin/env python3
"""Comprehensive Llama 3 validation.

This script validates ALL aspects of Llama 3 integration:
1. Model implementation exists
2. All backends work (transformers, llama.cpp, API, mock)
3. Inference performance benchmarking
4. Integration readiness for ensemble
5. HPC deployment readiness

Part of Phase 2: Complete System Validation
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def validate_llama_implementation() -> dict[str, any]:
    """Validate that Llama 3 implementation exists and is complete.

    Returns:
        Validation results for Llama implementation
    """
    print("\n" + "=" * 60)
    print("🔍 LLAMA 3 IMPLEMENTATION VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        from sentiment_detector.models.llama_sentiment import (
            LlamaSentimentModel,
            LlamaSentimentResult,
            create_llama_for_ensemble
        )

        print("✓ Llama 3 module imports successfully")

        # Check model IDs
        print(f"\n📋 Available model configurations:")
        for model_id, path in LlamaSentimentModel.MODEL_IDS.items():
            print(f"  • {model_id}: {path}")

        results["model_ids"] = LlamaSentimentModel.MODEL_IDS
        results["implementation_complete"] = True

        # Check helper function exists
        if callable(create_llama_for_ensemble):
            print("\n✓ Ensemble integration helper function exists")
            results["ensemble_helper"] = True
        else:
            results["issues"].append("create_llama_for_ensemble not callable")
            results["passed"] = False

    except ImportError as e:
        results["passed"] = False
        results["implementation_complete"] = False
        results["issues"].append(f"Llama 3 module not found: {e}")
        print(f"✗ Llama 3 module not found: {e}")

    return results


def validate_mock_backend() -> dict[str, any]:
    """Validate Llama 3 mock backend.

    Returns:
        Validation results for mock backend
    """
    print("\n" + "=" * 60)
    print("🔍 MOCK BACKEND VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

        model = LlamaSentimentModel(backend="mock")
        model.load()

        print("✓ Mock backend loads successfully")

        # Test single prediction
        test_texts = [
            "Bitcoin surges to new all-time high",
            "Markets crash on recession fears",
            "Economic data shows mixed signals"
        ]

        predictions = []
        for text in test_texts:
            result = model.predict(text)
            predictions.append({
                "text": text,
                "label": result.label,
                "confidence": result.confidence,
                "has_reasoning": bool(result.reasoning)
            })

            print(f"\n  Text: {text}")
            print(f"  → Label: {result.label}")
            print(f"  → Confidence: {result.confidence:.3f}")
            if result.reasoning:
                print(f"  → Reasoning: {result.reasoning[:80]}...")

        results["predictions"] = predictions
        results["single_prediction_works"] = True

        # Test batch prediction
        print("\n📊 Testing batch prediction...")
        start_time = time.time()
        batch_results = model.predict_batch(test_texts)
        elapsed = time.time() - start_time

        results["batch_prediction_works"] = len(batch_results) == len(test_texts)
        results["batch_time"] = elapsed
        results["texts_per_second"] = len(test_texts) / elapsed if elapsed > 0 else 0

        print(f"✓ Batch prediction works")
        print(f"  Processed {len(test_texts)} texts in {elapsed:.3f}s")
        print(f"  Throughput: {results['texts_per_second']:.0f} texts/sec")

    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"Mock backend failed: {e}")
        print(f"✗ Mock backend failed: {e}")

    return results


def validate_transformers_backend() -> dict[str, any]:
    """Validate Llama 3 transformers backend (requires model weights).

    Returns:
        Validation results for transformers backend
    """
    print("\n" + "=" * 60)
    print("🔍 TRANSFORMERS BACKEND VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": [],
        "skipped": False
    }

    # Check if model weights exist
    model_paths = [
        Path("models/llama3.1-8b-instruct"),
        Path("models/llama-3.1-8b-instruct"),
        Path("models/Meta-Llama-3-8B-Instruct")
    ]

    model_found = False
    model_path = None

    for path in model_paths:
        if path.exists():
            model_found = True
            model_path = path
            break

    if not model_found:
        print("⚠️  No Llama 3 model weights found")
        print("  Expected locations:")
        for path in model_paths:
            print(f"    • {path}")
        print("\n  Skipping transformers backend validation")
        results["skipped"] = True
        results["reason"] = "Model weights not downloaded"
        results["issues"].append("Model weights not found")
        return results

    try:
        from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

        print(f"✓ Found model weights at: {model_path}")

        # Try to load with transformers backend
        print("\n📊 Loading model with transformers backend...")
        print("  (This may take 30-60 seconds)")

        model = LlamaSentimentModel(
            model_id=str(model_path),
            backend="transformers",
            quantization="4bit"  # Use 4-bit for faster loading
        )

        start_time = time.time()
        model.load()
        load_time = time.time() - start_time

        print(f"✓ Model loaded in {load_time:.1f}s")

        results["load_time"] = load_time
        results["quantization"] = "4bit"

        # Test inference
        test_text = "Bitcoin surges to new all-time high on institutional demand"

        print(f"\n📊 Testing inference...")
        start_time = time.time()
        result = model.predict(test_text)
        inference_time = time.time() - start_time

        print(f"✓ Inference completed in {inference_time:.2f}s")
        print(f"  Label: {result.label}")
        print(f"  Confidence: {result.confidence:.3f}")
        if result.reasoning:
            print(f"  Reasoning: {result.reasoning[:100]}...")

        results["inference_time"] = inference_time
        results["inference_works"] = True

    except ImportError as e:
        results["passed"] = False
        results["issues"].append(f"Transformers library issue: {e}")
        print(f"✗ Transformers backend failed: {e}")
    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"Transformers backend error: {e}")
        print(f"✗ Transformers backend error: {e}")

    return results


def validate_llama_cpp_backend() -> dict[str, any]:
    """Validate Llama 3 llama.cpp backend (requires GGUF model).

    Returns:
        Validation results for llama.cpp backend
    """
    print("\n" + "=" * 60)
    print("🔍 LLAMA.CPP BACKEND VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": [],
        "skipped": False
    }

    # Check if GGUF model exists
    gguf_paths = [
        Path("models/llama-3.1-8b-instruct.Q4_K_M.gguf"),
        Path("models/llama3.1-8b-instruct.Q4_K_M.gguf"),
        Path("models/llama-3-8b-instruct.Q4_K_M.gguf")
    ]

    gguf_found = False
    gguf_path = None

    for path in gguf_paths:
        if path.exists():
            gguf_found = True
            gguf_path = path
            break

    if not gguf_found:
        print("⚠️  No GGUF model found")
        print("  Expected locations:")
        for path in gguf_paths:
            print(f"    • {path}")
        print("\n  Skipping llama.cpp backend validation")
        results["skipped"] = True
        results["reason"] = "GGUF model not downloaded"
        results["issues"].append("GGUF model not found")
        return results

    try:
        from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

        print(f"✓ Found GGUF model at: {gguf_path}")

        # Try to load with llama.cpp backend
        print("\n📊 Loading model with llama.cpp backend...")

        model = LlamaSentimentModel(
            model_id=str(gguf_path),
            backend="llama_cpp"
        )

        start_time = time.time()
        model.load()
        load_time = time.time() - start_time

        print(f"✓ Model loaded in {load_time:.1f}s")

        results["load_time"] = load_time

        # Test inference
        test_text = "Markets crash as recession fears intensify"

        print(f"\n📊 Testing inference...")
        start_time = time.time()
        result = model.predict(test_text)
        inference_time = time.time() - start_time

        print(f"✓ Inference completed in {inference_time:.2f}s")
        print(f"  Label: {result.label}")
        print(f"  Confidence: {result.confidence:.3f}")

        results["inference_time"] = inference_time
        results["inference_works"] = True

        # Benchmark throughput
        print(f"\n📊 Benchmarking throughput (10 texts)...")
        benchmark_texts = [test_text] * 10

        start_time = time.time()
        for text in benchmark_texts:
            model.predict(text)
        elapsed = time.time() - start_time

        throughput = len(benchmark_texts) / elapsed
        results["throughput"] = throughput

        print(f"✓ Throughput: {throughput:.1f} texts/sec")

    except ImportError as e:
        results["passed"] = False
        results["issues"].append(f"llama.cpp library issue: {e}")
        print(f"✗ llama.cpp backend failed: {e}")
    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"llama.cpp backend error: {e}")
        print(f"✗ llama.cpp backend error: {e}")

    return results


def validate_api_backend() -> dict[str, any]:
    """Validate Llama 3 external API backend.

    Returns:
        Validation results for API backend
    """
    print("\n" + "=" * 60)
    print("🔍 EXTERNAL API BACKEND VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": [],
        "skipped": False
    }

    # Check for API key in environment
    import os

    api_key = os.getenv("LLAMA_API_KEY") or os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("⚠️  No API key found in environment")
        print("  Set LLAMA_API_KEY or OPENROUTER_API_KEY to test")
        print("\n  Skipping API backend validation")
        results["skipped"] = True
        results["reason"] = "No API key configured"
        results["issues"].append("API key not found")
        return results

    try:
        from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

        print("✓ API key found in environment")

        # Try to load with API backend
        print("\n📊 Testing API backend...")

        model = LlamaSentimentModel(backend="api")
        model.load()

        print("✓ API backend initialized")

        # Test inference
        test_text = "Economic data shows mixed signals"

        print(f"\n📊 Testing API inference...")
        print("  (This will consume API credits)")

        start_time = time.time()
        result = model.predict(test_text)
        api_latency = time.time() - start_time

        print(f"✓ API call completed in {api_latency:.2f}s")
        print(f"  Label: {result.label}")
        print(f"  Confidence: {result.confidence:.3f}")

        results["api_latency"] = api_latency
        results["api_works"] = True

    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"API backend error: {e}")
        print(f"✗ API backend failed: {e}")

    return results


def validate_ensemble_integration() -> dict[str, any]:
    """Validate that Llama 3 can integrate into SentimentEnsemble.

    Returns:
        Validation results for ensemble integration
    """
    print("\n" + "=" * 60)
    print("🔍 ENSEMBLE INTEGRATION VALIDATION")
    print("=" * 60)

    results = {
        "passed": True,
        "issues": []
    }

    try:
        from sentiment_detector.models.llama_sentiment import create_llama_for_ensemble
        from sentiment_detector.models.sentiment_ensemble import SentimentEnsemble

        print("✓ Both modules import successfully")

        # Create Llama function for ensemble
        llama_func = create_llama_for_ensemble(backend="mock")

        print("✓ Llama function created for ensemble")

        # Try to add to ensemble
        test_ensemble = SentimentEnsemble(
            models={"llama3": llama_func},
            weights={"llama3": 1.0}
        )

        print("✓ Ensemble with Llama 3 instantiates")

        # Test prediction
        test_text = "Bitcoin price stabilizes after recent volatility"
        result = test_ensemble.predict(test_text)

        print(f"\n✓ Ensemble prediction works")
        print(f"  Label: {result.label}")
        print(f"  Confidence: {result.confidence:.3f}")
        print(f"  Models used: {list(result.model_predictions.keys())}")

        results["integration_works"] = True
        results["integrated"] = False  # Not yet in production ensemble

    except Exception as e:
        results["passed"] = False
        results["issues"].append(f"Ensemble integration failed: {e}")
        print(f"✗ Ensemble integration failed: {e}")

    return results


def validate_hpc_readiness() -> dict[str, any]:
    """Check HPC deployment readiness.

    Returns:
        Validation results for HPC readiness
    """
    print("\n" + "=" * 60)
    print("🔍 HPC DEPLOYMENT READINESS")
    print("=" * 60)

    results = {
        "ready": True,
        "blockers": []
    }

    # Check for HPC batch script
    hpc_script = Path("scripts/hpc/run_llama_sentiment.sh")
    if hpc_script.exists():
        print(f"✓ HPC batch script exists: {hpc_script}")
        results["batch_script"] = str(hpc_script)
    else:
        results["blockers"].append("HPC batch script not created")
        results["ready"] = False
        print(f"✗ HPC batch script missing: {hpc_script}")

    # Check for processing script
    process_script = Path("scripts/hpc/process_batch_llama.py")
    if process_script.exists():
        print(f"✓ Processing script exists: {process_script}")
        results["process_script"] = str(process_script)
    else:
        results["blockers"].append("HPC processing script not created")
        results["ready"] = False
        print(f"✗ Processing script missing: {process_script}")

    # Check dependencies
    print("\n📦 Checking dependencies...")
    try:
        import torch
        print(f"✓ PyTorch installed (version {torch.__version__})")
        results["pytorch"] = torch.__version__
    except ImportError:
        results["blockers"].append("PyTorch not installed")
        results["ready"] = False
        print("✗ PyTorch not installed")

    try:
        import transformers
        print(f"✓ Transformers installed (version {transformers.__version__})")
        results["transformers"] = transformers.__version__
    except ImportError:
        results["blockers"].append("Transformers not installed")
        results["ready"] = False
        print("✗ Transformers not installed")

    return results


def main():
    """Run comprehensive Llama 3 validation."""
    print("🔍 COMPREHENSIVE LLAMA 3 VALIDATION")
    print("=" * 60)
    print("Validating all aspects of Llama 3 integration")
    print()

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "overall_passed": True
    }

    try:
        # Validate implementation
        impl_results = validate_llama_implementation()
        all_results["implementation"] = impl_results
        if not impl_results["passed"]:
            all_results["overall_passed"] = False

        # Validate mock backend (always available)
        mock_results = validate_mock_backend()
        all_results["mock_backend"] = mock_results
        if not mock_results["passed"]:
            all_results["overall_passed"] = False

        # Validate transformers backend (if model available)
        transformers_results = validate_transformers_backend()
        all_results["transformers_backend"] = transformers_results
        if not transformers_results["passed"] and not transformers_results.get("skipped"):
            all_results["overall_passed"] = False

        # Validate llama.cpp backend (if GGUF available)
        cpp_results = validate_llama_cpp_backend()
        all_results["llama_cpp_backend"] = cpp_results
        if not cpp_results["passed"] and not cpp_results.get("skipped"):
            all_results["overall_passed"] = False

        # Validate API backend (if key available)
        api_results = validate_api_backend()
        all_results["api_backend"] = api_results
        if not api_results["passed"] and not api_results.get("skipped"):
            all_results["overall_passed"] = False

        # Validate ensemble integration
        ensemble_results = validate_ensemble_integration()
        all_results["ensemble_integration"] = ensemble_results
        if not ensemble_results["passed"]:
            all_results["overall_passed"] = False

        # Check HPC readiness
        hpc_results = validate_hpc_readiness()
        all_results["hpc_readiness"] = hpc_results

        # Summary
        print("\n" + "=" * 60)
        if all_results["overall_passed"]:
            print("✅ LLAMA 3 VALIDATION PASSED")
            print("   All available backends working")
        else:
            print("❌ LLAMA 3 VALIDATION FAILED")
            print("   Issues found in one or more components")

        # Recommendations
        print("\n📋 Recommendations:")
        if transformers_results.get("skipped"):
            print("  • Download Llama 3.1 8B model for full testing")
        if cpp_results.get("skipped"):
            print("  • Download GGUF model for faster inference")
        if api_results.get("skipped"):
            print("  • Set up API key for production fallback")
        if not ensemble_results.get("integrated"):
            print("  • Integrate Llama 3 into production ensemble")
        if not hpc_results.get("ready"):
            print("  • Create HPC deployment scripts")

        print("=" * 60)

        # Save results
        output_dir = Path("results/validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"llama3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
