import random
from src.config import ABC_PARAMS
from src.food_source import random_food_source


def initialize_colony(colony_size: int = None, seed: int = None) -> list:
    """
    Initialize the colony of food sources (positions in the search space).

    In the ABC algorithm, the number of employed bees equals the number of
    food sources, which is colony_size // 2. The same number of onlooker
    bees watch the employed bees, giving a total swarm of colony_size.

    Returns a list of food sources (each a [x1, x2] list). The length of
    this list is colony_size // 2 (number of employed bees = food sources).
    """
    if seed is not None:
        random.seed(seed)

    num_sources = (ABC_PARAMS["colony_size"] if colony_size is None else colony_size) // 2
    return [random_food_source() for _ in range(num_sources)]


if __name__ == "__main__":
    colony = initialize_colony(seed=42)
    print(f"Generated {len(colony)} food sources (employed bees).")
    for i, fs in enumerate(colony[:5]):
        print(f"  #{i}: {fs}")
    print("  ...")
