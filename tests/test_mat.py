import pytest

from cutstudio.core.mat import CuttingMatConfig


def test_default_cutting_mat():

    mat = CuttingMatConfig()

    assert mat.width_mm == 304.8
    assert mat.height_mm == 304.8


def test_custom_cutting_mat():

    mat = CuttingMatConfig(
        width_mm=330.2,
        height_mm=482.6
    )

    assert mat.width_mm == 330.2
    assert mat.height_mm == 482.6


def test_cutting_mat_dimensions_must_be_positive():

    with pytest.raises(ValueError):
        CuttingMatConfig(width_mm=0)

    with pytest.raises(ValueError):
        CuttingMatConfig(height_mm=-10)


@pytest.mark.parametrize(
    "width,height",
    [
        (float("inf"), 304.8),
        (304.8, float("inf")),
        (float("nan"), 304.8),
        (304.8, float("nan")),
    ]
)
def test_cutting_mat_dimensions_must_be_finite(width, height):

    with pytest.raises(ValueError):
        CuttingMatConfig(
            width_mm=width,
            height_mm=height
        )


def test_cutting_mat_configuration_is_immutable():

    mat = CuttingMatConfig()

    with pytest.raises(AttributeError):
        mat.width_mm = 400


def test_cutting_mat_rejects_non_numeric_dimensions():

    with pytest.raises(ValueError):
        CuttingMatConfig(width_mm="300")
