import gradio as gr

from three_way.ui.constants import PHASE_MESSAGES

_MODEL_BADGES = """
<div style="
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 8px;
">
  <span style="
      background: rgba(16,163,127,0.1);
      border: 1px solid rgba(16,163,127,0.28);
      border-radius: 20px;
      padding: 7px 22px;
      font-size: 13px;
      color: #5ecba0;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
  ">OpenAI</span>
  <span style="
      background: rgba(66,133,244,0.1);
      border: 1px solid rgba(66,133,244,0.28);
      border-radius: 20px;
      padding: 7px 22px;
      font-size: 13px;
      color: #7aa7f7;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
  ">Gemini</span>
  <span style="
      background: rgba(217,119,6,0.1);
      border: 1px solid rgba(217,119,6,0.28);
      border-radius: 20px;
      padding: 7px 22px;
      font-size: 13px;
      color: #eda832;
      font-weight: 600;
      letter-spacing: 0.04em;
      text-transform: uppercase;
  ">Claude</span>
</div>
"""


def build_panels():
    # ── Empty state ────────────────────────────────────────────────────
    with gr.Column(elem_id="phase-col", visible=True) as phase_col:
        gr.HTML(_MODEL_BADGES)
        phase_md = gr.Markdown(PHASE_MESSAGES[0], elem_id="phase-msg")

    # ── Chat panels (revealed on first submit) ─────────────────────────
    with gr.Row(visible=False, elem_id="panels-row") as panels_row:
        openai_chat = gr.Chatbot(
            label="OpenAI", height=460,
            layout="bubble", render_markdown=True,
            elem_id="openai-chat",
        )
        gemini_chat = gr.Chatbot(
            label="Gemini", height=460,
            layout="bubble", render_markdown=True,
            elem_id="gemini-chat",
        )
        claude_chat = gr.Chatbot(
            label="Claude", height=460,
            layout="bubble", render_markdown=True,
            elem_id="claude-chat",
        )

    status = gr.Markdown("", elem_id="status-bar")

    return panels_row, phase_col, phase_md, openai_chat, gemini_chat, claude_chat, status
