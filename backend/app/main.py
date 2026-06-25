import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

app = FastAPI(
    title="AI-Powered Customer Support Assistant",
    description="Fully offline backend: FastAPI + local Ollama for intent classification and mock tool execution.",
    version="1.0.0",
)

# CORS is permissive here only because this is a local-only prototype talking
# to a local Flutter dev client; restrict this in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
