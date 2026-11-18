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


class MatSettingsDialog(QDialog):

    PRESETS = {
        "12 x 12 inches": (304.8, 304.8),
        "12 x 24 inches": (304.8, 609.6),
        "12 x 36 inches": (304.8, 914.4),
        "12 x 48 inches": (304.8, 1219.2),
    }

    def __init__(self, mat_config, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Cutting Mat Settings")
        self.setMinimumWidth(340)

        self._updating = False

        layout = QVBoxLayout(self)

        description = QLabel(
            "Configure the physical cutting mat dimensions."
        )

        layout.addWidget(description)

        form = QFormLayout()

        self.preset_combo = QComboBox()

        self.preset_combo.addItems(
            list(self.PRESETS.keys()) + ["Custom"]
        )

        form.addRow(
            "Mat preset:",
            self.preset_combo
        )

        self.width_input = self._create_dimension_input()
        self.height_input = self._create_dimension_input()

        form.addRow(
            "Width:",
            self.width_input
        )

        form.addRow(
            "Height:",
            self.height_input
        )

        layout.addLayout(form)

        self.preset_combo.currentTextChanged.connect(
            self._preset_changed
        )

        self.width_input.valueChanged.connect(
            self._dimensions_changed
        )

        self.height_input.valueChanged.connect(
            self._dimensions_changed
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.width_input.setValue(mat_config.width_mm)
        self.height_input.setValue(mat_config.height_mm)

        self._select_matching_preset()

    def _create_dimension_input(self):

        spin = QDoubleSpinBox()

        spin.setRange(1.0, 5000.0)
        spin.setDecimals(1)
        spin.setSingleStep(10.0)
        spin.setSuffix(" mm")

        return spin

    def _select_matching_preset(self):

        dimensions = (
            self.width_input.value(),
            self.height_input.value()
        )

        for name, preset in self.PRESETS.items():

            if dimensions == preset:

                self.preset_combo.setCurrentText(name)
                return

        self.preset_combo.setCurrentText("Custom")

    def _preset_changed(self, name):

        if name not in self.PRESETS:
            return

        width, height = self.PRESETS[name]

        self._updating = True

        self.width_input.setValue(width)
        self.height_input.setValue(height)

        self._updating = False

    def _dimensions_changed(self):

        if self._updating:
            return

        self.preset_combo.setCurrentText("Custom")

    def get_mat_config(self):

        return CuttingMatConfig(
            width_mm=self.width_input.value(),
            height_mm=self.height_input.value()
        )
