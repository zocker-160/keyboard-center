
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton

class CEntryButton(QPushButton):

    onSelection = pyqtSignal(int)

    def __init__(self, name: str, position: int, parent=None):
        super().__init__(name, parent)

        self.setFlat(True)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)

        self.postition = position

        self.clicked.connect(self._clickTrigger)

    def _clickTrigger(self):
        print("trigger clicked", self.postition)
        self.onSelection.emit(self.postition)
