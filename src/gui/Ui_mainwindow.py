# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(906, 627)
        MainWindow.setStyleSheet("QLabel#asd {\n"
"    image: url(:/icons/MEMORY_1.png);\n"
"    border: 4px solid black;\n"
"    border-radius: 10;\n"
"}\n"
"\n"
"QLabel#asd:hover {\n"
"    border-color: rgb(0, 170, 255);\n"
"}\n"
"\n"
"QLabel#asd:pressed {\n"
"    border-color: red;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.supportedDevice = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.supportedDevice.setFont(font)
        self.supportedDevice.setAlignment(QtCore.Qt.AlignCenter)
        self.supportedDevice.setObjectName("supportedDevice")
        self.horizontalLayout_7.addWidget(self.supportedDevice)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_7.addWidget(self.line_2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.memoryKeySlots = QtWidgets.QHBoxLayout()
        self.memoryKeySlots.setObjectName("memoryKeySlots")
        self.horizontalLayout_6.addLayout(self.memoryKeySlots)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.openRGBedit = QtWidgets.QLineEdit(self.frame)
        self.openRGBedit.setObjectName("openRGBedit")
        self.horizontalLayout.addWidget(self.openRGBedit)
        self.openRGBhelp = QtWidgets.QPushButton(self.frame)
        self.openRGBhelp.setText("")
        icon = QtGui.QIcon.fromTheme("help-about")
        self.openRGBhelp.setIcon(icon)
        self.openRGBhelp.setObjectName("openRGBhelp")
        self.horizontalLayout.addWidget(self.openRGBhelp)
        self.horizontalLayout_6.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea.setObjectName("scrollArea")
        self.macroKeys = QtWidgets.QWidget()
        self.macroKeys.setGeometry(QtCore.QRect(0, 0, 83, 437))
        self.macroKeys.setObjectName("macroKeys")
        self.scrollArea.setWidget(self.macroKeys)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.macroNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.macroNameEdit.setObjectName("macroNameEdit")
        self.horizontalLayout_4.addWidget(self.macroNameEdit)
        self.gameMode = QtWidgets.QCheckBox(self.centralwidget)
        self.gameMode.setObjectName("gameMode")
        self.horizontalLayout_4.addWidget(self.gameMode)
        self.gameModeTime = QtWidgets.QSpinBox(self.centralwidget)
        self.gameModeTime.setMinimum(10)
        self.gameModeTime.setMaximum(1000)
        self.gameModeTime.setSingleStep(10)
        self.gameModeTime.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.gameModeTime.setObjectName("gameModeTime")
        self.horizontalLayout_4.addWidget(self.gameModeTime)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.addKey = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("input-keyboard")
        self.addKey.setIcon(icon)
        self.addKey.setObjectName("addKey")
        self.horizontalLayout_4.addWidget(self.addKey)
        self.addDelay = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.addDelay.setIcon(icon)
        self.addDelay.setObjectName("addDelay")
        self.horizontalLayout_4.addWidget(self.addDelay)
        self.addCommand = QtWidgets.QPushButton(self.centralwidget)
        self.addCommand.setObjectName("addCommand")
        self.horizontalLayout_4.addWidget(self.addCommand)
        self.clearAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearAllButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clearAllButton.setText("")
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.clearAllButton.setIcon(icon)
        self.clearAllButton.setObjectName("clearAllButton")
        self.horizontalLayout_4.addWidget(self.clearAllButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.keyListWidget = QtWidgets.QScrollArea(self.centralwidget)
        self.keyListWidget.setWidgetResizable(True)
        self.keyListWidget.setObjectName("keyListWidget")
        self.keyListWidgetContents = CListWidgetContent()
        self.keyListWidgetContents.setGeometry(QtCore.QRect(0, 0, 797, 385))
        self.keyListWidgetContents.setObjectName("keyListWidgetContents")
        self.keyListWidget.setWidget(self.keyListWidgetContents)
        self.verticalLayout_3.addWidget(self.keyListWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("edit-undo")
        self.resetButton.setIcon(icon)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_3.addWidget(self.resetButton)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_3.addWidget(self.line_3)
        self.disableNotifications = QtWidgets.QCheckBox(self.centralwidget)
        self.disableNotifications.setObjectName("disableNotifications")
        self.horizontalLayout_3.addWidget(self.disableNotifications)
        self.minimizeOnStart = QtWidgets.QCheckBox(self.centralwidget)
        self.minimizeOnStart.setObjectName("minimizeOnStart")
        self.horizontalLayout_3.addWidget(self.minimizeOnStart)
        self.useOpenRGB = QtWidgets.QCheckBox(self.centralwidget)
        self.useOpenRGB.setObjectName("useOpenRGB")
        self.horizontalLayout_3.addWidget(self.useOpenRGB)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.toTrayButton = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("go-bottom")
        self.toTrayButton.setIcon(icon)
        self.toTrayButton.setObjectName("toTrayButton")
        self.horizontalLayout_3.addWidget(self.toTrayButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon.fromTheme("document-save")
        self.saveButton.setIcon(icon)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 906, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.bottomStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.bottomStatusBar.setObjectName("bottomStatusBar")
        MainWindow.setStatusBar(self.bottomStatusBar)
        self.actionGitHub = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("system-help")
        self.actionGitHub.setIcon(icon)
        self.actionGitHub.setObjectName("actionGitHub")
        self.actionReport_issue = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("mail-send")
        self.actionReport_issue.setIcon(icon)
        self.actionReport_issue.setObjectName("actionReport_issue")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.actionAbout_Qt.setIcon(icon)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("help-about")
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExport_config = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-save-as")
        self.actionExport_config.setIcon(icon)
        self.actionExport_config.setObjectName("actionExport_config")
        self.actionOpenConfigFolder = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.actionOpenConfigFolder.setIcon(icon)
        self.actionOpenConfigFolder.setObjectName("actionOpenConfigFolder")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionRestartService = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.actionRestartService.setIcon(icon)
        self.actionRestartService.setObjectName("actionRestartService")
        self.actionOpenLogFolder = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("text")
        self.actionOpenLogFolder.setIcon(icon)
        self.actionOpenLogFolder.setObjectName("actionOpenLogFolder")
        self.menuFile.addAction(self.actionOpenConfigFolder)
        self.menuFile.addAction(self.actionOpenLogFolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRestartService)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionGitHub)
        self.menuAbout.addAction(self.actionReport_issue)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionAbout_Qt)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.gameMode.clicked['bool'].connect(self.gameModeTime.setEnabled) # type: ignore
        self.useOpenRGB.clicked['bool'].connect(self.frame.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Keyboard Center"))
        self.supportedDevice.setText(_translate("MainWindow", "no supported device found :("))
        self.label_2.setText(_translate("MainWindow", "OpenRGB Profile:"))
        self.openRGBhelp.setToolTip(_translate("MainWindow", "just freaking click it!"))
        self.openRGBhelp.setWhatsThis(_translate("MainWindow", "THIS IS A HELP BUTTON!"))
        self.label.setText(_translate("MainWindow", "Profile:"))
        self.macroNameEdit.setPlaceholderText(_translate("MainWindow", "name"))
        self.gameMode.setToolTip(_translate("MainWindow", "<html><head/><body><p>&quot;GameMode&quot; delays the execution of combos.</p><p>Some games truggle to recognize it when execution is too fast.</p></body></html>"))
        self.gameMode.setText(_translate("MainWindow", "GameMode"))
        self.gameModeTime.setToolTip(_translate("MainWindow", "delay in milliseconds"))
        self.gameModeTime.setSuffix(_translate("MainWindow", " ms"))
        self.addKey.setText(_translate("MainWindow", "Add Key"))
        self.addDelay.setText(_translate("MainWindow", "Add Delay"))
        self.addCommand.setText(_translate("MainWindow", "Add Command"))
        self.clearAllButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>delete profile</p></body></html>"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.disableNotifications.setToolTip(_translate("MainWindow", "disables notifications when switching memory profiles"))
        self.disableNotifications.setText(_translate("MainWindow", "disable profile notification"))
        self.minimizeOnStart.setText(_translate("MainWindow", "minimize to tray on start"))
        self.useOpenRGB.setToolTip(_translate("MainWindow", "enable / disable OpenRGB integration"))
        self.useOpenRGB.setText(_translate("MainWindow", "OpenRGB"))
        self.toTrayButton.setText(_translate("MainWindow", "To Tray"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionGitHub.setText(_translate("MainWindow", "GitHub"))
        self.actionReport_issue.setText(_translate("MainWindow", "Report issue"))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExport_config.setText(_translate("MainWindow", "Export config...(soon)"))
        self.actionOpenConfigFolder.setText(_translate("MainWindow", "Open config folder"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionRestartService.setText(_translate("MainWindow", "Force restart driver"))
        self.actionRestartService.setToolTip(_translate("MainWindow", "check status of the background service"))
        self.actionOpenLogFolder.setText(_translate("MainWindow", "Open log folder"))
from gui.customwidgets import CListWidgetContent
from . import ressources_rc
