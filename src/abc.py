from src.config import ABC_PARAMS
from src.fitness import evaluate_colony, get_best_source
from src.bee_operators import employed_bee_phase, onlooker_bee_phase, scout_bee_phase
from src.colony import initialize_colony
from src.selection import onlooker_selection


def run_abc(seed: int = None) -> dict:
    """Run the configured Artificial Bee Colony algorithm on the Ackley function.

    The ABC loop follows the standard three-phase structure:
        1. Employed Bee Phase  — each bee tries to improve its own food source.
        2. Onlooker Bee Phase  — bees chosen proportional to nectar quality
                                 (fitness-based roulette wheel) further exploit
                                 promising sources.
        3. Scout Bee Phase     — sources stagnant for more than `limit` cycles
                                 are abandoned and randomly re-initialised.

    Args:
        seed: Optional random seed for fully reproducible runs.

    Returns:
        A dictionary containing:
            best_source    : the best [x1, x2] found across all cycles.
            best_fitness   : corresponding Ackley value.
            fitness_history: list of best-ever fitness at each cycle end.
            colony         : final food sources (sorted ascending by fitness).
            fitness        : final fitness values.
    """
    colony = initialize_colony(
        colony_size=ABC_PARAMS["colony_size"],
        seed=seed,
    )

    fitness_values = evaluate_colony(colony)
    trial_counts = [0] * len(colony)

    best_source = None
    best_fitness = float("inf")
    fitness_history = []

    for _ in range(ABC_PARAMS["num_cycles"]):
        # --- Phase 1: Employed Bees ---
        colony, fitness_values, trial_counts = employed_bee_phase(
            colony, fitness_values, trial_counts
        )

        # --- Phase 2: Onlooker Bees ---
        selected = onlooker_selection(colony, fitness_values)
        colony, fitness_values, trial_counts = onlooker_bee_phase(
            colony, fitness_values, trial_counts, selected
        )

        # --- Phase 3: Scout Bees ---
        colony, fitness_values, trial_counts = scout_bee_phase(
            colony, fitness_values, trial_counts,
            limit=ABC_PARAMS["limit"],
        )

        # --- Record best-ever ---
        current_best_source, current_best_fitness = get_best_source(colony, fitness_values)
        if current_best_fitness < best_fitness:
            best_source = list(current_best_source)
            best_fitness = current_best_fitness

        fitness_history.append(best_fitness)

    return {
        "best_source": best_source,
        "best_fitness": best_fitness,
        "fitness_history": fitness_history,
        "colony": colony,
        "fitness": fitness_values,
    }
