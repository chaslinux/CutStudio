
from dataclasses import dataclass, field
from math import isfinite
from uuid import uuid4

from cutstudio.core.layer import Layer


@dataclass
class Document:

    width_mm: float = 304.8
    height_mm: float = 304.8

    layers: list[Layer] = field(
        default_factory=list
    )

    document_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    active_layer_id: str = ""

    def __post_init__(self):

        self.validate()

        if not self.layers:
            self.add_layer(Layer("Layer 1"))

        if not self.active_layer_id:
            self.active_layer_id = self.layers[0].layer_id

        elif self.get_layer(self.active_layer_id) is None:
            raise ValueError(
                "Active layer does not exist"
            )

    def validate(self):

        if (
            not isfinite(self.width_mm)
            or not isfinite(self.height_mm)
        ):
            raise ValueError(
                "Document dimensions must be finite"
            )

        if self.width_mm <= 0 or self.height_mm <= 0:
            raise ValueError(
                "Document dimensions must be greater than zero"
            )

        if not self.document_id:
            raise ValueError(
                "Document ID cannot be empty"
            )

    @property
    def active_layer(self):

        return self.get_layer(
            self.active_layer_id
        )

    def add_layer(self, layer: Layer):

        if any(
            existing.layer_id == layer.layer_id
            for existing in self.layers
        ):
            raise ValueError(
                "Layer already exists in document"
            )

        self.layers.append(layer)

        if not self.active_layer_id:
            self.active_layer_id = layer.layer_id

    def get_layer(self, layer_id: str):

        for layer in self.layers:

            if layer.layer_id == layer_id:
                return layer

        return None

    def remove_layer(self, layer_id: str):

        if len(self.layers) <= 1:
            raise RuntimeError(
                "A document must have at least one layer"
            )

        layer = self.get_layer(layer_id)

        if layer is None:
            raise ValueError(
                f"Layer not found: {layer_id}"
            )

        self.layers.remove(layer)

        if self.active_layer_id == layer_id:
            self.active_layer_id = self.layers[0].layer_id

        return layer

    def set_active_layer(self, layer_id: str):

        if self.get_layer(layer_id) is None:
            raise ValueError(
                f"Layer not found: {layer_id}"
            )

        self.active_layer_id = layer_id

