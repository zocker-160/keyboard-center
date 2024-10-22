import shlex
import uinput

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QVBoxLayout, 
    QWidget, 
    QLabel
)

# imports for pyuic
from .CKeySequenceEdit import CKeySequenceEdit
from .CEntryButton import CEntryButton

from ..config import config

class CListWidgetItem(QWidget):

    onMoveUp = pyqtSignal(QWidget)
    onMoveDown = pyqtSignal(QWidget)
    onDelete = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.position = int()
        self.label = QLabel()

    def setCurrPos(self, pos: int):
        self.position = pos
        self.label.setText(f"{pos+1}.")

    def getData(self) -> config.Value:
        raise NotImplementedError

    def setData(self, dat: list):
        raise NotImplementedError

    def _remove(self):
        self.onDelete.emit(self)

    def _moveUp(self):
        self.onMoveUp.emit(self)

    def _moveDown(self):
        self.onMoveDown.emit(self)


from .Ui_keypressWidget import Ui_KeyPressWidget

class KeyPressWidget(CListWidgetItem, Ui_KeyPressWidget):

    def __init__(self, parent: QWidget, value=config.KeyValue()):
        super().__init__(parent)

        self.setupUi(self)
        self.customModBox.setVisible(False)
        self.clearButton.pressed.connect(self._resetRawLabel)
        self.setNullKeyButton.pressed.connect(self.keySequenceEdit.setNull)

        self.keySequenceEdit.onNewKeySet.connect(self._setRawLabel)
        self.keySequenceEdit.rawEnabled = True

        # FIXME type workaround
        btnFlags = value.modFlags
        if isinstance(btnFlags, int):
            btnFlags = config.Modifiers(btnFlags)

        self.ctrlMod.setChecked(config.Modifiers.CTRL in btnFlags)
        self.altMod.setChecked(config.Modifiers.ALT in btnFlags)
        self.altGrMod.setChecked(config.Modifiers.ALTGR in btnFlags)
        self.shiftMod.setChecked(config.Modifiers.SHIFT in btnFlags)
        self.metaMod.setChecked(config.Modifiers.META in btnFlags)

        bCustom = config.Modifiers.CUSTOM in btnFlags
        self.customMod.setChecked(bCustom)
        self.customModBox.setVisible(bCustom)

        if bCustom:
            self.customSequenceEdit.setKeycode(value.customKeycode)
            self.customSequenceEdit.setKeySequence(value.customString)

        if value.keycode > 0:
            self.keySequenceEdit.setKeycode(value.keycode)
            self.keySequenceEdit.setKeySequence(value.string)

    def getData(self) -> config.KeyValue:
        if not self.keySequenceEdit.isSet():
            raise ValueError("No key assigned!")

        btnFlags = config.Modifiers.NONE

        if self.ctrlMod.isChecked():
            btnFlags |= config.Modifiers.CTRL

        if self.altMod.isChecked():
            btnFlags |= config.Modifiers.ALT

        if self.altGrMod.isChecked():
            btnFlags |= config.Modifiers.ALTGR

        if self.shiftMod.isChecked():
            btnFlags |= config.Modifiers.SHIFT

        if self.metaMod.isChecked():
            btnFlags |= config.Modifiers.META

        if self.customMod.isChecked():
            btnFlags |= config.Modifiers.CUSTOM

        print(self.keySequenceEdit.getKeycode())
        print(self.keySequenceEdit.toString())

        return config.KeyValue(
            modFlags=btnFlags,
            keycode=self.keySequenceEdit.getKeycode(),
            string=self.keySequenceEdit.toString(),
            customKeycode=self.customSequenceEdit.getKeycode(),
            customString=self.customSequenceEdit.toString(),
        )

    def _setRawLabel(self, number: int):
        if number == 0: # nullkey
            number = "nullkey"

        self.rawInputLabel.setText(str(number))

    def _resetRawLabel(self):
        self.rawInputLabel.setText("---")


from .Ui_delayWidget import Ui_DelayWidget

class DelayWidget(CListWidgetItem, Ui_DelayWidget):
    def __init__(self, parent: QWidget, value=config.DelayValue):
        super().__init__(parent)

        self.setupUi(self)
        self.spinBox.setValue(value.delay)
        self.clearButton.clicked.connect(lambda:self.spinBox.setValue(0))

    def getData(self) -> config.DelayValue:
        return config.DelayValue(delay=self.spinBox.value())

from .Ui_commandWidget import Ui_CommandWidget

class CommandWidget(CListWidgetItem, Ui_CommandWidget):
    def __init__(self, parent: QWidget, value=config.CommandValue()):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.commandEdit.setText(value.getCommand())

    def getData(self):
        if command := self.commandEdit.text():
            value = config.CommandValue()
            value.setCommand(command)
            return value
        else:
            raise ValueError("No command specified!")


class CListWidgetContent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.list = QVBoxLayout(self)

    def addWidget(self, widget: CListWidgetItem):
        self.list.addWidget(widget)

        widget.setCurrPos(self.list.count() - 1)
        widget.onDelete.connect(self.removeWidget)
        widget.onMoveUp.connect(self.moveWidgetUp)
        widget.onMoveDown.connect(self.moveWidgetDown)

    def removeWidget(self, widget: QWidget):
        self.list.removeWidget(widget)
        widget.deleteLater()
        self._updateOrder()

    def moveWidgetUp(self, widget: CListWidgetItem):
        if widget.position <= 0: return
        self.list.insertWidget(
            widget.position - 1,
            self.list.itemAt(widget.position).widget()
        )
        self._updateOrder()

    def moveWidgetDown(self, widget: CListWidgetItem):
        if widget.position >= self.list.count() - 1: return
        self.list.insertWidget(
            widget.position + 1,
            self.list.itemAt(widget.position).widget()
        )
        self._updateOrder()

    def setData(self, values: list[config.Value]):
        for value in values:
            if isinstance(value, config.KeyValue):
                self.addWidget(KeyPressWidget(self, value))

            elif isinstance(value, config.CommandValue):
                self.addWidget(CommandWidget(self, value))

            elif isinstance(value, config.DelayValue):
                self.addWidget(DelayWidget(self, value))

    def getData(self) -> list[config.Value]:
        return [item.getData() for item in self.getItems()]

    def getLayout(self) -> QVBoxLayout:
            return self.list

    def getItems(self) -> list[CListWidgetItem]:
        tmp = list()

        for i in range(self.list.count()):
            tmp.append(self.list.itemAt(i).widget())

        return tmp

    def clearAllEntries(self):
        for item in self.getItems():
            self.removeWidget(item)

    def _updateOrder(self):
        for i, item in enumerate(self.getItems()):
            item.setCurrPos(i)
