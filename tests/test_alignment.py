import pytest

from PySide6.QtWidgets import QApplication

from cutstudio.core.alignment import (
    align_objects,
    distribute_objects,
    object_geometric_bounds,
)
from cutstudio.core.objects import ObjectType, VectorObject
from cutstudio.ui.main_window import MainWindow

@pytest.fixture
def main_window():
    app = QApplication.instance() or QApplication([])
    window = MainWindow()

    yield window

    # Tests should not trigger the application's save confirmation.
    window.document_modified = False
    window.close()
    window.deleteLater()
    app.processEvents()

def _place_rect(window, x, y, width=20.0, height=10.0, rotation=0.0):
    obj = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=x,
        y=y,
        width=width,
        height=height,
        rotation=rotation,
    )
    window.renderer.add_object(obj, window.document.active_layer)
    return obj


def test_align_requires_at_least_two_objects():
    single = [VectorObject(ObjectType.RECTANGLE, x=10.0, y=20.0)]
    assert align_objects(single, "left") is False
    assert single[0].x == pytest.approx(10.0)


def test_align_horizontal_and_vertical_modes():
    a = VectorObject(ObjectType.RECTANGLE, x=10.0, y=15.0, width=20.0, height=20.0)
    b = VectorObject(ObjectType.RECTANGLE, x=50.0, y=55.0, width=40.0, height=40.0)

    assert align_objects([a, b], "left") is True
    assert a.x == pytest.approx(10.0) and b.x == pytest.approx(10.0)

    assert align_objects([a, b], "top") is True
    assert a.y == pytest.approx(15.0) and b.y == pytest.approx(15.0)


def test_align_right_bottom_centers_and_rotated():
    a = VectorObject(ObjectType.RECTANGLE, x=10.0, y=15.0, width=20.0, height=20.0)
    b = VectorObject(ObjectType.RECTANGLE, x=50.0, y=55.0, width=40.0, height=40.0)
    assert align_objects([a, b], "right") is True
    assert a.x == pytest.approx(70.0) and b.x == pytest.approx(50.0)

    assert align_objects([a, b], "bottom") is True
    assert a.y == pytest.approx(75.0) and b.y == pytest.approx(55.0)

    assert align_objects([a, b], "h_center") is True
    assert a.x + 10.0 == pytest.approx(70.0) and b.x + 20.0 == pytest.approx(70.0)

    assert align_objects([a, b], "v_center") is True
    assert a.y + 10.0 == pytest.approx(75.0) and b.y + 20.0 == pytest.approx(75.0)

    anchor = VectorObject(ObjectType.RECTANGLE, x=20.0, y=10.0, width=10.0, height=10.0)
    rotated = VectorObject(
        ObjectType.RECTANGLE, x=50.0, y=30.0, width=40.0, height=10.0, rotation=90.0
    )
    assert align_objects([anchor, rotated], "left") is True
    assert object_geometric_bounds(rotated).left == pytest.approx(20.0)


def test_distribute_and_main_window_integration(main_window):
    first = _place_rect(main_window, 0.0, 10.0, width=10.0, height=10.0)
    middle = _place_rect(main_window, 12.0, 25.0, width=10.0, height=10.0)
    last = _place_rect(main_window, 80.0, 50.0, width=10.0, height=10.0)
    main_window.record_history()

    for obj in (first, middle, last):
        main_window.renderer.items[obj.object_id].setSelected(True)

    main_window.distribute_selected_objects("horizontal")
    assert middle.x == pytest.approx(40.0)

    main_window.align_selected_objects("top")
    assert last.y == pytest.approx(10.0)

    print("\n--- BEFORE UNDO ---")
    print("History index:", main_window.history.undo_count)
    print("Can undo:", main_window.history.can_undo)

    for obj in (first, middle, last):
        current = main_window.renderer.find_object(obj.object_id)
        print(obj.object_id, "y =", current.y)

    print("\n--- HISTORY SNAPSHOTS ---")

    for index, state in enumerate(main_window.history._states):
        print(f"\nSnapshot {index}:")

        for layer in state.layers:
            for obj in layer.objects:
                print(
                    obj.object_id,
                    "x =", obj.x,
                    "y =", obj.y
                )

    print("Document positions:")
    for layer in main_window.document.layers:
        for obj in layer.objects:
            print(obj.x, obj.y)

    print("Graphics positions:")
    for object_id, item in main_window.renderer.items.items():
        print(item.pos().x(), item.pos().y())

    main_window.undo()

    print("\n--- AFTER UNDO ---")
    print("History index:", main_window.history.undo_count)

    for obj in (first, middle, last):
        current = main_window.renderer.find_object(obj.object_id)
        print(obj.object_id, "y =", current.y)

    main_window.redo()
    assert main_window.renderer.find_object(last.object_id).y == pytest.approx(10.0)

    layer = main_window.document.active_layer
    main_window.renderer.set_layer_locked(layer.layer_id, True)
    main_window.align_selected_objects("right")
    assert first.x == pytest.approx(0.0)
