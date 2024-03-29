import shlex
import uinput

from PyQt5.QtCore import pyqtSignal, QEvent, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QKeySequenceEdit, 
    QVBoxLayout, 
    QWidget, 
    QLabel
)

from lib.configparser import (
    MOD_ALTGR, 
    MOD_CTRL, 
    MOD_ALT, 
    MOD_SHIFT, 
    MOD_META, 
    TYPE_DELAY, 
    TYPE_DELAY_STR
)
from devices.allkeys import MODIFIER_SCANCODES

class CKeySequenceEdit(QKeySequenceEdit):

    onNewKeySet = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.rawEnabled = False

        self.pressedKeycode = None
        self.tmpKeycodes = list()

        self.editingFinished.connect(self.finalize)

    def getUinputKeycode(self) -> int:
        # We need to -8 to convert X keycode -> uinput keycode
        return self.pressedKeycode - 8

    def setKeycode(self, uinputKeycode: int) -> None:
        # We need to +8 to convert uinput keycode -> X keycode
        self.pressedKeycode = uinputKeycode + 8
        self.onNewKeySet.emit(self.pressedKeycode)

    def setKeySequence(self, keySequence: str):
        if keySequence.startswith("0x") and self.rawEnabled:
            keySequence = "nullkey"

        return super().setKeySequence(keySequence)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        #print("keypress:", a0.nativeScanCode())
        #print("keypress:", a0.key())

        # only one single non modifier is allowed
        if len(self.tmpKeycodes) > 0: return

        keycode = a0.nativeScanCode()
        if keycode in MODIFIER_SCANCODES and not self.rawEnabled:
            return

        self.pressedKeycode = keycode
        self.tmpKeycodes.append(a0.key())

        self.onNewKeySet.emit(self.pressedKeycode)

        return super().keyPressEvent(a0)

    def event(self, a0: QEvent) -> bool:
        # we need to filter Tab key press manually and send to
        # keyPressEvent because otherwise tab will unfocus the
        # KeySequenceEdit widget, which is not desired behavior
        if a0.type() == QEvent.KeyPress and a0.key() == Qt.Key_Tab:
            self.keyPressEvent(a0)
            return True

        return super().event(a0)

    def clear(self):
        self.pressedKeycode = None
        self.tmpKeycodes.clear()
        return super().clear()

    def finalize(self):
        self.tmpKeycodes.clear()

        #print("key:", self.toString())
        #print(self.pressedKeycode)

    def isSet(self):
        return not (self.keySequence().count() == 0 and not self.pressedKeycode)

    def setNull(self):
        self.setKeySequence("0x0")
        self.setKeycode(0)

    def toString(self):
        string = self.keySequence().toString()

        if self.rawEnabled and not string:
            return f"0x{self.pressedKeycode}"
        else:
            return string

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

from lib.configtypes import *
from gui.Ui_keypressWidget import Ui_KeyPressWidget

