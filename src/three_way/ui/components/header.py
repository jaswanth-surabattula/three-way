import gradio as gr


def build_header():
    with gr.Row(elem_id="header-row"):
        gr.Markdown("Three-Way Arena", elem_id="app-title")
        new_session_btn = gr.Button(
            "+ New Session", scale=0, min_width=140, elem_id="new-session-btn",
        )
    return new_session_btn
