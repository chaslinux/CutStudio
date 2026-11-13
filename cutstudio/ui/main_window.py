# ============================================================
# CUTSTUDIO
# Main Application Window
#
# SECTION 1 OF 4
# Imports, initialization, menus and toolbar
# ============================================================


# ------------------------------------------------------------
# PySide6 imports
# ------------------------------------------------------------

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QAction, QKeySequence

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGraphicsScene,
    QVBoxLayout,
    QToolBar,
    QDockWidget,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QStatusBar,
    QGraphicsView,
    QFormLayout,
    QDoubleSpinBox,
    QFileDialog,
    QMessageBox,
)


# ------------------------------------------------------------
# CutStudio core imports
# ------------------------------------------------------------

from cutstudio.core.constants import MAT_INCHES
from cutstudio.core.document import Document
from cutstudio.core.history import UndoHistory
from cutstudio.core.objects import ObjectType, VectorObject
from cutstudio.core.project_file import (
    ProjectFileError,
    load_project,
    save_project,
)
from cutstudio.core.units import mm_to_scene_units

# ------------------------------------------------------------
# Canvas imports
# ------------------------------------------------------------

from cutstudio.ui.canvas.cutting_mat import CuttingMat
from cutstudio.ui.canvas.renderer import CanvasRenderer


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "CutStudio - Design Workspace"
        )

        self.resize(1400, 900)

        # ----------------------------------------------------
        # Document model
        # ----------------------------------------------------

        self.document = Document()
        self.history = UndoHistory(self.document)

        # ----------------------------------------------------
        # Project file tracking
        # ----------------------------------------------------

        self.current_filename = None
        self.document_modified = False

        self.update_window_title()

        # ----------------------------------------------------
        # Graphics scene
        # ----------------------------------------------------

        self.scene = QGraphicsScene(self)

        self.scene.setSceneRect(
            QRectF(
                0,
                0,
                mm_to_scene_units(
                    self.document.width_mm
                ),
                mm_to_scene_units(
                    self.document.height_mm
                ),
            )
        )

        # ----------------------------------------------------
        # Canvas renderer
        # ----------------------------------------------------

        self.renderer = CanvasRenderer(
            self.document,
            self.scene
        )

        # ----------------------------------------------------
        # Cutting mat
        # ----------------------------------------------------

        self.canvas = CuttingMat(
            self.scene,
            self.renderer
        )

        self.setCentralWidget(self.canvas)

        # ----------------------------------------------------
        # Signals
        # ----------------------------------------------------

        self.scene.selectionChanged.connect(
            self.update_properties
        )

        self.canvas.objects_positions_changed.connect(
            self.on_objects_positions_changed
        )

        # ----------------------------------------------------
        # Build interface
        # ----------------------------------------------------

        self.create_menu()

        self.create_toolbar()

        self.create_left_panel()

        self.create_right_panel()

        self.create_status_bar()

        # ----------------------------------------------------
        # Initial canvas positioning
        # ----------------------------------------------------

        self.canvas.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        # ----------------------------------------------------
        # Keyboard shortcuts
        # ----------------------------------------------------

        self.create_keyboard_shortcuts()


# ---------------------------------
# Project state
# ---------------------------------

    def update_window_title(self):

        filename = (
            self.current_filename
            if self.current_filename
            else "Untitled"
        )

        modified = "*" if self.document_modified else ""

        self.setWindowTitle(
            f"CutStudio - {filename}{modified}"
        )

    def mark_modified(self):

        if not self.document_modified:

            self.document_modified = True

            self.update_window_title()


    def update_history_actions(self):

        if not hasattr(self, "undo_action"):
            return

        self.undo_action.setEnabled(
            self.history.can_undo
        )

        self.redo_action.setEnabled(
            self.history.can_redo
        )

    def record_history(self):

        if self.history.record(self.document):
            self.mark_modified()

        self.update_history_actions()

    def undo(self):

        document = self.history.undo()

        if document is not None:
            self.restore_document(document)

    def redo(self):

        document = self.history.redo()

        if document is not None:
            self.restore_document(document)

    def restore_document(self, document):

        self.document = document
        self.renderer.document = document

        self.scene.clearSelection()

        self.scene.setSceneRect(
            QRectF(
                0,
                0,
                mm_to_scene_units(document.width_mm),
                mm_to_scene_units(document.height_mm),
            )
        )

        self.renderer.rebuild()

        self.refresh_layer_list()
        self.clear_properties()
        self.update_properties()

        self.mark_modified()
        self.update_history_actions()

        self.statusBar().showMessage(
            "Document restored"
        )


    def on_objects_positions_changed(self):

        self.record_history()

        self.update_properties()


# ============================================================
# SECTION 1A: MENU BAR
# ============================================================


    def create_menu(self):

        menu_bar = self.menuBar()

        # ---------------------------------
        # File menu
        # ---------------------------------

        file_menu = menu_bar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("Open...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As...", self)
        save_as_action.setShortcut(
            QKeySequence.StandardKey.SaveAs
        )
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)

        # ---------------------------------
        # Other menus
        # ---------------------------------

        edit_menu = menu_bar.addMenu("Edit")

        self.edit_menu = edit_menu

        for name in ("View", "Machine", "Help"):
            menu_bar.addMenu(name)

        # Objects menu
        self.object_menu = menu_bar.addMenu("Objects")

    # ---------------------------------
    # Project file operations
    # ---------------------------------

    def confirm_unsaved_changes(self):

        if not self.document_modified:
            return True

        answer = QMessageBox.question(
            self,
            "Unsaved Changes",
            "This project has unsaved changes.\n"
            "Would you like to save them?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )

        if answer == QMessageBox.StandardButton.Save:
            return self.save_project()

        if answer == QMessageBox.StandardButton.Discard:
            return True

        return False

    def new_project(self):

        if not self.confirm_unsaved_changes():
            return

        self.document = Document()
        self.history.clear(self.document)
        self.update_history_actions()

        self.renderer.document = self.document

        self.current_filename = None
        self.document_modified = False

        self.scene.setSceneRect(
            QRectF(
                0,
                0,
                mm_to_scene_units(self.document.width_mm),
                mm_to_scene_units(self.document.height_mm),
            )
        )

        self.renderer.rebuild()

        self.refresh_layer_list()
        self.update_properties()
        self.update_window_title()

        self.statusBar().showMessage(
            "New project created"
        )

    def open_project(self):

        if not self.confirm_unsaved_changes():
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open CutStudio Project",
            "",
            "CutStudio Projects (*.cutstudio);;JSON Files (*.json)"
        )

        if not filename:
            return

        try:

            document = load_project(filename)

            self.document = document
            self.history.clear(document)
            self.update_history_actions()
            self.renderer.document = document

            self.current_filename = filename
            self.document_modified = False

            self.scene.setSceneRect(
                QRectF(
                    0,
                    0,
                    mm_to_scene_units(document.width_mm),
                    mm_to_scene_units(document.height_mm),
                )
            )

            self.renderer.rebuild()

            self.refresh_layer_list()
            self.update_properties()
            self.update_window_title()

            self.statusBar().showMessage(
                f"Opened {filename}"
            )

        except ProjectFileError as error:

            QMessageBox.critical(
                self,
                "Open Failed",
                str(error)
            )

    def save_project(self):

        if not self.current_filename:
            return self.save_project_as()

        try:

            self.renderer.sync_to_document()

            save_project(
                self.document,
                self.current_filename
            )

            self.document_modified = False

            self.update_window_title()

            self.statusBar().showMessage(
                "Project saved successfully"
            )

            return True

        except ProjectFileError as error:

            QMessageBox.critical(
                self,
                "Save Failed",
                str(error)
            )

            return False

    def save_project_as(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save CutStudio Project",
            "",
            "CutStudio Projects (*.cutstudio)"
        )

        if not filename:
            return False

        if not filename.lower().endswith(".cutstudio"):
            filename += ".cutstudio"

        previous_filename = self.current_filename

        self.current_filename = filename

        if not self.save_project():

            self.current_filename = previous_filename
            self.update_window_title()

            return False

        return True

