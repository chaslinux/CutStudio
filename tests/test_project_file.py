
import pytest

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
