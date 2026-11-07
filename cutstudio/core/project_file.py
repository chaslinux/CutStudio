
import json
from pathlib import Path

from cutstudio.core.document import Document
from cutstudio.core.layer import Layer
from cutstudio.core.objects import ObjectType, VectorObject


PROJECT_FORMAT_VERSION = 1


class ProjectFileError(Exception):
    """Raised when a CutStudio project cannot be saved or loaded."""


def document_to_dict(document):
    """Convert a Document into a JSON-compatible dictionary."""

    document.validate()

    return {
        "format": "cutstudio",
        "version": PROJECT_FORMAT_VERSION,
        "document": {
            "document_id": document.document_id,
            "width_mm": document.width_mm,
            "height_mm": document.height_mm,
            "active_layer_id": document.active_layer_id,
            "layers": [
                {
                    "layer_id": layer.layer_id,
                    "name": layer.name,
                    "visible": layer.visible,
                    "locked": layer.locked,
                    "objects": [
                        {
                            "object_id": obj.object_id,
                            "object_type": obj.object_type.value,
                            "x": obj.x,
                            "y": obj.y,
                            "width": obj.width,
                            "height": obj.height,
                            "rotation": obj.rotation,
                            "fill": obj.fill,
                            "stroke": obj.stroke,
                            "stroke_width": obj.stroke_width,
                            "text": obj.text,
                            "font_family": obj.font_family,
                            "font_size": obj.font_size,
                        }
                        for obj in layer.objects
                    ],
                }
                for layer in document.layers
            ],
        },
    }


def document_from_dict(data):
    """Reconstruct a Document from a project dictionary."""

    if not isinstance(data, dict):
        raise ProjectFileError("Project data must be an object")

    if data.get("format") != "cutstudio":
        raise ProjectFileError("Not a CutStudio project")

    if data.get("version") != PROJECT_FORMAT_VERSION:
        raise ProjectFileError("Unsupported project file version")

    document_data = data.get("document")

    if not isinstance(document_data, dict):
        raise ProjectFileError("Missing document data")

    try:
        layers = []

        for layer_data in document_data["layers"]:

            objects = []

            for object_data in layer_data["objects"]:

                obj = VectorObject(
                    object_type=ObjectType(
                        object_data["object_type"]
                    ),
                    x=object_data["x"],
                    y=object_data["y"],
                    width=object_data["width"],
                    height=object_data["height"],
                    rotation=object_data["rotation"],
                    fill=object_data["fill"],
                    stroke=object_data["stroke"],
                    stroke_width=object_data["stroke_width"],
                    text=object_data["text"],
                    font_family=object_data["font_family"],
                    font_size=object_data["font_size"],
                    object_id=object_data["object_id"],
                )

                objects.append(obj)

            layer = Layer(
                name=layer_data["name"],
                visible=layer_data["visible"],
                locked=layer_data["locked"],
                layer_id=layer_data["layer_id"],
                objects=objects,
            )

            layers.append(layer)

        return Document(
            width_mm=document_data["width_mm"],
            height_mm=document_data["height_mm"],
            layers=layers,
            document_id=document_data["document_id"],
            active_layer_id=document_data["active_layer_id"],
        )

    except (KeyError, TypeError, ValueError, RuntimeError) as error:
        raise ProjectFileError(
            f"Invalid project data: {error}"
        ) from error


def save_project(document, filename):
    """Save a CutStudio document as JSON."""

    path = Path(filename)

    try:
        data = document_to_dict(document)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

    except (OSError, TypeError, ValueError) as error:
        raise ProjectFileError(
            f"Could not save project: {error}"
        ) from error


def load_project(filename):
    """Load a CutStudio project from disk."""

    path = Path(filename)

    try:
        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        return document_from_dict(data)

    except (OSError, json.JSONDecodeError) as error:
        raise ProjectFileError(
            f"Could not load project: {error}"
        ) from error
