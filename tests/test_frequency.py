import pytest

from keno_stats import (
    cold_numbers,
    gap_analysis,
    hot_numbers,
    number_frequencies,
    windowed_frequencies,
)

DRAWS = [
    [1, 2, 3],
    [2, 3, 4],
    [3, 4, 5],
]


def test_number_frequencies():
    freq = number_frequencies(DRAWS)
    assert freq[3] == 3
    assert freq[1] == 1
    assert freq[9] == 0


def test_hot_numbers_ordering():
    hot = hot_numbers(DRAWS, top=2)
    assert hot[0] == (3, 3)
    assert hot[1][1] == 2  # 2 or 4, both appear twice


def test_cold_numbers_include_never_drawn():
    cold = cold_numbers(DRAWS, pool=6, bottom=3)
    numbers = [n for n, _ in cold]
    assert 6 in numbers  # never drawn
    assert cold[0][1] == 0


def test_windowed_frequencies():
    windows = windowed_frequencies(DRAWS, window=2)
    assert len(windows) == 2
    assert windows[0][3] == 2  # number 3 appears in both first draws


def test_windowed_invalid_window():
    with pytest.raises(ValueError):
        windowed_frequencies(DRAWS, window=0)


def test_gap_analysis():
    gaps = gap_analysis(DRAWS, pool=6)
    assert gaps[5] == 0  # in the most recent draw
    assert gaps[2] == 1  # last seen one draw ago
    assert gaps[1] == 2
    assert gaps[6] == 3  # never drawn => len(draws)
