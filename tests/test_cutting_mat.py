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

    bounds = canvas._item_geometric_scene_bounds(first).united(
        canvas._item_geometric_scene_bounds(second)
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


# ------------------------------------------------------------
# Locked-layer resize protection
# ------------------------------------------------------------

def test_locked_layer_objects_cannot_be_resized(
    canvas, monkeypatch
):
    from types import SimpleNamespace
    from PySide6.QtCore import QPointF

    scene = canvas.scene()

    item = scene.addRect(0, 0, 100, 100)

    item.setFlag(
        item.GraphicsItemFlag.ItemIsSelectable,
        True
    )

    item.setData(0x100, "locked-object")
    item.setSelected(True)

    assert item in scene.selectedItems()

    original_rect = item.rect()

    locked_layer = SimpleNamespace(locked=True)
    obj = SimpleNamespace(object_id="locked-object")

    canvas.renderer = SimpleNamespace(
        OBJECT_ID_ROLE=0x100,
        find_object_and_layer=lambda object_id: (
            obj, locked_layer
        ),
        sync_to_document=lambda: None,
    )

    monkeypatch.setattr(
        canvas,
        "_handle_at",
        lambda position: "se"
    )

    class FakeEvent:

        def button(self):
            return Qt.MouseButton.LeftButton

        def position(self):
            return QPointF(10, 10)

        def accept(self):
            self.accepted = True

    event = FakeEvent()
    event.accepted = False

    canvas.mousePressEvent(event)

    assert event.accepted
    assert item.rect() == original_rect


# ------------------------------------------------------------
# Mixed locked/unlocked group snapping regression
# ------------------------------------------------------------

def test_group_snapping_does_not_move_locked_objects(canvas):

    from types import SimpleNamespace

    scene = canvas.scene()

    first = scene.addRect(0, 0, 10, 10)
    second = scene.addRect(0, 0, 10, 10)
    locked = scene.addRect(0, 0, 10, 10)

    role = 0x100

    objects = {
        "first": (
            SimpleNamespace(object_id="first"),
            SimpleNamespace(locked=False),
        ),
        "second": (
            SimpleNamespace(object_id="second"),
            SimpleNamespace(locked=False),
        ),
        "locked": (
            SimpleNamespace(object_id="locked"),
            SimpleNamespace(locked=True),
        ),
    }

    for item, object_id, position in (
        (first, "first", (26, 30)),
        (second, "second", (50, 45)),
        (locked, "locked", (100, 100)),
    ):
        item.setData(role, object_id)
        item.setFlag(item.GraphicsItemFlag.ItemIsSelectable)
        item.setPos(*position)
        item.setSelected(True)

    original_difference = second.pos() - first.pos()
    locked_position = locked.pos()

    canvas.renderer = SimpleNamespace(
        OBJECT_ID_ROLE=role,
        find_object_and_layer=lambda object_id: objects.get(
            object_id, (None, None)
        ),
    )

    canvas.set_grid_spacing_inches(0.25)
    canvas.set_snap_to_grid(True)

    canvas._snap_selected_group()

    assert locked.pos() == locked_position

    assert first.pos().x() == pytest.approx(24.0)
    assert first.pos().y() == pytest.approx(24.0)

    new_difference = second.pos() - first.pos()

    assert new_difference.x() == pytest.approx(
        original_difference.x()
    )
    assert new_difference.y() == pytest.approx(
        original_difference.y()
    )


def test_snapping_ignores_stroke_width(canvas):

    from PySide6.QtGui import QPen

    scene = canvas.scene()

    item = scene.addRect(0, 0, 20, 20)
    pen = QPen()
    pen.setWidthF(20.0)
    item.setPen(pen)
    item.setFlag(item.GraphicsItemFlag.ItemIsSelectable)
    item.setPos(26.0, 30.0)
    item.setSelected(True)

    canvas.set_grid_spacing_inches(0.25)
    canvas.set_snap_to_grid(True)

    canvas._snap_selected_group()

    assert item.pos().x() == pytest.approx(24.0)
    assert item.pos().y() == pytest.approx(24.0)


def test_snapping_rotated_object_uses_geometric_bounds(canvas):

    from PySide6.QtGui import QPen

    scene = canvas.scene()

    # 20x10 rect rotated 90 degrees around its center (10, 5):
    # rotated local bounds occupy [5, 15] x [-5, 15].
    # At pos (26, 30), geometric scene bounds are [31, 41] x.
    item = scene.addRect(0, 0, 20, 10)
    pen = QPen()
    pen.setWidthF(12.0)
    item.setPen(pen)
    item.setTransformOriginPoint(item.rect().center())
    item.setRotation(90.0)
    item.setFlag(item.GraphicsItemFlag.ItemIsSelectable)
    item.setPos(26.0, 30.0)
    item.setSelected(True)

    canvas.set_grid_spacing_inches(0.25)
    canvas.set_snap_to_grid(True)

    canvas._snap_selected_group()

    bounds = canvas._item_geometric_scene_bounds(item)
    assert bounds.left() == pytest.approx(24.0)
    assert bounds.top() == pytest.approx(24.0)
    assert item.pos().x() == pytest.approx(19.0)
    assert item.pos().y() == pytest.approx(29.0)
