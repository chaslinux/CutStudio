from dataclasses import dataclass
from math import cos, radians, sin
from typing import Sequence

from cutstudio.core.objects import VectorObject


@dataclass(frozen=True)
class GeometricBounds:
    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top

    @property
    def center_x(self) -> float:
        return (self.left + self.right) / 2.0

    @property
    def center_y(self) -> float:
        return (self.top + self.bottom) / 2.0


def object_geometric_bounds(obj: VectorObject) -> GeometricBounds:
    """
    Return the axis-aligned geometric bounding box of a VectorObject in mm,
    accounting for rotation around the object's geometric centre.
    """
    if obj.rotation % 360.0 == 0.0:
        return GeometricBounds(
            left=obj.x,
            top=obj.y,
            right=obj.x + obj.width,
            bottom=obj.y + obj.height,
        )

    cx = obj.x + obj.width / 2.0
    cy = obj.y + obj.height / 2.0
    theta = radians(obj.rotation)
    cos_t = cos(theta)
    sin_t = sin(theta)

    corners = (
        (obj.x, obj.y),
        (obj.x + obj.width, obj.y),
        (obj.x + obj.width, obj.y + obj.height),
        (obj.x, obj.y + obj.height),
    )

    xs = []
    ys = []
    for px, py in corners:
        dx = px - cx
        dy = py - cy
        xs.append(cx + dx * cos_t - dy * sin_t)
        ys.append(cy + dx * sin_t + dy * cos_t)

    return GeometricBounds(
        left=min(xs),
        top=min(ys),
        right=max(xs),
        bottom=max(ys),
    )


def align_objects(objects: Sequence[VectorObject], mode: str) -> bool:
    """Align two or more VectorObjects in place using their geometric bounds."""
    valid_modes = {"left", "right", "top", "bottom", "h_center", "v_center"}
    if mode not in valid_modes:
        raise ValueError(f"Unsupported alignment mode: {mode}")

    if len(objects) < 2:
        return False

    bounds_list = [object_geometric_bounds(obj) for obj in objects]

    sel_left = min(b.left for b in bounds_list)
    sel_right = max(b.right for b in bounds_list)
    sel_top = min(b.top for b in bounds_list)
    sel_bottom = max(b.bottom for b in bounds_list)
    sel_center_x = (sel_left + sel_right) / 2.0
    sel_center_y = (sel_top + sel_bottom) / 2.0

    for obj, b in zip(objects, bounds_list):
        if mode == "left":
            obj.x += sel_left - b.left
        elif mode == "right":
            obj.x += sel_right - b.right
        elif mode == "h_center":
            obj.x += sel_center_x - b.center_x
        elif mode == "top":
            obj.y += sel_top - b.top
        elif mode == "bottom":
            obj.y += sel_bottom - b.bottom
        elif mode == "v_center":
            obj.y += sel_center_y - b.center_y

    return True


def distribute_objects(objects: Sequence[VectorObject], axis: str) -> bool:
    """Distribute three or more VectorObjects evenly along horizontal or vertical axis."""
    if axis not in {"horizontal", "vertical"}:
        raise ValueError(f"Unsupported distribution axis: {axis}")

    if len(objects) < 3:
        return False

    items = [
        (idx, obj, object_geometric_bounds(obj))
        for idx, obj in enumerate(objects)
    ]

    if axis == "horizontal":
        items.sort(key=lambda entry: (entry[2].center_x, entry[2].left, entry[0]))
        first_center = items[0][2].center_x
        last_center = items[-1][2].center_x
        step = (last_center - first_center) / (len(items) - 1)

        for step_idx, (_, obj, b) in enumerate(items[1:-1], start=1):
            target_center = first_center + step * step_idx
            obj.x += target_center - b.center_x
    else:
        items.sort(key=lambda entry: (entry[2].center_y, entry[2].top, entry[0]))
        first_center = items[0][2].center_y
        last_center = items[-1][2].center_y
        step = (last_center - first_center) / (len(items) - 1)

        for step_idx, (_, obj, b) in enumerate(items[1:-1], start=1):
            target_center = first_center + step * step_idx
            obj.y += target_center - b.center_y

    return True


def distribute_gaps(objects: Sequence[VectorObject], axis: str) -> bool:
    """
    Distribute three or more VectorObjects with equal gaps between
    their rotation-aware geometric bounding boxes.

    The first and last objects remain stationary.
    Intermediate objects are repositioned.

    Returns False if the requested distribution would require
    overlapping objects or fewer than three objects.
    """
    if axis not in {"horizontal", "vertical"}:
        raise ValueError(f"Unsupported distribution axis: {axis}")

    if len(objects) < 3:
        return False

    # A document object must not appear more than once.
    if len({id(obj) for obj in objects}) != len(objects):
        return False

    items = [
        (idx, obj, object_geometric_bounds(obj))
        for idx, obj in enumerate(objects)
    ]

    if axis == "horizontal":
        items.sort(
            key=lambda entry: (
                entry[2].left,
                entry[2].center_x,
                entry[0],
            )
        )

        first_edge = items[0][2].left
        last_edge = items[-1][2].right

        total_size = sum(
            bounds.width for _, _, bounds in items
        )

        total_gap = last_edge - first_edge - total_size

        if total_gap < -1e-9:
            return False

        gap = max(0.0, total_gap) / (len(items) - 1)

        current_position = first_edge

        for index, (_, obj, bounds) in enumerate(items):
            if index not in (0, len(items) - 1):
                obj.x += current_position - bounds.left

            current_position += bounds.width + gap

    else:
        items.sort(
            key=lambda entry: (
                entry[2].top,
                entry[2].center_y,
                entry[0],
            )
        )

        first_edge = items[0][2].top
        last_edge = items[-1][2].bottom

        total_size = sum(
            bounds.height for _, _, bounds in items
        )

        total_gap = last_edge - first_edge - total_size

        if total_gap < -1e-9:
            return False

        gap = max(0.0, total_gap) / (len(items) - 1)

        current_position = first_edge

        for index, (_, obj, bounds) in enumerate(items):
            if index not in (0, len(items) - 1):
                obj.y += current_position - bounds.top

            current_position += bounds.height + gap

    return True
