import math

import pytest

from keno_stats import (
    at_least,
    expected_hits,
    hit_distribution,
    hit_probability,
    odds_one_in,
    score_result,
)


class TestHitProbability:
    def test_distribution_sums_to_one(self):
        dist = hit_distribution(pool=80, drawn=20, picks=10)
        assert math.isclose(sum(dist.values()), 1.0, rel_tol=1e-12)

    def test_czech_keno_distribution_sums_to_one(self):
        dist = hit_distribution(pool=66, drawn=12, picks=8)
        assert math.isclose(sum(dist.values()), 1.0, rel_tol=1e-12)

    def test_known_value_10_of_10_greek_kino(self):
        # P(10/10) in a 20/80 keno: C(20,10)/C(80,10) ≈ 1.12e-7 (1 in ~8.9M)
        p = hit_probability(pool=80, drawn=20, picks=10, hits=10)
        assert math.isclose(p, math.comb(20, 10) / math.comb(80, 10), rel_tol=1e-12)
        assert 8_000_000 < odds_one_in(p) < 9_000_000

    def test_impossible_hits_return_zero(self):
        assert hit_probability(pool=80, drawn=20, picks=5, hits=6) == 0.0
        # 70 picks in 20/80: at least 10 must hit, so 5 hits is impossible
        assert hit_probability(pool=80, drawn=20, picks=70, hits=5) == 0.0

    def test_invalid_config_raises(self):
        with pytest.raises(ValueError):
            hit_probability(pool=0, drawn=20, picks=5, hits=2)
        with pytest.raises(ValueError):
            hit_probability(pool=80, drawn=81, picks=5, hits=2)

    def test_expected_hits(self):
        # 10 picks in 20/80 => expect 10 * 20/80 = 2.5 hits
        assert expected_hits(pool=80, drawn=20, picks=10) == pytest.approx(2.5)

    def test_at_least_matches_manual_sum(self):
        dist = hit_distribution(pool=80, drawn=20, picks=6)
        manual = sum(p for k, p in dist.items() if k >= 4)
        assert at_least(pool=80, drawn=20, picks=6, hits=4) == pytest.approx(manual)


class TestScoring:
    def test_rarer_outcome_scores_higher(self):
        common = score_result(pool=80, drawn=20, picks=10, hits=2)
        rare = score_result(pool=80, drawn=20, picks=10, hits=8)
        assert rare.score > common.score

    def test_jackpot_outcome_gets_top_tier(self):
        result = score_result(pool=80, drawn=20, picks=10, hits=10)
        assert result.tier == "COSMIC"

    def test_typical_outcome_is_common(self):
        # 2 hits on 10 picks is near the expectation => common
        result = score_result(pool=80, drawn=20, picks=10, hits=2)
        assert result.tier == "COMMON"

    def test_impossible_outcome_raises(self):
        with pytest.raises(ValueError):
            score_result(pool=80, drawn=20, picks=5, hits=6)