# ============================================================
# SECTION 1B: MAIN TOOLBAR
# ============================================================

    def create_toolbar(self):

        toolbar = QToolBar("Main Toolbar")

        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        actions = [
            ("Select", self.select_tool),
            ("Rectangle", self.add_rectangle),
            ("Ellipse", self.add_ellipse),
            ("Text", self.add_text),
        ]

        for label, callback in actions:

            action = QAction(label, self)

            action.triggered.connect(callback)

            toolbar.addAction(action)


# ============================================================
# SECTION 1C: KEYBOARD SHORTCUT REGISTRATION
# ============================================================

    def create_keyboard_shortcuts(self):

        # Actual shortcut actions will be connected to
        # the editing methods implemented in later sections.

        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut(
            QKeySequence.StandardKey.Undo
        )
        self.undo_action.triggered.connect(self.undo)
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut(
            QKeySequence.StandardKey.Redo
        )
        self.redo_action.triggered.connect(self.redo)
        self.edit_menu.addAction(self.redo_action)

        self.update_history_actions()

        self.duplicate_action = QAction(
            "Duplicate",
            self
        )

        self.duplicate_action.setShortcut(
            QKeySequence("Ctrl+D")
        )

        self.duplicate_action.triggered.connect(
            self.duplicate_selected_objects
        )

        self.object_menu.addAction(
            self.duplicate_action
        )

        self.delete_action = QAction(
            "Delete",
            self
        )

        self.delete_action.setShortcut(
            QKeySequence(Qt.Key.Key_Delete)
        )

        self.delete_action.triggered.connect(
            self.delete_selected_objects
        )

        self.object_menu.addAction(
            self.delete_action
        )

# ============================================================
# SECTION 2 OF 4
# Drawing Tools Panel
# Properties Panel
# Layer Management
# ============================================================


# ============================================================
# SECTION 2A: LEFT DRAWING TOOLS PANEL
# ============================================================

    def create_left_panel(self):

        dock = QDockWidget(
            "Drawing Tools",
            self
        )

        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
        )

        panel = QWidget()

        layout = QVBoxLayout(panel)

        tools = [
            ("Select", self.select_tool),
            ("Rectangle", self.add_rectangle),
            ("Ellipse", self.add_ellipse),
            ("Text", self.add_text),
        ]

        for label, callback in tools:

            button = QPushButton(label)

            button.clicked.connect(callback)

            layout.addWidget(button)

        layout.addStretch()

        dock.setWidget(panel)

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            dock
        )


# ============================================================
# SECTION 2B: RIGHT PROPERTIES AND LAYERS PANEL
# ============================================================

    def create_right_panel(self):

        dock = QDockWidget(
            "Properties / Layers",
            self
        )

        dock.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea
        )

        panel = QWidget()

        layout = QVBoxLayout(panel)

        layout.addWidget(
            QLabel("Object Properties")
        )

        self.property_values = {}

        self.property_inputs = {}

        form = QFormLayout()

        # ----------------------------------------------------
        # Object type
        # ----------------------------------------------------

        self.property_values["type"] = QLabel("—")

        form.addRow(
            "Type",
            self.property_values["type"]
        )

        # ----------------------------------------------------
        # Editable numerical properties
        # ----------------------------------------------------

        properties = [
            ("X (mm)", "x", -1000000, 1000000),
            ("Y (mm)", "y", -1000000, 1000000),
            ("Width (mm)", "width", 0.01, 1000000),
            ("Height (mm)", "height", 0.01, 1000000),
            (
                "Rotation (degrees)",
                "rotation",
                -360000,
                360000
            ),
        ]

        for label, key, minimum, maximum in properties:

            spinbox = QDoubleSpinBox()

            spinbox.setRange(
                minimum,
                maximum
            )

            spinbox.setDecimals(2)

            spinbox.setSingleStep(
                1.0 if key != "rotation" else 5.0
            )

            spinbox.setKeyboardTracking(False)

            spinbox.setEnabled(False)

            spinbox.editingFinished.connect(
                lambda property_key=key:
                    self.apply_property(property_key)
            )

            self.property_inputs[key] = spinbox

            form.addRow(
                label,
                spinbox
            )

        layout.addLayout(form)

        layout.addSpacing(15)

        # ----------------------------------------------------
        # Layer management
        # ----------------------------------------------------

        layout.addWidget(
            QLabel("Layers")
        )

        self.layer_list = QListWidget()

        self.layer_list.itemChanged.connect(
            self.on_layer_visibility_changed
        )

        self.layer_list.currentItemChanged.connect(
            self.on_layer_selected
        )

        layout.addWidget(
            self.layer_list
        )

        self.lock_button = QPushButton(
            "Lock Active Layer"
        )

        self.lock_button.clicked.connect(
            self.toggle_active_layer_lock
        )

        layout.addWidget(
            self.lock_button
        )

        self.refresh_layer_list()

        dock.setWidget(panel)

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock
        )

        self.update_properties()


