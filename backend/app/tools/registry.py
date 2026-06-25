"""
Tool registry — a factory/lookup mapping each supported intent to its mock
tool implementation. Adding a new intent + tool only requires:
  1. Writing a new `app/tools/<name>_tool.py` with a `run(message, memory)` fn.
  2. Registering it here.
No other code (router, schemas) needs to change, satisfying the
"easy to add new intents/tools" extensibility requirement.
"""
from typing import Callable, Dict

from app.services.memory_service import SessionMemory
from app.tools import (
    complaint_tool,
    escalation_tool,
    flight_tool,
    hotel_tool,
    refund_tool,
    tracking_tool,
)
from app.tools.base import ToolResult

ToolFn = Callable[[str, SessionMemory], ToolResult]

TOOL_REGISTRY: Dict[str, ToolFn] = {
    "order_tracking": tracking_tool.run,
    "refund_request": refund_tool.run,
    "complaint": complaint_tool.run,
    "escalation": escalation_tool.run,
    "hotel_search": hotel_tool.run,
    "flight_search": flight_tool.run,
}


def fallback_tool(message: str, memory: SessionMemory) -> ToolResult:
    """Graceful fallback when intent is unknown / no tool matches."""
    return ToolResult(
        ui_type="fallback",
        message=(
            "I couldn't confidently match that to a supported request "
            "(order tracking, refunds, complaints, escalation, hotels, or flights). "
            "Could you rephrase?"
        ),
        data={},
        tool_called="none",
    )


def get_tool(intent: str) -> ToolFn:
    return TOOL_REGISTRY.get(intent, fallback_tool)
