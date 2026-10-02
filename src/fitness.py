from src.ackley import ackley_2d


def evaluate_colony(colony: list) -> list:
    """
    Compute f(x1, x2) for every food source in the colony.

    Returns a list of floats, same order and length as `colony`,
    so fitness_values[i] is always the fitness of colony[i].
    """
    return [ackley_2d(fs[0], fs[1]) for fs in colony]


def sort_colony(colony: list, fitness_values: list, ascending: bool = True):
    """
    Sort the colony by fitness.

    ascending=True  -> best (lowest f) first. Use this for a
                       minimization problem like ours.
    ascending=False -> use only if you deliberately want worst-first
                       (e.g. to display/report the weakest food sources).

    Returns (sorted_colony, sorted_fitness_values) as a matched pair.
    """
    paired = list(zip(colony, fitness_values))
    paired.sort(key=lambda item: item[1], reverse=not ascending)
    sorted_colony = [fs for fs, _ in paired]
    sorted_fitness = [fit for _, fit in paired]
    return sorted_colony, sorted_fitness


def get_best_source(colony: list, fitness_values: list):
    """
    Return (best_food_source, best_fitness): the single best
    food source in this cycle (lowest Ackley value).

    Person 4 will compare this against the PREVIOUS cycle's best
    and only replace it if the new one is strictly better — that
    'keep the best ever seen' logic lives in bee_operators.py / abc.py, not
    here. This function only answers 'who's best in THIS cycle'.
    """
    sorted_colony, sorted_fitness = sort_colony(colony, fitness_values, ascending=True)
    return sorted_colony[0], sorted_fitness[0]


if __name__ == "__main__":
    from src.colony import initialize_colony

    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    sorted_colony, sorted_fit = sort_colony(colony, fitness)
    best, best_fit = get_best_source(colony, fitness)

    print("Best 5 (ascending fitness):")
    for fs, f in zip(sorted_colony[:5], sorted_fit[:5]):
        print(f"  {fs} -> f = {f:.6f}")
    print(f"\nBest food source: {best}")
    print(f"Best fitness: {best_fit:.6f}")
