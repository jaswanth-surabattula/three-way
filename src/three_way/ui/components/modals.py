import gradio as gr


def build_modals():
    """End-session report modal + model-change confirmation modal."""

    with gr.Column(visible=False, elem_id="end-session-modal") as end_session_modal:
        with gr.Column(elem_classes=["modal-inner"]):
            gr.Markdown("### Generate Session Report?")
            gr.Markdown("A summary of responses and model performance will be created.")
            with gr.Row(elem_classes=["modal-btn-row"]):
                report_yes_btn = gr.Button("Generate", variant="primary",   scale=1)
                report_no_btn  = gr.Button("Skip",     variant="secondary", scale=1)

    with gr.Column(visible=False, elem_id="model-change-modal") as model_change_modal:
        with gr.Column(elem_classes=["modal-inner"]):
            gr.Markdown("### Change Model?")
            gr.Markdown("Switching models will end the current session.")
            with gr.Row(elem_classes=["modal-btn-row"]):
                mc_yes_btn = gr.Button("Proceed", variant="primary",   scale=1)
                mc_no_btn  = gr.Button("Cancel",  variant="secondary", scale=1)

    return (
        end_session_modal, model_change_modal,
        report_yes_btn, report_no_btn,
        mc_yes_btn, mc_no_btn,
    )
