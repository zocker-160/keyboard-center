from PyQt5.QtCore import QObject, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget

from ..config import config


MODIFIER_KEYS = {
    Qt.Key_Control: config.Modifiers.CTRL,
    Qt.Key_Shift: config.Modifiers.SHIFT,
    Qt.Key_Alt: config.Modifiers.ALT,
    Qt.Key_AltGr: config.Modifiers.ALTGR,
    Qt.Key_Meta: config.Modifiers.META,
}

QT_MODIFIERS = {
    Qt.ControlModifier: config.Modifiers.CTRL,
    Qt.ShiftModifier: config.Modifiers.SHIFT,
    Qt.AltModifier: config.Modifiers.ALT,
    Qt.GroupSwitchModifier: config.Modifiers.ALTGR,
    Qt.MetaModifier: config.Modifiers.META,
}


class KeyRecorder(QObject):

    onNewKey = pyqtSignal(object)
    onStop = pyqtSignal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.app = QApplication.instance()
        self.isRecording = False
        self.modifiers = dict()

    def start(self):
        self.modifiers.clear()
        self.isRecording = True
        self.app.installEventFilter(self)
        self.parent().setFocus()

    def stop(self):
        self.app.removeEventFilter(self)
        self.isRecording = False

        # A modifier pressed on its own is also a valid action.
        for _, value in self.modifiers.values():
            if value is not None:
                self.onNewKey.emit(value)
        self.modifiers.clear()

    def eventFilter(self, obj, event):
        if obj == self.parent() and event.type() in (QEvent.WindowDeactivate, QEvent.Hide):
            self.onStop.emit()
            return False

        if event.type() == QEvent.Show and isinstance(obj, QWidget) and obj.windowType() == Qt.Popup:
            self.onStop.emit()
            return False

        if not isinstance(obj, QWidget) or obj.window() != self.parent():
            return False

        # Text input methods can consume dead keys before Qt sends key events.
        if event.type() == QEvent.FocusIn and obj != self.parent():
            self.parent().setFocus()
            return True

        if event.type() == QEvent.ShortcutOverride:
            event.accept()
            return True

        if event.type() not in (QEvent.KeyPress, QEvent.KeyRelease):
            return False

        if event.isAutoRepeat():
            return True

        # Qt uses XKB keycodes on both X11 and Wayland, as in CKeySequenceEdit.
        keycode = event.nativeScanCode() - 8
        if keycode <= 0:
            return True

        if event.type() == QEvent.KeyRelease:
            _, value = self.modifiers.pop(keycode, (None, None))
            if value is not None:
                self.onNewKey.emit(value)
            return True

        flags = config.Modifiers.NONE
        for qtModifier, modifier in QT_MODIFIERS.items():
            if event.modifiers() & qtModifier:
                flags |= modifier

        modifier = MODIFIER_KEYS.get(event.key())
        if modifier is not None:
            flags &= ~modifier
        for pressed, (heldModifier, _) in self.modifiers.items():
            flags |= heldModifier
            self.modifiers[pressed] = (heldModifier, None)

        key = Qt.Key_Tab if event.key() == Qt.Key_Backtab else event.key()
        string = QKeySequence(key).toString()
        try:
            string.encode()
        except UnicodeEncodeError:
            string = ""

        value = config.KeyValue(
            modFlags=flags, keycode=keycode, string=string or f"0x{keycode}")
        if modifier is not None:
            self.modifiers[keycode] = (modifier, value)
        else:
            self.onNewKey.emit(value)
        return True
