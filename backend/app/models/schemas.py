"""
Pydantic schemas for the AI Support Assistant API.

These models guarantee that every /chat response is strictly valid JSON
matching the contract the Flutter frontend depends on.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Intent(str, Enum):
    ORDER_TRACKING = "order_tracking"
    REFUND_REQUEST = "refund_request"
    COMPLAINT = "complaint"
    ESCALATION = "escalation"
    HOTEL_SEARCH = "hotel_search"
    FLIGHT_SEARCH = "flight_search"
    UNKNOWN = "unknown"


class UiType(str, Enum):
    HOTEL_PAGE = "hotel_page"
    FLIGHT_PAGE = "flight_page"
    TRACKING_PAGE = "tracking_page"
    REFUND_PAGE = "refund_page"
    COMPLAINT_PAGE = "complaint_page"
    ESCALATION_PAGE = "escalation_page"
    FALLBACK = "fallback"


class ChatRequest(BaseModel):
    """Incoming payload from the Flutter client."""

    message: str = Field(..., min_length=1, description="The user's latest message")
    session_id: str = Field(
        default="default",
        description="Conversation/session identifier used to scope short-term memory",
    )
    # Optional: client can also forward its own history, but the backend is the
    # source of truth and keeps its own in-memory store keyed by session_id.
    history: Optional[List[Dict[str, str]]] = Field(default=None)


class ChatResponse(BaseModel):
    """Strict, structured response contract returned by POST /chat."""

    intent: Intent
    tool_called: Optional[str] = None
    ui_type: UiType
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)
    session_id: str
    turn: int = Field(..., description="1-indexed turn count for this session")

    class Config:
        use_enum_values = True
