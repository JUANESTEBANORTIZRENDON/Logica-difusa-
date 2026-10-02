import numpy as np
import pytest

from model.config import VARIABLES
from model.membership import membership


def test_left_and_right_shoulders_are_preserved():
    assert membership(0, "trap", (0, 0, 50, 70)) == 1
    assert membership(50, "trap", (0, 0, 50, 70)) == 1
    assert membership(70, "trap", (0, 0, 50, 70)) == 0
    assert membership(80, "trap", (60, 80, 120, 120)) == 1
    assert membership(120, "trap", (60, 80, 120, 120)) == 1


def test_triangle_peak_edges_and_linear_segments():
    points = (50, 75, 100)
    assert membership(50, "tri", points) == 0
    assert membership(62.5, "tri", points) == pytest.approx(0.5)
    assert membership(75, "tri", points) == 1
    assert membership(87.5, "tri", points) == pytest.approx(0.5)
    assert membership(100, "tri", points) == 0


@pytest.mark.parametrize("variable", ["peso", "edad", "salida"])
def test_sets_cover_complete_domain(variable):
    definition = VARIABLES[variable]
    x = np.linspace(*definition["range"], 2001)
    curves = [membership(x, kind, points) for kind, points in definition["sets"].values()]
    assert np.all(np.maximum.reduce(curves) > 0)


def test_overlap_at_90_kg():
    sets = VARIABLES["peso"]["sets"]
    assert membership(90, *sets["intermedio"]) == pytest.approx(0.4)
    assert membership(90, *sets["elevado"]) == pytest.approx(1 / 3)
