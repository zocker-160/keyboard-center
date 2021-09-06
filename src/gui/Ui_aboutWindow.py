# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bene/Programmierkram/GitHub/G910-gui/src/gui/aboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aboutWindow(object):
    def setupUi(self, aboutWindow):
        aboutWindow.setObjectName("aboutWindow")
        aboutWindow.resize(625, 142)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(aboutWindow.sizePolicy().hasHeightForWidth())
        aboutWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/input-keyboard-virtual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        aboutWindow.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(aboutWindow)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(aboutWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(128, 128))
        self.label_3.setMaximumSize(QtCore.QSize(128, 128))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/icons/assets/input-keyboard-virtual.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.about_maintext = QtWidgets.QLabel(aboutWindow)
        self.about_maintext.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.about_maintext.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.about_maintext.setObjectName("about_maintext")
        self.horizontalLayout.addWidget(self.about_maintext)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(aboutWindow)
        QtCore.QMetaObject.connectSlotsByName(aboutWindow)

    def retranslateUi(self, aboutWindow):
        _translate = QtCore.QCoreApplication.translate
        aboutWindow.setWindowTitle(_translate("aboutWindow", "About"))
        self.about_maintext.setText(_translate("aboutWindow", "<html><head/><body><p>Keyboard Center - $$$</p><p>made by zocker_160</p><p>licensed under GPLv3 | 2021</p><p>source code: <a href=\"https://github.com/zocker-160/keyboard-center\"><span style=\" text-decoration: underline; color:#2980b9;\">https://github.com/zocker-160/keyboard-center</span></a></p></body></html>"))
from . import ressources_rc
