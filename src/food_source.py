import random
from src.config import ABC_PARAMS


def random_position() -> float:
    """One dimension value drawn uniformly from the search range."""
    low, high = ABC_PARAMS["bounds"]
    return random.uniform(low, high)


def random_food_source() -> list:
    """A full food source = [x1, x2, ...] with num_dimensions values."""
    return [random_position() for _ in range(ABC_PARAMS["num_dimensions"])]


def is_within_bounds(food_source: list) -> bool:
    """
    Sanity check used by tests (and later by bee operators) to
    confirm every dimension still respects -5 <= xi <= 5 after an operation.
    """
    low, high = ABC_PARAMS["bounds"]
    return all(low <= val <= high for val in food_source)


def clamp(value: float) -> float:
    """Clamp a single value to the search bounds [-5.0, 5.0]."""
    low, high = ABC_PARAMS["bounds"]
    return max(low, min(high, value))


if __name__ == "__main__":
    fs = random_food_source()
    print("Random food source:", fs)
    print("Within bounds?", is_within_bounds(fs))
