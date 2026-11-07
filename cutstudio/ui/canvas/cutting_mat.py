import math

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsView

from cutstudio.core.units import mm_to_scene_units
from cutstudio.core.constants import UNITS_PER_INCH


class CuttingMat(QGraphicsView):

    objects_positions_changed = Signal()

    def __init__(self, scene, renderer=None):

        super().__init__(scene)

        self.renderer = renderer

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

    def mouseReleaseEvent(self, event):

        super().mouseReleaseEvent(event)

        if self.renderer is not None:
            self.renderer.sync_to_document()

        self.objects_positions_changed.emit()
