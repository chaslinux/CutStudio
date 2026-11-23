
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtWidgets import QApplication

from cutstudio.ui.grid_settings_dialog import GridSettingsDialog


@pytest.fixture(scope="module")
def qt_app():
    app = QApplication.instance() or QApplication([])
    return app


def test_default_grid_settings(qt_app):

    dialog = GridSettingsDialog()

    spacing, interval = dialog.get_settings()

    assert spacing == pytest.approx(6.35)
    assert interval == 4


def test_major_interval_options(qt_app):

    dialog = GridSettingsDialog()

    options = [
        dialog.major_interval_combo.itemData(i)
        for i in range(dialog.major_interval_combo.count())
    ]

    assert options == [2, 4, 5, 10]


def test_inches_are_converted_to_millimetres(qt_app):

    dialog = GridSettingsDialog()

    dialog.units_combo.setCurrentText("Inches")
    dialog.spacing_input.setValue(0.25)

    spacing, _ = dialog.get_settings()

    assert spacing == pytest.approx(6.35)


def test_millimetre_spacing(qt_app):

    dialog = GridSettingsDialog()

    dialog.spacing_input.setValue(5.0)

    spacing, _ = dialog.get_settings()

    assert spacing == pytest.approx(5.0)


def test_custom_major_interval(qt_app):

    dialog = GridSettingsDialog()

    dialog.major_interval_combo.setCurrentIndex(
        dialog.major_interval_combo.findData(5)
    )

    _, interval = dialog.get_settings()

    assert interval == 5


@pytest.mark.parametrize(
    "spacing",
    [0, -1, float("inf"), float("nan")]
)
def test_invalid_initial_spacing_is_rejected(qt_app, spacing):

    with pytest.raises(ValueError):
        GridSettingsDialog(spacing_mm=spacing)


def test_invalid_major_interval_is_rejected(qt_app):

    with pytest.raises(ValueError):
        GridSettingsDialog(major_interval=3)

