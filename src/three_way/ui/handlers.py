import gradio as gr

from three_way.models.chat import ChatRequest
from three_way.services import arena
from three_way.ui.constants import PHASE_MESSAGES
from three_way.ui.helpers import display_to_model_id, format_response, history_to_messages


async def on_submit(
    prompt, openai_display, gemini_display, claude_display,
    oh, gh, ch, active,
):
    if not prompt.strip():
        yield oh, gh, ch, "_Please enter a prompt._", "", active, gr.update(), gr.update()
        return

    openai_model = display_to_model_id(openai_display)
    gemini_model = display_to_model_id(gemini_display)
    claude_model = display_to_model_id(claude_display)

    user_msg = {"role": "user", "content": prompt.strip()}
    oh = oh + [user_msg]
    gh = gh + [user_msg]
    ch = ch + [user_msg]

    yield (
        oh, gh, ch, "_Thinking…_", "", True,
        gr.update(visible=True),   # panels_row
        gr.update(visible=False),  # phase_col
    )

    openai_resp, gemini_resp, claude_resp = await arena.run(
        ChatRequest(messages=history_to_messages(oh)),
        ChatRequest(messages=history_to_messages(gh)),
        ChatRequest(messages=history_to_messages(ch)),
        openai_model, gemini_model, claude_model,
    )

    oh = oh + [{"role": "assistant", "content": format_response(openai_resp)}]
    gh = gh + [{"role": "assistant", "content": format_response(gemini_resp)}]
    ch = ch + [{"role": "assistant", "content": format_response(claude_resp)}]

    slowest = max(
        openai_resp.latency_seconds,
        gemini_resp.latency_seconds,
        claude_resp.latency_seconds,
    )
    yield (
        oh, gh, ch, f"_Done in {slowest:.2f}s (wall-clock)._", "", True,
        gr.update(visible=True),
        gr.update(visible=False),
    )


def on_new_session(p_idx):
    new_idx = (p_idx + 1) % len(PHASE_MESSAGES)
    return (
        [], [], [],
        "",
        False,
        gr.update(value=PHASE_MESSAGES[new_idx]),
        gr.update(visible=False),   # panels_row
        gr.update(visible=True),    # phase_col
        gr.update(visible=False),   # session_menu
        False,
        new_idx,
    )


def on_model_change(active):
    return gr.update(visible=True) if active else gr.update(visible=False)


def on_mc_yes():
    return gr.update(visible=False), gr.update(visible=True)


def on_mc_no():
    return (
        gr.update(visible=False),   # model_change_modal
        [], [], [],
        "",
        False,
        gr.update(visible=False),   # panels_row
        gr.update(visible=True),    # phase_col
    )


def on_chevron_click(visible):
    new_vis = not visible
    return gr.update(visible=new_vis), new_vis


def on_end_session_click():
    return gr.update(visible=False), False, gr.update(visible=True)


def on_report_yes():
    return gr.update(visible=False)


def on_report_no():
    return gr.update(visible=False)
