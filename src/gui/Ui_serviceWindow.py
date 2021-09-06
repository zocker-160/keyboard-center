# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bene/Programmierkram/GitHub/G910-gui/src/gui/serviceWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_serviceWindow(object):
    def setupUi(self, serviceWindow):
        serviceWindow.setObjectName("serviceWindow")
        serviceWindow.resize(358, 144)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/input-keyboard-virtual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        serviceWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(serviceWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainText = QtWidgets.QLabel(serviceWindow)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.mainText.setFont(font)
        self.mainText.setText("")
        self.mainText.setObjectName("mainText")
        self.verticalLayout.addWidget(self.mainText, 0, QtCore.Qt.AlignHCenter)
        self.informativeText = QtWidgets.QLabel(serviceWindow)
        self.informativeText.setText("")
        self.informativeText.setObjectName("informativeText")
        self.verticalLayout.addWidget(self.informativeText, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ignoreButton = QtWidgets.QPushButton(serviceWindow)
        self.ignoreButton.setObjectName("ignoreButton")
        self.horizontalLayout.addWidget(self.ignoreButton)
        self.retryButton = QtWidgets.QPushButton(serviceWindow)
        self.retryButton.setEnabled(False)
        icon = QtGui.QIcon.fromTheme("edit-undo")
        self.retryButton.setIcon(icon)
        self.retryButton.setObjectName("retryButton")
        self.horizontalLayout.addWidget(self.retryButton)
        self.cancelButton = QtWidgets.QPushButton(serviceWindow)
        icon = QtGui.QIcon.fromTheme("process-stop")
        self.cancelButton.setIcon(icon)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(serviceWindow)
        QtCore.QMetaObject.connectSlotsByName(serviceWindow)

    def retranslateUi(self, serviceWindow):
        _translate = QtCore.QCoreApplication.translate
        serviceWindow.setWindowTitle(_translate("serviceWindow", "Dialog"))
        self.ignoreButton.setText(_translate("serviceWindow", "Ignore"))
        self.retryButton.setText(_translate("serviceWindow", "Retry"))
        self.cancelButton.setText(_translate("serviceWindow", "Cancel"))
from . import ressources_rc
