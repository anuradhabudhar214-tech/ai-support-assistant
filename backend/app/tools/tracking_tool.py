"""Mock order tracking tool. Returns static, predefined data only."""
from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_TRACKING = {
    "order_id": "ORD-58213",
    "status": "Out for delivery",
    "carrier": "Swift Logistics",
    "estimated_delivery": "Today, 6:00 PM",
    "history": [
        {"stage": "Order placed", "done": True},
        {"stage": "Packed", "done": True},
        {"stage": "Shipped", "done": True},
        {"stage": "Out for delivery", "done": True},
        {"stage": "Delivered", "done": False},
    ],
}


def run(message: str, memory: SessionMemory) -> ToolResult:
    return ToolResult(
        ui_type="tracking_page",
        message="Here's the latest status for your order.",
        data={"tracking": _STATIC_TRACKING},
        tool_called="tracking_tool",
    )
