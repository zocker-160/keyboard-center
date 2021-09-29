
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QSizePolicy

class CEntryButton(QPushButton):

    onSelection = pyqtSignal(int)

    def __init__(self, name: str, position: int, parent=None, vert=False):
        super().__init__(name, parent)

        self.setFlat(True)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.NoFocus)
        if vert:
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.postition = position

        self.clicked.connect(self._clickTrigger)

    def _clickTrigger(self):
        print("trigger clicked", self.postition)
        self.onSelection.emit(self.postition)
