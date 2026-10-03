from src.config import ABC_PARAMS
from src.food_source import is_within_bounds
from src.colony import initialize_colony
from src.fitness import evaluate_colony, sort_colony, get_best_source


def test_colony_size_and_shape():
    colony = initialize_colony(seed=42)
    # colony length = colony_size // 2 (one source per employed bee)
    assert len(colony) == ABC_PARAMS["colony_size"] // 2
    for fs in colony:
        assert len(fs) == ABC_PARAMS["num_dimensions"]


def test_colony_within_bounds():
    colony = initialize_colony(seed=7)
    for fs in colony:
        assert is_within_bounds(fs)


def test_reproducible_with_seed():
    colony_a = initialize_colony(seed=123)
    colony_b = initialize_colony(seed=123)
    assert colony_a == colony_b


def test_evaluate_colony_matches_length():
    colony = initialize_colony(seed=1)
    fitness = evaluate_colony(colony)
    assert len(fitness) == len(colony)


def test_sort_colony_ascending():
    colony = initialize_colony(seed=1)
    fitness = evaluate_colony(colony)
    sorted_colony, sorted_fit = sort_colony(colony, fitness, ascending=True)
    assert sorted_fit == sorted(sorted_fit)


def test_get_best_source_is_the_minimum():
    colony = initialize_colony(seed=1)
    fitness = evaluate_colony(colony)
    best, best_fit = get_best_source(colony, fitness)
    assert best_fit == min(fitness)
    assert best == colony[fitness.index(min(fitness))]
