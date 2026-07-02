"""Frequency analysis over historical draws.

Descriptive statistics only: these tools describe what *has happened*
in past draws. They do not — and cannot — predict future draws.
Each draw is an independent event.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple

Draw = Sequence[int]


def number_frequencies(draws: Iterable[Draw]) -> Counter:
    """Count how many times each number appeared across draws."""
    counter: Counter = Counter()
    for draw in draws:
        counter.update(draw)
    return counter


def hot_numbers(draws: Iterable[Draw], top: int = 10) -> List[Tuple[int, int]]:
    """Most frequently drawn numbers as (number, count), descending."""
    return number_frequencies(draws).most_common(top)


def cold_numbers(
    draws: Iterable[Draw], pool: int, bottom: int = 10
) -> List[Tuple[int, int]]:
    """Least frequently drawn numbers, including never-drawn ones.

    Args:
        draws: Historical draws.
        pool: Pool size, so numbers that never appeared are included.
        bottom: How many to return.
    """
    freq = number_frequencies(draws)
    full = {n: freq.get(n, 0) for n in range(1, pool + 1)}
    return sorted(full.items(), key=lambda kv: (kv[1], kv[0]))[:bottom]


def windowed_frequencies(
    draws: Sequence[Draw], window: int
) -> Dict[int, Counter]:
    """Frequencies over a sliding window of the most recent draws.

    Returns:
        Mapping ``{window_start_index: Counter}`` for each full window.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    result: Dict[int, Counter] = {}
    for start in range(0, max(len(draws) - window + 1, 0)):
        result[start] = number_frequencies(draws[start : start + window])
    return result


def gap_analysis(draws: Sequence[Draw], pool: int) -> Dict[int, int]:
    """Draws elapsed since each number last appeared.

    A number appearing in the most recent draw has gap 0. A number that
    never appeared has gap ``len(draws)``.
    """
    gaps = {n: len(draws) for n in range(1, pool + 1)}
    for age, draw in enumerate(reversed(draws)):
        for n in draw:
            if gaps.get(n, 0) == len(draws):
                gaps[n] = age
    return gaps
