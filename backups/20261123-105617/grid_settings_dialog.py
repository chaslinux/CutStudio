
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDialogButtonBox,
    QLabel,
)


class GridSettingsDialog(QDialog):

    INCH_PRESETS = [
        ("1/16 inch", 1 / 16),
        ("1/8 inch", 1 / 8),
        ("1/4 inch", 1 / 4),
        ("1/2 inch", 1 / 2),
        ("1 inch", 1.0),
    ]

    MM_PRESETS = [
        ("1 mm", 1.0),
        ("2 mm", 2.0),
        ("3 mm", 3.0),
        ("5 mm", 5.0),
        ("6.35 mm (1/4 inch)", 6.35),
        ("10 mm", 10.0),
        ("12.7 mm (1/2 inch)", 12.7),
        ("25.4 mm (1 inch)", 25.4),
    ]

    def __init__(self, current_inches, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Grid Settings")
        self.setMinimumWidth(320)

        self.current_inches = current_inches

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Configure the cutting mat grid.")
        )

        form = QFormLayout()

        self.units_combo = QComboBox()
        self.units_combo.addItems([
            "Inches",
            "Millimetres",
        ])

        self.spacing_combo = QComboBox()

        form.addRow("Display units:", self.units_combo)
        form.addRow("Grid spacing:", self.spacing_combo)

        layout.addLayout(form)

        self.units_combo.currentTextChanged.connect(
            self._update_presets
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self._update_presets("Inches")

    def _update_presets(self, units):

        self.spacing_combo.clear()

        presets = (
            self.INCH_PRESETS
            if units == "Inches"
            else self.MM_PRESETS
        )

        for label, value in presets:
            self.spacing_combo.addItem(
                label,
                value
            )

        target = (
            self.current_inches
            if units == "Inches"
            else self.current_inches * 25.4
        )

        closest_index = min(
            range(len(presets)),
            key=lambda i: abs(presets[i][1] - target)
        )

        self.spacing_combo.setCurrentIndex(
            closest_index
        )

    def get_spacing_inches(self):
        value = self.spacing_combo.currentData()

        if self.units_combo.currentText() == "Millimetres":
            return value / 25.4

        return value

