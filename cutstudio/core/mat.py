from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CuttingMatConfig:
    """
    Physical cutting mat configuration.

    Dimensions are stored in millimetres.

    This configuration is independent of the document model.
    """

    width_mm: float = 304.8
    height_mm: float = 304.8

    def __post_init__(self):

        try:
            valid_dimensions = (
                isfinite(self.width_mm)
                and isfinite(self.height_mm)
            )
        except TypeError:
            valid_dimensions = False

        if not valid_dimensions:
            raise ValueError(
                "Cutting mat dimensions must be finite numbers"
            )

        if self.width_mm <= 0 or self.height_mm <= 0:
            raise ValueError(
                "Cutting mat dimensions must be greater than zero"
            )
