"""
Mock hotel search tool. Returns static, predefined data only.

Demonstrates follow-up comprehension: if the user's message references
"cheaper"/"cheap" and there was a prior hotel_search turn in memory, this tool
re-sorts/filters the same static dataset instead of re-asking for a city.
"""
from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_HOTELS = [
    {"name": "Grand Palace", "city": "Dubai", "price": 220, "rating": 4.8},
    {"name": "Marina Bay Suites", "city": "Dubai", "price": 180, "rating": 4.5},
    {"name": "Desert Rose Inn", "city": "Dubai", "price": 95, "rating": 4.1},
    {"name": "City Comfort Hotel", "city": "Dubai", "price": 70, "rating": 3.9},
]


def _format(hotels):
    return [
        {"name": h["name"], "price": f"${h['price']}", "rating": h["rating"]}
        for h in hotels
    ]


def run(message: str, memory: SessionMemory) -> ToolResult:
    text = message.lower()
    hotels = _STATIC_HOTELS

    is_follow_up = any(kw in text for kw in ["cheaper", "cheap", "lower price", "budget"])
    if is_follow_up:
        hotels = sorted(_STATIC_HOTELS, key=lambda h: h["price"])[:2]
        msg = "Here are cheaper hotel options based on your last search."
    else:
        hotels = sorted(_STATIC_HOTELS, key=lambda h: -h["rating"])
        msg = "Available hotels found."

    return ToolResult(
        ui_type="hotel_page",
        message=msg,
        data={"hotels": _format(hotels)},
        tool_called="hotel_tool",
    )
