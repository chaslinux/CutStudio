
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtWidgets import QApplication, QGraphicsScene

from cutstudio.core.document import Document
from cutstudio.core.objects import ObjectType, VectorObject
from cutstudio.ui.canvas.renderer import CanvasRenderer


@pytest.fixture(scope="session")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def setup_renderer(qt_app):

    document = Document()
    scene = QGraphicsScene()

    renderer = CanvasRenderer(document, scene)

    return document, scene, renderer


def test_add_object_to_document_and_canvas(setup_renderer):

    document, scene, renderer = setup_renderer

    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, document.active_layer)

    assert len(document.active_layer.objects) == 1
    assert obj.object_id in renderer.items
    assert len(scene.items()) == 1


def test_layer_visibility(setup_renderer):

    document, scene, renderer = setup_renderer

    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, document.active_layer)

    renderer.set_layer_visibility(
        document.active_layer_id,
        False
    )

    assert not renderer.items[obj.object_id].isVisible()


def test_layer_locking(setup_renderer):

    document, scene, renderer = setup_renderer

    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, document.active_layer)

    renderer.set_layer_locked(
        document.active_layer_id,
        True
    )

    assert document.active_layer.locked

    with pytest.raises(RuntimeError):
        renderer.add_object(
            VectorObject(ObjectType.ELLIPSE),
            document.active_layer
        )


def test_position_synchronization(setup_renderer):

    document, scene, renderer = setup_renderer

    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, document.active_layer)

    item = renderer.items[obj.object_id]

    item.setPos(96, 48)

    renderer.sync_to_document()

    assert obj.x == pytest.approx(25.4)
    assert obj.y == pytest.approx(12.7)

