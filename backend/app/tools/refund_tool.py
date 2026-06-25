"""Mock refund request tool. Returns static, predefined data only."""
from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_REFUND = {
    "refund_id": "REF-90442",
    "order_id": "ORD-58213",
    "amount": "$49.99",
    "status": "Approved - processing",
    "expected_in_account": "3-5 business days",
}


def run(message: str, memory: SessionMemory) -> ToolResult:
    return ToolResult(
        ui_type="refund_page",
        message="Your refund request has been received and approved.",
        data={"refund": _STATIC_REFUND},
        tool_called="refund_tool",
    )