class KeyPressWidget(CListWidgetItem, Ui_KeyPressWidget):
    def __init__(self, parent=None,
            bCtrl=False, bAlt=False, bShift=False, bMeta=False, bAltGr=False,
            bCustom=False, customKey: Key=None,
            key: Key=None):
        super().__init__(parent)

        self.setupUi(self)
        self.customModBox.setVisible(False)
        self.clearButton.pressed.connect(self._resetRawLabel)
        self.setNullKeyButton.pressed.connect(self.keySequenceEdit.setNull)

        self.keySequenceEdit.onNewKeySet.connect(self._setRawLabel)
        self.keySequenceEdit.rawEnabled = True

        self.ctrlMod.setChecked(bCtrl)
        self.altMod.setChecked(bAlt)
        self.altGrMod.setChecked(bAltGr)
        self.shiftMod.setChecked(bShift)
        self.metaMod.setChecked(bMeta)

        if customKey:
            self.customMod.setChecked(bCustom)
            self.customModBox.setVisible(bCustom)
            self.customSequenceEdit.setKeySequence(customKey.keyString)
            self.customSequenceEdit.setKeycode(customKey.keycode)

        if key:
            self.keySequenceEdit.setKeySequence(key.keyString)
            self.keySequenceEdit.setKeycode(key.keycode)

    def getData(self) -> ConfigEntry:
        # raise error when there is no actual key
        if not self.keySequenceEdit.isSet():
            raise ValueError("No key assigned!")

        keys = list()

        if self.ctrlMod.isChecked():
            keys.append( Key(uinput.KEY_LEFTCTRL[1], MOD_CTRL) )

        if self.altMod.isChecked():
            keys.append( Key(uinput.KEY_LEFTALT[1], MOD_ALT) )

        if self.altGrMod.isChecked():
            keys.append( Key(uinput.KEY_RIGHTALT[1], MOD_ALTGR) )

        if self.shiftMod.isChecked():
            keys.append( Key(uinput.KEY_LEFTSHIFT[1], MOD_SHIFT) )

        if self.metaMod.isChecked():
            keys.append( Key(uinput.KEY_LEFTMETA[1], MOD_META) )

        if self.customMod.isChecked():
            if self.customSequenceEdit.keySequence().count() == 0:
                raise ValueError("No custom mod key assigned!")
            else:
                keys.append( Key(
                    self.customSequenceEdit.getUinputKeycode(),
                    self.customSequenceEdit.toString()
                    ) )

        # finally add the key itself
        keys.append( Key(
            self.keySequenceEdit.getUinputKeycode(),
            self.keySequenceEdit.toString()
        ) )

        if len(keys) <= 0: return None
        if len(keys) == 1:
            return keys.pop()
        else:
            return Combo(keys)

    def _setRawLabel(self, number: int):
        if number == 8: # nullkey
            number = "nullkey"
        
        self.rawInputLabel.setText(str(number))

    def _resetRawLabel(self):
        self.rawInputLabel.setText("---")

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


from gui.Ui_delayWidget import Ui_DelayWidget

class DelayWidget(CListWidgetItem, Ui_DelayWidget):
    def __init__(self, parent=None, delay: int = None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.clearButton.clicked.connect(lambda:self.spinBox.setValue(0))

        if delay: self.spinBox.setValue(delay)

    def getData(self):
        return Delay(self.spinBox.value())

from gui.Ui_commandWidget import Ui_CommandWidget

class CommandWidget(CListWidgetItem, Ui_CommandWidget):
    def __init__(self, parent=None, command: str = ""):
        super().__init__(parent=parent)

        self.setupUi(self)

        if command: self.commandEdit.setText(command)

    def getData(self):
        if command := self.commandEdit.text():
            shlex.split(command)
            return Command(command)
        else:
            raise ValueError("No command specified!")

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


    def getKeyData(self) -> ConfigEntry:
        data = list()
        for item in self.getEntries():
            d = item.getData()    
            if type(d) in [Key, Delay, Combo, Command]:
                data.append(d)
                
        if len(data) == 0:
            return None
        if len(data) == 1:
            return data.pop()
        else:
            return Macro(data)

    def setKeyData(self, data: ConfigEntry, clear=True):
        if clear: self.clearAllEntries()

        if type(data) == Key:
            self.addWidget( KeyPressWidget(key=data) )

        elif type(data) == Delay:
            self.addWidget( DelayWidget(delay=data.duration) )

        elif type(data) == Command:
            self.addWidget( CommandWidget(command=data.command) )

        elif type(data) == Combo:
            bCtrl, bShift, bAlt, bAltGr, bMeta, bCustom = [False]*6
            customKey: Key = None
            for key in data.keylist:
                if key.keyString in [MOD_CTRL, MOD_SHIFT, MOD_ALT, MOD_ALTGR, MOD_META]:
                    bCtrl = key.keyString == MOD_CTRL or bCtrl
                    bShift = key.keyString == MOD_SHIFT or bShift
                    bAlt = key.keyString == MOD_ALT or bAlt
                    bAltGr = key.keyString == MOD_ALTGR or bAltGr
                    bMeta = key.keyString == MOD_META or bMeta
                
                elif key is data.keylist[-1]:
                    self.addWidget( KeyPressWidget(
                        bCtrl=bCtrl, bShift=bShift, bAlt=bAlt, bAltGr=bAltGr, bMeta=bMeta,
                        bCustom=bCustom, customKey=customKey,
                        key=key
                    ) )
                else:
                    bCustom = True
                    customKey = key

        elif type(data) == Macro:
            for comboKey in data.comboKeyList:
                self.setKeyData(comboKey, clear=False)

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
