"""Three-Way Arena — Gradio application entry point."""

import logging

import gradio as gr

from three_way.ui.components.header import build_header
from three_way.ui.components.input_bar import build_input_bar
from three_way.ui.components.modals import build_modals
from three_way.ui.components.panels import build_panels
from three_way.ui.css import CSS
from three_way.ui.handlers import (
    on_chevron_click,
    on_end_session_click,
    on_mc_no,
    on_mc_yes,
    on_model_change,
    on_new_session,
    on_report_no,
    on_report_yes,
    on_submit,
)
from three_way.utils.logging_setup import setup_logging

log = logging.getLogger(__name__)


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Three-Way Arena") as app:

        # ── State ──────────────────────────────────────────────────────
        session_active = gr.State(False)
        menu_visible   = gr.State(False)
        phase_idx      = gr.State(0)

        # ── Build UI ───────────────────────────────────────────────────
        (
            end_session_modal, model_change_modal,
            report_yes_btn, report_no_btn,
            mc_yes_btn, mc_no_btn,
        ) = build_modals()

        new_session_btn = build_header()

        (
            panels_row, phase_col, phase_md,
            openai_chat, gemini_chat, claude_chat,
            status,
        ) = build_panels()

        (
            prompt_box,
            openai_dd, gemini_dd, claude_dd,
            send_btn, chevron_btn,
            session_menu, end_session_btn,
        ) = build_input_bar()

        # ── Wire events ────────────────────────────────────────────────
        _submit_inputs = [
            prompt_box, openai_dd, gemini_dd, claude_dd,
            openai_chat, gemini_chat, claude_chat,
            session_active,
        ]
        _submit_outputs = [
            openai_chat, gemini_chat, claude_chat,
            status, prompt_box, session_active,
            panels_row, phase_col,
        ]

        send_btn.click(fn=on_submit, inputs=_submit_inputs, outputs=_submit_outputs)
        prompt_box.submit(fn=on_submit, inputs=_submit_inputs, outputs=_submit_outputs)

        new_session_btn.click(
            fn=on_new_session,
            inputs=[phase_idx],
            outputs=[
                openai_chat, gemini_chat, claude_chat,
                status, session_active,
                phase_md, panels_row, phase_col,
                session_menu, menu_visible, phase_idx,
            ],
        )

        for dd in [openai_dd, gemini_dd, claude_dd]:
            dd.change(
                fn=on_model_change,
                inputs=[session_active],
                outputs=[model_change_modal],
            )

        mc_yes_btn.click(
            fn=on_mc_yes,
            inputs=[],
            outputs=[model_change_modal, end_session_modal],
        )
        mc_no_btn.click(
            fn=on_mc_no,
            inputs=[],
            outputs=[
                model_change_modal,
                openai_chat, gemini_chat, claude_chat,
                status, session_active,
                panels_row, phase_col,
            ],
        )

        chevron_btn.click(
            fn=on_chevron_click,
            inputs=[menu_visible],
            outputs=[session_menu, menu_visible],
        )
        end_session_btn.click(
            fn=on_end_session_click,
            inputs=[],
            outputs=[session_menu, menu_visible, end_session_modal],
        )

        report_yes_btn.click(fn=on_report_yes, inputs=[], outputs=[end_session_modal])
        report_no_btn.click(fn=on_report_no,   inputs=[], outputs=[end_session_modal])

    return app


def launch() -> None:
    setup_logging()
    build_app().launch(css=CSS)
