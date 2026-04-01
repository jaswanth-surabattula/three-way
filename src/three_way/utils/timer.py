import time

from three_way.core.config import ModelConfig


class Timer:
    """Context manager that measures elapsed wall-clock time."""

    def __init__(self):
        self.elapsed: float = 0.0  # seconds, available after __exit__

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_) -> None:
        self.elapsed = time.perf_counter() - self._start


def calculate_cost(model: ModelConfig, input_tokens: int, output_tokens: int) -> float:
    """Return the total USD cost for a single API call.

    Applies large-context pricing when the model defines a threshold and
    input_tokens exceeds it (e.g. Gemini 2.5 Pro charges more above 200K tokens).

    Args:
        model:         ModelConfig for the model that was called.
        input_tokens:  Number of tokens in the prompt (what you sent).
        output_tokens: Number of tokens in the response (what came back).

    Returns:
        Total cost in USD, rounded to 6 decimal places.
    """
    use_large = (
        model.large_context_threshold > 0
        and input_tokens > model.large_context_threshold
    )
    input_rate  = model.input_cost_per_1k_large  if use_large else model.input_cost_per_1k
    output_rate = model.output_cost_per_1k_large if use_large else model.output_cost_per_1k

    input_cost  = (input_tokens  / 1000) * input_rate
    output_cost = (output_tokens / 1000) * output_rate
    return round(input_cost + output_cost, 6)