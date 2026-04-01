import asyncio
import logging

from three_way.models.chat import ChatRequest, ChatResponse
from three_way.services import claude_client, gemini_client, openai_client

log = logging.getLogger(__name__)


async def run(
    openai_request: ChatRequest,
    gemini_request: ChatRequest,
    claude_request: ChatRequest,
    openai_model: str,
    gemini_model: str,
    claude_model: str,
) -> tuple[ChatResponse, ChatResponse, ChatResponse]:
    """Fire all three providers simultaneously and return their responses.

    Uses asyncio.gather so all three API calls run in parallel — the total
    wait time is the slowest provider, not the sum of all three.

    Each provider receives its own ChatRequest so multi-turn sessions work
    correctly: each model's history contains only its own prior responses,
    not the other models' responses.

    Args:
        openai_request:  Full conversation history for OpenAI.
        gemini_request:  Full conversation history for Gemini.
        claude_request:  Full conversation history for Claude.
        openai_model:    Model ID for OpenAI, e.g. "gpt-4.1-mini".
        gemini_model:    Model ID for Gemini, e.g. "gemini-2.5-flash".
        claude_model:    Model ID for Claude, e.g. "claude-haiku-4-5-20251001".

    Returns:
        A tuple of (openai_response, gemini_response, claude_response).
        Each is a ChatResponse — check .error to know if a provider failed.
    """
    log.info(
        "Arena run  openai=%s  gemini=%s  claude=%s",
        openai_model, gemini_model, claude_model,
    )

    openai_response, gemini_response, claude_response = await asyncio.gather(
        openai_client.chat(openai_request, openai_model),
        gemini_client.chat(gemini_request, gemini_model),
        claude_client.chat(claude_request, claude_model),
    )

    errors = [r for r in (openai_response, gemini_response, claude_response) if r.error]
    if errors:
        for r in errors:
            log.error("Arena: provider %s returned error: %s", r.provider.value, r.error)

    wall_clock = max(
        openai_response.latency_seconds,
        gemini_response.latency_seconds,
        claude_response.latency_seconds,
    )
    log.info("Arena done  wall_clock=%.2fs", wall_clock)

    return openai_response, gemini_response, claude_response
