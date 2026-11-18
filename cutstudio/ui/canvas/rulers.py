import math

from PySide6.QtCore import Qt, QPoint, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from cutstudio.core.constants import UNITS_PER_INCH


RULER_SIZE = 28
MINOR_DIVISIONS = 4


class RulerWidget(QWidget):
    """A measurement ruler synchronized with the cutting mat."""

    def __init__(self, canvas, orientation, parent=None):

        super().__init__(parent)

        self.canvas = canvas
        self.orientation = orientation

        self.setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor("#eeeeee")
        )

        painter.setRenderHint(
            QPainter.RenderHint.TextAntialiasing
        )

        painter.setPen(
            QPen(QColor("#777777"), 1)
        )

        if self.orientation == "horizontal":
            self._draw_horizontal(painter)
        else:
            self._draw_vertical(painter)

        painter.setPen(
            QPen(QColor("#aaaaaa"), 1)
        )

        painter.drawRect(
            self.rect().adjusted(0, 0, -1, -1)
        )

        painter.end()

    def _visible_range(self):

        viewport = self.canvas.viewport()

        if self.orientation == "horizontal":

            first = self.canvas.mapToScene(
                QPoint(0, 0)
            ).x()

            last = self.canvas.mapToScene(
                QPoint(viewport.width(), 0)
            ).x()

        else:

            first = self.canvas.mapToScene(
                QPoint(0, 0)
            ).y()

            last = self.canvas.mapToScene(
                QPoint(0, viewport.height())
            ).y()

        return min(first, last), max(first, last)

    def _draw_horizontal(self, painter):

        start, end = self._visible_range()

        spacing = UNITS_PER_INCH / MINOR_DIVISIONS

        first_tick = math.floor(start / spacing)
        last_tick = math.ceil(end / spacing)

        height = self.height()

        for tick in range(first_tick, last_tick + 1):

            scene_x = tick * spacing

            viewport_position = self.canvas.mapFromScene(
                QPointF(scene_x, 0)
            )

            x = viewport_position.x()

            if not 0 <= x <= self.width():
                continue

            major = tick % MINOR_DIVISIONS == 0

            tick_length = 17 if major else 8

            painter.drawLine(
                x,
                height,
                x,
                height - tick_length
            )

            if major:

                inches = tick / MINOR_DIVISIONS

                painter.drawText(
                    QRectF(x + 3, 2, 38, 11),
                    Qt.AlignmentFlag.AlignLeft,
                    f"{inches:g}"
                )

    def _draw_vertical(self, painter):

        start, end = self._visible_range()

        spacing = UNITS_PER_INCH / MINOR_DIVISIONS

        first_tick = math.floor(start / spacing)
        last_tick = math.ceil(end / spacing)

        width = self.width()

        for tick in range(first_tick, last_tick + 1):

            scene_y = tick * spacing

            viewport_position = self.canvas.mapFromScene(
                QPointF(0, scene_y)
            )

            y = viewport_position.y()

            if not 0 <= y <= self.height():
                continue

            major = tick % MINOR_DIVISIONS == 0

            tick_length = 17 if major else 8

            painter.drawLine(
                width,
                y,
                width - tick_length,
                y
            )

            if major:

                inches = tick / MINOR_DIVISIONS

                painter.drawText(
                    QRectF(1, y + 2, 12, 20),
                    Qt.AlignmentFlag.AlignLeft,
                    f"{inches:g}"
                )
