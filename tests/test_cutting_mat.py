import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QGraphicsScene

from cutstudio.ui.canvas.cutting_mat import CuttingMat
from cutstudio.ui.canvas.rulers import (
    RulerWidget,
    RULER_SIZE,
)


@pytest.fixture(scope="session")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def canvas(qt_app):

    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 960, 960)

    widget = CuttingMat(scene)
    widget.resize(800, 600)
    widget.show()

    qt_app.processEvents()

    yield widget

    widget.close()
    widget.deleteLater()
    qt_app.processEvents()


def test_canvas_creates_horizontal_and_vertical_rulers(canvas):

    assert isinstance(canvas.horizontal_ruler, RulerWidget)
    assert isinstance(canvas.vertical_ruler, RulerWidget)


def test_ruler_orientation(canvas):

    assert canvas.horizontal_ruler.orientation == "horizontal"
    assert canvas.vertical_ruler.orientation == "vertical"


def test_ruler_size(canvas):

    assert RULER_SIZE == 28

    assert canvas.horizontal_ruler.height() == RULER_SIZE
    assert canvas.vertical_ruler.width() == RULER_SIZE


def test_ruler_widgets_are_visible(canvas):

    assert canvas.horizontal_ruler.isVisible()
    assert canvas.vertical_ruler.isVisible()
    assert canvas.ruler_corner.isVisible()


def test_zoom_in_increases_scale(canvas):

    original_scale = canvas.transform().m11()

    canvas.zoom_in()

    assert canvas.transform().m11() > original_scale


def test_zoom_out_decreases_scale(canvas):

    original_scale = canvas.transform().m11()

    canvas.zoom_out()

    assert canvas.transform().m11() < original_scale


def test_zoom_in_and_out_restore_scale(canvas):

    original_scale = canvas.transform().m11()

    canvas.zoom_in()
    canvas.zoom_out()

    assert canvas.transform().m11() == pytest.approx(
        original_scale
    )


def test_zoom_respects_maximum_scale(canvas):

    for _ in range(100):
        canvas.zoom_in()

    assert canvas.transform().m11() <= 5.0


def test_zoom_respects_minimum_scale(canvas):

    for _ in range(100):
        canvas.zoom_out()

    assert canvas.transform().m11() >= 0.1


def test_zoom_changed_signal(canvas):

    received = []

    canvas.zoom_changed.connect(received.append)

    canvas.zoom_in()

    assert len(received) == 1
    assert received[0] == pytest.approx(
        canvas.transform().m11() * 100
    )


def test_zoom_to_fit(canvas):

    canvas.zoom_to_fit()

    assert canvas.transform().m11() > 0

    assert canvas.transform().m11() == pytest.approx(
        canvas.transform().m22()
    )


def test_zoom_to_fit_emits_signal(canvas):

    received = []

    canvas.zoom_changed.connect(received.append)

    canvas.zoom_to_fit()

    assert len(received) == 1


def test_zoom_to_fit_handles_empty_scene(qt_app):

    scene = QGraphicsScene()
    canvas = CuttingMat(scene)

    original_scale = canvas.transform().m11()

    canvas.zoom_to_fit()

    assert canvas.transform().m11() == original_scale

    canvas.close()
    canvas.deleteLater()
    qt_app.processEvents()


def test_rulers_update_after_horizontal_scroll(canvas):

    canvas.horizontalScrollBar().setValue(
        canvas.horizontalScrollBar().maximum()
    )

    canvas._update_rulers()

    assert canvas.horizontal_ruler is not None


def test_rulers_update_after_vertical_scroll(canvas):

    canvas.verticalScrollBar().setValue(
        canvas.verticalScrollBar().maximum()
    )

    canvas._update_rulers()

    assert canvas.vertical_ruler is not None


def test_ruler_geometry_updates_after_resize(canvas):

    canvas.resize(1000, 700)

    QApplication.processEvents()

    viewport = canvas.viewport().geometry()

    assert canvas.horizontal_ruler.width() == viewport.width()
    assert canvas.vertical_ruler.height() == viewport.height()



def test_horizontal_ruler_uses_font_metrics(canvas):
    """Horizontal ruler labels use the font's actual ascent."""

    from PySide6.QtCore import QPointF

    class FakeMetrics:
        def ascent(self):
            return 14

    class FakePainter:
        def __init__(self):
            self.text_calls = []

        def fontMetrics(self):
            return FakeMetrics()

        def drawLine(self, *args):
            pass

        def drawText(self, *args):
            self.text_calls.append(args)

    painter = FakePainter()

    canvas.horizontal_ruler._draw_horizontal(painter)

    assert painter.text_calls

    for position, text in painter.text_calls:
        assert isinstance(position, QPointF)
        assert position.y() == pytest.approx(16)
        assert isinstance(text, str)


# ------------------------------------------------------------
# Grid spacing and snapping regression tests
# ------------------------------------------------------------

def test_grid_spacing_can_be_set_in_inches(canvas):

    canvas.set_grid_spacing_inches(0.25)

    assert canvas.grid_spacing == pytest.approx(24.0)


def test_grid_spacing_can_be_set_in_millimetres(canvas):

    canvas.set_grid_spacing_mm(6.35)

    assert canvas.grid_spacing == pytest.approx(24.0)


@pytest.mark.parametrize(
    "spacing",
    [0, -1, float("inf"), float("nan")]
)
def test_invalid_grid_spacing_is_rejected(canvas, spacing):

    with pytest.raises(ValueError):
        canvas.set_grid_spacing_mm(spacing)


@pytest.mark.parametrize("interval", [2, 4, 5, 10])
def test_valid_major_grid_intervals(canvas, interval):

    canvas.set_grid_major_interval(interval)

    assert canvas.grid_major_interval == interval


@pytest.mark.parametrize("interval", [0, 1, 3, 6, 20])
def test_invalid_major_grid_intervals_are_rejected(canvas, interval):

    with pytest.raises(ValueError):
        canvas.set_grid_major_interval(interval)


def test_group_snapping_preserves_relative_object_positions(canvas):

    scene = canvas.scene()

    first = scene.addRect(0, 0, 10, 10)
    second = scene.addRect(0, 0, 10, 10)

    first.setFlag(first.GraphicsItemFlag.ItemIsSelectable)
    second.setFlag(second.GraphicsItemFlag.ItemIsSelectable)

    first.setPos(26, 30)
    second.setPos(50, 45)

    first.setSelected(True)
    second.setSelected(True)

    original_difference = second.pos() - first.pos()

    canvas.set_grid_spacing_inches(0.25)
    canvas.set_snap_to_grid(True)

    canvas._snap_selected_group()

    new_difference = second.pos() - first.pos()

    assert new_difference.x() == pytest.approx(
        original_difference.x()
    )
    assert new_difference.y() == pytest.approx(
        original_difference.y()
    )

    bounds = first.sceneBoundingRect().united(
        second.sceneBoundingRect()
    )

    assert bounds.left() == pytest.approx(24.0)
    assert bounds.top() == pytest.approx(24.0)


def test_group_does_not_move_when_snapping_is_disabled(canvas):

    scene = canvas.scene()

    item = scene.addRect(0, 0, 10, 10)
    item.setFlag(item.GraphicsItemFlag.ItemIsSelectable)
    item.setPos(26, 30)
    item.setSelected(True)

    original_position = item.pos()

    canvas.set_snap_to_grid(False)
    canvas._snap_selected_group()

    assert item.pos() == original_position
