"""Hypergeometric probability utilities for lottery/keno analysis.

In a keno-style lottery, the operator draws ``drawn`` numbers from a pool
of ``pool`` numbers. A player picks ``picks`` numbers. The number of
matches ("hits") follows a hypergeometric distribution:

    P(X = k) = C(picks, k) * C(pool - picks, drawn - k) / C(pool, drawn)

This module is lottery-agnostic: it works for Greek Kino (20/80),
Czech Keno (12/66), or any pool/drawn configuration.
"""

from __future__ import annotations

from math import comb
from typing import Dict


def hit_probability(pool: int, drawn: int, picks: int, hits: int) -> float:
    """Probability of exactly ``hits`` matches.

    Args:
        pool: Total numbers in the lottery pool (e.g. 80 for Greek Kino).
        drawn: Numbers drawn by the operator (e.g. 20).
        picks: Numbers the player selected.
        hits: Exact number of matches to compute the probability for.

    Returns:
        Probability in [0, 1].

    Raises:
        ValueError: If the configuration is impossible.
    """
    _validate(pool, drawn, picks)
    if hits < 0 or hits > picks:
        return 0.0
    if hits > drawn or picks - hits > pool - drawn:
        return 0.0
    return comb(picks, hits) * comb(pool - picks, drawn - hits) / comb(pool, drawn)


def hit_distribution(pool: int, drawn: int, picks: int) -> Dict[int, float]:
    """Full probability distribution over all possible hit counts.

    Returns:
        Mapping ``{hits: probability}`` for hits in [0, picks].
        Probabilities sum to 1.0 (within floating point error).
    """
    _validate(pool, drawn, picks)
    return {k: hit_probability(pool, drawn, picks, k) for k in range(picks + 1)}


def at_least(pool: int, drawn: int, picks: int, hits: int) -> float:
    """Probability of getting *at least* ``hits`` matches."""
    dist = hit_distribution(pool, drawn, picks)
    return sum(p for k, p in dist.items() if k >= hits)


def expected_hits(pool: int, drawn: int, picks: int) -> float:
    """Expected number of hits: picks * drawn / pool."""
    _validate(pool, drawn, picks)
    return picks * drawn / pool


def odds_one_in(probability: float) -> float:
    """Convert a probability to '1 in N' odds. Returns inf for p == 0."""
    if probability <= 0:
        return float("inf")
    return 1.0 / probability


def _validate(pool: int, drawn: int, picks: int) -> None:
    if pool <= 0:
        raise ValueError(f"pool must be positive, got {pool}")
    if not 0 < drawn <= pool:
        raise ValueError(f"drawn must be in (0, pool], got {drawn}")
    if not 0 < picks <= pool:
        raise ValueError(f"picks must be in (0, pool], got {picks}")
