"""Reusable plots for ABC convergence and onlooker selection probabilities."""

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def selection_probabilities(fitness_values: Sequence[float]) -> list[float]:
    """Convert minimization fitness values into onlooker selection probabilities."""
    if not fitness_values:
        raise ValueError("fitness_values cannot be empty")

    maximum = max(fitness_values)
    selection_values = [(maximum - fitness) + 1e-10 for fitness in fitness_values]
    total = sum(selection_values)

    if total == 0:
        return [1.0 / len(fitness_values)] * len(fitness_values)
    return [value / total for value in selection_values]


def plot_selection_wheel(
    fitness_values: Sequence[float],
    output_path: str | Path,
    sample_size: int = 8,
) -> Path:
    """Save a pie chart showing onlooker selection probabilities for a colony sample."""
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")

    sample = list(fitness_values[:sample_size])
    if not sample:
        raise ValueError("fitness_values cannot be empty")

    probabilities = selection_probabilities(sample)
    deep_colors = [
        "#E8A838",   # amber — honey-inspired palette for ABC
        "#D9622B",
        "#C4421A",
        "#F0C96B",
        "#A8752E",
        "#F5A623",
        "#6B3D0D",
        "#FFDD99",
    ]
    colors = [deep_colors[index % len(deep_colors)] for index in range(len(sample))]
    labels = [f"Source {index + 1}\nf={fitness:.3f}" for index, fitness in enumerate(sample)]

    figure, axis = plt.subplots(figsize=(9, 7), constrained_layout=True)
    axis.pie(
        probabilities,
        labels=labels,
        colors=colors,
        startangle=90,
        counterclock=False,
        autopct=lambda value: f"{value:.1f}%" if value >= 3 else "",
        pctdistance=0.72,
        wedgeprops={"linewidth": 1.2, "edgecolor": "white"},
        textprops={"fontsize": 9, "color": "black"},
    )
    axis.set_title("Onlooker Bee Selection Probabilities\nFinal colony sample (waggle-dance fitness)")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path


def plot_convergence(
    fitness_history: Sequence[float],
    output_path: str | Path,
) -> Path:
    """Save the best-ever Ackley fitness against cycle number."""
    if not fitness_history:
        raise ValueError("fitness_history cannot be empty")

    cycles = range(1, len(fitness_history) + 1)
    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    axis.plot(
        cycles,
        fitness_history,
        color="#E8A838",
        linewidth=2.4,
        marker="o" if len(fitness_history) <= 40 else None,
        markersize=3,
        label="Best-so-far fitness",
    )
    axis.fill_between(cycles, fitness_history, 0, color="#E8A838", alpha=0.12)
    axis.set_title("ABC Convergence on the 2D Ackley Function")
    axis.set_xlabel("Cycle")
    axis.set_ylabel("Ackley fitness (lower is better)")
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper right")
    axis.set_ylim(bottom=0)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path


def plot_experiment_comparison(
    histories: dict[str, Sequence[float]],
    output_path: str | Path,
) -> Path:
    """Save a comparison plot for parameter experiments."""
    if not histories:
        raise ValueError("histories cannot be empty")

    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    for label, history in histories.items():
        if not history:
            raise ValueError(f"history for {label!r} cannot be empty")
        axis.plot(range(1, len(history) + 1), history, linewidth=2, label=label)

    axis.set_title("Parameter Sensitivity: Best-So-Far Fitness (ABC)")
    axis.set_xlabel("Cycle")
    axis.set_ylabel("Ackley fitness (lower is better)")
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper right", fontsize=9)
    axis.set_ylim(bottom=0)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path
