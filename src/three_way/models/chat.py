# src/three_way/models/chat.py

from enum import Enum
from pydantic import BaseModel, Field


class Provider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"


class ChatMessage(BaseModel):
    role: str        # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    max_tokens: int = Field(default=1024, gt=0, le=8192)


class ChatResponse(BaseModel):
    provider: Provider
    model: str
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_seconds: float = 0.0
    estimated_cost_usd: float = 0.0
    error: str | None = None   # None = success; string = something failed

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens