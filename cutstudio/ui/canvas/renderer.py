
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

        # Resize handles are separate from document objects.
        self.resize_handles = {}

    # ---------------------------------
    # Resize Handle Management
    # ---------------------------------

    def clear_resize_handles(self):

        for handle in self.resize_handles.values():
            self.scene.removeItem(handle)

        self.resize_handles.clear()

    def update_resize_handles(self, object_id=None):

        self.clear_resize_handles()

        if object_id is None:
            return

        obj, layer = self.find_object_and_layer(object_id)

        if obj is None or layer is None:
            return

        if layer.locked or obj.object_type == ObjectType.TEXT:
            return

        item = self.items.get(object_id)

        if item is None:
            return

        bounds = item.rect()

        positions = {
            "nw": (bounds.left(), bounds.top()),
            "n": (bounds.center().x(), bounds.top()),
            "ne": (bounds.right(), bounds.top()),
            "e": (bounds.right(), bounds.center().y()),
            "se": (bounds.right(), bounds.bottom()),
            "s": (bounds.center().x(), bounds.bottom()),
            "sw": (bounds.left(), bounds.bottom()),
            "w": (bounds.left(), bounds.center().y()),
        }

        # Rotation handle sits above the top-middle handle.
        positions["rotate"] = (
            bounds.center().x(),
            bounds.top() - 20
        )

        for name, position in positions.items():

            if name == "rotate":

                handle = QGraphicsEllipseItem(
                    QRectF(-5, -5, 10, 10)
                )

                handle.setBrush(
                    QBrush(QColor("#2878c8"))
                )

            else:

                handle = QGraphicsRectItem(
                    QRectF(-4, -4, 8, 8)
                )

                handle.setBrush(
                    QBrush(QColor("#ffffff"))
                )

            pen = QPen(QColor("#2878c8"))
            pen.setWidthF(1)
            handle.setPen(pen)

            handle.setFlag(
                handle.GraphicsItemFlag.ItemIgnoresTransformations,
                True
            )

            handle.setAcceptedMouseButtons(
                Qt.MouseButton.NoButton
            )

            handle.setZValue(10000)

            handle.setPos(item.mapToScene(*position))

            self.scene.addItem(handle)
            self.resize_handles[name] = handle


    # ---------------------------------
    # 1. Create and Add Graphics Items
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

        # Rotate around the visual centre of the object.
        item.setTransformOriginPoint(
            item.boundingRect().center()
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
    # 2. Find Objects and Manage Them
    # ---------------------------------

    def find_object(self, object_id):

        for layer in self.document.layers:

            obj = layer.find_object(object_id)

            if obj is not None:
                return obj

        return None

    def find_object_and_layer(self, object_id):

        for layer in self.document.layers:

            obj = layer.find_object(object_id)

            if obj is not None:
                return obj, layer

        return None, None

    # ---------------------------------
    # 3. Duplicate and Delete Objects
    # ---------------------------------

    def duplicate_objects(
        self,
        object_ids,
        offset_x=5.0,
        offset_y=5.0,
        offset_mm=None
    ):
        """
        Duplicate objects on their original layers.

        Coordinates and offsets are measured in millimetres.

        offset_mm is supported for compatibility with
        MainWindow. When supplied, it sets both X and Y offsets.

        Returns a list of duplicated VectorObjects.
        """

        if offset_mm is not None:

            offset_x = offset_mm
            offset_y = offset_mm

        object_ids = list(dict.fromkeys(object_ids))

        if not object_ids:
            return []

        originals = []

        # Validate the entire selection first.
        for object_id in object_ids:

            obj, layer = self.find_object_and_layer(object_id)

            if obj is None or layer is None:

                raise ValueError(
                    f"Object not found: {object_id}"
                )

            if layer.locked:

                raise RuntimeError(
                    "Cannot duplicate objects from a locked layer"
                )

            originals.append((obj, layer))

        # Create the duplicates.
        duplicates = []

        for original, layer in originals:

            duplicate = original.duplicate(
                offset_x=offset_x,
                offset_y=offset_y
            )

            self.add_object(duplicate, layer)

            duplicates.append(duplicate)

        return duplicates

    def delete_objects(self, object_ids):
        """
        Delete selected objects from their document layers
        and remove their graphics items from the scene.

        The entire operation is rejected if any selected
        object belongs to a locked layer.

        Returns the number of deleted objects.
        """

        object_ids = list(dict.fromkeys(object_ids))

        if not object_ids:
            return 0

        objects_to_delete = []

        # Validate everything before deleting anything.
        for object_id in object_ids:

            obj, layer = self.find_object_and_layer(object_id)

            if obj is None or layer is None:

                raise ValueError(
                    f"Object not found: {object_id}"
                )

            if layer.locked:

                raise RuntimeError(
                    "Cannot delete objects from a locked layer"
                )

            objects_to_delete.append(
                (obj, layer)
            )

        # Perform deletion.
        deleted_count = 0

        for obj, layer in objects_to_delete:

            layer.remove_object(obj.object_id)

            item = self.items.pop(
                obj.object_id,
                None
            )

            if item is not None:

                self.scene.removeItem(item)

            deleted_count += 1

        return deleted_count

    # ---------------------------------
    # 4. Update, Rebuild and Synchronize
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

            obj.width = scene_units_to_mm(
                item.boundingRect().width()
            )

            obj.height = scene_units_to_mm(
                item.boundingRect().height()
            )

        item.setTransformOriginPoint(
            item.boundingRect().center()
        )

        item.setPos(
            mm_to_scene_units(obj.x),
            mm_to_scene_units(obj.y)
        )

        item.setRotation(obj.rotation)

        item.update()

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
    # Layer Visibility
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
    # Layer Locking
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

