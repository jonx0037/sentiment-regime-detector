"""Chatbot endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sentiment_detector.api.schemas.chatbot import (
    ChatQueryRequest,
    ChatQueryResponse,
    ChatContextResponse,
)
from sentiment_detector.core.database import get_session
from sentiment_detector.core.logging import get_logger
from sentiment_detector.services.chatbot import chat, fetch_live_context

logger = get_logger(__name__)

router = APIRouter()


@router.get("/context", response_model=ChatContextResponse)
async def get_chatbot_context(
    session: AsyncSession = Depends(get_session),
) -> ChatContextResponse:
    """Get current dashboard context used by the chatbot."""
    try:
        ctx = await fetch_live_context(session)
        return ChatContextResponse(**ctx)
    except Exception as e:
        logger.error("Failed to fetch chatbot context", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard context")


@router.post("/query", response_model=ChatQueryResponse)
async def query_chatbot(
    request: ChatQueryRequest,
    session: AsyncSession = Depends(get_session),
) -> ChatQueryResponse:
    """Send a query to the chatbot and get a response."""
    try:
        result = await chat(
            session=session,
            query=request.query,
            conversation_history=[m.model_dump() for m in request.conversation_history],
            max_history_turns=request.max_history_turns,
        )
        return ChatQueryResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error("Chatbot query failed", error=str(e))
        raise HTTPException(status_code=500, detail="Chatbot query failed")
