from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QSystemTrayIcon,
    QAction,
    QMenu
)

class TrayIcon(QSystemTrayIcon):

    def __init__(self, parent, icon: QIcon, visible=True):
        super().__init__(icon, parent)

        self.setupUi()
        if visible: self.show()

        self.activated.connect(self._activated)

    def setupUi(self):
        self.hideshowAction = QAction("Hide / Show", self)
        self.hideshowAction.setIcon(QIcon.fromTheme("view-restore"))

        self.restartAction = QAction("Force Restart", self)
        self.restartAction.setIcon(QIcon.fromTheme("view-refresh"))

        self.exitAction = QAction("Exit", self)
        self.exitAction.setIcon(QIcon.fromTheme("application-exit"))

        trayMenu = QMenu(self.parent())
        trayMenu.addAction(self.hideshowAction)
        trayMenu.addSeparator()
        trayMenu.addSeparator()
        trayMenu.addAction(self.restartAction)
        trayMenu.addAction(self.exitAction)

        self.setContextMenu(trayMenu)

    def showInfo(self, title: str, msg: str):
        self.showMessage(title, msg, QSystemTrayIcon.Information)

    def showInfoIcon(self, title: str, msg: str, icon: str):
        self.showMessage(title, msg, QIcon(icon), 2000)

    #def showWarning(self):
    #    pass

    def showError(self, title: str, msg: str):
        self.showMessage(title, msg, QSystemTrayIcon.Critical, 0)

    def _activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason == QSystemTrayIcon.Trigger:
            self.hideshowAction.trigger()
