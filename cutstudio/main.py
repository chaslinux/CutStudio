
import os
import sys

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QDockWidget,
    QListWidget,
    QLabel,
    QPushButton,
    QStatusBar,
)


APP_NAME = "CutStudio"

MAT_INCHES = 12
UNITS_PER_INCH = 96
MAT_SIZE = MAT_INCHES * UNITS_PER_INCH


class CuttingMat(QGraphicsView):

    def __init__(self, scene):
        super().__init__(scene)

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

        mat = QRectF(
            0, 0, MAT_SIZE, MAT_SIZE
        )

        painter.fillRect(
            mat,
            QColor("#ffffff")
        )

        # Draw one-inch grid.
        grid_pen = QPen(
            QColor("#dedede")
        )

        grid_pen.setWidthF(0)
        painter.setPen(grid_pen)

        for x in range(
            0, MAT_SIZE + 1, UNITS_PER_INCH
        ):
            painter.drawLine(
                x, 0, x, MAT_SIZE
            )

        for y in range(
            0, MAT_SIZE + 1, UNITS_PER_INCH
        ):
            painter.drawLine(
                0, y, MAT_SIZE, y
            )

        # Mat boundary.
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


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "CutStudio - Design Workspace"
        )

        self.resize(1400, 900)

        self.scene = QGraphicsScene(self)

        self.scene.setSceneRect(
            QRectF(
                0,
                0,
                MAT_SIZE,
                MAT_SIZE
            )
        )

        self.canvas = CuttingMat(
            self.scene
        )

        self.setCentralWidget(
            self.canvas
        )

        self.create_menu()
        self.create_toolbar()
        self.create_left_panel()
        self.create_right_panel()
        self.create_status_bar()

        self.canvas.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    # ---------------------------------
    # Menu bar
    # ---------------------------------

    def create_menu(self):

        menu_bar = self.menuBar()

        menus = [
            "File",
            "Edit",
            "View",
            "Objects",
            "Machine",
            "Help",
        ]

        for name in menus:
            menu_bar.addMenu(name)

    # ---------------------------------
    # Main toolbar
    # ---------------------------------

    def create_toolbar(self):

        toolbar = QToolBar(
            "Main Toolbar"
        )

        toolbar.setMovable(False)

        self.addToolBar(toolbar)

        actions = [
            ("Select", self.select_tool),
            ("Rectangle", self.add_rectangle),
            ("Ellipse", self.add_ellipse),
            ("Text", self.add_text),
        ]

        for label, callback in actions:

            action = QAction(
                label,
                self
            )

            action.triggered.connect(
                callback
            )

            toolbar.addAction(action)

    # ---------------------------------
    # Left tool panel
    # ---------------------------------

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

            button.clicked.connect(
                callback
            )

            layout.addWidget(button)

        layout.addStretch()

        dock.setWidget(panel)

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            dock
        )

    # ---------------------------------
    # Right properties and layers
    # ---------------------------------

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

        layout.addWidget(
            QLabel("Select an object to view its properties.")
        )

        layout.addWidget(
            QLabel("Layers")
        )

        self.layer_list = QListWidget()

        self.layer_list.addItem(
            "Layer 1"
        )

        layout.addWidget(
            self.layer_list
        )

        dock.setWidget(panel)

        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            dock
        )

    # ---------------------------------
    # Status bar
    # ---------------------------------

    def create_status_bar(self):

        status = QStatusBar()

        status.showMessage(
            "Ready | 12 x 12 inch mat | "
            "Ctrl + mouse wheel to zoom"
        )

        self.setStatusBar(status)

    # ---------------------------------
    # Drawing tools
    # ---------------------------------

    def select_tool(self):

        self.canvas.setDragMode(
            QGraphicsView.DragMode.RubberBandDrag
        )

    def add_rectangle(self):

        size = 100

        item = QGraphicsRectItem(
            QRectF(
                -size / 2,
                -size / 2,
                size,
                size
            )
        )

        item.setPen(
            QPen(QColor("#222222"), 2)
        )

        item.setFlags(
            item.GraphicsItemFlag.ItemIsMovable
            | item.GraphicsItemFlag.ItemIsSelectable
        )

        item.setPos(
            self.canvas.mapToScene(
                self.canvas.viewport().rect().center()
            )
        )

        self.scene.addItem(item)

    def add_ellipse(self):

        size = 100

        item = QGraphicsEllipseItem(
            QRectF(
                -size / 2,
                -size / 2,
                size,
                size
            )
        )

        item.setPen(
            QPen(QColor("#222222"), 2)
        )

        item.setFlags(
            item.GraphicsItemFlag.ItemIsMovable
            | item.GraphicsItemFlag.ItemIsSelectable
        )

        item.setPos(
            self.canvas.mapToScene(
                self.canvas.viewport().rect().center()
            )
        )

        self.scene.addItem(item)

    def add_text(self):

        item = QGraphicsTextItem(
            "CutStudio"
        )

        item.setFont(
            QFont("DejaVu Sans", 36)
        )

        item.setDefaultTextColor(
            QColor("#222222")
        )

        item.setFlags(
            item.GraphicsItemFlag.ItemIsMovable
            | item.GraphicsItemFlag.ItemIsSelectable
        )

        item.setPos(
            self.canvas.mapToScene(
                self.canvas.viewport().rect().center()
            )
        )

        self.scene.addItem(item)


def main():

    # Use Qt's automatic platform detection.
    # Do not force X11 or Wayland.

    # Avoid problematic desktop-specific Qt theme plugins.
    # Respect an explicitly configured user environment.
    os.environ.setdefault(
        "QT_QPA_PLATFORMTHEME",
        "generic"
    )

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setOrganizationName("CutStudio")
    app.setApplicationVersion("0.1.0")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
