
import os
import sys

from PySide6.QtWidgets import QApplication

from cutstudio.core.constants import (
    APP_NAME,
    APP_VERSION,
    ORGANIZATION_NAME,
)

from cutstudio.ui.main_window import MainWindow


def main():

    # Respect Qt's automatic platform detection.
    # Avoid forcing X11 or Wayland.

    os.environ.setdefault(
        "QT_QPA_PLATFORMTHEME",
        "generic"
    )

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setApplicationVersion(APP_VERSION)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

