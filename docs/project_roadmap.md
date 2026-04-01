# Project Roadmap — Tri-Model LLM Arena

## Session Log

| Session | Date | What we built | Status |
|---|---|---|---|
| 1 | 2026-03-30 | `models/chat.py` — Pydantic schemas | Done |
| 2 | 2026-03-30 | `core/config.py` — model catalogue + API key helpers | Done |
| 3 | 2026-03-31 | `utils/timer.py` — Timer context manager + calculate_cost() with tiered pricing | Done |
| 4 | 2026-03-31 | `services/openai_client.py` | Done |
| 5 | 2026-03-31 | `services/gemini_client.py` + `services/claude_client.py` | Done |
| 6 | 2026-03-31 | `services/arena.py` — asyncio.gather orchestrator | Done |
| 7 | 2026-04-01 | Terminal smoke test + `__init__.py` main() | Done |
| 8 | 2026-04-01 | Gradio UI — 3-pane layout + model dropdowns | Done |
| 9 | 2026-04-01 | Gradio UI — wire submit + display responses | Done |
| 10 | - | Vision / image input support | Pending |
| 11 | - | Analytics panel (latency, tokens, cost per turn) | Pending |
| 12 | - | Session report (HTML export, charts, AI summary) | Pending |
| 13 | - | Polish + error handling | Pending |
| 14 | - | Deploy to Hugging Face Spaces | Pending |

---

## Phase Breakdown

### Phase 1 — Foundation ✅
**Files:** `models/chat.py`, `core/config.py`

- Pydantic schemas: `Provider`, `ChatMessage`, `ChatRequest`, `ChatResponse`
- Central config: model catalogue (OpenAI GPT-5.4, Gemini 2.5, Claude 4.x), tiered pricing support, API key helpers
- `ChatResponse.error` field so one failing provider doesn't crash the others

---

### Phase 2 — Utilities ✅
**File:** `utils/timer.py`

- `Timer` context manager — wraps a block of code and records elapsed time
- `calculate_cost()` — applies tiered pricing (short/long context) per model; shared by all three clients

---

### Phase 3 — API Clients ✅
**Files:** `services/openai_client.py`, `services/gemini_client.py`, `services/claude_client.py`, `services/arena.py`

- Each client: async `chat(request, model_id) -> ChatResponse` — same interface, different SDK internals
- `arena.py`: `asyncio.gather` fires all three simultaneously; total wait ≈ slowest provider
- Migrated Gemini SDK from deprecated `google-generativeai` to `google-genai`
- Confirmed live: Claude Haiku works; OpenAI and Gemini pending billing setup

---

### Phase 3 — Individual API Clients
**Files:** `services/openai_client.py`, `services/gemini_client.py`, `services/claude_client.py`

Each file exposes one async function:
```python
async def call_<provider>(
    messages: list[ChatMessage],
    model_id: str,
    max_tokens: int,
) -> ChatResponse
```

Each client: gets API key → starts timer → calls SDK → returns normalised `ChatResponse`.
Exceptions are caught and returned as `ChatResponse(error="...")` so failures are isolated.

Provider SDK differences to watch:
- OpenAI: `AsyncOpenAI`, `chat.completions.create()`
- Gemini: `google.generativeai`, role is `"model"` not `"assistant"`, `generate_content_async()`
- Claude: `AsyncAnthropic`, `messages.create()`

---

### Phase 4 — Orchestrator
**File:** `services/arena.py`

```python
async def run_arena(prompt, openai_model, gemini_model, claude_model, ...) -> list[ChatResponse]
```

Uses `asyncio.gather()` to fire all three API calls simultaneously.
Without this, calls would be sequential (~3× slower).
`return_exceptions=True` ensures one crash doesn't stop the others.

---

### Phase 5 — Gradio UI: Layout & Wiring ✅
**Files:** `ui/app.py`, `ui/components/`, `ui/handlers.py`, `ui/helpers.py`, `ui/css.py`, `ui/constants.py`

#### Component structure
- `app.py` — assembles all components and wires all Gradio events; the only file that imports from both `components/` and `handlers.py`
- `components/header.py` — app title + New Session button
- `components/panels.py` — 3 `gr.Chatbot` panels + empty-state badges (shown before first prompt)
- `components/input_bar.py` — prompt textarea + model dropdowns + send/chevron buttons + collapsible session menu
- `components/modals.py` — model-change confirmation modal + end-session/report modal
- `css.py` — all Gradio CSS overrides: pill-style dropdowns, dark theme, panel sizing
- `constants.py` — cycling empty-state phase messages

