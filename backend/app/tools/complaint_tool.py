"""Mock complaint logging tool. Returns static, predefined data only."""
import time

from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_COMPLAINT = {
    "ticket_id": "CMP-31207",
    "priority": "Medium",
    "status": "Logged",
    "sla": "Response within 24 hours",
}


def run(message: str, memory: SessionMemory) -> ToolResult:
    data = dict(_STATIC_COMPLAINT)
    data["logged_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    return ToolResult(
        ui_type="complaint_page",
        message="Your complaint has been logged. Our team will follow up shortly.",
        data={"complaint": data},
        tool_called="complaint_tool",
    )
