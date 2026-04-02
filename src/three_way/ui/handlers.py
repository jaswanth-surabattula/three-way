import logging

from three_way.models.chat import ChatRequest
from three_way.services import arena
from three_way.ui.helpers import (
    display_to_model_id,
    format_response,
    history_to_messages,
)

log = logging.getLogger(__name__)


async def on_submit(
    prompt: str,
    openai_display: str,
    gemini_display: str,
    claude_display: str,
    openai_history: list,
    gemini_history: list,
    claude_history: list,
):
    """Handle a new user message: fan out to all three providers."""
    prompt = (prompt or "").strip()
    if not prompt:
        yield openai_history, gemini_history, claude_history, ""
        return

    openai_history = list(openai_history or [])
    gemini_history = list(gemini_history or [])
    claude_history = list(claude_history or [])

    # Append user turn and yield immediately so UI shows the message
    openai_history.append({"role": "user", "content": prompt})
    gemini_history.append({"role": "user", "content": prompt})
    claude_history.append({"role": "user", "content": prompt})

    yield openai_history, gemini_history, claude_history, "Querying all three models…"

    try:
        openai_model = display_to_model_id(openai_display)
        gemini_model = display_to_model_id(gemini_display)
        claude_model = display_to_model_id(claude_display)
    except ValueError as exc:
        log.error("Model lookup failed: %s", exc)
        yield openai_history, gemini_history, claude_history, f"Error: {exc}"
        return

    openai_req = ChatRequest(messages=history_to_messages(openai_history))
    gemini_req = ChatRequest(messages=history_to_messages(gemini_history))
    claude_req = ChatRequest(messages=history_to_messages(claude_history))

    o_resp, g_resp, c_resp = await arena.run(
        openai_req, gemini_req, claude_req,
        openai_model, gemini_model, claude_model,
    )

    openai_history.append({"role": "assistant", "content": format_response(o_resp)})
    gemini_history.append({"role": "assistant", "content": format_response(g_resp)})
    claude_history.append({"role": "assistant", "content": format_response(c_resp)})

    wall = max(o_resp.latency_seconds, g_resp.latency_seconds, c_resp.latency_seconds)
    yield openai_history, gemini_history, claude_history, f"Done in {wall:.2f}s"


def on_new_session():
    """Reset all state."""
    return [], [], [], ""
