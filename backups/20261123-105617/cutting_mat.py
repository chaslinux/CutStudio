import math

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsView, QWidget

from cutstudio.ui.canvas.rulers import (
    RulerWidget,
    RULER_SIZE,
)

from cutstudio.core.units import mm_to_scene_units
from cutstudio.core.constants import UNITS_PER_INCH


class CuttingMat(QGraphicsView):

    objects_positions_changed = Signal()
    zoom_changed = Signal(float)

    def __init__(self, scene, renderer=None):

        super().__init__(scene)

        self.renderer = renderer

        self._resize_state = None
        self._rotation_state = None
        self._geometry_before = None
        self._pan_position = None

        # Grid settings. Scene coordinates use 96 units per inch.
        self.grid_visible = True
        self.grid_spacing = 24.0       # Quarter inch
        self.grid_major_interval = UNITS_PER_INCH
        self.snap_to_grid = False

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        self.setBackgroundBrush(
            QColor("#d7d9dc")
        )

        self.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        # Reserve space for measurement rulers.
        self.setViewportMargins(
            RULER_SIZE,
            RULER_SIZE,
            0,
            0
        )

        self.horizontal_ruler = RulerWidget(
            self,
            "horizontal",
            self
        )

        self.vertical_ruler = RulerWidget(
            self,
            "vertical",
            self
        )

        self.ruler_corner = QWidget(self)

        self.ruler_corner.setStyleSheet(
            "background-color: #eeeeee;"
            "border: 1px solid #aaaaaa;"
        )

        # Update rulers whenever the canvas scrolls.
        self.horizontalScrollBar().valueChanged.connect(
            self._update_rulers
        )

        self.verticalScrollBar().valueChanged.connect(
            self._update_rulers
        )

        self._update_ruler_geometries()

    def _update_ruler_geometries(self):
        """Position rulers alongside the graphics viewport."""

        frame = self.frameWidth()
        viewport = self.viewport().geometry()

        self.horizontal_ruler.setGeometry(
            viewport.x(),
            frame,
            viewport.width(),
            RULER_SIZE
        )

        self.vertical_ruler.setGeometry(
            frame,
            viewport.y(),
            RULER_SIZE,
            viewport.height()
        )

        self.ruler_corner.setGeometry(
            frame,
            frame,
            RULER_SIZE,
            RULER_SIZE
        )

        self._update_rulers()

    def _update_rulers(self, *args):
        """Refresh ruler markings after canvas navigation."""

        self.horizontal_ruler.update()
        self.vertical_ruler.update()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self._update_ruler_geometries()

    def drawBackground(self, painter, rect):

        mat = self.scene().sceneRect()

        painter.fillRect(
            mat,
            QColor("#ffffff")
        )

        if self.grid_visible and self.grid_spacing > 0:

            spacing = self.grid_spacing
            major_spacing = self.major_grid_spacing

            # Draw minor grid lines.
            first_x = math.ceil(
                mat.left() / spacing
            )
            last_x = math.floor(
                mat.right() / spacing
            )

            first_y = math.ceil(
                mat.top() / spacing
            )
            last_y = math.floor(
                mat.bottom() / spacing
            )

            minor_pen = QPen(QColor("#eeeeee"))
            minor_pen.setWidthF(0)
            painter.setPen(minor_pen)

            for index in range(first_x, last_x + 1):
                x = index * spacing
                painter.drawLine(
                    QPointF(x, mat.top()),
                    QPointF(x, mat.bottom())
                )

            for index in range(first_y, last_y + 1):
                y = index * spacing
                painter.drawLine(
                    QPointF(mat.left(), y),
                    QPointF(mat.right(), y)
                )

            # Draw major lines every inch.
            major_pen = QPen(QColor("#b8bec6"))
            major_pen.setWidthF(0)
            painter.setPen(major_pen)

            first_x = math.ceil(
                mat.left() / major_spacing
            )
            last_x = math.floor(
                mat.right() / major_spacing
            )

            first_y = math.ceil(
                mat.top() / major_spacing
            )
            last_y = math.floor(
                mat.bottom() / major_spacing
            )

            for index in range(first_x, last_x + 1):
                x = index * major_spacing
                painter.drawLine(
                    QPointF(x, mat.top()),
                    QPointF(x, mat.bottom())
                )

            for index in range(first_y, last_y + 1):
                y = index * major_spacing
                painter.drawLine(
                    QPointF(mat.left(), y),
                    QPointF(mat.right(), y)
                )

        border_pen = QPen(
            QColor("#3285c7")
        )

        border_pen.setWidthF(2)

        painter.setPen(border_pen)
        painter.drawRect(mat)

    def set_grid_visible(self, visible):

        self.grid_visible = bool(visible)
        self.viewport().update()

    def set_grid_spacing_inches(self, inches):

        if not math.isfinite(inches) or inches <= 0:
            raise ValueError("Grid spacing must be positive.")

        self.grid_spacing = inches * UNITS_PER_INCH
        self.viewport().update()

    def set_grid_spacing_mm(self, millimetres):

        if not math.isfinite(millimetres) or millimetres <= 0:
            raise ValueError("Grid spacing must be positive.")

        self.grid_spacing = mm_to_scene_units(millimetres)
        self.viewport().update()


    def set_grid_major_interval(self, interval):

        if interval not in (2, 4, 5, 10):
            raise ValueError("Invalid major grid interval.")

        self.grid_major_interval = interval
        self.viewport().update()

    def set_snap_to_grid(self, enabled):

        self.snap_to_grid = bool(enabled)

    def _snap_value(self, value):

        if not self.snap_to_grid:
            return value

        spacing = self.grid_spacing

        if spacing <= 0:
            return value

        return round(value / spacing) * spacing

    def _snap_selected_group(self):

        if not self.snap_to_grid:
            return

        selected = self.scene().selectedItems()

        if not selected:
            return

        # Snap the entire selection together so the relative
        # positions of multiple objects are preserved.
        bounds = selected[0].sceneBoundingRect()

        for item in selected[1:]:
            bounds = bounds.united(item.sceneBoundingRect())

        mat = self.scene().sceneRect()

        target_x = mat.left() + self._snap_value(
            bounds.left() - mat.left()
        )

        target_y = mat.top() + self._snap_value(
            bounds.top() - mat.top()
        )

        delta = QPointF(
            target_x - bounds.left(),
            target_y - bounds.top()
        )

        if delta.isNull():
            return

        for item in selected:
            item.setPos(item.pos() + delta)

    def wheelEvent(self, event):

        if (
            event.modifiers()
            & Qt.KeyboardModifier.ControlModifier
        ):

            factor = (
                1.15
                if event.angleDelta().y() > 0
                else 1 / 1.15
            )

            self._zoom_by(
                factor,
                QGraphicsView.ViewportAnchor.AnchorUnderMouse
            )

            event.accept()

        else:
            super().wheelEvent(event)

    def _zoom_by(self, factor, anchor=None):

        current_scale = self.transform().m11()

        min_scale = 0.1
        max_scale = 5.0

        new_scale = max(
            min_scale,
            min(max_scale, current_scale * factor)
        )

        factor = new_scale / current_scale

        if abs(factor - 1.0) < 0.0001:
            return

        previous_anchor = self.transformationAnchor()

        if anchor is None:
            anchor = (
                QGraphicsView.ViewportAnchor.AnchorViewCenter
            )

        self.setTransformationAnchor(anchor)

        self.scale(factor, factor)

        self.setTransformationAnchor(previous_anchor)

        self._update_rulers()
        self._emit_zoom_changed()

    def zoom_in(self):

        self._zoom_by(1.2)

    def zoom_out(self):

        self._zoom_by(1 / 1.2)

    def zoom_to_fit(self):

        scene_rect = self.scene().sceneRect()

        if scene_rect.isNull() or scene_rect.isEmpty():
            return

        # Add a 3% margin around the cutting mat.
        margin_x = scene_rect.width() * 0.03
        margin_y = scene_rect.height() * 0.03

        fit_rect = scene_rect.adjusted(
            -margin_x,
            -margin_y,
            margin_x,
            margin_y
        )

        self.fitInView(
            fit_rect,
            Qt.AspectRatioMode.KeepAspectRatio
        )

        self._update_rulers()
        self._emit_zoom_changed()

    def _emit_zoom_changed(self):

        zoom_percentage = self.transform().m11() * 100

        self.zoom_changed.emit(zoom_percentage)

    # ---------------------------------
    # Object Resizing
    # ---------------------------------

    def _handle_at(self, viewport_position):

        if self.renderer is None:
            return None

        # Check rotation first so it takes priority over
        # resize handles when detecting mouse interaction.
        handle_names = sorted(
            self.renderer.resize_handles,
            key=lambda name: name != "rotate"
        )

        for name in handle_names:

            handle = self.renderer.resize_handles[name]

            center = self.mapFromScene(handle.scenePos())

            hit_radius = 10 if name == "rotate" else 8

            if (
                abs(center.x() - viewport_position.x()) <= hit_radius
                and abs(center.y() - viewport_position.y()) <= hit_radius
            ):
                return name

        return None

    def _document_geometry(self):

        if self.renderer is None:
            return {}

        return {
            obj.object_id: (
                obj.x,
                obj.y,
                obj.width,
                obj.height,
                obj.rotation,
            )
            for layer in self.renderer.document.layers
            for obj in layer.objects
        }

    def _geometry_changed(self, before):

        after = self._document_geometry()

        if before is None:
            return False

        if before.keys() != after.keys():
            return True

        return any(
            not all(
                math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
                for a, b in zip(before[object_id], after[object_id])
            )
            for object_id in before
        )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:

            self._pan_position = event.position().toPoint()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

            event.accept()
            return

        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.renderer is not None
        ):

            handle_name = self._handle_at(
                event.position().toPoint()
            )

            selected_items = self.scene().selectedItems()

            if handle_name is not None and len(selected_items) == 1:

                item = selected_items[0]

                object_id = item.data(
                    self.renderer.OBJECT_ID_ROLE
                )

                if object_id is not None:

                    if handle_name == "rotate":

                        obj, layer = self.renderer.find_object_and_layer(
                            object_id
                        )

                        if obj is None or layer is None or layer.locked:
                            event.accept()
                            return

                        center = item.mapToScene(
                            item.rect().center()
                        )

                        mouse_position = self.mapToScene(
                            event.position().toPoint()
                        )

                        vector = mouse_position - center

                        if vector.isNull():
                            event.accept()
                            return

                        self._rotation_state = {
                            "item": item,
                            "object_id": object_id,
                            "center": center,
                            "start_angle": math.degrees(
                                math.atan2(vector.y(), vector.x())
                            ),
                            "start_rotation": item.rotation(),
                            "geometry_before": self._document_geometry(),
                        }

                        event.accept()
                        return

                    rect = item.rect()

                    width = rect.width()
                    height = rect.height()

                    horizontal = (
                        "w" if "w" in handle_name
                        else "e" if "e" in handle_name
                        else None
                    )

                    vertical = (
                        "n" if "n" in handle_name
                        else "s" if "s" in handle_name
                        else None
                    )

                    anchor_x = (
                        width if horizontal == "w"
                        else 0 if horizontal == "e"
                        else width / 2
                    )

                    anchor_y = (
                        height if vertical == "n"
                        else 0 if vertical == "s"
                        else height / 2
                    )

                    anchor_local = QPointF(
                        anchor_x,
                        anchor_y
                    )

                    self.renderer.sync_to_document()

                    obj = self.renderer.find_object(object_id)

                    scene_to_local, invertible = (
                        item.sceneTransform().inverted()
                    )

                    if not invertible:
                        event.accept()
                        return

                    self._resize_state = {
                        "item": item,
                        "object_id": object_id,
                        "scene_to_local": scene_to_local,
                        "width_mm": obj.width,
                        "height_mm": obj.height,
                        "handle": handle_name,
                        "horizontal": horizontal,
                        "vertical": vertical,
                        "anchor_local": anchor_local,
                        "anchor_scene": item.mapToScene(anchor_local),
                        "width": width,
                        "height": height,
                        "geometry_before": self._document_geometry(),
                    }

                    event.accept()
                    return

        if self.renderer is not None:
            self.renderer.sync_to_document()
            self._geometry_before = self._document_geometry()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if self._pan_position is not None:

            current = event.position().toPoint()
            delta = current - self._pan_position

            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )

            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )

            self._pan_position = current

            event.accept()
            return

        if self._rotation_state is not None:

            state = self._rotation_state

            item = state["item"]

            scene_position = self.mapToScene(
                event.position().toPoint()
            )

            vector = scene_position - state["center"]

            if vector.isNull():
                event.accept()
                return

            current_angle = math.degrees(
                math.atan2(vector.y(), vector.x())
            )

            delta = current_angle - state["start_angle"]

            # Keep the change within one revolution.
            delta = (delta + 180) % 360 - 180

            new_rotation = state["start_rotation"] + delta

            # Hold Shift to snap to 15-degree increments.
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:

                new_rotation = round(
                    new_rotation / 15.0
                ) * 15.0

            item.setRotation(new_rotation)

            self.renderer.sync_to_document()

            self.renderer.update_resize_handles(
                state["object_id"]
            )

            event.accept()
            return

        if self._resize_state is not None:

            state = self._resize_state

            item = state["item"]

            scene_position = self.mapToScene(
                event.position().toPoint()
            )

            # Always use the original transformation captured
            # when the resize operation began.
            local_position = state["scene_to_local"].map(
                scene_position
            )

            width = state["width"]
            height = state["height"]

            horizontal = state["horizontal"]
            vertical = state["vertical"]

            anchor = state["anchor_local"]

            # One scene unit is the minimum dimension.
            minimum_size = 1.0

            if horizontal == "w":

                width = max(
                    minimum_size,
                    anchor.x() - local_position.x()
                )

                new_anchor_x = width

            elif horizontal == "e":

                width = max(
                    minimum_size,
                    local_position.x() - anchor.x()
                )

                new_anchor_x = 0

            else:

                new_anchor_x = width / 2

            if vertical == "n":

                height = max(
                    minimum_size,
                    anchor.y() - local_position.y()
                )

                new_anchor_y = height

            elif vertical == "s":

                height = max(
                    minimum_size,
                    local_position.y() - anchor.y()
                )

                new_anchor_y = 0

            else:

                new_anchor_y = height / 2

            # Hold Shift to preserve the original aspect ratio.
            if (
                event.modifiers()
                & Qt.KeyboardModifier.ShiftModifier
            ):

                original_width = state["width"]
                original_height = state["height"]

                if original_width > 0 and original_height > 0:

                    width_scale = width / original_width
                    height_scale = height / original_height

                    # For corner handles, use the dimension
                    # with the greater proportional movement.
                    if horizontal is not None and vertical is not None:

                        scale = (
                            width_scale
                            if abs(width_scale - 1.0)
                            >= abs(height_scale - 1.0)
                            else height_scale
                        )

                    elif horizontal is not None:
                        scale = width_scale

                    elif vertical is not None:
                        scale = height_scale

                    else:
                        scale = 1.0

                    minimum_scale = max(
                        minimum_size / original_width,
                        minimum_size / original_height,
                    )

                    scale = max(scale, minimum_scale)

                    width = original_width * scale
                    height = original_height * scale

                    # Recalculate the stationary anchor.
                    if horizontal == "w":
                        new_anchor_x = width
                    elif horizontal == "e":
                        new_anchor_x = 0
                    else:
                        new_anchor_x = width / 2

                    if vertical == "n":
                        new_anchor_y = height
                    elif vertical == "s":
                        new_anchor_y = 0
                    else:
                        new_anchor_y = height / 2

            # Snap resized dimensions to the configured grid.
            # Only snap dimensions controlled by the active handle.
            if self.snap_to_grid:

                if horizontal is not None:
                    width = max(
                        minimum_size,
                        self._snap_value(width)
                    )

                if vertical is not None:
                    height = max(
                        minimum_size,
                        self._snap_value(height)
                    )

                # Recalculate the stationary anchor after snapping.
                if horizontal == "w":
                    new_anchor_x = width
                elif horizontal == "e":
                    new_anchor_x = 0
                else:
                    new_anchor_x = width / 2

                if vertical == "n":
                    new_anchor_y = height
                elif vertical == "s":
                    new_anchor_y = 0
                else:
                    new_anchor_y = height / 2

            item.setRect(
                QRectF(0, 0, width, height)
            )

            item.setTransformOriginPoint(
                item.boundingRect().center()
            )

            # Keep the opposite edge or corner stationary.
            new_anchor_scene = item.mapToScene(
                QPointF(new_anchor_x, new_anchor_y)
            )

            displacement = (
                state["anchor_scene"] - new_anchor_scene
            )

            item.setPos(
                item.pos() + displacement
            )

            self.renderer.sync_to_document()

            obj = self.renderer.find_object(
                state["object_id"]
            )

            # Preserve the untouched dimension exactly.
            if horizontal is not None and vertical is None:

                obj.height = state["height_mm"]

            elif vertical is not None and horizontal is None:

                obj.width = state["width_mm"]

            self.renderer.update_resize_handles(
                state["object_id"]
            )

            event.accept()
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.MiddleButton:


            self._pan_position = None
            self.unsetCursor()

            event.accept()
            return

        if self._rotation_state is not None:

            state = self._rotation_state
            self._rotation_state = None

            self.renderer.sync_to_document()

            self.renderer.update_resize_handles(
                state["object_id"]
            )

            if self._geometry_changed(
                state["geometry_before"]
            ):
                self.objects_positions_changed.emit()

            event.accept()
            return

        if self._resize_state is not None:

            state = self._resize_state
            self._resize_state = None

            self.renderer.sync_to_document()

            self.renderer.update_resize_handles(
                state["object_id"]
            )

            if self._geometry_changed(
                state["geometry_before"]
            ):
                self.objects_positions_changed.emit()

            event.accept()
            return

        super().mouseReleaseEvent(event)

        if self.renderer is not None:

            self._snap_selected_group()

            self.renderer.sync_to_document()

            if self._geometry_changed(self._geometry_before):
                self.objects_positions_changed.emit()

        self._geometry_before = None
