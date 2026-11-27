import pytest

from PySide6.QtWidgets import QApplication

from cutstudio.core.alignment import (
    align_objects,
    distribute_objects,
    distribute_gaps,
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


def test_distribute_gaps_horizontal_unequal_widths():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=10, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=20, y=0, width=20, height=10
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=80, y=0, width=30, height=10
    )

    assert distribute_gaps([a, b, c], "horizontal")

    bounds = [object_geometric_bounds(obj) for obj in (a, b, c)]

    assert bounds[0].right - bounds[0].left == pytest.approx(10)
    assert bounds[1].left - bounds[0].right == pytest.approx(25)
    assert bounds[2].left - bounds[1].right == pytest.approx(25)


def test_distribute_gaps_vertical_unequal_heights():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=10, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=0, y=20, width=10, height=20
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=0, y=80, width=10, height=30
    )

    assert distribute_gaps([a, b, c], "vertical")

    bounds = [object_geometric_bounds(obj) for obj in (a, b, c)]

    assert bounds[1].top - bounds[0].bottom == pytest.approx(25)
    assert bounds[2].top - bounds[1].bottom == pytest.approx(25)


def test_distribute_gaps_requires_three_objects():
    a = VectorObject(ObjectType.RECTANGLE, x=0, y=0)
    b = VectorObject(ObjectType.RECTANGLE, x=20, y=0)

    original_positions = [(obj.x, obj.y) for obj in (a, b)]

    assert distribute_gaps([a, b], "horizontal") is False
    assert [(obj.x, obj.y) for obj in (a, b)] == original_positions


def test_distribute_gaps_invalid_axis():
    objects = [
        VectorObject(ObjectType.RECTANGLE, x=0, y=0),
        VectorObject(ObjectType.RECTANGLE, x=20, y=0),
        VectorObject(ObjectType.RECTANGLE, x=80, y=0),
    ]

    with pytest.raises(ValueError):
        distribute_gaps(objects, "diagonal")


def test_distribute_gaps_preserves_anchor_objects():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=10, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=20, y=0, width=20, height=10
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=80, y=0, width=30, height=10
    )

    original_first = (a.x, a.y)
    original_last = (c.x, c.y)

    assert distribute_gaps([a, b, c], "horizontal")

    assert (a.x, a.y) == original_first
    assert (c.x, c.y) == original_last


def test_distribute_gaps_preserves_dimensions_and_rotation():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=10, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE,
        x=20, y=0, width=20, height=10, rotation=45
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=80, y=0, width=30, height=10
    )

    original = [
        (obj.width, obj.height, obj.rotation)
        for obj in (a, b, c)
    ]

    assert distribute_gaps([a, b, c], "horizontal")

    updated = [
        (obj.width, obj.height, obj.rotation)
        for obj in (a, b, c)
    ]

    assert updated == original


def test_distribute_gaps_rejects_overlapping_distribution():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=40, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=10, y=0, width=40, height=10
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=20, y=0, width=40, height=10
    )

    original = [(obj.x, obj.y) for obj in (a, b, c)]

    assert distribute_gaps([a, b, c], "horizontal") is False

    assert [(obj.x, obj.y) for obj in (a, b, c)] == original


def test_distribute_gaps_rejects_duplicate_objects():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=20, y=0
    )

    original = (a.x, a.y)

    assert distribute_gaps([a, b, a], "horizontal") is False
    assert (a.x, a.y) == original


def test_distribute_gaps_independent_of_selection_order():
    a = VectorObject(
        ObjectType.RECTANGLE, x=0, y=0, width=10, height=10
    )
    b = VectorObject(
        ObjectType.RECTANGLE, x=20, y=0, width=20, height=10
    )
    c = VectorObject(
        ObjectType.RECTANGLE, x=80, y=0, width=30, height=10
    )

    assert distribute_gaps([c, a, b], "horizontal")

    bounds = [
        object_geometric_bounds(obj)
        for obj in (a, b, c)
    ]

    assert bounds[1].left - bounds[0].right == pytest.approx(25)
    assert bounds[2].left - bounds[1].right == pytest.approx(25)



def test_gap_distribution_main_window_undo_redo(main_window):
    first = _place_rect(
        main_window, 0, 0, width=10, height=10
    )
    middle = _place_rect(
        main_window, 20, 0, width=20, height=10
    )
    last = _place_rect(
        main_window, 80, 0, width=30, height=10
    )

    # Establish the original layout as the undo baseline.
    main_window.history.clear(main_window.document)
    main_window._history_selections = {0: set()}
    main_window.update_history_actions()

    for obj in (first, middle, last):
        main_window.renderer.items[obj.object_id].setSelected(True)

    main_window.distribute_selected_gaps("horizontal")

    updated = main_window.renderer.find_object(middle.object_id)
    assert updated.x == pytest.approx(35.0)

    main_window.undo()

    restored = main_window.renderer.find_object(middle.object_id)
    assert restored.x == pytest.approx(20.0)

    main_window.redo()

    redone = main_window.renderer.find_object(middle.object_id)
    assert redone.x == pytest.approx(35.0)
