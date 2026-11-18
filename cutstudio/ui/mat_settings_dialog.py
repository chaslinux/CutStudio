from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QDialogButtonBox,
    QLabel,
)

from cutstudio.core.mat import CuttingMatConfig


MM_PER_INCH = 25.4


class CustomMatSizeDialog(QDialog):
    """Dialog for entering custom cutting mat dimensions in inches."""

    def __init__(self, width_mm, height_mm, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Custom Cutting Mat Size")
        self.setMinimumWidth(340)

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Enter your custom cutting mat dimensions.")
        )

        form = QFormLayout()

        self.width_input = self._create_dimension_input()
        self.height_input = self._create_dimension_input()

        self.width_input.setValue(width_mm / MM_PER_INCH)
        self.height_input.setValue(height_mm / MM_PER_INCH)

        form.addRow("Width:", self.width_input)
        form.addRow("Height:", self.height_input)

        layout.addLayout(form)

        self.metric_label = QLabel()
        layout.addWidget(self.metric_label)

        self.width_input.valueChanged.connect(self._update_metric)
        self.height_input.valueChanged.connect(self._update_metric)

        self._update_metric()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _create_dimension_input(self):

        spin = QDoubleSpinBox()

        spin.setRange(0.01, 999999.99)
        spin.setDecimals(2)
        spin.setSingleStep(0.25)
        spin.setSuffix(" inches")

        return spin

    def _update_metric(self):

        width_mm = self.width_input.value() * MM_PER_INCH
        height_mm = self.height_input.value() * MM_PER_INCH

        self.metric_label.setText(
            f"Metric: {width_mm:.1f} x {height_mm:.1f} mm"
        )

    def get_dimensions_mm(self):

        return (
            self.width_input.value() * MM_PER_INCH,
            self.height_input.value() * MM_PER_INCH,
        )


class MatSettingsDialog(QDialog):

    PRESETS = {
        "12 x 12 inches": (304.8, 304.8),
        "12 x 24 inches": (304.8, 609.6),
        "12 x 36 inches": (304.8, 914.4),
        "12 x 48 inches": (304.8, 1219.2),
    }

    CUSTOM_OPTION = "Custom Size..."

    def __init__(self, mat_config, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Cutting Mat Settings")
        self.setMinimumWidth(340)

        self._width_mm = mat_config.width_mm
        self._height_mm = mat_config.height_mm

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel("Select your cutting mat size.")
        )

        form = QFormLayout()

        self.preset_combo = QComboBox()

        self.preset_combo.addItems(
            list(self.PRESETS.keys()) + [self.CUSTOM_OPTION]
        )

        form.addRow("Mat size:", self.preset_combo)

        layout.addLayout(form)

        self.dimensions_label = QLabel()
        layout.addWidget(self.dimensions_label)

        self.preset_combo.currentTextChanged.connect(
            self._preset_changed
        )

        self._select_matching_preset()
        self._update_dimensions_label()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def _select_matching_preset(self):

        dimensions = (self._width_mm, self._height_mm)

        for name, preset in self.PRESETS.items():

            if all(
                abs(a - b) < 0.01
                for a, b in zip(dimensions, preset)
            ):
                self.preset_combo.setCurrentText(name)
                return

        self.preset_combo.setCurrentText(self.CUSTOM_OPTION)

    def _preset_changed(self, name):

        if name in self.PRESETS:

            self._width_mm, self._height_mm = self.PRESETS[name]

            self._update_dimensions_label()
            return

        if name != self.CUSTOM_OPTION:
            return

        dialog = CustomMatSizeDialog(
            self._width_mm,
            self._height_mm,
            self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:

            self._width_mm, self._height_mm = (
                dialog.get_dimensions_mm()
            )

            self._update_dimensions_label()

        else:

            self._select_matching_preset()

    def _update_dimensions_label(self):

        width_inches = self._width_mm / MM_PER_INCH
        height_inches = self._height_mm / MM_PER_INCH

        self.dimensions_label.setText(
            f"Selected mat: "
            f"{width_inches:g} x {height_inches:g} inches"
        )

    def get_mat_config(self):

        return CuttingMatConfig(
            width_mm=self._width_mm,
            height_mm=self._height_mm
        )
