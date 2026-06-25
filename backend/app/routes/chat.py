import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.intent_router import handle_chat
from app.services.memory_service import memory_store

logger = logging.getLogger("ai_support_assistant.chat_route")

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        return handle_chat(
            message=payload.message,
            session_id=payload.session_id,
            memory_store=memory_store,
        )
    except Exception as exc:  # noqa: BLE001 - graceful fallback per spec
        logger.exception("Unhandled error in /chat")
        raise HTTPException(status_code=500, detail="Internal error processing chat message") from exc


@router.post("/chat/reset")
def reset_session(session_id: str = "default") -> dict:
    memory_store.clear(session_id)
    return {"status": "ok", "session_id": session_id, "message": "Session memory cleared."}
