"""
Llama 3 Sentiment Model Integration.

This module provides an interface for integrating Llama 3 (7B/8B)
into the sentiment ensemble. Llama 3 is used for:
- Zero-shot sentiment classification
- Financial context understanding
- Handling nuanced/sarcastic content

Per Dakalbab et al. (2024), LLMs improve ensemble accuracy
especially for complex financial discourse.

Supports:
- Local inference via transformers/llama.cpp
- MANEFRAME HPC deployment
- API fallback (OpenRouter, Together AI)
"""

from dataclasses import dataclass
from typing import Optional, Literal, Callable
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)

# Try to import LLM libraries
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available for Llama 3")

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False


class LlamaBackend(Enum):
    """Supported Llama inference backends."""
    TRANSFORMERS = "transformers"  # HuggingFace transformers
    LLAMA_CPP = "llama_cpp"        # llama.cpp (quantized)
    API = "api"                     # External API
    MOCK = "mock"                   # Testing mode


@dataclass
class LlamaSentimentResult:
    """
    Sentiment result from Llama model.
    
    Attributes:
        label: Sentiment label (POSITIVE, NEGATIVE, NEUTRAL)
        confidence: Model confidence [0, 1]
        reasoning: Optional explanation from model
        raw_output: Raw model output text
    """
    label: str
    confidence: float
    reasoning: Optional[str] = None
    raw_output: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "confidence": self.confidence,
            "reasoning": self.reasoning
        }


# Prompt templates for sentiment analysis
SENTIMENT_PROMPT_TEMPLATE = """Analyze the sentiment of this financial text.

Text: {text}

Classify as POSITIVE, NEGATIVE, or NEUTRAL.
Provide your answer in this exact format:
SENTIMENT: [POSITIVE/NEGATIVE/NEUTRAL]
CONFIDENCE: [0.0-1.0]
REASON: [brief explanation]"""

SENTIMENT_PROMPT_SIMPLE = """Financial sentiment (POSITIVE/NEGATIVE/NEUTRAL):
Text: "{text}"
Answer:"""


