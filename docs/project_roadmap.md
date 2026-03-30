# Project Roadmap — Tri-Model LLM Arena

## Session Log

| Session | Date | What we built | Status |
|---|---|---|---|
| 1 | 2026-03-30 | `models/chat.py` — Pydantic schemas | Done |
| 2 | 2026-03-30 | `core/config.py` — model catalogue + API key helpers | Done |
| 3 | next | `utils/timer.py` — latency context manager + cost helper | Pending |
| 4 | - | `services/openai_client.py` | Pending |
| 5 | - | `services/gemini_client.py` + `services/claude_client.py` | Pending |
| 6 | - | `services/arena.py` — concurrent orchestrator | Pending |
| 7 | - | Terminal smoke test + debug | Pending |
| 8 | - | Gradio UI — 3-pane layout + model dropdowns | Pending |
| 9 | - | Gradio UI — wire submit + display responses | Pending |
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
- Central config: full model catalogue (OpenAI GPT-4.1, Gemini 2.x/2.5, Claude 4.x), pricing, API key helpers
- `ChatResponse.error` field so one failing provider doesn't crash the others

---

### Phase 2 — Utilities
**File:** `utils/timer.py`

- `Timer` context manager — wraps a block of code and records elapsed time
- `calculate_cost(prompt_tokens, completion_tokens, input_rate, output_rate)` — shared math used by all three clients

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

### Phase 5 — Terminal Smoke Test
**File:** `src/three_way/__init__.py` (update `main()`)

Run `uv run three-way` and verify all three clients return real responses.
Fix any auth errors or SDK quirks here — much easier than debugging inside a UI.

---

### Phase 6 — Gradio UI: Core Layout
**File:** `ui/app.py`

- 3-column layout, one per provider
- Each column: provider label, model dropdown (populated from `models_for_provider()`), response text box
- Shared prompt input + submit button at the bottom
- Model dropdowns auto-update from config — no UI code changes needed when adding new models

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
