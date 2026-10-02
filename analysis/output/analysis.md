# Artificial Bee Colony (ABC) Analysis

## Baseline run

- Seed: `42`
- Colony size: `50`  (employed = onlooker = 25)
- Cycles: `100`
- Abandonment limit: `10`
- Best food source: `[-6.051847618532281e-06, 1.1499099686052401e-06]`
- Initial best fitness: `3.276279`
- Final best fitness: `0.000017`
- Improvement: `3.276262`

The convergence plot records the best value found up to each cycle. Because the ABC algorithm applies greedy selection in the employed and onlooker phases, the best-so-far curve should never increase.

## Onlooker selection wheel

Onlooker bees choose food sources based on nectar quality communicated via the waggle dance. The pie chart uses the final colony sample and applies the same inverse-fitness transformation as `src.selection`.

## Parameter sensitivity

| Variant | Final best fitness | Interpretation |
| --- | ---: | --- |
| Smaller colony (colony_size=20) | 0.000437 | Fewer bees reduce exploration diversity; convergence may be faster but to worse optima. |
| Larger colony (colony_size=100) | 0.000000 | More bees increase exploration; slower per-cycle progress but better coverage. |
| Low limit (limit=3) | 0.010691 | Frequent abandonment leads to more scouting (exploration) but less exploitation of promising sources. |
| High limit (limit=30) | 0.000000 | Sources persist longer; stronger exploitation but may get stuck in local optima. |
| Fewer cycles (num_cycles=50) | 0.000131 | Less time to converge; final fitness is typically worse. |
| More cycles (num_cycles=200) | 0.000008 | Extra time allows finer exploitation near the global minimum. |

These comparisons use the same seed and one changed parameter per run. They are illustrative rather than a statistical benchmark; repeated runs with multiple seeds are recommended for a rigorous performance comparison.

## Generated files

- `convergence.png` — baseline best-fitness curve per cycle
- `selection_wheel.png` — sample onlooker selection probabilities
- `parameter_comparison.png` — parameter sensitivity curves
