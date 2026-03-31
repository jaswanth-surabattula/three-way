from google import genai
from google.genai import types

from three_way.core.config import get_api_key, get_model
from three_way.models.chat import ChatRequest, ChatResponse, Provider
from three_way.utils.timer import Timer, calculate_cost


def _to_gemini_contents(request: ChatRequest) -> list[types.Content]:
    """Convert our ChatMessage list to Gemini's Content format.

    Gemini uses "model" instead of "assistant" for the assistant role,
    and wraps content in a Parts list instead of a plain string.
    """
    role_map = {"user": "user", "assistant": "model"}
    return [
        types.Content(role=role_map[m.role], parts=[types.Part(text=m.content)])
        for m in request.messages
    ]


async def chat(request: ChatRequest, model_id: str) -> ChatResponse:
    """Send a chat request to Gemini and return a normalised ChatResponse.

    Args:
        request:  The shared ChatRequest (messages + max_tokens).
        model_id: One of the Gemini model IDs from SUPPORTED_MODELS,
                  e.g. "gemini-2.5-flash".

    Returns:
        ChatResponse populated with content, token counts, latency, and cost.
        On failure, returns a ChatResponse with error set and content empty.
    """
    model_config = get_model(model_id)
    client = genai.Client(api_key=get_api_key("gemini"))

    contents = _to_gemini_contents(request)
    config = types.GenerateContentConfig(max_output_tokens=request.max_tokens)

    try:
        with Timer() as t:
            response = await client.aio.models.generate_content(
                model=model_config.model_id,
                contents=contents,
                config=config,
            )

        usage = response.usage_metadata
        prompt_tokens = usage.prompt_token_count if usage else 0
        completion_tokens = usage.candidates_token_count if usage else 0

        return ChatResponse(
            provider=Provider.GEMINI,
            model=model_config.display_name,
            content=response.text or "",
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
            provider=Provider.GEMINI,
            model=model_config.display_name,
            content="",
            error=str(e),
        )
