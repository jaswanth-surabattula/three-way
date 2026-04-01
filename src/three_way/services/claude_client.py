import logging
from typing import cast

from anthropic import AsyncAnthropic
from anthropic.types import MessageParam, TextBlock

from three_way.core.config import get_api_key, get_model
from three_way.models.chat import ChatRequest, ChatResponse, Provider
from three_way.utils.timer import Timer, calculate_cost

log = logging.getLogger(__name__)


async def chat(request: ChatRequest, model_id: str) -> ChatResponse:
    """Send a chat request to Claude and return a normalised ChatResponse.

    Args:
        request:  The shared ChatRequest (messages + max_tokens).
        model_id: One of the Claude model IDs from SUPPORTED_MODELS,
                  e.g. "claude-haiku-4-5-20251001".

    Returns:
        ChatResponse populated with content, token counts, latency, and cost.
        On failure, returns a ChatResponse with error set and content empty.
    """
    model_config = get_model(model_id)
    client = AsyncAnthropic(api_key=get_api_key("claude"))

    messages = cast(list[MessageParam], [m.model_dump() for m in request.messages])

    log.info("Claude request  model=%s  turns=%d  max_tokens=%d",
             model_id, len(request.messages), request.max_tokens)

    try:
        with Timer() as t:
            response = await client.messages.create(
                model=model_config.model_id,
                messages=messages,
                max_tokens=request.max_tokens,
            )

        usage = response.usage
        text = next(block.text for block in response.content if isinstance(block, TextBlock))

        log.info(
            "Claude response model=%s  stop=%s  tokens=%d+%d  latency=%.2fs",
            model_id, response.stop_reason, usage.input_tokens, usage.output_tokens, t.elapsed,
        )
        if response.stop_reason == "max_tokens":
            log.warning("Claude response truncated (stop_reason=max_tokens)  model=%s", model_id)

        return ChatResponse(
            provider=Provider.CLAUDE,
            model=model_config.display_name,
            content=text,
            prompt_tokens=usage.input_tokens,
            completion_tokens=usage.output_tokens,
            latency_seconds=t.elapsed,
            estimated_cost_usd=calculate_cost(
                model_config,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
            ),
        )

    except Exception as e:
        log.error("Claude error  model=%s  error=%s", model_id, e, exc_info=True)
        return ChatResponse(
            provider=Provider.CLAUDE,
            model=model_config.display_name,
            content="",
            error=str(e),
        )
