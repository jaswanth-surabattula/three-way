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

Last updated: 2026-03-30
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


# ---------------------------------------------------------------------------
# Full model catalogue — text and vision models only (no image generation).
#
# To add a new model: copy an existing entry, update the fields, and add it
# to SUPPORTED_MODELS. See docs/how_to_update_models.md for full instructions.
# ---------------------------------------------------------------------------

SUPPORTED_MODELS: dict[str, ModelConfig] = {

    # ── OpenAI ──────────────────────────────────────────────────────────────
    # Latest flagship family (April 2025). Verify IDs at:
    # https://platform.openai.com/docs/models
    "gpt-4.1": ModelConfig(
        provider="openai",
        model_id="gpt-4.1",
        display_name="GPT-4.1",
        input_cost_per_1k=0.002000,   # $2.00 / 1M
        output_cost_per_1k=0.008000,  # $8.00 / 1M
        supports_vision=True,
    ),
    "gpt-4.1-mini": ModelConfig(
        provider="openai",
        model_id="gpt-4.1-mini",
        display_name="GPT-4.1 Mini",
        input_cost_per_1k=0.000400,   # $0.40 / 1M
        output_cost_per_1k=0.001600,  # $1.60 / 1M
        supports_vision=True,
    ),
    "gpt-4.1-nano": ModelConfig(
        provider="openai",
        model_id="gpt-4.1-nano",
        display_name="GPT-4.1 Nano",
        input_cost_per_1k=0.000100,   # $0.10 / 1M
        output_cost_per_1k=0.000400,  # $0.40 / 1M
        supports_vision=True,
    ),
    # Reasoning models — excellent for complex tasks; text-only
    "o4-mini": ModelConfig(
        provider="openai",
        model_id="o4-mini",
        display_name="o4 Mini",
        input_cost_per_1k=0.001100,   # $1.10 / 1M
        output_cost_per_1k=0.004400,  # $4.40 / 1M
        supports_vision=False,
    ),
    "o3": ModelConfig(
        provider="openai",
        model_id="o3",
        display_name="o3",
        input_cost_per_1k=0.010000,   # $10.00 / 1M
        output_cost_per_1k=0.040000,  # $40.00 / 1M
        supports_vision=False,
    ),

    # ── Google Gemini ────────────────────────────────────────────────────────
    # Latest family as of mid-2025 is 2.5. There is no Gemini 3.x yet.
    # Verify exact model ID strings at: https://ai.google.dev/gemini-api/docs/models
    "gemini-2.5-pro": ModelConfig(
        provider="gemini",
        model_id="gemini-2.5-pro",
        display_name="Gemini 2.5 Pro",
        input_cost_per_1k=0.001250,   # $1.25 / 1M (≤200K context)
        output_cost_per_1k=0.010000,  # $10.00 / 1M
        supports_vision=True,
    ),
    "gemini-2.5-flash": ModelConfig(
        provider="gemini",
        model_id="gemini-2.5-flash",
        display_name="Gemini 2.5 Flash",
        input_cost_per_1k=0.000150,   # $0.15 / 1M
        output_cost_per_1k=0.000600,  # $0.60 / 1M
        supports_vision=True,
    ),
    "gemini-2.0-flash": ModelConfig(
        provider="gemini",
        model_id="gemini-2.0-flash",
        display_name="Gemini 2.0 Flash",
        input_cost_per_1k=0.000100,   # $0.10 / 1M
        output_cost_per_1k=0.000400,  # $0.40 / 1M
        supports_vision=True,
    ),
    "gemini-2.0-flash-lite": ModelConfig(
        provider="gemini",
        model_id="gemini-2.0-flash-lite",
        display_name="Gemini 2.0 Flash Lite",
        input_cost_per_1k=0.0,        # free tier
        output_cost_per_1k=0.0,
        supports_vision=True,
    ),

    # ── Anthropic Claude ─────────────────────────────────────────────────────
    # Model IDs confirmed at: https://docs.anthropic.com/en/docs/about-claude/models
    "claude-opus-4-6": ModelConfig(
        provider="claude",
        model_id="claude-opus-4-6",
        display_name="Claude Opus 4.6",
        input_cost_per_1k=0.015000,   # $15.00 / 1M
        output_cost_per_1k=0.075000,  # $75.00 / 1M
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
        input_cost_per_1k=0.000800,   # $0.80 / 1M
        output_cost_per_1k=0.004000,  # $4.00 / 1M
        supports_vision=True,
    ),
}

# Default (cheapest/free) model per provider — used when the user hasn't picked one.
DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4.1-nano",
    "gemini": "gemini-2.0-flash-lite",  # free tier
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
