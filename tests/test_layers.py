
import pytest

from cutstudio.core.layer import Layer
from cutstudio.core.objects import (
    ObjectType,
    VectorObject,
)


def test_add_and_find_object():

    layer = Layer("Layer 1")

    obj = VectorObject(ObjectType.RECTANGLE)

    layer.add_object(obj)

    assert len(layer.objects) == 1
    assert layer.find_object(obj.object_id) is obj


def test_remove_object():

    layer = Layer("Layer 1")

    obj = VectorObject(ObjectType.ELLIPSE)

    layer.add_object(obj)

    removed = layer.remove_object(obj.object_id)

    assert removed is obj
    assert len(layer.objects) == 0


def test_locked_layer_rejects_changes():

    layer = Layer("Locked Layer", locked=True)

    obj = VectorObject(ObjectType.RECTANGLE)

    with pytest.raises(RuntimeError):
        layer.add_object(obj)

