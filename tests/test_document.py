
import pytest

from cutstudio.core.document import Document
from cutstudio.core.layer import Layer


def test_default_document():

    document = Document()

    assert document.width_mm == 304.8
    assert document.height_mm == 304.8
    assert len(document.layers) == 1
    assert document.active_layer.name == "Layer 1"


def test_add_layer():

    document = Document()

    layer = Layer("Layer 2")

    document.add_layer(layer)

    assert len(document.layers) == 2
    assert document.get_layer(layer.layer_id) is layer


def test_remove_layer():

    document = Document()

    first_layer = document.active_layer
    second_layer = Layer("Layer 2")

    document.add_layer(second_layer)

    document.remove_layer(first_layer.layer_id)

    assert len(document.layers) == 1
    assert document.active_layer is second_layer


def test_document_must_have_positive_dimensions():

    with pytest.raises(ValueError):
        Document(width_mm=0)


def test_document_cannot_remove_last_layer():

    document = Document()

    with pytest.raises(RuntimeError):
        document.remove_layer(
            document.active_layer_id
        )

