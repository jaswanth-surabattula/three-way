"""Central configuration: API keys and model catalogue.

Pricing is hardcoded — no provider offers an official pricing API.
Check the links below and update rates when they change.

Pricing references (verify before updating):
  OpenAI  → https://openai.com/api/pricing/
  Gemini  → https://ai.google.dev/pricing
  Claude  → https://www.anthropic.com/pricing#api

Model ID references (verify exact strings before updating):
  OpenAI  → https://platform.openai.com/docs/models
  Gemini  → https://ai.google.dev/gemini-api/docs/models
  Claude  → https://docs.anthropic.com/en/docs/about-claude/models

Last updated: 2026-03-31
See docs/how_to_update_models.md for step-by-step update instructions.
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class ModelConfig:
    provider: str            # "openai" | "gemini" | "claude"
    model_id: str            # exact ID sent to the API
    display_name: str        # human-readable label for the UI
    input_cost_per_1k: float   # USD per 1K input tokens  (0.0 = free tier)
    output_cost_per_1k: float  # USD per 1K output tokens (0.0 = free tier)
    supports_vision: bool = field(default=False)  # True = accepts image input
    # Large-context pricing tier (e.g. Gemini 2.5 Pro charges more above 200K tokens).
    # If input_cost_per_1k_large is 0.0, no tiered pricing applies for this model.
    large_context_threshold: int = field(default=0)       # tokens above which large pricing kicks in
    input_cost_per_1k_large: float = field(default=0.0)   # USD per 1K input tokens  (large context)
    output_cost_per_1k_large: float = field(default=0.0)  # USD per 1K output tokens (large context)


# ---------------------------------------------------------------------------
# Full model catalogue — text and vision models only (no image generation).
#
# To add a new model: copy an existing entry, update the fields, and add it
# to SUPPORTED_MODELS. See docs/how_to_update_models.md for full instructions.
# ---------------------------------------------------------------------------

SUPPORTED_MODELS: dict[str, ModelConfig] = {

    # ── OpenAI ──────────────────────────────────────────────────────────────
    # GPT-5.4 family. Verify IDs and pricing at:
    # https://platform.openai.com/docs/models
    # https://developers.openai.com/api/docs/pricing
    # Pricing verified 2026-03-31.
    # NOTE: The exact token threshold separating short/long context for gpt-5.4
    # and gpt-5.4-pro is not documented — 128K used as a reasonable default.
    # Verify and update large_context_threshold if OpenAI publishes the boundary.
    "gpt-5.4-pro": ModelConfig(
        provider="openai",
        model_id="gpt-5.4-pro",
        display_name="GPT-5.4 Pro",
        input_cost_per_1k=0.030000,        # $30.00 / 1M (short context)
        output_cost_per_1k=0.180000,       # $180.00 / 1M (short context)
        supports_vision=True,
        large_context_threshold=128_000,
        input_cost_per_1k_large=0.060000,  # $60.00 / 1M (long context)
        output_cost_per_1k_large=0.270000, # $270.00 / 1M (long context)
    ),
    "gpt-5.4": ModelConfig(
        provider="openai",
        model_id="gpt-5.4",
        display_name="GPT-5.4",
        input_cost_per_1k=0.002500,        # $2.50 / 1M (short context)
        output_cost_per_1k=0.015000,       # $15.00 / 1M (short context)
        supports_vision=True,
        large_context_threshold=128_000,
        input_cost_per_1k_large=0.005000,  # $5.00 / 1M (long context)
        output_cost_per_1k_large=0.022500, # $22.50 / 1M (long context)
    ),
    "gpt-5.4-mini": ModelConfig(
        provider="openai",
        model_id="gpt-5.4-mini",
        display_name="GPT-5.4 Mini",
        input_cost_per_1k=0.000750,   # $0.75 / 1M
        output_cost_per_1k=0.004500,  # $4.50 / 1M
        supports_vision=True,
    ),
    "gpt-5.4-nano": ModelConfig(
        provider="openai",
        model_id="gpt-5.4-nano",
        display_name="GPT-5.4 Nano",
        input_cost_per_1k=0.000200,   # $0.20 / 1M
        output_cost_per_1k=0.001250,  # $1.25 / 1M
        supports_vision=True,
    ),

    # ── Google Gemini ────────────────────────────────────────────────────────
    # Gemini 2.5 family only. Verify exact model IDs at:
    # https://ai.google.dev/gemini-api/docs/models
    # Pricing verified 2026-03-31: https://ai.google.dev/pricing
    "gemini-2.5-pro": ModelConfig(
        provider="gemini",
        model_id="gemini-2.5-pro",
        display_name="Gemini 2.5 Pro",
        input_cost_per_1k=0.001250,        # $1.25 / 1M  (≤200K tokens)
        output_cost_per_1k=0.010000,       # $10.00 / 1M (≤200K tokens)
        supports_vision=True,
        large_context_threshold=200_000,
        input_cost_per_1k_large=0.002500,  # $2.50 / 1M  (>200K tokens)
        output_cost_per_1k_large=0.015000, # $15.00 / 1M (>200K tokens)
    ),
    "gemini-2.5-flash": ModelConfig(
        provider="gemini",
        model_id="gemini-2.5-flash",
        display_name="Gemini 2.5 Flash",
        input_cost_per_1k=0.000300,   # $0.30 / 1M
        output_cost_per_1k=0.002500,  # $2.50 / 1M
        supports_vision=True,
    ),
    "gemini-2.5-flash-lite": ModelConfig(
        provider="gemini",
        model_id="gemini-2.5-flash-lite",
        display_name="Gemini 2.5 Flash Lite",
        input_cost_per_1k=0.000100,   # $0.10 / 1M
        output_cost_per_1k=0.000400,  # $0.40 / 1M
        supports_vision=True,
    ),

    # ── Anthropic Claude ─────────────────────────────────────────────────────
    # Model IDs confirmed at: https://docs.anthropic.com/en/docs/about-claude/models
    # Pricing verified 2026-03-31: https://platform.claude.com/docs/en/about-claude/pricing
    # Note: Claude has NO tiered context pricing — flat rate across the full 1M context window.
    "claude-opus-4-6": ModelConfig(
        provider="claude",
        model_id="claude-opus-4-6",
        display_name="Claude Opus 4.6",
        input_cost_per_1k=0.005000,   # $5.00 / 1M
        output_cost_per_1k=0.025000,  # $25.00 / 1M
        supports_vision=True,
    ),
    "claude-sonnet-4-6": ModelConfig(
        provider="claude",
        model_id="claude-sonnet-4-6",
        display_name="Claude Sonnet 4.6",
        input_cost_per_1k=0.003000,   # $3.00 / 1M
        output_cost_per_1k=0.015000,  # $15.00 / 1M
        supports_vision=True,
    ),
    "claude-haiku-4-5-20251001": ModelConfig(
        provider="claude",
        model_id="claude-haiku-4-5-20251001",
        display_name="Claude Haiku 4.5",
        input_cost_per_1k=0.001000,   # $1.00 / 1M
        output_cost_per_1k=0.005000,  # $5.00 / 1M
        supports_vision=True,
    ),
}

# Default (cheapest/free) model per provider — used when the user hasn't picked one.
DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-5.4-nano",
    "gemini": "gemini-2.5-flash-lite",
    "claude": "claude-haiku-4-5-20251001",
}


def get_model(model_id: str) -> ModelConfig:
    """Return config for a model ID.

    Raises KeyError with a helpful message if the model isn't in the catalogue.
    """
    if model_id not in SUPPORTED_MODELS:
        available = ", ".join(SUPPORTED_MODELS)
        raise KeyError(
            f"Unknown model '{model_id}'. Available models: {available}"
        )
    return SUPPORTED_MODELS[model_id]


def models_for_provider(provider: str) -> dict[str, ModelConfig]:
    """Return all supported models for a given provider."""
    return {k: v for k, v in SUPPORTED_MODELS.items() if v.provider == provider}


# ---------------------------------------------------------------------------
# API key helpers
# ---------------------------------------------------------------------------

_ENV_VARS: dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
}


def get_api_key(provider: str) -> str:
    """Return the API key for the given provider.

    Raises EnvironmentError with a clear message if the key is missing.
    """
    env_var = _ENV_VARS[provider]
    key = os.getenv(env_var)
    if not key:
        raise EnvironmentError(
            f"Missing API key: set {env_var} in your .env file."
        )
    return key
