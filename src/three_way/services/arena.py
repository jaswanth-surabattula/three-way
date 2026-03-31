import asyncio

from three_way.models.chat import ChatRequest, ChatResponse
from three_way.services import claude_client, gemini_client, openai_client


async def run(
    request: ChatRequest,
    openai_model: str,
    gemini_model: str,
    claude_model: str,
) -> tuple[ChatResponse, ChatResponse, ChatResponse]:
    """Fire all three providers simultaneously and return their responses.

    Uses asyncio.gather so all three API calls run in parallel — the total
    wait time is the slowest provider, not the sum of all three.

    Args:
        request:       The shared ChatRequest sent to every provider.
        openai_model:  Model ID for OpenAI, e.g. "gpt-4.1-mini".
        gemini_model:  Model ID for Gemini, e.g. "gemini-2.5-flash".
        claude_model:  Model ID for Claude, e.g. "claude-haiku-4-5-20251001".

    Returns:
        A tuple of (openai_response, gemini_response, claude_response).
        Each is a ChatResponse — check .error to know if a provider failed.
    """
    openai_response, gemini_response, claude_response = await asyncio.gather(
        openai_client.chat(request, openai_model),
        gemini_client.chat(request, gemini_model),
        claude_client.chat(request, claude_model),
    )
    return openai_response, gemini_response, claude_response
