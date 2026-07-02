"""keno-stats-engine — hypergeometric statistics for keno-style lotteries.

Descriptive statistics and rarity-based scoring. Analysis, not prediction.
"""

from .hypergeometric import (
    at_least,
    expected_hits,
    hit_distribution,
    hit_probability,
    odds_one_in,
)
from .scoring import ScoredResult, score_result
from .frequency import (
    cold_numbers,
    gap_analysis,
    hot_numbers,
    number_frequencies,
    windowed_frequencies,
)

__version__ = "0.1.0"

__all__ = [
    "at_least",
    "expected_hits",
    "hit_distribution",
    "hit_probability",
    "odds_one_in",
    "ScoredResult",
    "score_result",
    "cold_numbers",
    "gap_analysis",
    "hot_numbers",
    "number_frequencies",
    "windowed_frequencies",
]
