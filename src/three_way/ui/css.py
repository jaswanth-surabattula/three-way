CSS = """
/* ── Reset & Base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container {
    background: #0a0a0a !important;
    color: #e5e7eb !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    overflow: hidden;
}

/* Hide Gradio default chrome */
.gradio-container > .main,
footer, .svelte-1ipelgc,
#component-0 > .wrap {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* ── Hide Python bridge components from view ──────────────────────────────── */
#hidden-controls,
#openai-dd, #gemini-dd, #claude-dd,
#h-prompt, #h-submit, #h-new-session {
    display: none !important;
}

/* ── App Shell ────────────────────────────────────────────────────────────── */
#app-shell {
    position: fixed;
    inset: 0;
    display: flex;
    background: #0a0a0a;
    overflow: hidden;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
#sidebar {
    width: 64px;
    min-width: 64px;
    background: #111111;
    border-right: 1px solid #1f1f1f;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px 0;
    gap: 8px;
    z-index: 50;
}

.sidebar-logo {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    cursor: pointer;
    transition: background 0.2s;
    margin-bottom: 8px;
}
.sidebar-logo:hover { background: #222222; }

.sidebar-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.2s, opacity 0.2s;
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
}

.sidebar-btn-new {
    background: #2563eb;
}
.sidebar-btn-new:hover { background: #1d4ed8; }

.sidebar-spacer { flex: 1; }

.sidebar-btn-settings {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #9ca3af;
}
.sidebar-btn-settings:hover { background: #222222; color: #e5e7eb; }

/* ── Main Content ─────────────────────────────────────────────────────────── */
#content {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
#header {
    height: 56px;
    min-height: 56px;
    background: #111111;
    border-bottom: 1px solid #1f1f1f;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 8px;
    z-index: 40;
}

.provider-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border: 1px solid;
    cursor: default;
    user-select: none;
}
.chip-openai  { background: #0e1b17; color: #86efac; border-color: #2d5a4c; }
.chip-gemini  { background: #131b2d; color: #93c5fd; border-color: #314c81; }
.chip-claude  { background: #1b1612; color: #fbbf24; border-color: #5a4230; }

.header-spacer { flex: 1; }

.new-session-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    background: #2563eb;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background 0.2s;
}
.new-session-btn:hover { background: #1d4ed8; }

/* ── Hero Section ─────────────────────────────────────────────────────────── */
#hero {
    position: absolute;
    top: 56px; /* below header */
    left: 0; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* Shift up so title sits comfortably above the input bar */
    transform: translateY(-110px);
    pointer-events: none;
    z-index: 3;
    transition: opacity 0.5s ease, transform 0.5s ease;
}

body.started #hero {
    opacity: 0;
    transform: translateY(-130px);
    pointer-events: none;
}

.hero-title {
    font-size: clamp(40px, 6vw, 72px);
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 50%, #ffffff 100%);
    background-size: 200% 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 3s linear infinite;
    margin-bottom: 16px;
}

@keyframes shine {
    0%   { background-position: 200% center; }
    100% { background-position: -200% center; }
}

.hero-subtitle {
    font-size: clamp(14px, 2vw, 18px);
    color: #6b7280;
    font-weight: 400;
    height: 28px;
    overflow: hidden;
}

.hero-phrase {
    display: block;
    animation: phraseIn 0.5s ease forwards;
}

@keyframes phraseIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Input Bar ────────────────────────────────────────────────────────────── */
#input-bar {
    position: absolute;
    left: 50%;
    transform: translateX(-50%) translateY(-50%);
    top: 55%;
    width: min(680px, calc(100% - 48px));
    background: #111111;
    border: 1px solid #262626;
    border-radius: 28px;
    padding: 16px 16px 12px;
    z-index: 10;
    transition: top 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                border-radius 0.3s ease,
                bottom 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}

body.started #input-bar {
    top: unset;
    bottom: 16px;
    transform: translateX(-50%);
    border-radius: 24px;
}

#input-bar textarea {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    color: #e5e7eb;
    font-size: 15px;
    font-family: 'Inter', system-ui, sans-serif;
    line-height: 1.6;
    resize: none;
    min-height: 48px;
    max-height: 160px;
    overflow-y: auto;
}
#input-bar textarea::placeholder { color: #4b5563; }

/* ── Input Toolbar ────────────────────────────────────────────────────────── */
#input-toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.tool-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #1a2840;
    border: 1px solid #1e3a5f;
    color: #60a5fa;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s;
    flex-shrink: 0;
}
.tool-btn:hover { background: #1e3060; }

/* Model chips in toolbar */
.model-chip-wrap {
    position: relative;
    flex-shrink: 0;
}

.model-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 10px;
    border-radius: 16px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid;
    cursor: pointer;
    white-space: nowrap;
    transition: opacity 0.2s;
    background: inherit;
}
.model-chip:hover { opacity: 0.85; }

.model-chip svg { flex-shrink: 0; }

.model-chip.chip-openai  { background: #0e1b17; color: #86efac; border-color: #2d5a4c; }
.model-chip.chip-gemini  { background: #131b2d; color: #93c5fd; border-color: #314c81; }
.model-chip.chip-claude  { background: #1b1612; color: #fbbf24; border-color: #5a4230; }

/* Upward-opening dropdown menus */
.model-menu {
    display: none;
    position: absolute;
    bottom: calc(100% + 8px);
    left: 0;
    min-width: 180px;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 6px;
    list-style: none;
    z-index: 100;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.5);
}
.model-chip-wrap:hover .model-menu,
.model-menu:hover { display: block; }

.model-menu li {
    padding: 8px 12px;
    font-size: 13px;
    color: #e5e7eb;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
    white-space: nowrap;
}
.model-menu li:hover { background: #262626; }
.model-menu li.active { color: #60a5fa; font-weight: 600; }

/* Send button */
.toolbar-spacer { flex: 1; }

.send-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #2563eb;
    border: none;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.2s, transform 0.1s;
    flex-shrink: 0;
}
.send-btn:hover { background: #1d4ed8; }
.send-btn:active { transform: scale(0.92); }
.send-btn:disabled { background: #374151; cursor: not-allowed; }

/* ── Panels Row ───────────────────────────────────────────────────────────── */
#panels-row {
    position: absolute;
    top: 56px;
    left: 0; right: 0;
    bottom: 100px;
    display: none;
    gap: 1px;
    background: #1f1f1f;
    z-index: 2;
    overflow: hidden;
}

body.started #panels-row { display: flex !important; }

.panel-col {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #0a0a0a;
    overflow: hidden;
}

.panel-header {
    padding: 10px 16px;
    background: #111111;
    border-bottom: 1px solid #1f1f1f;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-header.openai  { color: #86efac; }
.panel-header.gemini  { color: #93c5fd; }
.panel-header.claude  { color: #fbbf24; }

/* Gradio chatbot overrides */
#openai-chat, #gemini-chat, #claude-chat {
    flex: 1 !important;
    overflow-y: auto !important;
    border: none !important;
    background: transparent !important;
    height: 100% !important;
}

#openai-chat .wrap, #gemini-chat .wrap, #claude-chat .wrap {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

#openai-chat .message-wrap,
#gemini-chat .message-wrap,
#claude-chat .message-wrap {
    padding: 12px 16px !important;
    gap: 12px !important;
}

/* ── Status Bar ───────────────────────────────────────────────────────────── */
#status-bar {
    position: absolute;
    bottom: 0;
    left: 0; right: 0;
    height: 28px;
    display: flex;
    align-items: center;
    padding: 0 16px;
    font-size: 11px;
    color: #4b5563;
    background: #0a0a0a;
    border-top: 1px solid #1a1a1a;
    z-index: 1;
}

/* ── Footer Text ──────────────────────────────────────────────────────────── */
#footer-text {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    font-size: 12px;
    color: #374151;
    white-space: nowrap;
    pointer-events: none;
    transition: opacity 0.5s;
    z-index: 3;
}
body.started #footer-text { opacity: 0; }

/* ── Hidden Gradio Wrappers ───────────────────────────────────────────────── */
#hidden-controls {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
    top: -9999px;
    left: -9999px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a3a; }
"""
