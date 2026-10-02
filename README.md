# CSE 4112 ML Lab — Artificial Bee Colony on the 2D Ackley Function

Find the global minimum of the 2D Ackley function using an Artificial Bee Colony (ABC) Algorithm.

- Search space: -5 <= x1, x2 <= 5
- Global minimum: f(x1*, x2*) = f(0, 0) = 0
- Encoding: continuous real-valued food source = [x1, x2]
- ABC settings: colony_size = 50 (25 employed + 25 onlooker), cycles = 100, limit = 10

## Team pipeline (sequential — each person builds on the last)

| # | Owner | Scope | Status |
|---|-------|-------|--------|
| 1 | Person 1 | Ackley function, ABC config, food source representation | ✅ Done |
| 2 | Person 2 | Colony initialisation, fitness evaluation, sorting, per-cycle best | ✅ Done |
| 3 | Person 3 | Onlooker bee selection (fitness-proportionate / waggle dance) | ✅ Done |
| 4 | Person 4 | Employed bee phase, onlooker bee phase, scout bee phase | ✅ Done |
| 5 | Person 5 | Full ABC loop, experiments, graphs, analysis | ✅ Done |

## Folder structure

```
ABC/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py          # Person 1 — all ABC/Ackley parameters in one place
│   ├── ackley.py          # Person 1 — ackley_2d(), ackley_nd()
│   ├── food_source.py     # Person 1 — real-valued food source helpers
│   ├── colony.py          # Person 2 — initialize_colony()
│   ├── fitness.py         # Person 2 — evaluate_colony(), sort_colony(), get_best_source()
│   ├── selection.py       # Person 3 — onlooker_selection(), compute_selection_probabilities()
│   ├── bee_operators.py   # Person 4 — employed_bee_phase(), onlooker_bee_phase(), scout_bee_phase()
│   └── abc.py             # Person 5 — run_abc()
├── tests/
│   ├── __init__.py
│   ├── test_ackley.py
│   ├── test_colony_fitness.py
│   ├── test_bee_operators.py
│   └── test_analysis.py
└── analysis/
    ├── __init__.py
    ├── README.md
    ├── plotting.py        # convergence, selection wheel, parameter comparison plots
    ├── run_analysis.py    # orchestrates baseline + 6 experiments + writes report
    └── output/            # generated at runtime (PNGs + analysis.md)
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running things

Run the full ABC analysis (baseline + 6 parameter experiments + graphs):

```bash
python -m analysis.run_analysis
```

Run the tests:

```bash
pytest -v
```

## How ABC works (for the report / viva)

The Artificial Bee Colony algorithm mimics the foraging behaviour of honeybees.
The colony is divided into three functional groups:

| Bee type | Count | Role |
|----------|-------|------|
| Employed | colony_size // 2 | Each exploits one food source; tries to find a better neighbour using the perturbation formula `v_ij = x_ij + φ·(x_ij − x_kj)` |
| Onlooker | colony_size // 2 | Watch the waggle dance and probabilistically choose (roulette-wheel) a source to further exploit |
| Scout    | ≤ 1 per cycle | Any source stagnant for `limit` consecutive cycles is abandoned; that bee becomes a scout and randomly discovers a new source |

### Key differences from Genetic Algorithm

| Aspect | GA | ABC |
|--------|----|-----|
| Population unit | Chromosome [x1, x2] | Food source [x1, x2] |
| New solution creation | Crossover + mutation | Perturbation formula (employed & onlooker phases) |
| Diversity mechanism | Mutation probability pm | Scout bee abandonment (trial counter ≥ limit) |
| Selection | Roulette wheel (parents for crossover) | Roulette wheel (onlookers choosing sources) |
| Elitism | Top-k carry-over | Greedy acceptance in every phase |

## Design notes

- **Real-valued encoding**: a food source is `[x1, x2]`, directly in the continuous search space.
  No encode/decode step needed.
- **Minimisation**: lower `f(x1, x2)` = better nectar quality.  All three phases use greedy
  acceptance (accept neighbour only if it is strictly better) so the best-ever fitness
  never increases.
- **Reproducibility**: `initialize_colony(seed=...)` accepts a seed for exact reproducibility —
  useful for the report's worked examples and for debugging with teammates.
- **Limit-based diversity**: the trial counter per source replaces GA's fixed mutation probability.
  If a source cannot improve for `limit` cycles it is abandoned, forcing the assigned bee to
  explore a completely new random location.  This is ABC's main anti-stagnation mechanism.
