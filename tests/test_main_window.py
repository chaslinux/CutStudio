import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from PySide6.QtWidgets import QApplication, QDialog

from cutstudio.core.mat import CuttingMatConfig
from cutstudio.core.units import mm_to_scene_units

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


def test_undo_redo_restores_layer_visibility_in_graphics(main_window):

    obj = add_rectangle(main_window)

    layer = main_window.document.active_layer
    item = main_window.renderer.items[obj.object_id]

    main_window.renderer.set_layer_visibility(
        layer.layer_id,
        False
    )

    main_window.record_history()

    assert not item.isVisible()

    main_window.undo()

    restored_item = main_window.renderer.items[obj.object_id]

    assert main_window.document.active_layer.visible is True
    assert restored_item.isVisible()

    main_window.redo()

    restored_item = main_window.renderer.items[obj.object_id]

    assert main_window.document.active_layer.visible is False
    assert not restored_item.isVisible()


def test_undo_redo_restores_layer_locking_in_graphics(main_window):

    obj = add_rectangle(main_window)

    layer = main_window.document.active_layer

    main_window.renderer.set_layer_locked(
        layer.layer_id,
        True
    )

    main_window.record_history()

    item = main_window.renderer.items[obj.object_id]

    assert not (
        item.flags()
        & item.GraphicsItemFlag.ItemIsMovable
    )

    main_window.undo()

    restored_item = main_window.renderer.items[obj.object_id]

    assert main_window.document.active_layer.locked is False

    assert (
        restored_item.flags()
        & restored_item.GraphicsItemFlag.ItemIsMovable
    )

    main_window.redo()

    restored_item = main_window.renderer.items[obj.object_id]

    assert main_window.document.active_layer.locked is True

    assert not (
        restored_item.flags()
        & restored_item.GraphicsItemFlag.ItemIsMovable
    )


def test_undo_redo_preserves_object_ids(main_window):

    first = add_rectangle(main_window)
    second = add_rectangle(main_window, 80, 80)

    original_ids = {
        first.object_id,
        second.object_id
    }

    main_window.undo()

    main_window.redo()

    restored_ids = {
        obj.object_id
        for obj in main_window.document.active_layer.objects
    }

    assert restored_ids == original_ids

    assert set(main_window.renderer.items.keys()) >= original_ids


def test_undo_restores_selection_after_object_deletion(main_window):

    obj = add_rectangle(main_window)

    select_objects(main_window, obj)

    main_window.delete_selected_objects()

    assert len(main_window.document.active_layer.objects) == 0

    main_window.undo()

    restored_item = main_window.renderer.items[obj.object_id]

    assert restored_item.isSelected()

# ============================================================
# CLIPBOARD TESTS
# ============================================================

def select_objects(window, *objects):

    window.scene.clearSelection()

    for obj in objects:
        window.renderer.items[obj.object_id].setSelected(True)


def test_copy_multiple_selected_objects(main_window):

    first = add_rectangle(main_window, 10, 20)
    second = add_rectangle(main_window, 80, 90)

    select_objects(main_window, first, second)

    main_window.copy_selected_objects()

    assert len(main_window.clipboard_objects) == 2
    assert len(main_window.document.active_layer.objects) == 2


def test_copy_does_not_modify_original_objects(main_window):

    original = add_rectangle(main_window, 10, 20)

    select_objects(main_window, original)

    main_window.copy_selected_objects()

    assert main_window.clipboard_objects[0] is not original
    assert main_window.clipboard_objects[0].object_id == original.object_id

    assert original.x == pytest.approx(10)
    assert original.y == pytest.approx(20)


def test_paste_creates_new_objects(main_window):

    original = add_rectangle(main_window, 10, 20)

    select_objects(main_window, original)

    main_window.copy_selected_objects()
    main_window.paste_objects()

    objects = main_window.document.active_layer.objects

    assert len(objects) == 2

    pasted = objects[-1]

    assert pasted.object_id != original.object_id
    assert pasted.x == pytest.approx(15)
    assert pasted.y == pytest.approx(25)


def test_paste_multiple_objects(main_window):

    first = add_rectangle(main_window, 10, 20)
    second = add_rectangle(main_window, 80, 90)

    select_objects(main_window, first, second)

    main_window.copy_selected_objects()
    main_window.paste_objects()

    objects = main_window.document.active_layer.objects

    assert len(objects) == 4

    pasted = objects[2:]

    assert len(pasted) == 2

    assert pasted[0].object_id != first.object_id
    assert pasted[1].object_id != second.object_id


def test_repeated_paste_creates_unique_objects(main_window):

    original = add_rectangle(main_window)

    select_objects(main_window, original)

    main_window.copy_selected_objects()

    main_window.paste_objects()
    main_window.paste_objects()

    objects = main_window.document.active_layer.objects

    assert len(objects) == 3

    object_ids = [obj.object_id for obj in objects]

    assert len(set(object_ids)) == 3


def test_paste_supports_undo_redo(main_window):

    original = add_rectangle(main_window)

    select_objects(main_window, original)

    main_window.copy_selected_objects()
    main_window.paste_objects()

    assert len(main_window.document.active_layer.objects) == 2

    main_window.undo()

    assert len(main_window.document.active_layer.objects) == 1

    main_window.redo()

    assert len(main_window.document.active_layer.objects) == 2


