#! /usr/bin/env python3

import logging

from PyQt5.QtGui import (
    QCloseEvent,
    QKeyEvent,
    QIcon,
)
from PyQt5.QtCore import (
    QTimer,
)
from PyQt5.QtWidgets import (
    QDialog,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
)

from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface
from devices.allkeys import ALL_MEMORY_KEYS, ALL_MACRO_KEYS
from lib.QSingleApplication import QSingleApplication
from lib.configparser import Configparser
from lib.servicehelper import *

from gui.tray import TrayIcon
from gui.CEntryButton import CEntryButton
from gui.customwidgets import CommandWidget, DelayWidget, KeyPressWidget
from gui.Ui_mainwindow import Ui_MainWindow

from constants import *
from service import BackgroundService, NoKeyboardException, NoEndpointException

PLACEHOLDER_STR = "$$$"

class MainWindow(QMainWindow, Ui_MainWindow):

    service: BackgroundService = None

    def __init__(self, 
            app: QSingleApplication, 
            devmode=False, trayVisible=True):
        super().__init__()
        self.app = app
        self.devmode = devmode
        self.logger = logging.getLogger("QT")

        self.app.onActivate.connect(self.activateTrigger)

        self.healthCheck = QTimer(self)
        self.healthCheck.timeout.connect(self._serviceHealthCheck)

        #if not devmode: self.checkServiceStatus(manual=False)
        self.configparser = self.getConfiguration()
        self.initBackgroundService()

        self.icon = QIcon(":/icons/assets/input-keyboard-virtual.png")
        self.tray = TrayIcon(self, self.icon, trayVisible)

        self.setupUi()
        self.setupSlots()

        # workaround for weird KDE bug where spinner keeps running
        # in task bar despite app being long started
        # by calling show() we make sure the spinner stops
        # and then we hide() afterwards when needed
        self.show()
        self.center()
        if not self.devmode and self.configparser.getMinimizeOnStart():
            self.hide()

    def setupUi(self):
        self.logger.debug("setting up GUI...")
        super().setupUi(self)
        # TODO: why the fuck is this not in the layout??
        self.macroKeySlots = QVBoxLayout(self.macroKeys)

        self.setWindowIcon(self.icon)

        #self.generateProfileButtons()
        self.loadConfiguration()
        
        #self.tray.messageClicked.connect(lambda: print("MESSAGE CLICKED"))
        #self.tray.showMessage("TITLE", "MESSAGE", QSystemTrayIcon.Warning, 10000)

        #self.icon = QIcon()
        #self.icon.addPixmap(QPixmap(":/icons/assets/input-keyboard-virtual.png"), QIcon.Normal, QIcon.Off)

    def setupSlots(self):
        self.actionOpenConfigFolder.triggered.connect(self.openConfigFolder)
        self.actionOpenLogFolder.triggered.connect(self.openLogFolder)
        self.actionRestartService.triggered.connect(self.forceRestart)
        self.actionAbout_Qt.triggered.connect(self.app.aboutQt)
        self.actionAbout.triggered.connect(self.showAbout)

        self.actionGitHub.triggered.connect(self.showGitHub)
        self.actionReport_issue.triggered.connect(self.showReportIssue)
        self.actionExit.triggered.connect(self.close)
        self.openRGBhelp.clicked.connect(self.showOpenRGBsetup)

        self.addKey.clicked.connect(self.addBlankKeyWidget)
        self.addDelay.clicked.connect(self.addBlankDelayWidget)
        self.addCommand.clicked.connect(self.addBlankCommandWidget)
        self.saveButton.clicked.connect(lambda: self.saveData(saveToFile=True))
        self.toTrayButton.clicked.connect(self.hide)
        self.clearAllButton.clicked.connect(
            self.keyListWidgetContents.clearAllEntries)
        self.clearAllButton.clicked.connect(self.macroNameEdit.clear)
        self.resetButton.clicked.connect(self.loadData)

        # trayicon actions
        self.tray.hideshowAction.triggered.connect(
            lambda: self.setHidden(not self.isHidden()))
        self.tray.restartAction.triggered.connect(self.forceRestart)
        self.tray.exitAction.triggered.connect(self.close)

    def getConfiguration(self):
        try:
            configparser = Configparser(TEMPLATE_LOCATION, silent=False)
        except Exception as e:
            self.showErrorMSG(
                "Could not load config file! \n\n",
                detailText=str(e),
                title_msg="FATAL ERROR"
            )
            raise

        return configparser

    def initBackgroundService(self):
        if self.service:
            self.logger.debug("deleting BGService")
            self.service.wait()
            self.service.deleteLater()
            self.service = None

        try:
            useOpenRGB = self.configparser.getUseOpenRGB()
            if self.devmode:
                useOpenRGB = False

            self.service = BackgroundService(self.configparser, useOpenRGB)
            self.service.notificationEvent.connect(self.showNotification)
            self.service.notificationIconEvent.connect(self.showNotificationIcon)
            self.service.quitTriggered.connect(self._forcedHealthCheck)
            self.service.start()

        except NoKeyboardException:
            pass
        except NoEndpointException as e:
            self.showErrorMSG(
                "Failed to load keyboard endpoint!",
                detailText=str(e),
                title_msg="FATAL ERROR"
            )
            raise
        # TODO HIDFailedToOpenException
        except Exception as e:
            self.showErrorMSG(
                "Error during init of keyboard!",
                detailText=str(e),
                title_msg="FATAL ERROR"
            )
            raise

        self.logger.debug("start health check...")
        self.healthCheck.start(1000 * 10) # every 10 seconds

    def _forcedHealthCheck(self):
        try:
            self.service.wait()
        except:
            pass

        self._serviceHealthCheck()

    def _serviceHealthCheck(self):
        if not self.service or not self.service.isRunning():
            self.healthCheck.stop()

            self.logger.debug("restarting service...")
            self.initBackgroundService()
            self.resetProfileButtons()
            self.loadConfiguration()

    def loadConfiguration(self):
        try:
            self.configparser.load(True)
            _did = self.configparser.getDeviceID()
            self.usbDevice: KeyboardInterface = SUPPORTED_DEVICES[_did]
        except TypeError:
            return
        except Exception as e:
            self.showErrorMSG(
                f"Error during loading of keyboard config! \n\n",
                detailText=f"err:({str(e)})",
                title_msg="FATAL ERROR")
            raise

        self.generateProfileButtons()

    def resetProfileButtons(self):
        self.supportedDevice.setText("no supported device found :(")
        self.saveButton.setDisabled(True)
        self.resetButton.setDisabled(True)

        while self.macroKeySlots.count():
            child = self.macroKeySlots.takeAt(0)
            if w := child.widget():
                w.deleteLater()

        while self.memoryKeySlots.count():
            child = self.memoryKeySlots.takeAt(0)
            if w := child.widget():
                w.deleteLater()

    def generateProfileButtons(self):
        # generate buttons
        for i in range(self.usbDevice.numMemoryKeys):
            btn = CEntryButton(
                name=f"M{i+1}",
                position=i,
                parent=self)
            btn.onSelection.connect(self.setCurrMemory)
            self.memoryKeySlots.addWidget(btn)
        #else:
        #    # this is needed to move all the buttons to the left
        #    self.memoryKeySlots.addSpacerItem(QSpacerItem(
        #        40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        for y in range(self.usbDevice.numMacroKeys):
            btn = CEntryButton(
                name=f"G{y+1}",
                position=y,
                parent=self,
                vert=True)
            btn.onSelection.connect(self.setCurrMacro)
            self.macroKeySlots.addWidget(btn)
    
        self.setCurrMemory(0, save=False, load=False)
        self.setCurrMacro(0, save=False)

        # set device name
        self.supportedDevice.setText(self.usbDevice.devicename)

        # enable buttons
        self.saveButton.setEnabled(True)
        self.resetButton.setEnabled(True)

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

    def addBlankDelayWidget(self):
        self.keyListWidgetContents.addWidget(DelayWidget())

    def addBlankCommandWidget(self):
        self.keyListWidgetContents.addWidget(CommandWidget())

    def saveData(self, saveToFile=False):
        self.logger.info("saving")
        try:
            data = self.keyListWidgetContents.getKeyData()
            if data:
                data.name = self.macroNameEdit.text()
                if self.gameMode.isChecked():
                    data.gamemode = self.gameModeTime.value()
                else:
                    data.gamemode = 0
            print(data)
            self.configparser.saveFromGui(
                profile=ALL_MEMORY_KEYS[self.currMemory],
                macroKey=ALL_MACRO_KEYS[self.currMacro],
                orgb=self.openRGBedit.text(),
                data=data,
                notifications= not self.disableNotifications.isChecked(),
                minOnStart=self.minimizeOnStart.isChecked(),
                useOpenRGB=self.useOpenRGB.isChecked(),
                bSavetoFile=saveToFile
            )
        except Exception as e:
            self.showErrorMSG(str(e))
            return False
        if saveToFile:
            self.bottomStatusBar.showMessage(
                "Configuration saved to file", 2000
            )
        return True

    def loadData(self):
        print("loading", self.currMemory, self.currMacro)
        d, orgb = self.configparser.loadForGui(
            ALL_MEMORY_KEYS[self.currMemory],
            ALL_MACRO_KEYS[self.currMacro]
        )

        try:
            self.keyListWidgetContents.setKeyData(d)
        except TypeError:
            self.bottomStatusBar.showMessage("loading failed: ignoring...")
        except Exception as e:
            self.logger.exception(e)
            self.showErrorMSG(str(e))
        
        if d:
            #print("AAAAA", d, d.name, orgb)
            self.macroNameEdit.setText(d.name)

            if d.gamemode > 1:
                self.gameMode.setChecked(True)
                self.gameModeTime.setEnabled(True)
                self.gameModeTime.setValue(d.gamemode)
            else:
                self.gameMode.setChecked(False)
                self.gameModeTime.setDisabled(True)
        else:
            self.macroNameEdit.setText("")
            self.gameMode.setChecked(False)
            self.gameModeTime.setDisabled(True)
        
        self.openRGBedit.setText(orgb)

        self.disableNotifications.setChecked(not self.configparser.getShowNotifications())
        self.minimizeOnStart.setChecked(self.configparser.getMinimizeOnStart())

        orgb = self.configparser.getUseOpenRGB()
        self.useOpenRGB.setChecked(orgb)
        self.frame.setEnabled(orgb)

    ### function overloading
    def keyPressEvent(self, a0: QKeyEvent):
        print(a0.nativeScanCode())
        return super().keyPressEvent(a0)

    def closeEvent(self, event: QCloseEvent):
        if not self.isHidden():
            r = self.showQuestionMSG("Do you want to save unsaved changes?")

            if r == QMessageBox.Cancel:
                event.ignore()
                return
            if r == QMessageBox.Yes:
                self.saveData(saveToFile=True)

        self.service.quit(False)
        self.service.wait()
        self.service.deleteLater()

        self.tray.deleteLater()

        return super().closeEvent(event)

    ### actions
    def openConfigFolder(self):
        openUrl(self.configparser.configFolder)

    def openLogFolder(self):
        openUrl(Configparser.getLogFolder())

    def showGitHub(self):
        openUrl("https://github.com/zocker-160/keyboard-center")

    def showReportIssue(self):
        openUrl("https://github.com/zocker-160/keyboard-center/issues")

    def showOpenRGBsetup(self):
        openUrl("https://github.com/zocker-160/keyboard-center#setup-openrgb-integration")

    def showNotification(self, title: str, msg: str, urgent: bool):
        if urgent:
            self.tray.showError(title, msg)
        else:
            self.tray.showInfo(title, msg)

    def showNotificationIcon(self, title: str, msg: str, iconPath: str):
        if self.disableNotifications.isChecked(): return

        self.tray.showInfoIcon(title, msg, iconPath)

    def forceRestart(self):
        try:
            self.logger.debug("force restarting service")
            self.service.quit(True)
        except:
            pass

    ### popup messages
    @staticmethod
    def showErrorMSG(msg_str, title_msg="ERROR", detailText=""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(str(msg_str))
        msg.setDetailedText(detailText)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        return msg.exec_()

    @staticmethod
    def showInfoMSG(msg_str: str, title_msg="Info"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msg_str)
        msg.setWindowTitle(title_msg)
        msg.setDefaultButton(QMessageBox.Close)
        return msg.exec_()

    @staticmethod
    def showQuestionMSG(msg_str: str, title_msg="Question"):
        msg = QMessageBox()
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
        about = f"""
        <h4>{APP_NAME}</h4>
        Version v{VERSION}
        <br>
        (c) 2021 - 2024 zocker_160
        <br>
        GPLv3
        <br><br>
        <a href="https://github.com/zocker-160/keyboard-center">https://github.com/zocker-160/keyboard-center</a>
        """

        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            about
        )

    def showSettings(self):
        # TODO
        pass

    ### other ui stuff
    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(
            self.app.primaryScreen().availableGeometry().center())
        self.move(qr.topLeft())

    def activateTrigger(self):
        self.logger.debug("window activation from secondary instance triggered")

        self.show()
        self.showNormal()
        self.activateWindow()
