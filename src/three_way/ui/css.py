CSS = """
/* ════════════════════════════════════════════════════════════════════════
   Three-Way Arena — Stylesheet
   Palette: bg #0d0d1a  surface #161622  accent-openai #10a37f
            accent-gemini #4285f4  accent-claude #d97706
   ════════════════════════════════════════════════════════════════════════ */

/* ── Reset & base ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

body {
    background: #0d0d1a !important;
    background-image:
        radial-gradient(ellipse 90% 60% at 50% -10%, rgba(80,80,180,0.07) 0%, transparent 65%) !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, system-ui, sans-serif !important;
    min-height: 100vh !important;
    margin: 0 !important;
}

.gradio-container {
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    min-height: 100vh !important;
}

footer { display: none !important; }

/* Gradio adds its own borders/backgrounds on blocks — strip them */
.block { border: none !important; background: transparent !important; box-shadow: none !important; }

/* ── Header ───────────────────────────────────────────────────────────── */
#header-row {
    padding: 14px 28px !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    align-items: center !important;
    background: rgba(13,13,26,0.96) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
    margin-bottom: 0 !important;
    gap: 0 !important;
}

#app-title p, #app-title span {
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #b0b0d8 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin: 0 !important;
}

#new-session-btn button,
#new-session-btn button span,
#new-session-btn button * {
    white-space: nowrap !important;
}
#new-session-btn button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #9090b8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 5px 12px !important;
    min-height: 28px !important;
    min-width: max-content !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
#new-session-btn button:hover {
    background: rgba(255,255,255,0.09) !important;
    color: #c0c0e0 !important;
    border-color: rgba(255,255,255,0.22) !important;
}

/* ── Empty state ──────────────────────────────────────────────────────── */
#phase-col {
    /* No display override — Gradio must be able to set display:none here */
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 0 !important;
    min-height: 0 !important;
    padding-top: 18vh !important;
    padding-bottom: 28px !important;
    gap: 16px !important;
}

#phase-msg p, #phase-msg span {
    font-size: 1.85rem !important;
    font-weight: 300 !important;
    color: #5a5a80 !important;
    text-align: center !important;
    letter-spacing: -0.02em !important;
    line-height: 1.45 !important;
    margin: 0 !important;
}

/* ── Status bar ───────────────────────────────────────────────────────── */
#status-bar {
    padding: 4px 28px !important;
    min-height: 22px !important;
    margin: 0 !important;
}
#status-bar p, #status-bar span {
    color: #3a3a58 !important;
    font-size: 11px !important;
    text-align: center !important;
    margin: 0 !important;
    letter-spacing: 0.01em !important;
}

/* ── Chat panels ──────────────────────────────────────────────────────── */
#panels-row {
    padding: 16px 20px 4px !important;
    gap: 12px !important;
    flex: 1 !important;
    align-items: stretch !important;
}

/* Brand-colored top border per model */
#openai-chat.block {
    border-top: 2px solid #10a37f !important;
    border-radius: 12px !important;
    background: #111120 !important;
    overflow: hidden !important;
}
#gemini-chat.block {
    border-top: 2px solid #4285f4 !important;
    border-radius: 12px !important;
    background: #111120 !important;
    overflow: hidden !important;
}
#claude-chat.block {
    border-top: 2px solid #d97706 !important;
    border-radius: 12px !important;
    background: #111120 !important;
    overflow: hidden !important;
}

/* Panel label (model name) */
#openai-chat .label-wrap span { color: #10a37f !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }
#gemini-chat .label-wrap span { color: #4285f4 !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }
#claude-chat .label-wrap span  { color: #d97706 !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }

/* Chat bubble styles */
.message-bubble-border { border-radius: 12px !important; }
.bubble-wrap            { padding: 4px 12px !important; }

/* ── Input area ───────────────────────────────────────────────────────── */
#input-wrap {
    padding: 8px 20px 24px !important;
    max-width: 860px !important;
    margin: 0 auto !important;
    width: 100% !important;
}

#chat-input-card {
    --input-background-fill: transparent;  /* kill Gradio's gray textarea fill */
    background: #161622 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.02) inset,
        0 8px 40px rgba(0,0,0,0.55) !important;
    gap: 0 !important;
    padding: 0 !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
#chat-input-card:focus-within {
    border-color: rgba(255,255,255,0.15) !important;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.04) inset,
        0 0 0 3px rgba(100,100,200,0.06),
        0 8px 40px rgba(0,0,0,0.6) !important;
}

/* Prompt textbox — everything transparent so card background shows through */
#prompt-input,
#prompt-input *,
#prompt-input .block,
#prompt-input label {
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
#prompt-input textarea {
    min-height: 58px !important;
    max-height: 200px !important;
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    --input-background-fill: transparent !important;
    box-shadow: none !important;
    resize: none !important;
    font-size: 15px !important;
    color: #d0d0ee !important;
    padding: 18px 20px 10px !important;
    line-height: 1.65 !important;
    outline: none !important;
    caret-color: #8888cc !important;
}
#prompt-input textarea::placeholder { color: #70708a !important; }
/* Only hide the label text span — NOT the <label> wrapper that contains the textarea in Gradio 5 */
#prompt-input .label-wrap { display: none !important; }

/* Toolbar divider — hidden */
#toolbar-divider { display: none !important; }

/* Bottom row — explicit flex row so pills stay horizontal */
#bottom-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    padding: 9px 12px 12px !important;
    gap: 6px !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
/* Strip backgrounds/borders from Gradio wrappers; override Gradio's inline min-width/flex */
#bottom-row > div, #bottom-row > div > div, #bottom-row form {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    flex: 0 0 auto !important;
    min-width: 0 !important;
    width: fit-content !important;
}

/* ── Model dropdowns — pill-button style, grouped left ───────────────────── */
#openai-dd, #gemini-dd, #claude-dd {
    display: inline-flex !important;
    flex: 0 0 auto !important;   /* size to content, don't fill row */
    min-width: 0 !important;
    width: fit-content !important;
    background: transparent !important;
}
#openai-dd > *, #gemini-dd > *, #claude-dd > *,
#openai-dd .block, #gemini-dd .block, #claude-dd .block,
#openai-dd label, #gemini-dd label, #claude-dd label {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    min-height: unset !important;
    gap: 0 !important;
    width: fit-content !important;
    min-width: 0 !important;
}
#openai-dd .label-wrap, #gemini-dd .label-wrap, #claude-dd .label-wrap { display: none !important; }

/* Hide the chevron arrow — pill buttons don't need it */
#openai-dd .wrap svg, #gemini-dd .wrap svg, #claude-dd .wrap svg { display: none !important; }

/* Shared pill shape */
#openai-dd .wrap, #openai-dd [data-testid="dropdown"],
#gemini-dd .wrap, #gemini-dd [data-testid="dropdown"],
#claude-dd .wrap, #claude-dd [data-testid="dropdown"] {
    border-radius: 20px !important;
    padding: 5px 16px !important;
    height: auto !important;
    min-height: unset !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    transition: all 0.15s ease !important;
    width: max-content !important;
}

/* OpenAI pill — teal */
#openai-dd .wrap, #openai-dd [data-testid="dropdown"] {
    background: rgba(16,163,127,0.08) !important;
    border: 1px solid rgba(16,163,127,0.32) !important;
    box-shadow: none !important;
}
#openai-dd .wrap:hover { background: rgba(16,163,127,0.15) !important; border-color: rgba(16,163,127,0.55) !important; }
#openai-dd .wrap span,
#openai-dd .wrap input { font-size: 13px !important; color: #4ed9a8 !important; font-weight: 600 !important; background: transparent !important; letter-spacing: 0.01em !important; }

/* Gemini pill — blue */
#gemini-dd .wrap, #gemini-dd [data-testid="dropdown"] {
    background: rgba(66,133,244,0.08) !important;
    border: 1px solid rgba(66,133,244,0.32) !important;
    box-shadow: none !important;
}
#gemini-dd .wrap:hover { background: rgba(66,133,244,0.15) !important; border-color: rgba(66,133,244,0.55) !important; }
#gemini-dd .wrap span,
#gemini-dd .wrap input { font-size: 13px !important; color: #6ab0ff !important; font-weight: 600 !important; background: transparent !important; letter-spacing: 0.01em !important; }

/* Claude pill — amber */
#claude-dd .wrap, #claude-dd [data-testid="dropdown"] {
    background: rgba(217,119,6,0.08) !important;
    border: 1px solid rgba(217,119,6,0.32) !important;
    box-shadow: none !important;
}
#claude-dd .wrap:hover { background: rgba(217,119,6,0.15) !important; border-color: rgba(217,119,6,0.55) !important; }
#claude-dd .wrap span,
#claude-dd .wrap input { font-size: 13px !important; color: #f5b63a !important; font-weight: 600 !important; background: transparent !important; letter-spacing: 0.01em !important; }

/* ── Send group — pushed to the right ────────────────────────────────────── */
#send-group {
    margin-left: auto !important;
    flex-shrink: 0 !important;
    gap: 4px !important;
    align-items: center !important;
}

#send-btn button {
    border-radius: 8px !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    background: #4a4af0 !important;
    border: none !important;
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 0 !important;
    line-height: 1 !important;
    transition: background 0.15s ease !important;
    box-shadow: 0 2px 8px rgba(74,74,240,0.35) !important;
}
#send-btn button:hover {
    background: #5c5cf5 !important;
    box-shadow: 0 3px 12px rgba(74,74,240,0.45) !important;
}
#send-btn button:active {
    background: #3838d8 !important;
    box-shadow: none !important;
}

#send-chevron button {
    border-radius: 8px !important;
    width: 24px !important;
    height: 32px !important;
    min-width: 24px !important;
    min-height: 32px !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #50507a !important;
    font-size: 9px !important;
    padding: 0 !important;
    line-height: 1 !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
#send-chevron button:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #8080a8 !important;
}

/* ── Session dropdown menu ────────────────────────────────────────────── */
#session-menu {
    max-width: 176px !important;
    margin-left: auto !important;
    background: #1c1c2c !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.75), 0 0 0 1px rgba(255,255,255,0.03) !important;
    margin-top: 4px !important;
}
#session-menu button {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
    padding: 0 12px !important;
    min-height: 34px !important;
    font-size: 13px !important;
    color: #9090b0 !important;
    background: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    transition: all 0.12s ease !important;
    box-shadow: none !important;
}
#session-menu button:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #e0e0f0 !important;
}

/* ── Modals ───────────────────────────────────────────────────────────── */
#end-session-modal, #model-change-modal {
    position: fixed !important;
    inset: 0 !important;
    background: rgba(0,0,0,0.82) !important;
    z-index: 9990 !important;
    width: 100vw !important;
    height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
}

.modal-inner {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    background: #1c1c2c !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-radius: 18px !important;
    padding: 32px 36px !important;
    min-width: 340px !important;
    max-width: 440px !important;
    z-index: 9999 !important;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.04) inset,
        0 40px 100px rgba(0,0,0,0.9) !important;
    gap: 10px !important;
}

.modal-inner h3, .modal-inner h2 {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #e0e0f0 !important;
    margin: 0 !important;
    line-height: 1.4 !important;
}

.modal-inner p, .modal-inner span {
    font-size: 13px !important;
    color: #60607a !important;
    line-height: 1.55 !important;
    margin: 4px 0 0 !important;
}

.modal-btn-row {
    gap: 8px !important;
    margin-top: 14px !important;
}

.modal-btn-row button {
    border-radius: 9px !important;
    min-height: 36px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}

/* ── Suppress Gradio generating animation ───────────────────────────────── */
/* Kill the animation; override orange border only on top-level containers */
.generating { animation: none !important; }
#panels-row.generating,
#chat-input-card.generating,
#prompt-input.generating { border-color: transparent !important; box-shadow: none !important; outline: none !important; }

/* ── Chatbot action buttons ──────────────────────────────────────────────── */
/* Per-message copy/flag buttons — hide all */
.message-buttons { display: none !important; }
/* Panel header: Gradio renders Share → Delete → Copy in that order.
   Hide all except the last child (Copy), which we keep. */
#openai-chat .label-wrap button:not(:last-child),
#gemini-chat .label-wrap button:not(:last-child),
#claude-chat .label-wrap button:not(:last-child) { display: none !important; }
"""
