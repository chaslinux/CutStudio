
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QBrush, QFont, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
)

from cutstudio.core.objects import ObjectType

from cutstudio.core.units import (
    mm_to_scene_units,
    scene_units_to_mm,
)


class CanvasRenderer:

    OBJECT_ID_ROLE = 0

    def __init__(self, document, scene):

        self.document = document
        self.scene = scene

        self.items = {}

    # ---------------------------------
    # Create graphics items
    # ---------------------------------

    def create_item(self, obj):

        width = mm_to_scene_units(obj.width)
        height = mm_to_scene_units(obj.height)

        if obj.object_type == ObjectType.RECTANGLE:

            item = QGraphicsRectItem(
                QRectF(0, 0, width, height)
            )

        elif obj.object_type == ObjectType.ELLIPSE:

            item = QGraphicsEllipseItem(
                QRectF(0, 0, width, height)
            )

        elif obj.object_type == ObjectType.TEXT:

            item = QGraphicsTextItem(obj.text)

            font = QFont(obj.font_family)

            font.setPointSizeF(
                obj.font_size * 72 / 25.4
            )

            item.setFont(font)

            obj.width = scene_units_to_mm(
                item.boundingRect().width()
            )

            obj.height = scene_units_to_mm(
                item.boundingRect().height()
            )

        else:

            raise ValueError(
                f"Unsupported object type: {obj.object_type}"
            )

        pen = QPen(QColor(obj.stroke))

        pen.setWidthF(
            mm_to_scene_units(obj.stroke_width)
        )

        if isinstance(item, (QGraphicsRectItem, QGraphicsEllipseItem)):

            item.setPen(pen)

            if obj.fill.lower() == "none":

                item.setBrush(
                    QBrush(Qt.BrushStyle.NoBrush)
                )

            else:

                item.setBrush(
                    QBrush(QColor(obj.fill))
                )

        elif isinstance(item, QGraphicsTextItem):

            item.setDefaultTextColor(
                QColor(obj.stroke)
            )

        item.setRotation(obj.rotation)

        item.setPos(
            mm_to_scene_units(obj.x),
            mm_to_scene_units(obj.y)
        )

        item.setData(
            self.OBJECT_ID_ROLE,
            obj.object_id
        )

        return item

    # ---------------------------------
    # Add document object
    # ---------------------------------

    def add_object(self, obj, layer):

        if layer.locked:

            raise RuntimeError(
                "Cannot add objects to a locked layer"
            )

        if obj.object_id in self.items:

            raise ValueError(
                "Object is already displayed"
            )

        if self.find_object(obj.object_id) is not None:

            raise ValueError(
                "Object already exists in document"
            )

        item = self.create_item(obj)

        flags = (
            item.GraphicsItemFlag.ItemIsSelectable
            | item.GraphicsItemFlag.ItemIsMovable
        )

        item.setFlags(flags)

        item.setVisible(layer.visible)

        layer.add_object(obj)

        self.scene.addItem(item)

        self.items[obj.object_id] = item

        return item

    # ---------------------------------
    # Find document object
    # ---------------------------------

    def find_object(self, object_id):

        for layer in self.document.layers:

            obj = layer.find_object(object_id)

            if obj is not None:
                return obj

        return None

    # ---------------------------------
    # Update canvas from document object
    # ---------------------------------

    def update_item_from_object(self, obj):

        item = self.items.get(obj.object_id)

        if item is None:

            raise ValueError(
                "Object is not displayed on the canvas"
            )

        width = mm_to_scene_units(obj.width)
        height = mm_to_scene_units(obj.height)

        if isinstance(item, QGraphicsRectItem):

            item.setRect(
                QRectF(0, 0, width, height)
            )

        elif isinstance(item, QGraphicsEllipseItem):

            item.setRect(
                QRectF(0, 0, width, height)
            )

        elif isinstance(item, QGraphicsTextItem):

            # Text dimensions are controlled by its font and content.
            obj.width = scene_units_to_mm(
                item.boundingRect().width()
            )

            obj.height = scene_units_to_mm(
                item.boundingRect().height()
            )

        item.setPos(
            mm_to_scene_units(obj.x),
            mm_to_scene_units(obj.y)
        )

        item.setRotation(obj.rotation)

        item.update()

    # ---------------------------------
    # Rebuild canvas
    # ---------------------------------

    def rebuild(self):

        self.scene.clear()

        self.items.clear()

        for layer in self.document.layers:

            for obj in layer.objects:

                item = self.create_item(obj)

                flags = (
                    item.GraphicsItemFlag.ItemIsSelectable
                )

                if not layer.locked:

                    flags |= (
                        item.GraphicsItemFlag.ItemIsMovable
                    )

                item.setFlags(flags)

                item.setVisible(layer.visible)

                self.scene.addItem(item)

                self.items[obj.object_id] = item

    # ---------------------------------
    # Synchronize canvas to document
    # ---------------------------------

    def sync_to_document(self):

        for layer in self.document.layers:

            for obj in layer.objects:

                item = self.items.get(obj.object_id)

                if item is None:
                    continue

                obj.x = scene_units_to_mm(
                    item.pos().x()
                )

                obj.y = scene_units_to_mm(
                    item.pos().y()
                )

                obj.rotation = item.rotation()

                if isinstance(item, QGraphicsRectItem):

                    rect = item.rect()

                    obj.width = scene_units_to_mm(
                        rect.width()
                    )

                    obj.height = scene_units_to_mm(
                        rect.height()
                    )

                elif isinstance(item, QGraphicsEllipseItem):

                    rect = item.rect()

                    obj.width = scene_units_to_mm(
                        rect.width()
                    )

                    obj.height = scene_units_to_mm(
                        rect.height()
                    )

                elif isinstance(item, QGraphicsTextItem):

                    obj.width = scene_units_to_mm(
                        item.boundingRect().width()
                    )

                    obj.height = scene_units_to_mm(
                        item.boundingRect().height()
                    )

    # ---------------------------------
    # Layer visibility
    # ---------------------------------

    def set_layer_visibility(self, layer_id, visible):

        layer = self.document.get_layer(layer_id)

        if layer is None:

            raise ValueError(
                "Layer not found"
            )

        layer.visible = visible

        for obj in layer.objects:

            item = self.items.get(obj.object_id)

            if item is not None:
                item.setVisible(visible)

    # ---------------------------------
    # Layer locking
    # ---------------------------------

    def set_layer_locked(self, layer_id, locked):

        layer = self.document.get_layer(layer_id)

        if layer is None:

            raise ValueError(
                "Layer not found"
            )

        layer.locked = locked

        for obj in layer.objects:

            item = self.items.get(obj.object_id)

            if item is None:
                continue

            flags = (
                item.GraphicsItemFlag.ItemIsSelectable
            )

            if not locked:

                flags |= (
                    item.GraphicsItemFlag.ItemIsMovable
                )

            item.setFlags(flags)

