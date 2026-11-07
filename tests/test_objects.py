
import pytest

from cutstudio.core.objects import (
    ObjectType,
    VectorObject,
)


def test_create_rectangle():

    obj = VectorObject(
        object_type=ObjectType.RECTANGLE,
        width=50,
        height=25,
    )

    assert obj.object_type == ObjectType.RECTANGLE
    assert obj.width == 50
    assert obj.height == 25
    assert obj.object_id


def test_object_ids_are_unique():

    first = VectorObject(ObjectType.RECTANGLE)
    second = VectorObject(ObjectType.RECTANGLE)

    assert first.object_id != second.object_id


def test_negative_dimensions_rejected():

    with pytest.raises(ValueError):
        VectorObject(
            object_type=ObjectType.RECTANGLE,
            width=-10,
        )


def test_negative_stroke_width_rejected():

    with pytest.raises(ValueError):
        VectorObject(
            object_type=ObjectType.RECTANGLE,
            stroke_width=-1,
        )

