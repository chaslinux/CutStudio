import math

from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsView

from cutstudio.core.units import mm_to_scene_units
from cutstudio.core.constants import UNITS_PER_INCH


class CuttingMat(QGraphicsView):

    objects_positions_changed = Signal()

    def __init__(self, scene, renderer=None):

        super().__init__(scene)

        self.renderer = renderer

        self._resize_state = None
        self._geometry_before = None

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

    def drawBackground(self, painter, rect):

        mat = self.scene().sceneRect()

        painter.fillRect(
            mat,
            QColor("#ffffff")
        )

        grid_pen = QPen(
            QColor("#dedede")
        )

        grid_pen.setWidthF(0)

        painter.setPen(grid_pen)

        spacing = UNITS_PER_INCH

        start_x = math.floor(mat.left() / spacing) * spacing
        end_x = math.ceil(mat.right() / spacing) * spacing

        start_y = math.floor(mat.top() / spacing) * spacing
        end_y = math.ceil(mat.bottom() / spacing) * spacing

        for x in range(start_x, end_x + 1, spacing):
            painter.drawLine(
                x, mat.top(), x, mat.bottom()
            )

        for y in range(start_y, end_y + 1, spacing):
            painter.drawLine(
                mat.left(), y, mat.right(), y
            )

        border_pen = QPen(
            QColor("#3285c7")
        )

        border_pen.setWidthF(2)

        painter.setPen(border_pen)
        painter.drawRect(mat)

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

            self.scale(factor, factor)
            event.accept()

        else:
            super().wheelEvent(event)

    # ---------------------------------
    # Object Resizing
    # ---------------------------------

    def _handle_at(self, viewport_position):

        if self.renderer is None:
            return None

        for name, handle in self.renderer.resize_handles.items():

            center = self.mapFromScene(handle.scenePos())

            if (
                abs(center.x() - viewport_position.x()) <= 8
                and abs(center.y() - viewport_position.y()) <= 8
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

                    self._resize_state = {
                        "item": item,
                        "object_id": object_id,
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

        if self._resize_state is not None:

            state = self._resize_state

            item = state["item"]

            scene_position = self.mapToScene(
                event.position().toPoint()
            )

            local_position = item.mapFromScene(
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

            item.setRect(
                QRectF(0, 0, width, height)
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

            self.renderer.sync_to_document()

            if self._geometry_changed(self._geometry_before):
                self.objects_positions_changed.emit()

        self._geometry_before = None
