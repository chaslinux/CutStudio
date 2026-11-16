import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtWidgets import QApplication

from cutstudio.core.objects import ObjectType, VectorObject
from cutstudio.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def main_window(qt_app):
    window = MainWindow()
    yield window

    # Prevent the unsaved-changes dialog during test cleanup.
    window.document_modified = False

    window.close()
    window.deleteLater()

    qt_app.processEvents()

def add_rectangle(window, x=10.0, y=10.0):
    obj = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=x,
        y=y,
        width=50.0,
        height=40.0,
    )

    window.renderer.add_object(
        obj,
        window.document.active_layer
    )

    window.record_history()

    return obj


def test_duplicate_multiple_selected_objects(main_window):

    first = add_rectangle(main_window, 10, 20)
    second = add_rectangle(main_window, 80, 90)

    main_window.scene.clearSelection()

    main_window.renderer.items[first.object_id].setSelected(True)
    main_window.renderer.items[second.object_id].setSelected(True)

    main_window.duplicate_selected_objects()

    assert len(main_window.document.active_layer.objects) == 4

    duplicates = [
        obj for obj in main_window.document.active_layer.objects
        if obj.object_id not in (first.object_id, second.object_id)
    ]

    assert len(duplicates) == 2

    assert duplicates[0].x == pytest.approx(15.0)
    assert duplicates[0].y == pytest.approx(25.0)

    assert duplicates[1].x == pytest.approx(85.0)
    assert duplicates[1].y == pytest.approx(95.0)


def test_duplicate_multiple_objects_undo_redo(main_window):

    first = add_rectangle(main_window)
    second = add_rectangle(main_window, 80, 80)

    main_window.scene.clearSelection()

    main_window.renderer.items[first.object_id].setSelected(True)
    main_window.renderer.items[second.object_id].setSelected(True)

    main_window.duplicate_selected_objects()

    assert len(main_window.document.active_layer.objects) == 4

    main_window.undo()

    assert len(main_window.document.active_layer.objects) == 2

    main_window.redo()

    assert len(main_window.document.active_layer.objects) == 4


def test_delete_multiple_objects_undo(main_window):

    first = add_rectangle(main_window)
    second = add_rectangle(main_window, 80, 80)

    main_window.scene.clearSelection()

    main_window.renderer.items[first.object_id].setSelected(True)
    main_window.renderer.items[second.object_id].setSelected(True)

    main_window.delete_selected_objects()

    assert len(main_window.document.active_layer.objects) == 0

    main_window.undo()

    assert len(main_window.document.active_layer.objects) == 2
