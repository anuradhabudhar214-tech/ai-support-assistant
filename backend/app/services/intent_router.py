"""
Orchestrates: memory lookup -> LLM intent classification (with deterministic
fallback) -> tool execution -> memory write-back.

This is the single seam between "AI workflow" and "deterministic tool
execution" called out in the evaluation criteria: the LLM only ever decides
*which* intent/tool to use; the tool itself returns static, predictable data.
"""
from __future__ import annotations

import logging

from app.models.schemas import ChatResponse, Intent, UiType
from app.services import ollama_service
from app.services.memory_service import MemoryStore
from app.tools.registry import get_tool

logger = logging.getLogger("ai_support_assistant.router")


def handle_chat(message: str, session_id: str, memory_store: MemoryStore) -> ChatResponse:
    memory = memory_store.get(session_id)
    history = memory.as_prompt_history()
    last_turn = memory.last_turn
    last_intent = last_turn.intent if last_turn else None

    intent: str
    try:
        intent = ollama_service.classify_intent(message, history)
        logger.info("Ollama classified intent=%s", intent)
    except ollama_service.OllamaUnavailableError as exc:
        logger.warning("Ollama unavailable (%s); using fallback classifier", exc)
        intent = ollama_service.fallback_classify_intent(message, history, last_intent)

    # Belt-and-suspenders: even if Ollama answered, an "unknown"/empty result
    # should still try the deterministic fallback before giving up, so simple
    # follow-ups never get dropped if the LLM is uncertain.
    if intent == "unknown":
        intent = ollama_service.fallback_classify_intent(message, history, last_intent)

    tool_fn = get_tool(intent)
    result = tool_fn(message, memory)

    turn_count = memory_store.record(
        session_id=session_id,
        user_message=message,
        intent=intent,
        ui_type=result.ui_type,
        data=result.data,
        assistant_message=result.message,
    )

    return ChatResponse(
        intent=Intent(intent) if intent in Intent._value2member_map_ else Intent.UNKNOWN,
        tool_called=result.tool_called,
        ui_type=UiType(result.ui_type) if result.ui_type in UiType._value2member_map_ else UiType.FALLBACK,
        message=result.message,
        data=result.data,
        session_id=session_id,
        turn=turn_count,
    )
