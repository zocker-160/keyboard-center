
from ruamel.yaml.tokens import FlowMappingStartToken
import uinput

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QKeyEvent, QKeySequence, QMouseEvent
from PyQt5.QtWidgets import QKeySequenceEdit, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton

from lib.configparser import MOD_CTRL, MOD_ALT, MOD_SHIFT, MOD_META

class CKeySequenceEdit(QKeySequenceEdit):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pressedKeycode = None
        self.tmpKeycodes = list()

        self.editingFinished.connect(self.finalize)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        # only one single non modifier is allowed
        if a0.modifiers() or len(self.tmpKeycodes) > 0: return

        self.pressedKeycode = a0.nativeScanCode()
        self.tmpKeycodes.append(a0.key())

        return super().keyPressEvent(a0)

    def clear(self):
        self.pressedKeycode = None
        self.tmpKeycodes.clear()
        print("")
        return super().clear()

    def finalize(self):
        self.tmpKeycodes.clear()
        #print(self.keySequence().toString())
        #print(self.pressedKeycode)

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

    def getData(self):
        raise NotImplementedError

    def setData(self, dat: list):
        raise NotImplementedError

    def _remove(self):
        self.onDelete.emit(self)

    def _moveUp(self):
        self.onMoveUp.emit(self)

    def _moveDown(self):
        self.onMoveDown.emit(self)

from gui.Ui_keypressWidget import Ui_KeyPressWidget

class KeyPressWidget(CListWidgetItem, Ui_KeyPressWidget):
    def __init__(self, parent=None,
                bCtrl=False, bAlt=False, bShift=False, bMeta=False,
                key: str = None, rawKey: tuple = None):
        super().__init__(parent)

        self.setupUi(self)

        self.ctrlMod.setChecked(bCtrl)
        self.altMod.setChecked(bAlt)
        self.shiftMod.setChecked(bShift)
        self.metaMod.setChecked(bMeta)
        if key: self.keySequenceEdit.setKeySequence(key)
        # We need to +8 to convert uinput keycode -> X keycode
        if rawKey: self.keySequenceEdit.pressedKeycode = rawKey[1] + 8

    def getData(self) -> list:
        # return nothing when there is no actual key
        if self.keySequenceEdit.keySequence().count() == 0:
            return None

        res = list()

        for mod in [self.ctrlMod, self.altMod, self.shiftMod, self.metaMod]:
            if mod.isChecked():
                if mod is self.ctrlMod:
                    res.append( (MOD_CTRL, uinput.KEY_LEFTCTRL[1]) )
                elif mod is self.altMod:
                    res.append( (MOD_ALT, uinput.KEY_LEFTALT[1]) )
                elif mod is self.shiftMod:
                    res.append( (MOD_SHIFT, uinput.KEY_LEFTSHIFT[1]) )
                elif mod is self.metaMod:
                    res.append( (MOD_META, 125) ) # X keycode is 133

        # finally add the key itself
        res.append( (
            self.keySequenceEdit.keySequence().toString(),
            # We need to -8 to convert X keycode -> uinput keycode
            self.keySequenceEdit.pressedKeycode - 8
            )
        )

        return res

    def __setData(self, data: list):
        """ 
        Expects data in the following form:

        @example [('Ctrl', 29), ('C', 46)]
        @example [('Ctrl', 29), ('V', 47)]
        """

        for key, _ in data:
            if key in [MOD_CTRL, MOD_ALT, MOD_SHIFT, MOD_META]:
                if key == MOD_CTRL:
                    self.ctrlMod.setChecked(True)
                elif key == MOD_ALT:
                    self.altMod.setChecked(True)
                elif key == MOD_SHIFT:
                    self.shiftMod.setChecked(True)
                elif key == MOD_META:
                    self.metaMod.setChecked(True)
                else:
                    pass


class CListWidgetContent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.list = QVBoxLayout(self)

    def addWidget(self, widget: CListWidgetItem):
        self.list.addWidget(widget)

        widget.setCurrPos(self.list.count()-1)
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
            widget.position-1,
            self.list.itemAt(widget.position).widget()
        )
        self._updateOrder()

    def moveWidgetDown(self, widget: CListWidgetItem):
        if widget.position >= self.list.count()-1: return
        self.list.insertWidget(
            widget.position+1,
            self.list.itemAt(widget.position).widget()
        )
        self._updateOrder()        


    def getKeyData(self):
        data = list()
        for item in self.getEntries():
            d = item.getData()
            if d:
                data.append(d)
            else:
                raise ValueError("Not all entries have a key assigned!")

        return data

    def setKeyData(self, data: list, values: list):
        """
        Converts data into the corresponding widget and adds it

        @example data [['Ctrl', 'C'], ['Ctrl', 'V']]
        @example data [['Ctrl', 'X'], ['Ctrl', 'V']]

        @example values [[[1, 29], [1, 45]], [[1, 29], [1, 47]]]
        """
        self.clearAllEntries()
        
        for i, entry in enumerate(data):
            sKey = None
            sKeyRaw = None
            bCtrl, bShift, bAlt, bmeta = [False]*4
            for y, key in enumerate(entry):
                if key == MOD_CTRL:
                    bCtrl = True
                elif key == MOD_ALT:
                    bAlt = True
                elif key == MOD_SHIFT:
                    bShift = True
                elif key == MOD_META:
                    bmeta = True
                else:
                    sKey = key
                    sKeyRaw = values[i][y]

            print("rawvalue:", sKeyRaw)
            # TODO: add support for delays
            self.addWidget(KeyPressWidget(
                bCtrl=bCtrl, bAlt=bAlt, bShift=bShift, bMeta=bmeta,
                key=sKey, rawKey=sKeyRaw))


    def getLayout(self) -> QVBoxLayout:
        return self.list

    def getEntries(self) -> list:
        tmp = list()

        for i in range(self.list.count()):
            tmp.append(self.list.itemAt(i).widget())
        
        return tmp

    def clearAllEntries(self):
        for item in self.getEntries():
            self.removeWidget(item)

    def _updateOrder(self):
        entries = self.getEntries()
        for i, item in enumerate(entries):
            item.setCurrPos(i)
    