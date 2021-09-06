#! /usr/bin/env python3

import os
import sys
import webbrowser

from PyQt5.QtGui import QCloseEvent, QKeyEvent, QKeySequence
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QDialog, QHBoxLayout, QLabel, QListView, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout, QWidget

from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface
from devices.allkeys import ALL_MEMORY_KEYS, ALL_MACRO_KEYS
from lib.configparser import Configparser
from lib.servicehelper import *

from gui.CEntryButton import CEntryButton
from gui.customwidgets import KeyPressWidget
from gui.Ui_mainwindow import Ui_MainWindow
from gui.Ui_aboutWindow import Ui_aboutWindow
from gui.Ui_serviceWindow import Ui_serviceWindow

PARENT_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_LOCATION = os.path.join(
    PARENT_LOCATION, "config", "testconfig.yaml.example"
)

PLACEHOLDER_STR = "$$$"
VERSION = "0.1.4-testing"

class AboutWindow(QDialog, Ui_aboutWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.setupUi(self)
        self.about_maintext.setText(
            self.about_maintext.text().replace(PLACEHOLDER_STR, VERSION)
        )

class ServiceWindow(QDialog, Ui_serviceWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.returnState = 0 # 0: ignore / OK; 1: retry; 2: cancel

        self.setupUi(self)
        self.setWindowTitle("Service Status Checker")
        self.mainText.setText("checking background service status:")
        self.informativeText.setText("fuck off")

        self.ignoreButton.clicked.connect(lambda: self._setReturnState(0))
        self.retryButton.clicked.connect(lambda: self._setReturnState(1))
        self.cancelButton.clicked.connect(lambda: self._setReturnState(2))

        self.checkService()

    def checkService(self):
        self.setInformativeText("service enabled?")
        if not isServiceEnabled():
            self.setInformativeText("enabling service...")
            if not enableService():
                self._errorState("failed to enable service!")
                return

        self.setInformativeText("service running?")
        if not isServiceRunning():
            self.setInformativeText("starting service...")
            if not startService():
                self._errorState("failed to start service!")
                return

        self.setInformativeText("service needs reload?")
        if needsReload():
            self.setInformativeText("reloading service...")
            if not reloadService():
                self._errorState("failed to reload service!")
                return

        QTimer.singleShot(200, self.ignoreButton.click)

    def setInformativeText(self, text: str) -> None:
        print(text)
        self.informativeText.setText(text)

    def _setReturnState(self, state: int):
        self.returnState = state
        self.close()

    def _errorState(self, msg: str):
        self.setInformativeText("ERROR: "+msg)
        self.retryButton.setEnabled(True)

    def exec_(self) -> int:
        super().exec_()
        return self.returnState

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app: QApplication, devmode=False):
        super().__init__()
        self.app = app
        if not devmode: self.checkServiceStatus()
        self.readConfiguration()

        self.setupUi(self)
        self.initGuiControls()
        self.generateProfileButtons()

        self.setCurrMemory(0, save=False, load=False)
        self.setCurrMacro(0, save=False)

    def checkServiceStatus(self):
        msg = ServiceWindow()
        ret = msg.exec_()

        if ret == 0: # ignore / OK
            pass
        elif ret == 1: # retry
            self.checkServiceStatus()
        elif ret == 2: # cancel
            sys.exit()

    def readConfiguration(self):
        try:
            self.configparser = Configparser(TEMPLATE_LOCATION, False)
        except Exception as e:
            self.showErrorMSG(
                "Could not load config file! \n\n",
                detailText=str(e),
                title_msg="FATAL ERROR"
            )
            sys.exit()

        try:
            _did = self.configparser.getSettings()["usbDeviceID"]
            self.usbDevice: KeyboardInterface = SUPPORTED_DEVICES[_did]
        except Exception as e:
            self.showErrorMSG(
                f"No supported keyboard found! :(\n(err:{_did})",
                title_msg="FATAL ERROR"
            )
            r = self.showQuestionMSG("Do you want to try again?")
            if r == QMessageBox.Yes:
                # we need to add a small delay, since detecting the keyboard
                # takes a little bit of time
                self.checkServiceStatus()
                from time import sleep
                sleep(0.5)
                self.readConfiguration()
            else:
                sys.exit()

    def initGuiControls(self):
        self.actionAbout_Qt.triggered.connect(self.app.aboutQt)
        self.actionAbout.triggered.connect(self.showAbout)

        self.actionGitHub.triggered.connect(self.showGitHub)
        self.actionReport_issue.triggered.connect(self.showReportIssue)
        self.actionExit.triggered.connect(self.close)

        self.addKey.clicked.connect(self.addBlankKeyWidget)
        self.saveButton.clicked.connect(lambda: self.saveData(True))
        self.clearAllButton.clicked.connect(
            self.keyListWidgetContents.clearAllEntries)
        self.clearAllButton.clicked.connect(self.macroNameEdit.clear)
        self.resetButton.clicked.connect(self.loadData)

    def generateProfileButtons(self):
        # set device name
        self.supportedDevice.setText(self.usbDevice.devicename)

        # generate buttons
        for i in range(self.usbDevice.numMemoryKeys):
            btn = CEntryButton(
                name=f"M{i+1}",
                position=i,
                parent=self)
            btn.onSelection.connect(self.setCurrMemory)
            self.memoryKeySlots.addWidget(btn)
        else:
            # this is needed to move all the buttons to the left
            self.memoryKeySlots.addSpacerItem(QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
        self.macroKeySlots = QVBoxLayout(self.macroKeys)
        for y in range(self.usbDevice.numMacroKeys):
            btn = CEntryButton(
                name=f"G{y+1}",
                position=y,
                parent=self)
            btn.onSelection.connect(self.setCurrMacro)
            self.macroKeySlots.addWidget(btn)
    
    def setCurrMemory(self, id: int, save=True, load=True):
        if save: self.saveData()

        def __setMarked(item, value: bool):
            if item:
                item.setChecked(value)
            
        self.currMemory = id
        for i in range(self.memoryKeySlots.count()):
            if i == id:
                __setMarked(self.memoryKeySlots.itemAt(i).widget(), True)
            else:
                __setMarked(self.memoryKeySlots.itemAt(i).widget(), False)

        if load: self.loadData()

    def setCurrMacro(self, id: int, save=True, load=True):
        # don't switch currMacro when saving fails
        if save and not self.saveData():
            id = self.currMacro
            load = False

        self.currMacro = id
        for i in range(self.macroKeySlots.count()):
            if i == id:
                self.macroKeySlots.itemAt(i).widget().setChecked(True)
            else:
                self.macroKeySlots.itemAt(i).widget().setChecked(False)

        if load: self.loadData()

    def addBlankKeyWidget(self):
        self.keyListWidgetContents.addWidget(KeyPressWidget())


    def saveData(self, saveToFile=False):
        print("saving")
        try:
            data = self.keyListWidgetContents.getKeyData()
            print(data)
            self.configparser.saveFromGui(
                profile=ALL_MEMORY_KEYS[self.currMemory],
                macroKey=ALL_MACRO_KEYS[self.currMacro],
                name=self.macroNameEdit.text(),
                data=data,
                bSavetoFile=saveToFile
            )
        except Exception as e:
            self.showErrorMSG(str(e))
            return False
        if saveToFile:
            self.bottomStatusBar.showMessage(
                "Configuration saved to file!", 2000
            )
        return True

    def loadData(self):
        print("loading", self.currMemory, self.currMacro)
        d, name, val = self.configparser.loadForGui(
            ALL_MEMORY_KEYS[self.currMemory],
            ALL_MACRO_KEYS[self.currMacro]
        )

        print(d, name, val)

        try:
            self.keyListWidgetContents.setKeyData(d, val)
        except TypeError:
            self.bottomStatusBar.showMessage("loading failed: ignoring...")
        except Exception as e:
            self.showErrorMSG(str(e))
        
        self.macroNameEdit.setText(name)


    # function overloading
    def keyPressEvent(self, a0: QKeyEvent):
        print(a0.nativeScanCode())
        return super().keyPressEvent(a0)

    def closeEvent(self, a0: QCloseEvent):
        r = self.showQuestionMSG("Do you want to save unsaved changes?")

        if r == QMessageBox.Cancel:
            a0.ignore()
            return
        if r == QMessageBox.Yes:
            self.saveData(True)
        return super().closeEvent(a0)

    ### menu actions
    def showGitHub(self):
        webbrowser.open("https://github.com/zocker-160/keyboard-center")

    def showReportIssue(self):
        webbrowser.open("https://github.com/zocker-160/keyboard-center/issues")

    ### popup messages
    def showErrorMSG(self, msg_str, title_msg="ERROR", detailText=""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(str(msg_str))
        msg.setDetailedText(detailText)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        return msg.exec_()

    def showInfoMSG(self, msg_str: str, title_msg="Info"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        return msg.exec_()

    def showQuestionMSG(self, msg_str: str, title_msg="Question"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.addButton(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Yes)
        
        return msg.exec_()

    ### secondary windows
    def showAbout(self):
        about = AboutWindow(self)
        about.show()

    ### other ui stuff
    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(
            self.app.primaryScreen().availableGeometry().center())
        self.move(qr.topLeft())

def main():
    app = QApplication(sys.argv)
    devmode = True if "-dev" in sys.argv else False

    window = MainWindow(app, devmode)
    window.center()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
