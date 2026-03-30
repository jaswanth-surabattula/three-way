# How to Update the Model Catalogue

This project intentionally uses hardcoded model definitions — no dynamic fetching.
When providers release new models or change pricing, follow the steps below.

---

## Where models are defined

All models live in one file:

```
src/three_way/core/config.py
```

The `SUPPORTED_MODELS` dictionary maps a model ID string to a `ModelConfig` object.
The `DEFAULT_MODELS` dictionary points to the cheapest/free model per provider.

---

## Step 1 — Find the new model's ID

Each provider has a models page where exact API IDs are listed.
The ID you put in `config.py` must match exactly what you send to the API.

| Provider | Models page |
|---|---|
| OpenAI | https://platform.openai.com/docs/models |
| Gemini | https://ai.google.dev/gemini-api/docs/models |
| Claude | https://docs.anthropic.com/en/docs/about-claude/models |

> **Tip:** On the Anthropic page, look for the "API model name" column — that's the exact string.
> For Gemini, model IDs sometimes include a date suffix like `gemini-2.5-pro-preview-05-06`.
> Use whichever string their docs say to pass to the API.

---

## Step 2 — Find the new model's pricing

| Provider | Pricing page |
|---|---|
| OpenAI | https://openai.com/api/pricing/ |
| Gemini | https://ai.google.dev/pricing |
| Claude | https://www.anthropic.com/pricing#api |

Pricing pages show cost per **1 million tokens**.
The config stores cost per **1,000 tokens**, so divide by 1,000:

```
$1.25 per 1M tokens  →  0.001250 per 1K tokens
$0.10 per 1M tokens  →  0.000100 per 1K tokens
$0     (free tier)   →  0.0
```

---

## Step 3 — Add the model to `config.py`

Open `src/three_way/core/config.py` and add a new entry to `SUPPORTED_MODELS`.
Copy the closest existing entry and update the fields:

```python
"your-model-id-here": ModelConfig(
    provider="openai",               # "openai" | "gemini" | "claude"
    model_id="your-model-id-here",   # must match the API exactly
    display_name="Human Name",       # shown in the UI
    input_cost_per_1k=0.002000,      # from Step 2 (÷ 1000)
    output_cost_per_1k=0.008000,     # from Step 2 (÷ 1000)
    supports_vision=True,            # True if model accepts image input
),
```

The key (left of the colon) and `model_id` should be the same string.

---

## Step 4 — Update `DEFAULT_MODELS` if needed

If the new model should be the default (e.g. it replaced the previous cheapest option),
update the pointer in `DEFAULT_MODELS`:

```python
DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4.1-nano",           # ← change this if needed
    "gemini": "gemini-2.0-flash-lite",
    "claude": "claude-haiku-4-5-20251001",
}
```

---

## Step 5 — Update the "Last updated" date

At the top of `config.py`, update this line:

```python
Last updated: YYYY-MM-DD
```

---

## Step 6 — Remove deprecated models

If a provider has retired a model, remove its entry from `SUPPORTED_MODELS`.
Check the provider's deprecation notices:

| Provider | Deprecation notices |
|---|---|
| OpenAI | https://platform.openai.com/docs/deprecations |
| Gemini | https://ai.google.dev/gemini-api/docs/models (look for "deprecated" labels) |
| Claude | https://docs.anthropic.com/en/docs/about-claude/models (look for sunset dates) |

---

## Quick reference — current model families (as of 2026-03-30)

### OpenAI
- **GPT-4.1 family** — `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano` (vision capable)
- **Reasoning** — `o3`, `o4-mini` (text only, think step-by-step before answering)

### Google Gemini
- **2.5 family** — `gemini-2.5-pro`, `gemini-2.5-flash` (latest, most capable)
- **2.0 family** — `gemini-2.0-flash`, `gemini-2.0-flash-lite` (stable, `flash-lite` is free tier)
- Note: there is no Gemini 3.x as of this writing.

### Anthropic Claude
- `claude-opus-4-6` — most capable, most expensive
- `claude-sonnet-4-6` — balanced
- `claude-haiku-4-5-20251001` — fastest, cheapest

---

## A note on pricing accuracy

Hardcoded prices can drift from reality over time.
Before running cost estimates in a demo or presentation, take 2 minutes to spot-check
the prices against the provider's pricing page.
The links at the top of `config.py` go directly to the right pages.
