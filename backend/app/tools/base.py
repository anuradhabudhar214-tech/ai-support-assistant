"""Shared types for mock tool implementations."""
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    ui_type: str
    message: str
    data: Dict[str, Any]
    tool_called: str