class LlamaSentimentModel:
    """
    Llama 3 model for sentiment analysis.
    
    Supports multiple backends:
    - transformers: Full model via HuggingFace
    - llama_cpp: Quantized GGUF model
    - api: External API (OpenRouter, Together AI)
    - mock: Testing without GPU
    
    Example:
        >>> model = LlamaSentimentModel(backend="transformers")
        >>> model.load()
        >>> result = model.predict("Bitcoin surges to new ATH!")
        >>> print(result.label, result.confidence)
    """
    
    # Model identifiers
    MODEL_IDS = {
        "llama3-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
        "llama3-7b": "meta-llama/Llama-3-7B-hf",  # Alias
        "llama3.1-8b": "meta-llama/Llama-3.1-8B-Instruct",
    }
    
    def __init__(
        self,
        model_id: str = "llama3-8b",
        backend: Literal["transformers", "llama_cpp", "api", "mock"] = "mock",
        device: str = "auto",
        quantization: Optional[str] = None,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        max_tokens: int = 256,
        temperature: float = 0.1
    ):
        """
        Initialize Llama sentiment model.
        
        Args:
            model_id: Model identifier or path
            backend: Inference backend to use
            device: Device for inference
            quantization: Quantization method (4bit, 8bit, None)
            api_key: API key for external APIs
            api_url: API endpoint URL
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
        """
        self.model_id = self.MODEL_IDS.get(model_id, model_id)
        self.backend = LlamaBackend(backend)
        self.device = device
        self.quantization = quantization
        self.api_key = api_key
        self.api_url = api_url
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        self._model = None
        self._tokenizer = None
        self._loaded = False
    
    def load(self) -> None:
        """Load the model based on backend."""
        if self._loaded:
            return
        
        if self.backend == LlamaBackend.MOCK:
            logger.info("Using mock Llama backend for testing")
            self._loaded = True
            return
        
        if self.backend == LlamaBackend.TRANSFORMERS:
            self._load_transformers()
        elif self.backend == LlamaBackend.LLAMA_CPP:
            self._load_llama_cpp()
        elif self.backend == LlamaBackend.API:
            self._setup_api()
        
        self._loaded = True
    
    def _load_transformers(self) -> None:
        """Load model via HuggingFace transformers."""
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not available")
        
        logger.info(f"Loading {self.model_id} via transformers...")
        
        # Determine device
        if self.device == "auto":
            if torch.cuda.is_available():
                device_map = "auto"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                device_map = "mps"
            else:
                device_map = "cpu"
        else:
            device_map = self.device
        
        # Load with optional quantization
        load_kwargs = {
            "device_map": device_map,
            "trust_remote_code": True,
        }
        
        if self.quantization == "4bit":
            from transformers import BitsAndBytesConfig
            load_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16
            )
        elif self.quantization == "8bit":
            load_kwargs["load_in_8bit"] = True
        
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id, **load_kwargs
        )
        
        logger.info(f"Loaded Llama model on {device_map}")
    
    def _load_llama_cpp(self) -> None:
        """Load quantized model via llama.cpp."""
        if not LLAMA_CPP_AVAILABLE:
            raise ImportError("llama-cpp-python not available")
        
        logger.info(f"Loading {self.model_id} via llama.cpp...")
        
        # Assumes model_id is path to GGUF file
        self._model = Llama(
            model_path=self.model_id,
            n_ctx=2048,
            n_threads=4,
            n_gpu_layers=-1  # Use all GPU layers
        )
        
        logger.info("Loaded llama.cpp model")
    
    def _setup_api(self) -> None:
        """Setup API client."""
        if not self.api_key or not self.api_url:
            raise ValueError("api_key and api_url required for API backend")
        
        logger.info(f"Using API backend: {self.api_url}")
    
    def predict(self, text: str) -> LlamaSentimentResult:
        """
        Predict sentiment for a single text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            LlamaSentimentResult with label and confidence
        """
        if not self._loaded:
            self.load()
        
        if self.backend == LlamaBackend.MOCK:
            return self._mock_predict(text)
        
        # Generate prompt
        prompt = SENTIMENT_PROMPT_TEMPLATE.format(text=text[:1000])
        
        # Get model output
        if self.backend == LlamaBackend.TRANSFORMERS:
            output = self._generate_transformers(prompt)
        elif self.backend == LlamaBackend.LLAMA_CPP:
            output = self._generate_llama_cpp(prompt)
        elif self.backend == LlamaBackend.API:
            output = self._generate_api(prompt)
        else:
            return self._mock_predict(text)
        
        # Parse output
        return self._parse_output(output)
    
    def _generate_transformers(self, prompt: str) -> str:
        """Generate using transformers."""
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self._tokenizer.eos_token_id
            )
        
        response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Remove prompt from response
        return response[len(prompt):].strip()
    
    def _generate_llama_cpp(self, prompt: str) -> str:
        """Generate using llama.cpp."""
        output = self._model(
            prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stop=["Text:", "\n\n"]
        )
        return output["choices"][0]["text"]
    
    def _generate_api(self, prompt: str) -> str:
        """Generate using external API."""
        import requests
        
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model_id,
                "prompt": prompt,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"]
    
    def _parse_output(self, output: str) -> LlamaSentimentResult:
        """Parse model output to extract sentiment."""
        output = output.upper()
        
        # Extract sentiment label
        label = "NEUTRAL"
        if "POSITIVE" in output:
            label = "POSITIVE"
        elif "NEGATIVE" in output:
            label = "NEGATIVE"
        
        # Extract confidence
        confidence = 0.7  # Default
        conf_match = re.search(r'CONFIDENCE[:\s]*([0-9.]+)', output)
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                pass
        
        # Extract reasoning
        reason_match = re.search(r'REASON[:\s]*(.+?)(?:\n|$)', output, re.IGNORECASE)
        reasoning = reason_match.group(1).strip() if reason_match else None
        
        return LlamaSentimentResult(
            label=label,
            confidence=confidence,
            reasoning=reasoning,
            raw_output=output
        )
    
    def _mock_predict(self, text: str) -> LlamaSentimentResult:
        """Mock prediction for testing."""
        text_lower = text.lower()
        
        # Simple keyword-based mock
        positive_words = ['surge', 'gain', 'bull', 'up', 'rise', 'profit', 'moon']
        negative_words = ['crash', 'drop', 'bear', 'down', 'loss', 'fear', 'dump']
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            label = "POSITIVE"
            confidence = 0.6 + min(pos_count, 3) * 0.1
        elif neg_count > pos_count:
            label = "NEGATIVE"
            confidence = 0.6 + min(neg_count, 3) * 0.1
        else:
            label = "NEUTRAL"
            confidence = 0.5
        
        return LlamaSentimentResult(
            label=label,
            confidence=confidence,
            reasoning="Mock prediction based on keyword matching",
            raw_output=None
        )
    
    def predict_batch(
        self,
        texts: list[str],
        batch_size: int = 8
    ) -> list[LlamaSentimentResult]:
        """
        Predict sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            batch_size: Batch size for processing
            
        Returns:
            List of LlamaSentimentResult objects
        """
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results


def create_llama_for_ensemble(
    backend: str = "mock",
    model_id: str = "llama3-8b",
    **kwargs
) -> Callable[[str], tuple[str, float]]:
    """
    Create a Llama model function for use in SentimentEnsemble.
    
    Returns a callable that takes text and returns (label, confidence).
    
    Example:
        >>> llama_fn = create_llama_for_ensemble(backend="mock")
        >>> label, conf = llama_fn("Bitcoin surges!")
    """
    model = LlamaSentimentModel(
        model_id=model_id,
        backend=backend,
        **kwargs
    )
    model.load()
    
    def predict_fn(text: str) -> tuple[str, float]:
        result = model.predict(text)
        return result.label, result.confidence
    
    return predict_fn