def test_cut_removes_selected_objects(main_window):

    first = add_rectangle(main_window)
    second = add_rectangle(main_window, 80, 80)

    select_objects(main_window, first, second)

    main_window.cut_selected_objects()

    assert len(main_window.clipboard_objects) == 2
    assert len(main_window.document.active_layer.objects) == 0


def test_cut_supports_undo(main_window):

    first = add_rectangle(main_window)
    second = add_rectangle(main_window, 80, 80)

    select_objects(main_window, first, second)

    main_window.cut_selected_objects()

    assert len(main_window.document.active_layer.objects) == 0

    main_window.undo()

    assert len(main_window.document.active_layer.objects) == 2


def test_cut_then_paste(main_window):

    original = add_rectangle(main_window)

    select_objects(main_window, original)

    main_window.cut_selected_objects()

    assert len(main_window.document.active_layer.objects) == 0

    main_window.paste_objects()

    objects = main_window.document.active_layer.objects

    assert len(objects) == 1
    assert objects[0].object_id != original.object_id


def test_paste_rejects_locked_layer(main_window):

    original = add_rectangle(main_window)

    select_objects(main_window, original)

    main_window.copy_selected_objects()

    layer = main_window.document.active_layer

    main_window.renderer.set_layer_locked(
        layer.layer_id,
        True
    )

    main_window.paste_objects()

    assert len(layer.objects) == 1


# ============================================================
# CUTTING MAT TESTS
# ============================================================

def test_default_cutting_mat_on_startup(main_window):

    assert main_window.mat_config == CuttingMatConfig()

    rect = main_window.scene.sceneRect()

    assert rect.width() == pytest.approx(
        mm_to_scene_units(304.8)
    )

    assert rect.height() == pytest.approx(
        mm_to_scene_units(304.8)
    )


def test_custom_mat_updates_scene_rectangle(main_window):

    main_window.mat_config = CuttingMatConfig(
        width_mm=304.8,
        height_mm=609.6
    )

    main_window._update_mat_scene_rect()

    rect = main_window.scene.sceneRect()

    assert rect.width() == pytest.approx(
        mm_to_scene_units(304.8)
    )

    assert rect.height() == pytest.approx(
        mm_to_scene_units(609.6)
    )


def test_accepting_mat_settings_marks_project_modified(
    main_window,
    monkeypatch
):

    custom_mat = CuttingMatConfig(
        width_mm=304.8,
        height_mm=609.6
    )

    class FakeDialog:

        DialogCode = QDialog.DialogCode

        def __init__(self, config, parent):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

        def get_mat_config(self):
            return custom_mat

    monkeypatch.setattr(
        "cutstudio.ui.main_window.MatSettingsDialog",
        FakeDialog
    )

    main_window.document_modified = False

    main_window.show_mat_settings()

    assert main_window.mat_config == custom_mat
    assert main_window.document_modified is True


def test_cancelling_mat_settings_changes_nothing(
    main_window,
    monkeypatch
):

    original_mat = main_window.mat_config

    class FakeDialog:

        DialogCode = QDialog.DialogCode

        def __init__(self, config, parent):
            pass

        def exec(self):
            return QDialog.DialogCode.Rejected

    monkeypatch.setattr(
        "cutstudio.ui.main_window.MatSettingsDialog",
        FakeDialog
    )

    main_window.document_modified = False

    main_window.show_mat_settings()

    assert main_window.mat_config == original_mat
    assert main_window.document_modified is False



# ============================================================
# PERMANENT MAT STATUS TESTS
# ============================================================

def test_mat_status_label_shows_initial_dimensions(main_window):

    assert main_window.mat_status_label.text() == (
        "12 x 12 inch mat | Ctrl + mouse wheel to zoom"
    )


def test_temporary_status_message_preserves_mat_dimensions(
    main_window
):

    original_text = main_window.mat_status_label.text()

    main_window.statusBar().showMessage(
        "Document restored"
    )

    assert main_window.mat_status_label.text() == original_text


def test_mat_status_updates_after_changing_preset(
    main_window,
    monkeypatch
):

    custom_mat = CuttingMatConfig(
        width_mm=304.8,
        height_mm=609.6
    )

    class FakeDialog:

        DialogCode = QDialog.DialogCode

        def __init__(self, config, parent):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

        def get_mat_config(self):
            return custom_mat

    monkeypatch.setattr(
        "cutstudio.ui.main_window.MatSettingsDialog",
        FakeDialog
    )

    main_window.show_mat_settings()

    assert main_window.mat_status_label.text() == (
        "12 x 24 inch mat | Ctrl + mouse wheel to zoom"
    )


def test_accepting_unchanged_mat_preserves_status(
    main_window,
    monkeypatch
):

    original_mat = main_window.mat_config
    original_status = main_window.mat_status_label.text()

    class FakeDialog:

        DialogCode = QDialog.DialogCode

        def __init__(self, config, parent):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

        def get_mat_config(self):
            return original_mat

    monkeypatch.setattr(
        "cutstudio.ui.main_window.MatSettingsDialog",
        FakeDialog
    )

    main_window.document_modified = False

    main_window.show_mat_settings()

    assert main_window.mat_config == original_mat
    assert main_window.mat_status_label.text() == original_status
    assert main_window.document_modified is False
