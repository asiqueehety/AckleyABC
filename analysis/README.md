# Analysis — ABC Ackley Experiments

This folder contains the analysis and plotting utilities for the ABC algorithm
run on the 2D Ackley function.

## Files

| File | Description |
|------|-------------|
| `plotting.py` | Reusable plot functions (convergence curve, onlooker selection wheel, parameter comparison) |
| `run_analysis.py` | Orchestrates the baseline run + 6 parameter experiments and writes all artifacts |
| `output/` | Generated plots and analysis.md (created at runtime) |

## Running

From the `ABC/` directory:

```bash
python -m analysis.run_analysis
```

Or with custom options:

```bash
python -m analysis.run_analysis --output-dir analysis/output --seed 42
```

## Outputs

- `convergence.png` — best-so-far fitness per cycle
- `selection_wheel.png` — pie chart of onlooker selection probabilities
- `parameter_comparison.png` — multi-line comparison of parameter variants
- `analysis.md` — written report with baseline stats and interpretation table
