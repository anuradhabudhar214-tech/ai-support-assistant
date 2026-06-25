"""Mock escalation tool. Returns static, predefined data only."""
from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_ESCALATION = {
    "escalation_id": "ESC-77310",
    "assigned_to": "Senior Support Team",
    "status": "Escalated",
    "expected_response": "Within 2 hours",
}


def run(message: str, memory: SessionMemory) -> ToolResult:
    return ToolResult(
        ui_type="escalation_page",
        message="Your request has been escalated to our senior support team.",
        data={"escalation": _STATIC_ESCALATION},
        tool_called="escalation_tool",
    )
