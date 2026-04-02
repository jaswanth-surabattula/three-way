"""Three-Way Arena — Gradio UI entry point.

Architecture:
  - gr.HTML renders all visual chrome (sidebar, header, hero, input bar).
    This bypasses Gradio's Svelte flex-wrapper injection entirely.
  - Hidden Gradio components (Textbox, Dropdown, Button, Chatbot) act as the
    Python bridge for event handling.
  - JS copies values from the visual HTML into the hidden components and
    programmatically clicks the hidden submit button to trigger Python.
"""

import json
import gradio as gr

from three_way.core.config import SUPPORTED_MODELS, DEFAULT_MODELS
from three_way.ui.constants import PHASE_MESSAGES
from three_way.ui.css import CSS
from three_way.ui.handlers import on_new_session, on_submit
from three_way.ui.helpers import dropdown_choices
from three_way.utils.logging_setup import setup_logging


# ---------------------------------------------------------------------------
# Model data for the toolbar chips
# ---------------------------------------------------------------------------

def _model_options(provider: str) -> list[str]:
    from three_way.core.config import models_for_provider
    return [m.display_name for m in models_for_provider(provider).values()]


_OPENAI_MODELS  = _model_options("openai")
_GEMINI_MODELS  = _model_options("gemini")
_CLAUDE_MODELS  = _model_options("claude")

_DEFAULT_OPENAI = SUPPORTED_MODELS[DEFAULT_MODELS["openai"]].display_name
_DEFAULT_GEMINI = SUPPORTED_MODELS[DEFAULT_MODELS["gemini"]].display_name
_DEFAULT_CLAUDE = SUPPORTED_MODELS[DEFAULT_MODELS["claude"]].display_name


def _menu_items(models: list[str], provider: str, default: str) -> str:
    items = []
    for m in models:
        cls = "active" if m == default else ""
        items.append(
            f'<li class="{cls}" '
            f'onclick="selectModel(\'{provider}\', this)">{m}</li>'
        )
    return "\n".join(items)


