"""Pydantic models for bike sales agent."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    conversation_id: str


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    conversation_id: str
    interest_detected: bool = False