import math

ABC_PARAMS = {
    # --- Problem definition ---
    "num_dimensions": 2,              # food source = [x1, x2]
    "bounds": (-5.0, 5.0),           # search space: -5 <= x1, x2 <= 5

    # --- Ackley function parameters (recommended values) ---
    "ackley_a": 20.0,
    "ackley_b": 0.2,
    "ackley_c": 2 * math.pi,

    # --- ABC hyperparameters ---
    "colony_size": 50,        # total bees = employed + onlooker (each half)
    "num_cycles": 100,        # number of foraging cycles (= generations in GA)
    "limit": 10,              # abandonment threshold: trials before scout reset
}
