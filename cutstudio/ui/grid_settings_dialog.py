import math

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QDialogButtonBox,
    QLabel,
)


MM_PER_INCH = 25.4

MAJOR_INTERVAL_OPTIONS = [2, 4, 5, 10]


class GridSettingsDialog(QDialog):
    """Configure grid spacing and major grid line intervals."""

    def __init__(
        self,
        spacing_mm=6.35,
        major_interval=4,
        parent=None
    ):
        super().__init__(parent)

        if (
            not isinstance(spacing_mm, (int, float))
            or not math.isfinite(spacing_mm)
            or spacing_mm <= 0
        ):
            raise ValueError(
                "Grid spacing must be a positive finite number."
            )

        if (
            isinstance(major_interval, bool)
            or not isinstance(major_interval, int)
            or major_interval not in MAJOR_INTERVAL_OPTIONS
        ):
            raise ValueError("Invalid major grid interval.")

        self.setWindowTitle("Grid Settings")
        self.setMinimumWidth(340)

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel("Configure the cutting mat grid.")
        )

        form = QFormLayout()

        self.units_combo = QComboBox()
        self.units_combo.addItems([
            "Millimetres",
            "Inches",
        ])

        self.spacing_input = QDoubleSpinBox()
        self.spacing_input.setRange(0.0001, 999999.0)
        self.spacing_input.setDecimals(4)
        self.spacing_input.setSingleStep(1.0)
        self.spacing_input.setValue(spacing_mm)

        self.major_interval_combo = QComboBox()

        for interval in MAJOR_INTERVAL_OPTIONS:
            self.major_interval_combo.addItem(
                f"Every {interval} minor lines",
                interval
            )

        self.major_interval_combo.setCurrentIndex(
            self.major_interval_combo.findData(major_interval)
        )

        form.addRow("Units:", self.units_combo)
        form.addRow("Minor grid spacing:", self.spacing_input)
        form.addRow(
            "Major line interval:",
            self.major_interval_combo
        )

        layout.addLayout(form)

        self.units_combo.currentTextChanged.connect(
            self._units_changed
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _units_changed(self, units):
        current_value = self.spacing_input.value()

        if units == "Inches":
            converted = current_value / MM_PER_INCH
            self.spacing_input.setSingleStep(0.0625)
        else:
            converted = current_value * MM_PER_INCH
            self.spacing_input.setSingleStep(1.0)

        self.spacing_input.setValue(converted)

    def get_settings(self):
        spacing = self.spacing_input.value()

        if self.units_combo.currentText() == "Inches":
            spacing *= MM_PER_INCH

        return (
            spacing,
            self.major_interval_combo.currentData()
        )
