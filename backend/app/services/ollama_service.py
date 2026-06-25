"""
Local LLM client for intent classification & tool routing via Ollama's REST API.

Design goals:
- Deterministic, strictly-JSON output from the LLM (low temperature, explicit
  schema in the prompt, `format: json` Ollama option).
- Graceful fallback: if Ollama is unreachable or returns malformed JSON, fall
  back to a deterministic keyword classifier so the API never breaks.
- Conversation-aware: short-term memory is folded into the prompt so the LLM
  can resolve follow-ups like "show cheaper ones".
"""
from __future__ import annotations

import json
import logging
import os
from typing import Dict, List, Optional

import httpx

logger = logging.getLogger("ai_support_assistant.ollama")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "15"))

VALID_INTENTS = [
    "order_tracking",
    "refund_request",
    "complaint",
    "escalation",
    "hotel_search",
    "flight_search",
    "unknown",
]

SYSTEM_PROMPT = (
    "You are an intent classification engine for a customer support assistant.\n"
    "Classify the user's latest message into exactly one of these intents:\n"
    + ", ".join(VALID_INTENTS)
    + "\n\n"
    "Rules:\n"
    "- Use the recent conversation turns to resolve follow-up references\n"
    '  (e.g. "show cheaper ones", "what about tomorrow") to the SAME intent as the\n'
    "  prior relevant turn.\n"
    "- Respond with ONLY a JSON object, no prose, no markdown fences.\n"
    '- JSON schema: {"intent": "<one of the listed intents>", "reasoning": "<short reason>"}\n'
    '- If nothing matches, use "unknown".\n'
)


class OllamaUnavailableError(Exception):
    """Raised when Ollama cannot be reached or returns an unusable response."""


def _build_user_prompt(message: str, history: List[Dict[str, str]]) -> str:
    convo = ""
    for turn in history[-5:]:
        role = turn.get("role", "user")
        content = turn.get("content", "")
        convo += f"{role}: {content}\n"
    convo += f"user: {message}\n"
    return (
        "Conversation so far (most recent last):\n"
        f"{convo}\n"
        "Classify ONLY the final user message above, using prior turns for context.\n"
        "Return the JSON object now."
    )


def classify_intent(message: str, history: List[Dict[str, str]]) -> str:
    """
    Calls the local Ollama /api/generate endpoint with a structured prompt and
    returns a validated intent string. Raises OllamaUnavailableError on any
    failure so the caller can apply a fallback classifier.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "system": SYSTEM_PROMPT,
        "prompt": _build_user_prompt(message, history),
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.0},
    }
    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT_SECONDS, trust_env=False) as client:
            resp = client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
            resp.raise_for_status()
            body = resp.json()
    except Exception as exc:  # noqa: BLE001 - any transport/env issue should fall back, not crash the API
        raise OllamaUnavailableError(f"Ollama request failed: {exc}") from exc

    raw_text = body.get("response", "").strip()
    try:
        parsed = json.loads(raw_text)
        intent = parsed.get("intent", "unknown")
    except (json.JSONDecodeError, AttributeError) as exc:
        raise OllamaUnavailableError(f"Ollama returned non-JSON output: {raw_text!r}") from exc

    if intent not in VALID_INTENTS:
        logger.warning("Ollama returned unrecognized intent %r, defaulting to unknown", intent)
        intent = "unknown"
    return intent


# ---------------------------------------------------------------------------
# Deterministic fallback classifier
# ---------------------------------------------------------------------------
_KEYWORDS = {
    "order_tracking": ["track", "tracking", "where is my order", "shipment", "delivery status"],
    "refund_request": ["refund", "money back", "return my", "reimburse"],
    "complaint": ["complain", "complaint", "unhappy", "bad experience", "disappointed", "issue with"],
    "escalation": ["escalate", "speak to a manager", "supervisor", "human agent", "escalation"],
    "hotel_search": ["hotel", "hotels", "stay in", "accommodation", "cheaper ones", "cheaper option"],
    "flight_search": ["flight", "flights", "fly to", "book a flight", "airfare"],
}

# Follow-up phrases that should inherit the previous turn's intent rather than
# being independently classified (handles "show cheaper ones" style queries).
_FOLLOW_UP_PHRASES = [
    "cheaper",
    "more expensive",
    "another option",
    "something else",
    "what about",
    "same but",
    "instead",
]


def fallback_classify_intent(message: str, history: List[Dict[str, str]], last_intent: Optional[str]) -> str:
    text = message.lower()

    if last_intent and last_intent != "unknown":
        if any(phrase in text for phrase in _FOLLOW_UP_PHRASES):
            return last_intent

    for intent, keywords in _KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return intent

    return "unknown"
