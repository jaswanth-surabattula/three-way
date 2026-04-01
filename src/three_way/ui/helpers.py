from three_way.core.config import DEFAULT_MODELS, SUPPORTED_MODELS, models_for_provider
from three_way.models.chat import ChatMessage


def display_to_model_id(display_name: str) -> str:
    for model_id, cfg in SUPPORTED_MODELS.items():
        if cfg.display_name == display_name:
            return model_id
    raise ValueError(f"Unknown display name: {display_name!r}")


def dropdown_choices(provider: str) -> tuple[list[str], str]:
    models = models_for_provider(provider)
    choices = [m.display_name for m in models.values()]
    default = SUPPORTED_MODELS[DEFAULT_MODELS[provider]].display_name
    return choices, default


def history_to_messages(history: list[dict]) -> list[ChatMessage]:
    def _extract_text(content) -> str:
        if isinstance(content, list):
            return " ".join(p["text"] for p in content if p.get("type") == "text")
        return content
    return [ChatMessage(role=m["role"], content=_extract_text(m["content"])) for m in history]


def format_response(resp) -> str:
    if resp.error:
        return f"**Error:** {resp.error}"
    stats = (
        f"\n\n---\n*{resp.latency_seconds:.2f}s &nbsp;|&nbsp; "
        f"{resp.total_tokens} tokens &nbsp;|&nbsp; "
        f"${resp.estimated_cost_usd:.6f}*"
    )
    return (resp.content or "") + stats
