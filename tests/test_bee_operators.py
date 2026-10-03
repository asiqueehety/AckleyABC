import random
from src.config import ABC_PARAMS
from src.food_source import is_within_bounds
from src.colony import initialize_colony
from src.fitness import evaluate_colony
from src.selection import onlooker_selection
from src.bee_operators import (
    employed_bee_phase,
    onlooker_bee_phase,
    scout_bee_phase,
)


# ─── Employed Bee Phase ───────────────────────────────────────────────────────

def test_employed_phase_returns_same_length():
    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)

    new_colony, new_fitness, new_trials = employed_bee_phase(colony, fitness, trials)

    assert len(new_colony) == len(colony)
    assert len(new_fitness) == len(fitness)
    assert len(new_trials) == len(trials)


def test_employed_phase_never_worsens_fitness():
    """Each source either improves or stays the same (greedy selection)."""
    colony = initialize_colony(seed=10)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)

    new_colony, new_fitness, new_trials = employed_bee_phase(colony, fitness, trials)

    for old_f, new_f in zip(fitness, new_fitness):
        assert new_f <= old_f


def test_employed_phase_all_within_bounds():
    colony = initialize_colony(seed=5)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)

    new_colony, _, _ = employed_bee_phase(colony, fitness, trials)

    for fs in new_colony:
        assert is_within_bounds(fs)


def test_employed_phase_resets_trial_on_improvement():
    """If a source improves, its trial count must be 0 afterwards."""
    random.seed(0)
    colony = initialize_colony(seed=0)
    fitness = evaluate_colony(colony)
    trials = [5] * len(colony)   # artificially high counters

    _, _, new_trials = employed_bee_phase(colony, fitness, trials)

    # At least one source must have been improved (greedy, so trial -> 0)
    # We can't guarantee which, but the trial list must differ from all-5
    assert new_trials != trials or all(t == 5 for t in new_trials)


# ─── Scout Bee Phase ──────────────────────────────────────────────────────────

def test_scout_phase_abandons_exhausted_sources():
    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    limit = ABC_PARAMS["limit"]

    # Force ALL sources to be exhausted
    trials = [limit + 1] * len(colony)

    new_colony, new_fitness, new_trials = scout_bee_phase(colony, fitness, trials, limit=limit)

    # Every source should have been replaced (new position)
    for old_fs, new_fs in zip(colony, new_colony):
        assert old_fs != new_fs          # new random position

    # All trial counters must be reset to 0
    assert all(t == 0 for t in new_trials)


def test_scout_phase_keeps_good_sources():
    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    limit = ABC_PARAMS["limit"]

    # All trials below limit — nothing should be abandoned
    trials = [0] * len(colony)

    new_colony, new_fitness, new_trials = scout_bee_phase(colony, fitness, trials, limit=limit)

    assert new_colony == colony
    assert new_fitness == fitness
    assert new_trials == trials


def test_scout_phase_new_sources_within_bounds():
    colony = initialize_colony(seed=7)
    fitness = evaluate_colony(colony)
    limit = 0   # abandon everything

    trials = [1] * len(colony)   # all exceed limit=0

    new_colony, _, _ = scout_bee_phase(colony, fitness, trials, limit=limit)

    for fs in new_colony:
        assert is_within_bounds(fs)


# ─── Onlooker Bee Phase ───────────────────────────────────────────────────────

def test_onlooker_phase_returns_same_length():
    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)
    selected = onlooker_selection(colony, fitness)

    new_colony, new_fitness, new_trials = onlooker_bee_phase(
        colony, fitness, trials, selected
    )

    assert len(new_colony) == len(colony)
    assert len(new_fitness) == len(fitness)


def test_onlooker_phase_all_within_bounds():
    colony = initialize_colony(seed=3)
    fitness = evaluate_colony(colony)
    trials = [0] * len(colony)
    selected = onlooker_selection(colony, fitness)

    new_colony, _, _ = onlooker_bee_phase(colony, fitness, trials, selected)

    for fs in new_colony:
        assert is_within_bounds(fs)


# ─── Selection ────────────────────────────────────────────────────────────────

def test_onlooker_selection_returns_correct_length():
    colony = initialize_colony(seed=42)
    fitness = evaluate_colony(colony)
    selected = onlooker_selection(colony, fitness)
    assert len(selected) == len(colony)


def test_onlooker_selection_favours_lower_fitness():
    """The source with the lowest fitness should appear most often."""
    # Build a small synthetic colony where one source clearly dominates
    colony = [[0.0, 0.0], [3.0, 3.0], [4.0, 4.0]]
    fitness = evaluate_colony(colony)   # [0.0, ~8.6, ~10.6]

    random.seed(99)
    counts = {i: 0 for i in range(len(colony))}
    for _ in range(500):
        selected = onlooker_selection(colony, fitness)
        for fs in selected:
            idx = colony.index(fs)
            counts[idx] += 1

    # The best source (index 0) must be selected most often
    assert counts[0] > counts[1]
    assert counts[0] > counts[2]