# ============================================================
# SECTION 2C: REFRESH LAYER LIST
# ============================================================

    def refresh_layer_list(self):

        self.layer_list.blockSignals(True)

        self.layer_list.clear()

        for layer in self.document.layers:

            item = QListWidgetItem(
                layer.name
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                layer.layer_id
            )

            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsSelectable
            )

            item.setCheckState(
                Qt.CheckState.Checked
                if layer.visible
                else Qt.CheckState.Unchecked
            )

            self.layer_list.addItem(item)

            if (
                layer.layer_id
                == self.document.active_layer_id
            ):

                self.layer_list.setCurrentItem(item)

        self.layer_list.blockSignals(False)

        self.update_lock_button()


# ============================================================
# SECTION 2D: UPDATE LAYER LOCK BUTTON
# ============================================================

    def update_lock_button(self):

        layer = self.document.active_layer

        if layer is None:
            return

        self.lock_button.setText(
            "Unlock Active Layer"
            if layer.locked
            else "Lock Active Layer"
        )


# ============================================================
# SECTION 2E: LAYER VISIBILITY
# ============================================================

    def on_layer_visibility_changed(self, item):

        layer_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        visible = (
            item.checkState()
            == Qt.CheckState.Checked
        )

        self.renderer.set_layer_visibility(
            layer_id,
            visible
        )

        self.record_history()

        self.update_properties()


# ============================================================
# SECTION 2F: ACTIVE LAYER SELECTION
# ============================================================

    def on_layer_selected(self, current, previous):

        if current is None:
            return

        layer_id = current.data(
            Qt.ItemDataRole.UserRole
        )

        self.document.set_active_layer(
            layer_id
        )

        self.update_lock_button()


# ============================================================
# SECTION 2G: TOGGLE ACTIVE LAYER LOCK
# ============================================================

    def toggle_active_layer_lock(self):

        layer = self.document.active_layer

        if layer is None:
            return

        self.renderer.set_layer_locked(
            layer.layer_id,
            not layer.locked
        )

        self.record_history()

        self.update_lock_button()

        self.update_properties()

# ============================================================
# SECTION 3 OF 4
# Object Lookup
# Object Properties
# Selection Handling
# Property Editing
# ============================================================


# ============================================================
# SECTION 3A: FIND OBJECT AND OWNING LAYER
# ============================================================

    def find_object_and_layer(self, object_id):

        for layer in self.document.layers:

            obj = layer.find_object(object_id)

            if obj is not None:

                return obj, layer

        return None, None


# ============================================================
# SECTION 3B: CLEAR OBJECT PROPERTIES
# ============================================================

    def clear_properties(self):

        self.property_values["type"].setText("—")

        for spinbox in self.property_inputs.values():

            spinbox.blockSignals(True)

            spinbox.setValue(0)

            spinbox.setEnabled(False)

            spinbox.blockSignals(False)


