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
    QMainWindow,
    QMessageBox,
    QDialog
)

from lib.QSingleApplication import QSingleApplication
from lib import utils

from gui.tray import TrayIcon
from gui.Ui_mainwindow import Ui_MainWindow
from gui.customwidgets import CommandWidget, DelayWidget, KeyPressWidget, CEntryButton
from gui.settingswindow import SettingsWindow

from config import config
from config.constants import *

from devices.allkeys import Mkey, Gkey
from devices.keyboard import SUPPORTED_DEVICES, KeyboardInterface

from service import BackgroundService, NoKeyboardException, NoEndpointException

PLACEHOLDER_STR = "$$$"

class MainWindow(QMainWindow, Ui_MainWindow):

    service: BackgroundService = None
    usbDevice: KeyboardInterface = None
    
    currMkey: Mkey = Mkey.M1
    currGkey: Gkey = Gkey.G1

    def __init__(self, 
            app: QSingleApplication, 
            devmode=False, trayVisible=True):
        super().__init__()
        self.app = app
        self.devmode = devmode
        self.logger = logging.getLogger("GUI")

        self.app.onActivate.connect(self.activateTrigger)

        self.healthCheck = QTimer(self)
        self.healthCheck.timeout.connect(self._serviceHealthCheck)

        self.config = self.loadConfiguration()
        
        self.initBackgroundService() # TODO
        self.initUsbDevice()

        self.icon = QIcon.fromTheme("keyboard-center", QIcon.fromTheme("preferences-desktop-keyboard"))
        self.tray = TrayIcon(self, self.icon, trayVisible)

        self.initUI()
        self.initSlots()

        # workaround for weird KDE bug where spinner keeps running
        # in task bar despite app being long started
        # by calling show() we make sure the spinner stops
        # and then we hide() afterwards when needed
        self.show()
        if not self.devmode and self.config.data.settings.minimizeOnStart:
            self.hide()

    def initUI(self):
        self.logger.debug("setting up GUI")
        self.setupUi(self)
        self.setWindowIcon(self.icon)
        self.initProfileButtons()

    def initProfileButtons(self):
        for i in range(self.usbDevice.numMemoryKeys):
            key = Mkey(i+1) # Mkey count starts at 1

            btn = CEntryButton(self, key, vert=False)
            btn.onSelection.connect(self.setCurrMkey)

            self.memoryKeySlots.addWidget(btn)

        for y in range(self.usbDevice.numMacroKeys):
            key = Gkey(y+1) # Gkey count starts at 1

            btn = CEntryButton(self, key, vert=True)
            btn.onSelection.connect(self.setCurrGkey)

            self.macroKeySlots.addWidget(btn)

        # set device name
        self.supportedDevice.setText(self.usbDevice.devicename)

        # enable buttons
        self.saveButton.setEnabled(True)
        self.resetButton.setEnabled(True)

        self.updateProfileButtons()
        self.loadData()

    def updateProfileButtons(self):
        for i in range(self.memoryKeySlots.count()):
            w = self.memoryKeySlots.itemAt(i).widget()

            if isinstance(w, CEntryButton):
                w.setChecked(self.currMkey == w.key)

        for i in range(self.macroKeySlots.count()):
            w = self.macroKeySlots.itemAt(i).widget()

            if isinstance(w, CEntryButton):
                w.setChecked(self.currGkey == w.key)

    def initSlots(self):
        self.actionOpenConfigFolder.triggered.connect(self.openConfigFolder)
        self.actionOpenLogFolder.triggered.connect(self.openLogFolder)
        self.actionSettings.triggered.connect(self.showSettings)
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

    def loadConfiguration(self) -> config.ConfigLoader:
        try:
            cl = config.ConfigLoader()
            cl.load()
            return cl
        except Exception as e:
            self.showErrorMSG(
                "Failed to load configuration file! \n\n",
                detailText=str(e),
                title_msg="FATAL ERROR"
            )
            raise

    def initBackgroundService(self):
        if self.service:
            self.logger.debug("waiting for BGService")
            self.service.wait()
            self.service.deleteLater()
            self.service = None

        try:
            self.service = BackgroundService(self.config, self.devmode)
            self.service.notificationEvent.connect(self.showNotification)
            self.service.notificationIconEvent.connect(self.showNotificationIcon)
            self.service.quitTriggered.connect(self._forcedHealthCheck)
            self.service.start()

        except NoKeyboardException:
            # TODO
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

        #self.logger.debug("starting health check")
        #self.healthCheck.start(1000 * 10) # every 10 seconds

    def initUsbDevice(self):
        try:
            self.usbDevice = SUPPORTED_DEVICES[self.config.data.settings.usbDeviceID]
        except Exception as e:
            self.showErrorMSG(
                f"Error during loading of keyboard config! \n\n",
                detailText=f"err:({str(e)})",
                title_msg="FATAL ERROR")
            raise

    def setCurrMkey(self, key: Mkey, save=True):
        if save and not self.saveData():
            return
        
        self.currMkey = key
        self.updateProfileButtons()
        self.loadData()

    def setCurrGkey(self, key: Gkey, save=True):
        if save and not self.saveData():
            return

        self.currGkey = key
        self.updateProfileButtons()
        self.loadData()

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
            self.loadConfiguration_renameME()


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


    def addBlankKeyWidget(self):
        self.keyListWidgetContents.addWidget(KeyPressWidget(self))

    def addBlankDelayWidget(self):
        self.keyListWidgetContents.addWidget(DelayWidget(self))

    def addBlankCommandWidget(self):
        self.keyListWidgetContents.addWidget(CommandWidget(self))

    def saveData(self, saveToFile=False) -> bool:
        self.logger.debug("saving")

        try:
            self.config.data.setRGBprofile(self.currMkey, self.openRGBedit.text())
            self.config.data.setEntry(self.currMkey, self.currGkey, config.Entry(
                name=self.macroNameEdit.text(),
                type=config.EntryType.UI,
                gamemode=self.gameModeTime.value() if self.gameMode.isChecked() else 0,
                values=self.keyListWidgetContents.getData()
            ))

            if saveToFile:
                self.logger.info("saving to disk")
                self.config.save()
                self.bottomStatusBar.showMessage(
                    "Configuration saved to file", 2000)

            return True

        except ValueError as e:
            self.showErrorMSG(str(e))
            return False
        except Exception as e:
            self.showErrorMSG(str(e)) # TODO create better error message
            self.logger.exception(e)
            return False

    def loadData(self):
        self.logger.debug(f"loading {self.currMkey.name} / {self.currGkey.name}")

        #self.frame.setEnabled(self.config.data.settings.useOpenRGB)
        self.openRGBedit.setText(self.config.data.getRGBprofile(self.currMkey))

        self.keyListWidgetContents.clearAllEntries()
        entry = self.config.data.getEntry(self.currMkey, self.currGkey)
        if entry:
            self.macroNameEdit.setText(entry.name)
            if entry.gamemode > 1:
                self.gameMode.setChecked(True)
                self.gameModeTime.setEnabled(True)
                self.gameModeTime.setValue(entry.gamemode)
            else:
                self.gameMode.setChecked(False)
                self.gameModeTime.setDisabled(True)

            if entry.type == config.EntryType.UI:
                self.keyListWidgetContents.setData(entry.values)
            else:
                # TODO
                pass
        else:
            self.macroNameEdit.setText("")
            self.gameMode.setChecked(False)
            self.gameModeTime.setDisabled(True)

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
        utils.openUrl(self.config.configFolder)

    def openLogFolder(self):
        utils.openUrl(utils.getLogFolder())

    def showGitHub(self):
        utils.openUrl("https://github.com/zocker-160/keyboard-center")

    def showReportIssue(self):
        utils.openUrl("https://github.com/zocker-160/keyboard-center/issues")

    def showOpenRGBsetup(self):
        utils.openUrl("https://github.com/zocker-160/keyboard-center#setup-openrgb-integration")

    def showNotification(self, title: str, msg: str, urgent: bool):
        if urgent:
            self.tray.showError(title, msg)
        else:
            self.tray.showInfo(title, msg)

    def showNotificationIcon(self, title: str, msg: str, iconPath: str):
        if self.config.data.settings.showNotifications:
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
        settings = SettingsWindow(self, self.config)
        if settings.exec() == 1:
            self.config.save()


    ### other ui stuff
    def activateTrigger(self):
        self.logger.debug("window activation from secondary instance triggered")

        self.show()
        self.showNormal()
        self.activateWindow()
