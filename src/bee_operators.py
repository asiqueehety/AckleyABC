import random
from typing import List, Tuple, Optional
from src.config import ABC_PARAMS
from src.food_source import is_within_bounds, clamp
from src.fitness import sort_colony


def employed_bee_phase(
    colony: list,
    fitness_values: list,
    trial_counts: list,
) -> Tuple[list, list, list]:
    """
    Employed Bee Phase of the ABC algorithm.

    Each employed bee (one per food source) attempts to find a better
    neighbouring food source by modifying ONE randomly chosen dimension
    using the standard ABC perturbation formula:

        v_ij = x_ij + phi_ij * (x_ij - x_kj)

    where:
        - x_i  is the current food source
        - x_k  is a DIFFERENT randomly chosen food source (k != i)
        - j    is a randomly selected dimension index
        - phi  is a uniform random number in [-1, 1]

    If the neighbour v_i is better (lower Ackley) it REPLACES x_i and the
    trial counter resets to 0; otherwise x_i is kept and its trial count
    increments by 1.

    Args:
        colony:        current list of food sources.
        fitness_values: corresponding Ackley values.
        trial_counts:  number of consecutive cycles each source has NOT improved.

    Returns:
        (new_colony, new_fitness, new_trial_counts) — all same length as input.
    """
    from src.ackley import ackley_2d

    n = len(colony)
    new_colony = [list(fs) for fs in colony]
    new_fitness = list(fitness_values)
    new_trials = list(trial_counts)

    for i in range(n):
        # Choose a random partner k != i
        k = random.choice([idx for idx in range(n) if idx != i])

        # Choose a random dimension to perturb
        j = random.randrange(len(colony[i]))

        # Perturbation
        phi = random.uniform(-1.0, 1.0)
        candidate = list(colony[i])
        candidate[j] = clamp(colony[i][j] + phi * (colony[i][j] - colony[k][j]))

        candidate_fitness = ackley_2d(candidate[0], candidate[1])

        # Greedy selection: keep whichever is better (lower)
        if candidate_fitness < fitness_values[i]:
            new_colony[i] = candidate
            new_fitness[i] = candidate_fitness
            new_trials[i] = 0
        else:
            new_trials[i] = trial_counts[i] + 1

    return new_colony, new_fitness, new_trials


def onlooker_bee_phase(
    colony: list,
    fitness_values: list,
    trial_counts: list,
    selected_sources: list,
) -> Tuple[list, list, list]:
    """
    Onlooker Bee Phase of the ABC algorithm.

    After employed bees share information via the waggle dance, onlooker
    bees choose sources probabilistically (done by Person 3's selection.py)
    and apply the SAME perturbation formula as the employed bee phase to
    the chosen source.

    Args:
        colony:          current food sources.
        fitness_values:  corresponding Ackley values.
        trial_counts:    trial counter per source.
        selected_sources: list of food sources chosen by onlookers (from selection.py).

    Returns:
        (new_colony, new_fitness, new_trial_counts)
    """
    from src.ackley import ackley_2d

    n = len(colony)
    new_colony = [list(fs) for fs in colony]
    new_fitness = list(fitness_values)
    new_trials = list(trial_counts)

    for selected in selected_sources:
        # Find the index of the selected source in the current colony
        try:
            i = next(idx for idx, fs in enumerate(colony) if fs == selected)
        except StopIteration:
            continue   # guard against stale reference

        # Choose a random partner k != i
        k = random.choice([idx for idx in range(n) if idx != i])

        # Choose a random dimension
        j = random.randrange(len(colony[i]))

        phi = random.uniform(-1.0, 1.0)
        candidate = list(colony[i])
        candidate[j] = clamp(colony[i][j] + phi * (colony[i][j] - colony[k][j]))

        candidate_fitness = ackley_2d(candidate[0], candidate[1])

        if candidate_fitness < new_fitness[i]:
            new_colony[i] = candidate
            new_fitness[i] = candidate_fitness
            new_trials[i] = 0
        else:
            new_trials[i] = new_trials[i] + 1

    return new_colony, new_fitness, new_trials


def scout_bee_phase(
    colony: list,
    fitness_values: list,
    trial_counts: list,
    limit: Optional[int] = None,
) -> Tuple[list, list, list]:
    """
    Scout Bee Phase of the ABC algorithm.

    Any food source whose trial counter exceeds `limit` is ABANDONED.
    The employed bee that was exploiting it becomes a scout and randomly
    discovers a new food source (uniformly sampled from the search space).

    This is the ABC's main mechanism for escaping local optima — analogous
    to mutation resetting a gene in GA, but triggered adaptively by the
    trial counter rather than by a fixed probability.

    Args:
        colony:        current food sources.
        fitness_values: corresponding Ackley values.
        trial_counts:  trial counter per source.
        limit:         abandonment threshold (default ABC_PARAMS["limit"]).

    Returns:
        (new_colony, new_fitness, reset_trial_counts)
    """
    from src.ackley import ackley_2d
    from src.food_source import random_food_source

    if limit is None:
        limit = ABC_PARAMS["limit"]

    new_colony = [list(fs) for fs in colony]
    new_fitness = list(fitness_values)
    new_trials = list(trial_counts)

    for i in range(len(colony)):
        if trial_counts[i] > limit:
            # Abandon: scout randomly discovers a fresh food source
            new_source = random_food_source()
            new_colony[i] = new_source
            new_fitness[i] = ackley_2d(new_source[0], new_source[1])
            new_trials[i] = 0

    return new_colony, new_fitness, new_trials


if __name__ == "__main__":
    from src.colony import initialize_colony
    from src.fitness import evaluate_colony

    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)

    print("Before employed phase, best fitness:", min(fitness))
    colony, fitness, trials = employed_bee_phase(colony, fitness, trials)
    print("After employed phase,  best fitness:", min(fitness))
    colony, fitness, trials = scout_bee_phase(colony, fitness, trials)
    print("After scout phase,     best fitness:", min(fitness))
