from cutstudio.core.constants import UNITS_PER_INCH

MM_PER_INCH = 25.4


def mm_to_inches(value: float) -> float:
    return value / MM_PER_INCH


def inches_to_mm(value: float) -> float:
    return value * MM_PER_INCH


def mm_to_scene_units(value: float) -> float:
    return value * UNITS_PER_INCH / MM_PER_INCH


def scene_units_to_mm(value: float) -> float:
    return value * MM_PER_INCH / UNITS_PER_INCH


def inches_to_scene_units(value: float) -> float:
    return value * UNITS_PER_INCH


def scene_units_to_inches(value: float) -> float:
    return value / UNITS_PER_INCH
