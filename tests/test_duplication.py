
from cutstudio.core.objects import ObjectType, VectorObject


def test_duplicate_creates_new_object_id():

    original = VectorObject(ObjectType.RECTANGLE)

    duplicate = original.duplicate()

    assert duplicate.object_id != original.object_id


def test_duplicate_preserves_object_properties():

    original = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=20.0,
        y=30.0,
        width=50.0,
        height=40.0,
        rotation=45.0,
        fill="#ff0000",
        stroke="#000000",
        stroke_width=1.5,
    )

    duplicate = original.duplicate()

    assert duplicate.object_type == original.object_type
    assert duplicate.width == original.width
    assert duplicate.height == original.height
    assert duplicate.rotation == original.rotation
    assert duplicate.fill == original.fill
    assert duplicate.stroke == original.stroke
    assert duplicate.stroke_width == original.stroke_width


def test_duplicate_has_offset_position():

    original = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=10.0,
        y=20.0,
    )

    duplicate = original.duplicate()

    assert duplicate.x == 15.0
    assert duplicate.y == 25.0


def test_duplicate_does_not_modify_original():

    original = VectorObject(
        object_type=ObjectType.ELLIPSE,
        x=10.0,
        y=20.0,
    )

    duplicate = original.duplicate()

    assert original.x == 10.0
    assert original.y == 20.0

    duplicate.x = 100.0

    assert original.x == 10.0


def test_duplicate_preserves_text_properties():

    original = VectorObject(
        object_type=ObjectType.TEXT,
        x=10.0,
        y=20.0,
        text="CutStudio",
        font_family="DejaVu Sans",
        font_size=15.0,
        stroke="#0000ff",
    )

    duplicate = original.duplicate()

    assert duplicate.text == original.text
    assert duplicate.font_family == original.font_family
    assert duplicate.font_size == original.font_size
    assert duplicate.stroke == original.stroke


def test_duplicate_supports_custom_offset():

    original = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=10.0,
        y=20.0,
    )

    duplicate = original.duplicate(
        offset_x=10.0,
        offset_y=15.0
    )

    assert duplicate.x == 20.0
    assert duplicate.y == 35.0

