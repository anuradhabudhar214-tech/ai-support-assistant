"""
Simple in-memory short-term conversation memory.

Keeps the last N turns per session_id so the intent router / prompt builder
can resolve follow-up references like "show cheaper ones".
"""
from collections import deque
from dataclasses import dataclass, field
from threading import Lock
from typing import Deque, Dict, List, Optional

MAX_TURNS = 5  # keep last 3-5 turns as required by the spec


@dataclass
class Turn:
    user_message: str
    intent: str
    ui_type: str
    data: dict
    assistant_message: str


@dataclass
class SessionMemory:
    turns: Deque[Turn] = field(default_factory=lambda: deque(maxlen=MAX_TURNS))

    @property
    def turn_count(self) -> int:
        return len(self.turns)

    def last_turn_with_intent(self, intent: str) -> Optional[Turn]:
        for turn in reversed(self.turns):
            if turn.intent == intent:
                return turn
        return None

    @property
    def last_turn(self) -> Optional[Turn]:
        return self.turns[-1] if self.turns else None

    def as_prompt_history(self) -> List[Dict[str, str]]:
        history = []
        for t in self.turns:
            history.append({"role": "user", "content": t.user_message})
            history.append({"role": "assistant", "content": t.assistant_message})
        return history


class MemoryStore:
    """Thread-safe registry of SessionMemory keyed by session_id."""

    def __init__(self) -> None:
        self._sessions: Dict[str, SessionMemory] = {}
        self._lock = Lock()

    def get(self, session_id: str) -> SessionMemory:
        with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = SessionMemory()
            return self._sessions[session_id]

    def record(
        self,
        session_id: str,
        user_message: str,
        intent: str,
        ui_type: str,
        data: dict,
        assistant_message: str,
    ) -> int:
        session = self.get(session_id)
        session.turns.append(
            Turn(
                user_message=user_message,
                intent=intent,
                ui_type=ui_type,
                data=data,
                assistant_message=assistant_message,
            )
        )
        return session.turn_count

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)


# Module-level singleton used by the FastAPI app
memory_store = MemoryStore()
