"""Chatbot request/response schemas."""

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    conversation_history: list[ChatMessage] = Field(default_factory=list)
    max_history_turns: int = Field(default=6, ge=0, le=20)


class ChatSource(BaseModel):
    source: str
    snippet: str


class ChatQueryResponse(BaseModel):
    response: str
    sources_used: list[ChatSource]
    regime_context_used: bool


class ChatContextResponse(BaseModel):
    """Live dashboard context for the chatbot system prompt."""

    current_regime: str | None
    regime_confidence: float | None
    probabilities: dict[str, float] = {}
    sentiment_scores: dict[str, float]
    stress_level: float | None
    vix_level: float | None = None
    volatility_regime: str | None = None
    volatility_score: float | None = None
    recent_transitions: list[dict]
    summary: str
