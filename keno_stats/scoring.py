"""Rarity-based scoring for lottery hit results.

The core idea: a result's score should reflect how *statistically rare*
it is, not just how many numbers matched. Hitting 5/5 on a 5-number
ticket is far rarer than 5/15 on a 15-number ticket, and should score
accordingly.

We use the surprisal (information content) of the outcome:

    score = round(base * log2(1 / P(hits)))

where P(hits) is the hypergeometric probability of that exact outcome.
Rarer outcomes carry more information => higher score.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2

from .hypergeometric import hit_probability

#: Multiplier applied to the surprisal. Tune per deployment.
DEFAULT_BASE = 10

#: Tier thresholds expressed as "1 in N" rarity of the outcome.
#: An outcome rarer than the threshold earns the tier.
TIERS = (
    ("COSMIC", 1_000_000),
    ("DIAMOND", 100_000),
    ("GOLD", 10_000),
    ("SILVER", 1_000),
    ("BRONZE", 100),
    ("COMMON", 0),
)


@dataclass(frozen=True)
class ScoredResult:
    """Outcome of scoring a single ticket against a draw."""

    picks: int
    hits: int
    probability: float
    score: int
    tier: str


def score_result(
    pool: int,
    drawn: int,
    picks: int,
    hits: int,
    base: int = DEFAULT_BASE,
) -> ScoredResult:
    """Score a ticket outcome by its statistical rarity.

    Args:
        pool: Lottery pool size (e.g. 80).
        drawn: Numbers drawn per round (e.g. 20).
        picks: Numbers on the player's ticket.
        hits: Numbers matched.
        base: Score multiplier.

    Returns:
        A :class:`ScoredResult` with probability, score and tier.
    """
    p = hit_probability(pool, drawn, picks, hits)
    if p <= 0:
        raise ValueError(
            f"Impossible outcome: {hits} hits with {picks} picks "
            f"in a {drawn}/{pool} lottery"
        )
    score = round(base * log2(1 / p)) if p < 1 else 0
    return ScoredResult(
        picks=picks,
        hits=hits,
        probability=p,
        score=score,
        tier=_tier_for(p),
    )


def _tier_for(probability: float) -> str:
    rarity = 1 / probability if probability > 0 else float("inf")
    for name, threshold in TIERS:
        if rarity >= threshold:
            return name
    return TIERS[-1][0]