# ============================================================
# SECTION 3C: UPDATE OBJECT PROPERTIES
# ============================================================

    def update_properties(self):

        selected_items = self.scene.selectedItems()

        if not selected_items:

            self.renderer.clear_resize_handles()

            self.clear_properties()

            return

        item = selected_items[0]

        object_id = item.data(
            CanvasRenderer.OBJECT_ID_ROLE
        )

        if object_id is None:

            self.renderer.clear_resize_handles()

            self.clear_properties()

            return

        self.renderer.update_resize_handles(object_id)

        # Synchronize canvas positions with document model.
        self.renderer.sync_to_document()

        obj, layer = self.find_object_and_layer(
            object_id
        )

        if obj is None or layer is None:

            self.clear_properties()

            return

        self.property_values["type"].setText(
            obj.object_type.value.capitalize()
        )

        values = {
            "x": obj.x,
            "y": obj.y,
            "width": obj.width,
            "height": obj.height,
            "rotation": obj.rotation,
        }

        editable = not layer.locked

        for key, value in values.items():

            spinbox = self.property_inputs[key]

            spinbox.blockSignals(True)

            spinbox.setValue(value)

            # Text dimensions are controlled by font and content.
            # Font editing will be implemented in a later phase.
            if (
                obj.object_type == ObjectType.TEXT
                and key in ("width", "height")
            ):

                spinbox.setEnabled(False)

            else:

                spinbox.setEnabled(editable)

            spinbox.blockSignals(False)


# ============================================================
# SECTION 3D: APPLY OBJECT PROPERTY CHANGES
# ============================================================

    def apply_property(self, key):

        selected_items = self.scene.selectedItems()

        if len(selected_items) != 1:

            return

        item = selected_items[0]

        object_id = item.data(
            CanvasRenderer.OBJECT_ID_ROLE
        )

        if object_id is None:

            return

        self.renderer.sync_to_document()

        obj, layer = self.find_object_and_layer(
            object_id
        )

        if obj is None or layer is None:

            return

        # Prevent editing objects on locked layers.
        if layer.locked:

            self.update_properties()

            return

        # Text dimensions are not directly editable.
        if (
            obj.object_type == ObjectType.TEXT
            and key in ("width", "height")
        ):

            return

        value = self.property_inputs[key].value()

        # Reject zero or negative object dimensions.
        if key in ("width", "height") and value <= 0:

            self.update_properties()

            return

        old_value = getattr(obj, key)

        if value == old_value:
            return

        setattr(obj, key, value)

        try:

            obj.validate()

            self.renderer.update_item_from_object(
                obj
            )

            self.renderer.sync_to_document()

            self.record_history()

            self.statusBar().showMessage(
                f"Updated {key}: {value:.2f}"
            )

        except (ValueError, RuntimeError) as error:

            # Restore the previous model value.
            setattr(obj, key, old_value)

            self.renderer.update_item_from_object(
                obj
            )

            self.statusBar().showMessage(
                f"Could not update property: {error}"
            )

        self.update_properties()


# ============================================================
# SECTION 3E: STATUS BAR
# ============================================================

    def create_status_bar(self):

        status = QStatusBar()

        status.showMessage(
            f"Ready | {MAT_INCHES} x {MAT_INCHES} inch mat | "
            "Ctrl + mouse wheel to zoom"
        )

        self.setStatusBar(status)

# ============================================================
# CUTSTUDIO
# SECTION 4 OF 4
# Object Duplication
# Object Deletion
# Selection Management
# Drawing Tools
# ============================================================


# ============================================================
# SECTION 4A: SELECT TOOL
# ============================================================

    def select_tool(self):

        self.canvas.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )


# ============================================================
# SECTION 4B: DUPLICATE SELECTED OBJECTS
# ============================================================

    def duplicate_selected_objects(self):

        selected_items = self.scene.selectedItems()

        if not selected_items:

            self.statusBar().showMessage(
                "No objects selected for duplication"
            )

            return

        # Collect selected object IDs.
        object_ids = []

        for item in selected_items:

            object_id = item.data(
                CanvasRenderer.OBJECT_ID_ROLE
            )

            if object_id is not None:
                object_ids.append(object_id)

        if not object_ids:
            return

        # Synchronize canvas positions before duplication.
        self.renderer.sync_to_document()

        try:

            duplicated = self.renderer.duplicate_objects(
                object_ids,
                offset_mm=5.0
            )

        except (ValueError, RuntimeError) as error:

            self.statusBar().showMessage(
                f"Could not duplicate objects: {error}"
            )

            return

        # Select the newly duplicated objects.
        self.scene.clearSelection()

        for obj in duplicated:

            item = self.renderer.items.get(
                obj.object_id
            )

            if item is not None:
                item.setSelected(True)

        self.update_properties()

        self.record_history()

        self.statusBar().showMessage(
            f"Duplicated {len(duplicated)} object(s)"
        )


