
from dataclasses import dataclass, field

from cutstudio.core.objects import VectorObject


@dataclass
class Layer:

    name: str = "Layer 1"

    visible: bool = True
    locked: bool = False

    objects: list[VectorObject] = field(
        default_factory=list
    )

    layer_id: str = ""

    def __post_init__(self):

        if not self.layer_id:
            from uuid import uuid4
            self.layer_id = str(uuid4())

        if not self.name.strip():
            raise ValueError(
                "Layer name cannot be empty"
            )

    def add_object(self, obj: VectorObject):

        if self.locked:
            raise RuntimeError(
                "Cannot modify a locked layer"
            )

        if any(
            existing.object_id == obj.object_id
            for existing in self.objects
        ):
            raise ValueError(
                "Object already exists in this layer"
            )

        self.objects.append(obj)

    def remove_object(self, object_id: str):

        if self.locked:
            raise RuntimeError(
                "Cannot modify a locked layer"
            )

        for obj in self.objects:

            if obj.object_id == object_id:
                self.objects.remove(obj)
                return obj

        raise ValueError(
            f"Object not found: {object_id}"
        )

    def find_object(self, object_id: str):

        for obj in self.objects:

            if obj.object_id == object_id:
                return obj

        return None

