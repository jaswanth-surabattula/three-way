import gradio as gr

from three_way.ui.helpers import dropdown_choices


def build_input_bar():
    openai_choices, openai_default = dropdown_choices("openai")
    gemini_choices, gemini_default = dropdown_choices("gemini")
    claude_choices, claude_default = dropdown_choices("claude")

    with gr.Column(elem_id="input-wrap"):
        with gr.Column(elem_id="chat-input-card"):
            prompt_box = gr.Textbox(
                placeholder="Ask anything…",
                label="",
                lines=1,
                max_lines=8,
                show_label=False,
                elem_id="prompt-input",
            )
            gr.HTML('<div id="toolbar-divider"></div>')
            with gr.Row(elem_id="bottom-row"):
                openai_dd = gr.Dropdown(
                    choices=openai_choices, value=openai_default,
                    show_label=False, interactive=True,
                    scale=0, min_width=0, elem_id="openai-dd",
                )
                gemini_dd = gr.Dropdown(
                    choices=gemini_choices, value=gemini_default,
                    show_label=False, interactive=True,
                    scale=0, min_width=0, elem_id="gemini-dd",
                )
                claude_dd = gr.Dropdown(
                    choices=claude_choices, value=claude_default,
                    show_label=False, interactive=True,
                    scale=0, min_width=0, elem_id="claude-dd",
                )
                with gr.Row(elem_id="send-group", scale=0):
                    send_btn    = gr.Button("›", min_width=38, elem_id="send-btn")
                    chevron_btn = gr.Button("▾", min_width=28, elem_id="send-chevron")

        with gr.Column(visible=False, elem_id="session-menu") as session_menu:
            end_session_btn = gr.Button("End Session")

    return (
        prompt_box,
        openai_dd, gemini_dd, claude_dd,
        send_btn, chevron_btn,
        session_menu, end_session_btn,
    )
