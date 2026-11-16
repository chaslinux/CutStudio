
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtWidgets import QApplication, QGraphicsScene

from cutstudio.core.document import Document
from cutstudio.core.layer import Layer
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


def test_duplicate_single_object(setup_renderer):

    document, scene, renderer = setup_renderer

    original = VectorObject(
        ObjectType.RECTANGLE,
        x=10.0,
        y=20.0,
        width=50.0,
        height=40.0,
    )

    layer = document.active_layer

    renderer.add_object(original, layer)

    duplicates = renderer.duplicate_objects(
        [original.object_id]
    )

    assert len(duplicates) == 1

    duplicate = duplicates[0]

    assert duplicate.object_id != original.object_id
    assert duplicate.x == pytest.approx(15.0)
    assert duplicate.y == pytest.approx(25.0)

    assert layer.find_object(duplicate.object_id) is duplicate
    assert duplicate.object_id in renderer.items
    assert len(scene.items()) == 2


def test_duplicate_multiple_objects(setup_renderer):

    document, scene, renderer = setup_renderer

    layer = document.active_layer

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)

    renderer.add_object(first, layer)
    renderer.add_object(second, layer)

    duplicates = renderer.duplicate_objects(
        [first.object_id, second.object_id]
    )

    assert len(duplicates) == 2

    assert duplicates[0].object_type == ObjectType.RECTANGLE
    assert duplicates[1].object_type == ObjectType.ELLIPSE

    assert len(layer.objects) == 4
    assert len(scene.items()) == 4

    assert duplicates[0].object_id != first.object_id
    assert duplicates[1].object_id != second.object_id


def test_duplicate_objects_on_original_layers(setup_renderer):

    document, scene, renderer = setup_renderer

    first_layer = document.active_layer
    second_layer = Layer("Layer 2")

    document.add_layer(second_layer)

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)

    renderer.add_object(first, first_layer)
    renderer.add_object(second, second_layer)

    duplicates = renderer.duplicate_objects(
        [first.object_id, second.object_id]
    )

    assert len(duplicates) == 2

    assert first_layer.find_object(
        duplicates[0].object_id
    ) is duplicates[0]

    assert second_layer.find_object(
        duplicates[1].object_id
    ) is duplicates[1]


def test_duplicate_rejects_locked_layer_selection(setup_renderer):

    document, scene, renderer = setup_renderer

    unlocked_layer = document.active_layer
    locked_layer = Layer("Locked Layer")

    document.add_layer(locked_layer)

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)

    # Add both objects while their layers are unlocked.
    renderer.add_object(first, unlocked_layer)
    renderer.add_object(second, locked_layer)

    # Lock the second layer after adding its object.
    renderer.set_layer_locked(
        locked_layer.layer_id,
        True
    )

    original_count = len(scene.items())

    with pytest.raises(RuntimeError):
        renderer.duplicate_objects(
            [first.object_id, second.object_id]
        )

    # The operation must not partially duplicate the selection.
    assert len(unlocked_layer.objects) == 1
    assert len(locked_layer.objects) == 1
    assert len(scene.items()) == original_count


def test_duplicate_preserves_hidden_layer_visibility(setup_renderer):

    document, scene, renderer = setup_renderer

    layer = document.active_layer

    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, layer)

    renderer.set_layer_visibility(
        layer.layer_id,
        False
    )

    duplicates = renderer.duplicate_objects(
        [obj.object_id]
    )

    duplicate = duplicates[0]

    assert duplicate.object_id in renderer.items
    assert not renderer.items[duplicate.object_id].isVisible()


def test_duplicate_empty_selection(setup_renderer):

    document, scene, renderer = setup_renderer

    duplicates = renderer.duplicate_objects([])

    assert duplicates == []
    assert len(document.active_layer.objects) == 0
    assert len(scene.items()) == 0


def test_delete_single_object(setup_renderer):

    document, scene, renderer = setup_renderer

    layer = document.active_layer
    obj = VectorObject(ObjectType.RECTANGLE)

    renderer.add_object(obj, layer)

    deleted = renderer.delete_objects([obj.object_id])

    assert deleted == 1
    assert layer.find_object(obj.object_id) is None
    assert obj.object_id not in renderer.items
    assert len(scene.items()) == 0


def test_delete_multiple_objects(setup_renderer):

    document, scene, renderer = setup_renderer

    layer = document.active_layer

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)
    third = VectorObject(ObjectType.TEXT)

    for obj in (first, second, third):
        renderer.add_object(obj, layer)

    deleted = renderer.delete_objects([
        first.object_id,
        second.object_id
    ])

    assert deleted == 2
    assert len(layer.objects) == 1
    assert layer.objects[0] is third
    assert len(scene.items()) == 1


def test_delete_objects_across_layers(setup_renderer):

    document, scene, renderer = setup_renderer

    first_layer = document.active_layer
    second_layer = Layer("Layer 2")

    document.add_layer(second_layer)

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)

    renderer.add_object(first, first_layer)
    renderer.add_object(second, second_layer)

    deleted = renderer.delete_objects([
        first.object_id,
        second.object_id
    ])

    assert deleted == 2
    assert len(first_layer.objects) == 0
    assert len(second_layer.objects) == 0
    assert len(scene.items()) == 0


def test_delete_rejects_locked_layer_selection(setup_renderer):

    document, scene, renderer = setup_renderer

    unlocked_layer = document.active_layer
    locked_layer = Layer("Locked Layer")

    document.add_layer(locked_layer)

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.ELLIPSE)

    renderer.add_object(first, unlocked_layer)
    renderer.add_object(second, locked_layer)

    renderer.set_layer_locked(
        locked_layer.layer_id,
        True
    )

    original_count = len(scene.items())

    with pytest.raises(RuntimeError):
        renderer.delete_objects([
            first.object_id,
            second.object_id
        ])

    # Neither object should have been deleted.
    assert unlocked_layer.find_object(first.object_id) is first
    assert locked_layer.find_object(second.object_id) is second

    assert len(scene.items()) == original_count

    assert first.object_id in renderer.items
    assert second.object_id in renderer.items


def test_delete_empty_selection(setup_renderer):

    document, scene, renderer = setup_renderer

    deleted = renderer.delete_objects([])

    assert deleted == 0
    assert len(document.active_layer.objects) == 0
    assert len(scene.items()) == 0