def _build_html() -> str:
    phrases_json = json.dumps(PHASE_MESSAGES)

    openai_menu = _menu_items(_OPENAI_MODELS, "openai", _DEFAULT_OPENAI)
    gemini_menu = _menu_items(_GEMINI_MODELS, "gemini", _DEFAULT_GEMINI)
    claude_menu = _menu_items(_CLAUDE_MODELS, "claude", _DEFAULT_CLAUDE)

    return f"""
<div id="app-shell">

  <!-- ── Sidebar ─────────────────────────────────────────────────── -->
  <div id="sidebar">
    <div class="sidebar-logo">3</div>
    <button class="sidebar-btn sidebar-btn-new"
            onclick="newSession()"
            title="New session">
      <!-- Plus icon -->
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none"
           xmlns="http://www.w3.org/2000/svg">
        <path d="M8 3v10M3 8h10" stroke="currentColor"
              stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>
    <div class="sidebar-spacer"></div>
    <button class="sidebar-btn sidebar-btn-settings" title="Settings">
      <!-- Gear icon -->
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
           xmlns="http://www.w3.org/2000/svg">
        <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"
              stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1
                 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0
                 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2
                 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65
                 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1
                 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0
                 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65
                 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2
                 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0
                 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2
                 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0
                 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0
                 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0
                 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65
                 0 0 0-1.51 1Z"
              stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
    </button>
  </div>

  <!-- ── Main content ─────────────────────────────────────────────── -->
  <div id="content">

    <!-- Header -->
    <div id="header">
      <span class="provider-chip chip-openai">OpenAI</span>
      <span class="provider-chip chip-gemini">Gemini</span>
      <span class="provider-chip chip-claude">Claude</span>
      <div class="header-spacer"></div>
      <button class="new-session-btn" onclick="newSession()">
        &#8635; New Session
      </button>
    </div>

    <!-- Hero -->
    <div id="hero">
      <div class="hero-title">Three-Way</div>
      <div class="hero-subtitle">
        <span class="hero-phrase" id="hero-phrase"></span>
      </div>
    </div>

    <!-- Footer hint -->
    <div id="footer-text">
      Three-Way brings you the best of OpenAI, Google, and Anthropic in one view.
    </div>

    <!-- Input bar -->
    <div id="input-bar">
      <textarea id="visual-prompt"
                placeholder="Ask all three models…"
                rows="1"
                onkeydown="handleKey(event)"
                oninput="autoResize(this)"></textarea>
      <div id="input-toolbar">

        <!-- Image attach button -->
        <button class="tool-btn" title="Attach image (coming soon)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="3"
                  stroke="currentColor" stroke-width="1.8"/>
            <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>
            <path d="m21 15-5-5L5 21" stroke="currentColor"
                  stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <!-- OpenAI model chip -->
        <div class="model-chip-wrap">
          <button class="model-chip chip-openai" id="chip-openai">
            <span id="chip-openai-label">{_DEFAULT_OPENAI}</span>
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M2 4l3-3 3 3M2 7l3 3 3-3"
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
          <ul class="model-menu" id="menu-openai">
            {openai_menu}
          </ul>
        </div>

        <!-- Gemini model chip -->
        <div class="model-chip-wrap">
          <button class="model-chip chip-gemini" id="chip-gemini">
            <span id="chip-gemini-label">{_DEFAULT_GEMINI}</span>
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M2 4l3-3 3 3M2 7l3 3 3-3"
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
          <ul class="model-menu" id="menu-gemini">
            {gemini_menu}
          </ul>
        </div>

        <!-- Claude model chip -->
        <div class="model-chip-wrap">
          <button class="model-chip chip-claude" id="chip-claude">
            <span id="chip-claude-label">{_DEFAULT_CLAUDE}</span>
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M2 4l3-3 3 3M2 7l3 3 3-3"
                    stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
          <ul class="model-menu" id="menu-claude">
            {claude_menu}
          </ul>
        </div>

        <div class="toolbar-spacer"></div>

        <!-- Send button -->
        <button class="send-btn" id="send-btn" onclick="submitPrompt()" title="Send">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <path d="M22 2L11 13" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M22 2L15 22 11 13 2 9l20-7Z" stroke="currentColor"
                  stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

      </div><!-- /input-toolbar -->
    </div><!-- /input-bar -->

  </div><!-- /content -->
</div><!-- /app-shell -->

<script>
(function() {{
  // ── Rotating subtitle phrases ──────────────────────────────────────────
  const PHRASES = {phrases_json};
  let phraseIdx = 0;

  function showPhrase() {{
    const el = document.getElementById('hero-phrase');
    if (!el) return;
    el.style.animation = 'none';
    el.offsetHeight; // reflow
    el.textContent = PHRASES[phraseIdx];
    el.style.animation = 'phraseIn 0.5s ease forwards';
    phraseIdx = (phraseIdx + 1) % PHRASES.length;
  }}

  showPhrase();
  setInterval(showPhrase, 4000);

  // ── Auto-resize textarea ──────────────────────────────────────────────
  window.autoResize = function(el) {{
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }};

  // ── Enter to send (Shift+Enter = newline) ─────────────────────────────
  window.handleKey = function(e) {{
    if (e.key === 'Enter' && !e.shiftKey) {{
      e.preventDefault();
      submitPrompt();
    }}
  }};

  // ── Model selection ───────────────────────────────────────────────────
  window.selectModel = function(provider, li) {{
    const name = li.textContent.trim();
    // Update chip label
    const label = document.getElementById('chip-' + provider + '-label');
    if (label) label.textContent = name;
    // Update active class in menu
    const menu = document.getElementById('menu-' + provider);
    if (menu) {{
      menu.querySelectorAll('li').forEach(function(item) {{
        item.classList.toggle('active', item === li);
      }});
    }}
    // Write to hidden Gradio dropdown
    setGradioDropdown(provider + '-dd', name);
  }};

  function setGradioDropdown(elemId, value) {{
    const wrap = document.getElementById(elemId);
    if (!wrap) return;
    const input = wrap.querySelector('input');
    if (!input) return;
    const nativeSet = Object.getOwnPropertyDescriptor(
      window.HTMLInputElement.prototype, 'value'
    ).set;
    nativeSet.call(input, value);
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
  }}

  // ── Submit ────────────────────────────────────────────────────────────
  window.submitPrompt = function() {{
    const ta = document.getElementById('visual-prompt');
    if (!ta) return;
    const text = ta.value.trim();
    if (!text) return;

    // Copy to hidden Gradio textbox
    const hPromptWrap = document.getElementById('h-prompt');
    if (hPromptWrap) {{
      const inp = hPromptWrap.querySelector('textarea') ||
                  hPromptWrap.querySelector('input');
      if (inp) {{
        const nativeSet = Object.getOwnPropertyDescriptor(
          Object.getPrototypeOf(inp), 'value'
        ).set;
        nativeSet.call(inp, text);
        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
      }}
    }}

    // Mark as started (hero fades, input moves to bottom)
    document.body.classList.add('started');

    // Clear visual textarea
    ta.value = '';
    ta.style.height = 'auto';

    // Click hidden submit button
    setTimeout(function() {{
      const btn = document.getElementById('h-submit');
      if (btn) btn.click();
    }}, 50);
  }};

  // ── New Session ───────────────────────────────────────────────────────
  window.newSession = function() {{
    document.body.classList.remove('started');
    // Click hidden new-session button
    const btn = document.getElementById('h-new-session');
    if (btn) btn.click();
    // Reset chip labels
    const defaults = {{
      openai: document.getElementById('menu-openai')?.querySelector('li:first-child')?.textContent,
      gemini: document.getElementById('menu-gemini')?.querySelector('li:first-child')?.textContent,
      claude: document.getElementById('menu-claude')?.querySelector('li:first-child')?.textContent,
    }};
    for (const [provider, name] of Object.entries(defaults)) {{
      if (!name) continue;
      const label = document.getElementById('chip-' + provider + '-label');
      if (label) label.textContent = name;
    }}
    // Reset visual textarea
    const ta = document.getElementById('visual-prompt');
    if (ta) {{ ta.value = ''; ta.style.height = 'auto'; }}
  }};
}})();
</script>
"""


