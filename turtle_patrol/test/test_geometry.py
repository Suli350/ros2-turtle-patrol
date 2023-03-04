import math

import pytest

from turtle_patrol.geometry import distance, normalize_angle, pairs


def test_normalize_angle_wraps():
    assert normalize_angle(0.0) == pytest.approx(0.0)
    assert normalize_angle(2 * math.pi + 0.5) == pytest.approx(0.5)
    assert normalize_angle(-2 * math.pi - 0.5) == pytest.approx(-0.5)
    assert -math.pi <= normalize_angle(3 * math.pi) < math.pi


def test_distance():
    assert distance(0, 0, 3, 4) == pytest.approx(5.0)


def test_pairs():
    assert pairs([1.0, 2.0, 3.0, 4.0]) == [(1.0, 2.0), (3.0, 4.0)]
    with pytest.raises(ValueError):
        pairs([1.0, 2.0, 3.0])