#### How UI events wire to backend
Each Gradio event uses `.click()` or `.submit()` on a component, binding an `inputs` list → handler function → `outputs` list. No direct backend calls live in `app.py`; all logic is in `handlers.py`.

Example — send button wired to submission handler:
```python
send_btn.click(
    fn=on_submit,
    inputs=[prompt_box, openai_dd, gemini_dd, claude_dd,
            openai_chat, gemini_chat, claude_chat, session_active],
    outputs=[openai_chat, gemini_chat, claude_chat,
             status, prompt_box, session_active, panels_row, phase_col],
)
```

#### Handler → service flow (`on_submit`)
1. `helpers.display_to_model_id(dd_value)` — maps dropdown display name to model ID string (e.g. `"GPT-5.4 Nano"` → `"gpt-5.4-nano"`)
2. `helpers.history_to_messages(chat_history)` — converts Gradio chat list to `list[ChatMessage]`
3. `arena.run(req_a, req_b, req_c, model_a, model_b, model_c)` — fires all three APIs via `asyncio.gather`; waits for the slowest
4. `helpers.format_response(response)` — appends latency / token / cost stats table to response text
5. Yields updated chat histories + status string back to Gradio (UI updates live)

#### UI state management
Three `gr.State` objects carry state between events (not stored server-side):
- `session_active: bool` — gates model-change confirmation modal
- `menu_visible: bool` — tracks chevron toggle open/close
- `phase_idx: int` — cycles empty-state phase messages on each New Session click

---

### Phase 6 — Terminal Smoke Test ✅
**File:** `src/three_way/__init__.py`

`main()` calls `arena.run()` with a hardcoded prompt and prints all three responses.
Confirms all three clients fire and return before touching the UI — easier to debug auth errors here.

---

### Phase 7 — Vision / Image Support
---

### Phase 7 — Vision / Image Support
**Files:** `ui/app.py`, each client file

- Image upload component in the UI
- Pass image alongside text to vision-capable models (`supports_vision=True`)
- Models where `supports_vision=False` (e.g. o3) skip the image and show a note
- Each SDK handles image input differently (base64 / bytes / URL) — handled per client

---

### Phase 8 — Analytics Panel
**File:** `ui/app.py`

Live stats table after each query:

| | OpenAI | Gemini | Claude |
|---|---|---|---|
| Latency | Xs | Xs | Xs |
| Tokens in | N | N | N |
| Tokens out | N | N | N |
| Est. cost | $X | $X | $X |

Plus running session totals (cumulative tokens + cost across all turns).

---

### Phase 9 — Session Report
**File:** `services/report.py`, `ui/app.py`

"Download Report" button generates an HTML file containing:
1. Full conversation history (all prompts + all three responses)
2. Charts: latency over turns, cost accumulation (matplotlib or plotly)
3. AI-generated performance summary — send the session to one of the three models and ask it to evaluate

---

### Phase 10 — Error Handling & Polish

- Rate limit errors → clear user-facing message (not a stack trace)
- Empty/null responses → handled gracefully
- API timeouts → cancel after 30s, show timeout message
- Mobile layout → vertical stack for small screens (Gradio responsive options)

---

### Phase 11 — Deploy to Hugging Face Spaces

1. Create a free Space on huggingface.co (Gradio SDK)
2. Add API keys as **Secrets** in Space settings (never committed to git)
3. Ensure `app.py` exists at the project root as the entry point
4. Push — Spaces auto-builds and serves a public URL

---

## Key Design Decisions (for reference)

| Decision | Why |
|---|---|
| Pydantic for `ChatResponse` | Normalises all three providers into one schema; `error` field isolates failures |
| Frozen dataclass for `ModelConfig` | Config is set-once; immutability prevents accidental changes |
| Hardcoded pricing | No provider offers a pricing API; links to pricing pages are in `config.py` header |
| `SUPPORTED_MODELS` keyed by model ID | O(1) lookup; UI dropdowns auto-populate from this dict |
| `asyncio.gather` in arena | Fires all three calls simultaneously; waits for the slowest, not the sum |
| Error returned in `ChatResponse`, not raised | One bad API key shouldn't crash the other two responses |
