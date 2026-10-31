
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QDialog,
    QWidget,
    QLabel,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QVBoxLayout,
    QDialogButtonBox
)

from ..config import config

class SettingsWindow(QDialog):
    
    def __init__(self, parent: QWidget, config: config.ConfigLoader):
        super().__init__(parent)

        self.config = config
        self.initUi()
        self.loadSettings()

    def initUi(self):
        self.mainlayout = QVBoxLayout(self)

        title = QLabel("<h4>Settings</h4>", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #title.setMaximumHeight(30)

        confirmButtons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        self.showNotifications = QCheckBox("show notifications", self)
        self.minimize = QCheckBox("minimize to tray on start", self)
        self.openRGB = QCheckBox("enable OpenRGB integration", self)
        self.appearance = QComboBox(self)
        self.appearance.addItem("auto (default)", "auto")
        self.appearance.addItem("light", "light")
        self.appearance.addItem("dark", "dark")
        appearanceLayout = QFormLayout()
        appearanceLayout.addRow("Appearance:", self.appearance)

        self.mainlayout.addWidget(title)
        self.mainlayout.addWidget(self.showNotifications)
        self.mainlayout.addWidget(self.minimize)
        self.mainlayout.addWidget(self.openRGB)
        self.mainlayout.addLayout(appearanceLayout)
        self.mainlayout.addWidget(confirmButtons)

        confirmButtons.accepted.connect(self.accept)
        confirmButtons.rejected.connect(self.reject)

    def loadSettings(self):
        self.showNotifications.setChecked(self.config.data.settings.showNotifications)
        self.minimize.setChecked(self.config.data.settings.minimizeOnStart)
        self.openRGB.setChecked(self.config.data.settings.useOpenRGB)
        index = self.appearance.findData(self.config.data.settings.appearance)
        self.appearance.setCurrentIndex(max(0, index))

    def accept(self):
        self.config.data.settings.showNotifications = self.showNotifications.isChecked()
        self.config.data.settings.minimizeOnStart = self.minimize.isChecked()
        self.config.data.settings.useOpenRGB = self.openRGB.isChecked()
        self.config.data.settings.appearance = self.appearance.currentData()
        return super().accept()
