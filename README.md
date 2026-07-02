# keno-stats-engine

Hypergeometric statistics and rarity-based scoring for keno-style lotteries.
**Analysis, not prediction** — every draw is an independent event; this library
describes probabilities and past frequencies, it does not forecast anything.

Extracted from the statistics core powering [LotoRadar.com](https://lotoradar.com),
a live lottery statistics platform running in production since March 2026.

## The math

In a keno-style lottery the operator draws `drawn` numbers from a pool of
`pool`. A player picks `picks` numbers. The number of matches ("hits")
follows a **hypergeometric distribution**:

```
P(X = k) = C(picks, k) · C(pool − picks, drawn − k) / C(pool, drawn)
```

Works for any configuration: Greek Kino (20/80), Czech Keno (12/66),
or anything else.

## Install

```bash
pip install .
# dev:
pip install .[dev]
```

## Usage

```python
from keno_stats import hit_probability, hit_distribution, odds_one_in, score_result

# Probability of hitting 10/10 in a 20/80 keno
p = hit_probability(pool=80, drawn=20, picks=10, hits=10)
print(f"1 in {odds_one_in(p):,.0f}")   # 1 in 8,911,711

# Full distribution for a 6-number ticket
for hits, prob in hit_distribution(pool=80, drawn=20, picks=6).items():
    print(f"{hits} hits: {prob:.4%}")

# Rarity-based scoring: score = 10 · log2(1/P)
result = score_result(pool=80, drawn=20, picks=10, hits=8)
print(result.score, result.tier)   # rare outcome => high score, high tier
```

### Frequency analysis (descriptive only)

```python
from keno_stats import hot_numbers, cold_numbers, gap_analysis

draws = [[3, 17, 42, ...], ...]          # historical draws
hot_numbers(draws, top=10)               # most frequent numbers
cold_numbers(draws, pool=80, bottom=10)  # least frequent, incl. never drawn
gap_analysis(draws, pool=80)             # draws since each number last appeared
```

## Why rarity-based scoring?

Raw hit counts are misleading: 5/5 on a 5-pick ticket is far rarer than
5/15 on a 15-pick ticket. Scoring by **surprisal** — `log2(1/P)` of the
exact outcome — makes results comparable across ticket sizes and lottery
formats. This is the mechanism behind LotoRadar's tier system
(COMMON → COSMIC).

## Tests

```bash
pytest
```

## Disclaimer

This library is for statistical education and analysis. Past draw
frequencies have **no bearing** on future draws. Lottery outcomes cannot
be predicted. Play responsibly, 18+.

## License

MIT
