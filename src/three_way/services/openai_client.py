from typing import cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from three_way.core.config import get_api_key, get_model
from three_way.models.chat import ChatRequest, ChatResponse, Provider
from three_way.utils.timer import Timer, calculate_cost


async def chat(request: ChatRequest, model_id: str) -> ChatResponse:
    """Send a chat request to OpenAI and return a normalised ChatResponse.

    Args:
        request:  The shared ChatRequest (messages + max_tokens).
        model_id: One of the OpenAI model IDs from SUPPORTED_MODELS,
                  e.g. "gpt-4.1-mini".

    Returns:
        ChatResponse populated with content, token counts, latency, and cost.
        On failure, returns a ChatResponse with error set and content empty.
    """
    model_config = get_model(model_id)
    client = AsyncOpenAI(api_key=get_api_key("openai"))

    messages = cast(list[ChatCompletionMessageParam], [m.model_dump() for m in request.messages])

    try:
        with Timer() as t:
            response = await client.chat.completions.create(
                model=model_config.model_id,
                messages=messages,
                max_completion_tokens=request.max_tokens,
            )

        choice = response.choices[0]
        usage = response.usage
        prompt_tokens = usage.prompt_tokens if usage else 0
        completion_tokens = usage.completion_tokens if usage else 0

        return ChatResponse(
            provider=Provider.OPENAI,
            model=model_config.display_name,
            content=choice.message.content or "",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            latency_seconds=t.elapsed,
            estimated_cost_usd=calculate_cost(
                model_config,
                input_tokens=prompt_tokens,
                output_tokens=completion_tokens,
            ),
        )

    except Exception as e:
        return ChatResponse(
            provider=Provider.OPENAI,
            model=model_config.display_name,
            content="",
            error=str(e),
        )
