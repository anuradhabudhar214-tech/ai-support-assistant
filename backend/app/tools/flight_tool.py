"""Mock flight search tool. Returns static, predefined data only."""
from app.services.memory_service import SessionMemory
from app.tools.base import ToolResult

_STATIC_FLIGHTS = [
    {"airline": "SkyWay Airlines", "from": "JFK", "to": "DXB", "price": 640, "duration": "13h 10m"},
    {"airline": "Aero Gulf", "from": "JFK", "to": "DXB", "price": 575, "duration": "14h 45m"},
    {"airline": "BlueJet", "from": "JFK", "to": "DXB", "price": 510, "duration": "16h 20m"},
]


def _format(flights):
    return [
        {
            "airline": f["airline"],
            "route": f"{f['from']} -> {f['to']}",
            "price": f"${f['price']}",
            "duration": f["duration"],
        }
        for f in flights
    ]


def run(message: str, memory: SessionMemory) -> ToolResult:
    text = message.lower()
    flights = _STATIC_FLIGHTS

    if any(kw in text for kw in ["cheaper", "cheap", "lower price", "budget"]):
        flights = sorted(_STATIC_FLIGHTS, key=lambda f: f["price"])[:2]
        msg = "Here are cheaper flight options based on your last search."
    else:
        flights = sorted(_STATIC_FLIGHTS, key=lambda f: f["price"])
        msg = "Available flights found."

    return ToolResult(
        ui_type="flight_page",
        message=msg,
        data={"flights": _format(flights)},
        tool_called="flight_tool",
    )
