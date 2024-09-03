from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QWidget

from enum import Enum

class CEntryButton(QPushButton):

    onSelection = pyqtSignal(Enum)

    def __init__(self, parent: QWidget, key: Enum, vert=False):
        super().__init__(key.name, parent)

        self.setFlat(True)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if vert:
            self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        else:
            self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.key = key
        self.clicked.connect(self.onClick)

    def onClick(self):
        #print("clicked", self.key)
        self.onSelection.emit(self.key)
