
import pytest

from cutstudio.core.mat import CuttingMatConfig

from cutstudio.core.document import Document
from cutstudio.core.layer import Layer
from cutstudio.core.objects import ObjectType, VectorObject
from cutstudio.core.project_file import (
    ProjectFileError,
    save_project,
    load_project,
    document_to_dict,
    document_from_dict,
)


def test_document_round_trip():

    document = Document()

    obj = VectorObject(
        object_type=ObjectType.RECTANGLE,
        x=10,
        y=20,
        width=50,
        height=60,
        fill="#ff0000",
    )

    document.active_layer.add_object(obj)

    data = document_to_dict(document)

    restored = document_from_dict(data)

    restored_obj = restored.active_layer.objects[0]

    assert restored_obj.object_id == obj.object_id
    assert restored_obj.x == 10
    assert restored_obj.y == 20
    assert restored_obj.width == 50
    assert restored_obj.height == 60
    assert restored_obj.fill == "#ff0000"


def test_save_and_load_project(tmp_path):

    document = Document()

    obj = VectorObject(ObjectType.ELLIPSE)

    document.active_layer.add_object(obj)

    filename = tmp_path / "test.cutstudio"

    save_project(document, filename)

    restored = load_project(filename)

    assert restored.document_id == document.document_id
    assert len(restored.active_layer.objects) == 1


def test_invalid_project_format():

    with pytest.raises(ProjectFileError):

        document_from_dict({
            "format": "something_else",
            "version": 1,
        })


def test_unsupported_project_version():

    with pytest.raises(ProjectFileError):

        document_from_dict({
            "format": "cutstudio",
            "version": 999,
            "document": {},
        })


def test_missing_project_file(tmp_path):

    with pytest.raises(ProjectFileError):

        load_project(tmp_path / "missing.cutstudio")


def test_mat_configuration_round_trip(tmp_path):

    document = Document()

    mat = CuttingMatConfig(
        width_mm=304.8,
        height_mm=609.6
    )

    filename = tmp_path / "mat_test.cutstudio"

    save_project(document, filename, mat)

    restored_document, restored_mat = load_project(
        filename,
        include_mat_config=True
    )

    assert restored_document.document_id == document.document_id
    assert restored_mat.width_mm == 304.8
    assert restored_mat.height_mm == 609.6


def test_legacy_project_uses_default_mat():

    document = Document()

    data = document_to_dict(document)

    restored_document, restored_mat = document_from_dict(
        data,
        include_mat_config=True
    )

    assert restored_document.document_id == document.document_id
    assert restored_mat == CuttingMatConfig()


def test_invalid_mat_dimensions_rejected():

    document = Document()

    data = document_to_dict(document)

    data["mat"] = {
        "width_mm": -100,
        "height_mm": 304.8
    }

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_document_dimensions_independent_of_mat():

    document = Document(
        width_mm=200,
        height_mm=150
    )

    mat = CuttingMatConfig(
        width_mm=304.8,
        height_mm=609.6
    )

    data = document_to_dict(document, mat)

    restored_document, restored_mat = document_from_dict(
        data,
        include_mat_config=True
    )

    assert restored_document.width_mm == 200
    assert restored_document.height_mm == 150

    assert restored_mat.width_mm == 304.8
    assert restored_mat.height_mm == 609.6


@pytest.mark.parametrize("invalid_mat", [
    None,
    [],
    "invalid",
    123,
])
def test_invalid_mat_structure_rejected(invalid_mat):

    document = Document()
    data = document_to_dict(document)

    data["mat"] = invalid_mat

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_invalid_mat_dimensions_rejected_on_load(tmp_path):

    document = Document()
    data = document_to_dict(document)

    data["mat"] = {
        "width_mm": -100,
        "height_mm": 304.8
    }

    import json

    filename = tmp_path / "invalid_mat.cutstudio"
    filename.write_text(json.dumps(data))

    with pytest.raises(ProjectFileError):
        load_project(filename, include_mat_config=True)


def test_round_trip_preserves_all_layer_state():

    document = Document()

    first = document.active_layer
    first.name = "Artwork"
    first.visible = False
    first.locked = True

    second = Layer(
        name="Background",
        visible=True,
        locked=False
    )

    document.add_layer(second)
    document.set_active_layer(second.layer_id)

    restored = document_from_dict(
        document_to_dict(document)
    )

    assert len(restored.layers) == 2
    assert restored.layers[0].layer_id == first.layer_id
    assert restored.layers[0].name == "Artwork"
    assert restored.layers[0].visible is False
    assert restored.layers[0].locked is True
    assert restored.active_layer_id == second.layer_id


def test_round_trip_preserves_all_object_properties():

    document = Document()

    obj = VectorObject(
        object_type=ObjectType.TEXT,
        x=12.5,
        y=24.5,
        width=80,
        height=30,
        rotation=45,
        fill="#123456",
        stroke="#654321",
        stroke_width=1.5,
        text="CutStudio",
        font_family="DejaVu Sans",
        font_size=18,
    )

    document.active_layer.add_object(obj)

    restored = document_from_dict(
        document_to_dict(document)
    )

    result = restored.active_layer.objects[0]

    for field in (
        "object_id",
        "object_type",
        "x",
        "y",
        "width",
        "height",
        "rotation",
        "fill",
        "stroke",
        "stroke_width",
        "text",
        "font_family",
        "font_size",
    ):
        assert getattr(result, field) == getattr(obj, field)


def test_round_trip_preserves_multiple_layers_and_objects():

    document = Document()

    second = Layer(name="Second")
    document.add_layer(second)

    first_obj = VectorObject(ObjectType.RECTANGLE)
    second_obj = VectorObject(ObjectType.ELLIPSE)

    document.active_layer.add_object(first_obj)
    second.add_object(second_obj)

    restored = document_from_dict(
        document_to_dict(document)
    )

    assert restored.layers[0].objects[0].object_id == first_obj.object_id
    assert restored.layers[1].objects[0].object_id == second_obj.object_id


def test_document_round_trip_preserves_document_dimensions():

    document = Document(
        width_mm=500,
        height_mm=250
    )

    restored = document_from_dict(
        document_to_dict(document)
    )

    assert restored.width_mm == 500
    assert restored.height_mm == 250


def test_duplicate_layer_ids_rejected():

    document = Document()

    data = document_to_dict(document)

    duplicate = dict(data["document"]["layers"][0])
    data["document"]["layers"].append(duplicate)

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_duplicate_object_ids_rejected():

    document = Document()

    obj = VectorObject(ObjectType.RECTANGLE)
    document.active_layer.add_object(obj)

    data = document_to_dict(document)

    duplicate = dict(
        data["document"]["layers"][0]["objects"][0]
    )

    data["document"]["layers"][0]["objects"].append(
        duplicate
    )

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_non_finite_document_dimensions_rejected():

    document = Document()
    data = document_to_dict(document)

    data["document"]["width_mm"] = float("nan")

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_invalid_layer_visibility_rejected():

    document = Document()
    data = document_to_dict(document)

    data["document"]["layers"][0]["visible"] = "yes"

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_invalid_layer_locking_rejected():

    document = Document()
    data = document_to_dict(document)

    data["document"]["layers"][0]["locked"] = 1

    with pytest.raises(ProjectFileError):
        document_from_dict(data)


def test_invalid_json_rejected(tmp_path):

    filename = tmp_path / "broken.cutstudio"
    filename.write_text("{invalid json")

    with pytest.raises(ProjectFileError):
        load_project(filename)
