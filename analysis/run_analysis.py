"""Run the ABC algorithm, generate plots, and write a parameter analysis report.

Run from the ABC directory:
    python -m analysis.run_analysis
"""

import argparse
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from src.config import ABC_PARAMS
from src.fitness import evaluate_colony
from src.abc import run_abc
from src.colony import initialize_colony

from analysis.plotting import (
    plot_convergence,
    plot_experiment_comparison,
    plot_selection_wheel,
)


@contextmanager
def temporary_parameters(overrides: dict[str, object]) -> Iterator[None]:
    """Temporarily apply ABC parameters and restore them even if a run fails."""
    original = {key: ABC_PARAMS[key] for key in overrides}
    ABC_PARAMS.update(overrides)
    try:
        yield
    finally:
        ABC_PARAMS.update(original)


def _run_variant(label: str, seed: int, overrides: dict[str, object]) -> dict:
    with temporary_parameters(overrides):
        result = run_abc(seed=seed)
    return {
        "label": label,
        "best_fitness": result["best_fitness"],
        "history": result["fitness_history"],
    }


def _write_report(
    output_path: Path,
    seed: int,
    baseline: dict,
    variants: list[dict],
) -> None:
    baseline_start = baseline["fitness_history"][0]
    baseline_end = baseline["best_fitness"]
    improvement = baseline_start - baseline_end

    lines = [
        "# Artificial Bee Colony (ABC) Analysis",
        "",
        "## Baseline run",
        "",
        f"- Seed: `{seed}`",
        f"- Colony size: `{ABC_PARAMS['colony_size']}`  (employed = onlooker = {ABC_PARAMS['colony_size'] // 2})",
        f"- Cycles: `{ABC_PARAMS['num_cycles']}`",
        f"- Abandonment limit: `{ABC_PARAMS['limit']}`",
        f"- Best food source: `{baseline['best_source']}`",
        f"- Initial best fitness: `{baseline_start:.6f}`",
        f"- Final best fitness: `{baseline_end:.6f}`",
        f"- Improvement: `{improvement:.6f}`",
        "",
        "The convergence plot records the best value found up to each cycle. "
        "Because the ABC algorithm applies greedy selection in the employed and onlooker "
        "phases, the best-so-far curve should never increase.",
        "",
        "## Onlooker selection wheel",
        "",
        "Onlooker bees choose food sources based on nectar quality communicated via "
        "the waggle dance. The pie chart uses the final colony sample and applies "
        "the same inverse-fitness transformation as `src.selection`.",
        "",
        "## Parameter sensitivity",
        "",
        "| Variant | Final best fitness | Interpretation |",
        "| --- | ---: | --- |",
    ]

    interpretations = {
        "Smaller colony (colony_size=20)": "Fewer bees reduce exploration diversity; convergence may be faster but to worse optima.",
        "Larger colony (colony_size=100)": "More bees increase exploration; slower per-cycle progress but better coverage.",
        "Low limit (limit=3)": "Frequent abandonment leads to more scouting (exploration) but less exploitation of promising sources.",
        "High limit (limit=30)": "Sources persist longer; stronger exploitation but may get stuck in local optima.",
        "Fewer cycles (num_cycles=50)": "Less time to converge; final fitness is typically worse.",
        "More cycles (num_cycles=200)": "Extra time allows finer exploitation near the global minimum.",
    }
    for variant in variants:
        label = variant["label"]
        lines.append(
            f"| {label} | {variant['best_fitness']:.6f} | {interpretations[label]} |"
        )

    lines.extend(
        [
            "",
            "These comparisons use the same seed and one changed parameter per run. "
            "They are illustrative rather than a statistical benchmark; repeated runs "
            "with multiple seeds are recommended for a rigorous performance comparison.",
            "",
            "## Generated files",
            "",
            "- `convergence.png` — baseline best-fitness curve per cycle",
            "- `selection_wheel.png` — sample onlooker selection probabilities",
            "- `parameter_comparison.png` — parameter sensitivity curves",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_analysis(output_dir: str | Path = "analysis/output", seed: int = 42) -> dict:
    """Run the baseline and parameter experiments and generate all artifacts."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    baseline = run_abc(seed=seed)
    initial_colony = initialize_colony(seed=seed)
    initial_fitness = evaluate_colony(initial_colony)
    plot_selection_wheel(initial_fitness, output_path / "selection_wheel.png")
    plot_convergence(baseline["fitness_history"], output_path / "convergence.png")

    variants = [
        ("Smaller colony (colony_size=20)", {"colony_size": 20}),
        ("Larger colony (colony_size=100)", {"colony_size": 100}),
        ("Low limit (limit=3)", {"limit": 3}),
        ("High limit (limit=30)", {"limit": 30}),
        ("Fewer cycles (num_cycles=50)", {"num_cycles": 50}),
        ("More cycles (num_cycles=200)", {"num_cycles": 200}),
    ]
    experiment_results = [
        _run_variant(label, seed, overrides) for label, overrides in variants
    ]
    histories = {"Baseline": baseline["fitness_history"]}
    histories.update({result["label"]: result["history"] for result in experiment_results})
    plot_experiment_comparison(histories, output_path / "parameter_comparison.png")

    baseline_report = dict(baseline)
    baseline_report["best_source"] = baseline["best_source"]
    _write_report(output_path / "analysis.md", seed, baseline_report, experiment_results)

    return {
        "output_dir": output_path,
        "baseline": baseline,
        "experiments": experiment_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="analysis/output")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    result = run_analysis(args.output_dir, args.seed)
    baseline = result["baseline"]
    print(f"Analysis written to: {result['output_dir']}")
    print(f"Best food source: {baseline['best_source']}")
    print(f"Best fitness: {baseline['best_fitness']:.6f}")
    print(f"Generated experiments: {len(result['experiments'])}")


if __name__ == "__main__":
    main()
