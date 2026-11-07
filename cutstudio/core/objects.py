
from dataclasses import dataclass, field, replace
from enum import Enum
from math import isfinite
from uuid import uuid4


class ObjectType(str, Enum):
    RECTANGLE = "rectangle"
    ELLIPSE = "ellipse"
    TEXT = "text"


@dataclass
class VectorObject:

    object_type: ObjectType

    x: float = 0.0
    y: float = 0.0

    width: float = 25.4
    height: float = 25.4

    rotation: float = 0.0

    fill: str = "none"
    stroke: str = "#222222"
    stroke_width: float = 0.5291667

    text: str = ""
    font_family: str = "DejaVu Sans"
    font_size: float = 9.525

    object_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    def __post_init__(self):
        self.object_type = ObjectType(self.object_type)
        self.validate()

    def validate(self):

        numeric_values = {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "rotation": self.rotation,
            "stroke_width": self.stroke_width,
            "font_size": self.font_size,
        }

        for name, value in numeric_values.items():

            if not isfinite(value):
                raise ValueError(
                    f"{name} must be a finite number"
                )

        if self.width < 0 or self.height < 0:
            raise ValueError(
                "Object dimensions cannot be negative"
            )

        if self.stroke_width < 0:
            raise ValueError(
                "Stroke width cannot be negative"
            )

        if self.font_size <= 0:
            raise ValueError(
                "Font size must be greater than zero"
            )

        if not self.object_id:
            raise ValueError(
                "Object ID cannot be empty"
            )

    def duplicate(
        self,
        offset_x: float = 5.0,
        offset_y: float = 5.0
    ):
        """
        Create an independent copy of this object.

        Coordinates and offsets are measured in millimetres.
        The duplicate receives a new unique object ID.
        """

        return replace(
            self,
            x=self.x + offset_x,
            y=self.y + offset_y,
            object_id=str(uuid4())
        )