# ============================================================
# SECTION 4C: DELETE SELECTED OBJECTS
# ============================================================

    def delete_selected_objects(self):

        selected_items = self.scene.selectedItems()

        if not selected_items:

            self.statusBar().showMessage(
                "No objects selected for deletion"
            )

            return

        # Collect selected object IDs.
        object_ids = []

        for item in selected_items:

            object_id = item.data(
                CanvasRenderer.OBJECT_ID_ROLE
            )

            if object_id is not None:
                object_ids.append(object_id)

        if not object_ids:
            return

        # Synchronize document positions first.
        self.renderer.sync_to_document()

        try:

            deleted_count = self.renderer.delete_objects(
                object_ids
            )

        except (ValueError, RuntimeError) as error:

            self.statusBar().showMessage(
                f"Could not delete objects: {error}"
            )

            return

        self.clear_properties()

        self.record_history()

        self.statusBar().showMessage(
            f"Deleted {deleted_count} object(s)"
        )


# ============================================================
# SECTION 4D: GET OBJECT POSITION
# ============================================================

    def get_object_position(
        self,
        width_mm=0,
        height_mm=0
    ):

        center = self.canvas.mapToScene(
            self.canvas.viewport().rect().center()
        )

        return (
            center.x()
            - mm_to_scene_units(width_mm) / 2,

            center.y()
            - mm_to_scene_units(height_mm) / 2,
        )


# ============================================================
# SECTION 4E: ADD RECTANGLE
# ============================================================

    def add_rectangle(self):


        layer = self.document.active_layer

        if layer.locked:

            self.statusBar().showMessage(
                "Cannot draw on a locked layer"
            )

            return

        width = 100 * 25.4 / 96
        height = 100 * 25.4 / 96

        x, y = self.get_object_position(
            width,
            height
        )

        obj = VectorObject(
            object_type=ObjectType.RECTANGLE,

            x=x * 25.4 / 96,
            y=y * 25.4 / 96,

            width=width,
            height=height,

            stroke="#222222",
            stroke_width=2 * 25.4 / 96,
        )

        self.renderer.add_object(
            obj,
            layer
        )

        self.scene.clearSelection()

        self.renderer.items[
            obj.object_id
        ].setSelected(True)

        self.record_history()


# ============================================================
# SECTION 4F: ADD ELLIPSE
# ============================================================

    def add_ellipse(self):

        layer = self.document.active_layer

        if layer.locked:

            self.statusBar().showMessage(
                "Cannot draw on a locked layer"
            )

            return

        width = 100 * 25.4 / 96
        height = 100 * 25.4 / 96

        x, y = self.get_object_position(
            width,
            height
        )

        obj = VectorObject(
            object_type=ObjectType.ELLIPSE,

            x=x * 25.4 / 96,
            y=y * 25.4 / 96,

            width=width,
            height=height,

            stroke="#222222",
            stroke_width=2 * 25.4 / 96,
        )

        self.renderer.add_object(
            obj,
            layer
        )

        self.scene.clearSelection()

        self.renderer.items[
            obj.object_id
        ].setSelected(True)

        self.record_history()


# ============================================================
# SECTION 4G: ADD TEXT
# ============================================================

    def add_text(self):

        layer = self.document.active_layer

        if layer.locked:

            self.statusBar().showMessage(
                "Cannot add text to a locked layer"
            )

            return

        x, y = self.get_object_position()

        obj = VectorObject(
            object_type=ObjectType.TEXT,

            x=x * 25.4 / 96,
            y=y * 25.4 / 96,

            text="CutStudio",

            font_family="DejaVu Sans",
            font_size=12.7,

            stroke="#222222",
        )

        self.renderer.add_object(
            obj,
            layer
        )

        self.scene.clearSelection()

        self.renderer.items[
            obj.object_id
        ].setSelected(True)

        self.record_history()


# ============================================================
# END OF MAIN WINDOW
# ============================================================

