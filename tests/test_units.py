
import pytest

from cutstudio.core.units import (
    mm_to_inches,
    inches_to_mm,
    mm_to_scene_units,
    scene_units_to_mm,
)


def test_inches_to_mm():
    assert inches_to_mm(12) == pytest.approx(304.8)


def test_mm_to_inches():
    assert mm_to_inches(304.8) == pytest.approx(12)


def test_mm_to_scene_units():
    assert mm_to_scene_units(25.4) == pytest.approx(96)


def test_scene_units_to_mm():
    assert scene_units_to_mm(96) == pytest.approx(25.4)

