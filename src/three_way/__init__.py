import asyncio

from three_way.core.config import DEFAULT_MODELS
from three_way.models.chat import ChatMessage, ChatRequest
from three_way.services import arena


def main() -> None:
    prompt = input("Enter your prompt: ").strip()
    if not prompt:
        print("No prompt entered. Exiting.")
        return

    request = ChatRequest(messages=[ChatMessage(role="user", content=prompt)])

    openai_model = DEFAULT_MODELS["openai"]
    gemini_model = DEFAULT_MODELS["gemini"]
    claude_model = DEFAULT_MODELS["claude"]

    print(f"\nSending to {openai_model} | {gemini_model} | {claude_model} ...\n")

    responses = asyncio.run(
        arena.run(request, openai_model, gemini_model, claude_model)
    )

    for response in responses:
        print(f"── {response.provider.value.upper()} ({response.model}) ──")
        if response.error:
            print(f"  ERROR: {response.error}")
        else:
            print(f"  {response.content}")
            print(f"  Latency: {response.latency_seconds:.2f}s | "
                  f"Tokens: {response.total_tokens} | "
                  f"Cost: ${response.estimated_cost_usd:.6f}")
        print()