# ---------------------------------------------------------------------------
# JS passed to launch() — moves the panels row into #content for correct
# z-index stacking (model menus appear above chat panels)
# ---------------------------------------------------------------------------
_LAUNCH_JS = """
() => {
    function relocatePanels() {
        const content = document.getElementById('content');
        const panels  = document.getElementById('panels-row');
        if (content && panels && panels.parentElement !== content) {
            content.appendChild(panels);
        }
    }
    setTimeout(relocatePanels, 300);
    setTimeout(relocatePanels, 1000);
    setTimeout(relocatePanels, 3000);
}
"""


# ---------------------------------------------------------------------------
# Build the Gradio app
# ---------------------------------------------------------------------------

def build_app() -> gr.Blocks:
    openai_choices, openai_default = dropdown_choices("openai")
    gemini_choices, gemini_default = dropdown_choices("gemini")
    claude_choices, claude_default = dropdown_choices("claude")

    with gr.Blocks(title="Three-Way Arena") as app:

        # ── Visual shell (sidebar + header + hero + input bar) ──────────
        gr.HTML(_build_html())

        # ── Hidden Gradio components (Python bridge) ────────────────────
        with gr.Group(elem_id="hidden-controls"):
            h_prompt = gr.Textbox(
                elem_id="h-prompt",
                label="prompt",
                show_label=False,
                visible=True,
            )
            h_openai_dd = gr.Dropdown(
                choices=openai_choices,
                value=openai_default,
                elem_id="openai-dd",
                label="OpenAI model",
                show_label=False,
                visible=True,
            )
            h_gemini_dd = gr.Dropdown(
                choices=gemini_choices,
                value=gemini_default,
                elem_id="gemini-dd",
                label="Gemini model",
                show_label=False,
                visible=True,
            )
            h_claude_dd = gr.Dropdown(
                choices=claude_choices,
                value=claude_default,
                elem_id="claude-dd",
                label="Claude model",
                show_label=False,
                visible=True,
            )
            h_submit = gr.Button(
                value="Submit",
                elem_id="h-submit",
                visible=True,
            )
            h_new_session = gr.Button(
                value="New Session",
                elem_id="h-new-session",
                visible=True,
            )

        # ── Chat panels row (visible=True so it renders to DOM; CSS hides it)
        with gr.Row(elem_id="panels-row", visible=True):
            with gr.Column(elem_classes=["panel-col"]):
                gr.HTML('<div class="panel-header openai">OpenAI</div>')
                openai_chat = gr.Chatbot(
                    elem_id="openai-chat",
                    show_label=False,
                    height=None,
                )
            with gr.Column(elem_classes=["panel-col"]):
                gr.HTML('<div class="panel-header gemini">Gemini</div>')
                gemini_chat = gr.Chatbot(
                    elem_id="gemini-chat",
                    show_label=False,
                    height=None,
                )
            with gr.Column(elem_classes=["panel-col"]):
                gr.HTML('<div class="panel-header claude">Claude</div>')
                claude_chat = gr.Chatbot(
                    elem_id="claude-chat",
                    show_label=False,
                    height=None,
                )

        # Status textbox (hidden, used for status text if needed)
        status_box = gr.Textbox(
            elem_id="status-box",
            show_label=False,
            visible=False,
        )

        # ── Event wiring ────────────────────────────────────────────────
        h_submit.click(
            fn=on_submit,
            inputs=[
                h_prompt,
                h_openai_dd, h_gemini_dd, h_claude_dd,
                openai_chat, gemini_chat, claude_chat,
            ],
            outputs=[openai_chat, gemini_chat, claude_chat, status_box],
        )

        h_new_session.click(
            fn=on_new_session,
            inputs=[],
            outputs=[openai_chat, gemini_chat, claude_chat, status_box],
        )

    return app


def launch() -> None:
    setup_logging()
    app = build_app()
    app.launch(
        server_name="0.0.0.0",
        css=CSS,
        js=_LAUNCH_JS,
    )


if __name__ == "__main__":
    launch()
