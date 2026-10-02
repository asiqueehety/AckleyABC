import random


def onlooker_selection(colony: list, fitness_values: list) -> list:
    """
    Onlooker bee selection via fitness-proportionate (roulette-wheel) selection.

    In ABC the onlooker bees choose food sources based on the nectar amount
    (fitness) of the sources communicated by employed bees via the waggle dance.
    Because we MINIMISE Ackley, lower fitness = better nectar quality, so we
    invert the fitness to compute selection probabilities — exactly the same
    transformation used in the GA's roulette-wheel selection.

    Args:
        colony:        list of food sources (each is a [x1, x2] position).
        fitness_values: corresponding Ackley values (lower = better).

    Returns:
        A list of food sources of the same length as `colony`, where each
        element is the food source that the corresponding onlooker bee
        chose to exploit.  Multiple onlookers can pick the same source.
    """
    if len(colony) != len(fitness_values):
        raise ValueError("colony and fitness_values must have the same length")

    if not colony:
        return []

    max_fitness = max(fitness_values)

    # Invert: lower Ackley value -> larger selection weight
    selection_weights = [
        (max_fitness - fitness) + 1e-10
        for fitness in fitness_values
    ]

    total = sum(selection_weights)

    if total == 0:
        probabilities = [1.0 / len(colony)] * len(colony)
    else:
        probabilities = [w / total for w in selection_weights]

    # Build cumulative probabilities for roulette-wheel spin
    cumulative = []
    running = 0.0
    for p in probabilities:
        running += p
        cumulative.append(running)

    selected = []
    for _ in range(len(colony)):          # one onlooker per employed bee
        r = random.random()
        for i, cp in enumerate(cumulative):
            if r <= cp:
                selected.append(colony[i])
                break

    return selected


def compute_selection_probabilities(fitness_values: list) -> list:
    """
    Pure helper (no randomness) — convert fitness values into selection
    probabilities using the same inverse-fitness scheme as
    onlooker_selection().

    Used by the analysis module to visualise the probability distribution
    without actually performing a selection.
    """
    if not fitness_values:
        raise ValueError("fitness_values cannot be empty")

    max_fitness = max(fitness_values)
    weights = [(max_fitness - f) + 1e-10 for f in fitness_values]
    total = sum(weights)

    if total == 0:
        return [1.0 / len(fitness_values)] * len(fitness_values)
    return [w / total for w in weights]
