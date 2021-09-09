# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bene/Programmierkram/GitHub/G910-gui/src/gui/keypressWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeyPressWidget(object):
    def setupUi(self, KeyPressWidget):
        KeyPressWidget.setObjectName("KeyPressWidget")
        KeyPressWidget.resize(726, 53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(KeyPressWidget.sizePolicy().hasHeightForWidth())
        KeyPressWidget.setSizePolicy(sizePolicy)
        KeyPressWidget.setMinimumSize(QtCore.QSize(0, 40))
        KeyPressWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        KeyPressWidget.setAutoFillBackground(True)
        KeyPressWidget.setStyleSheet("QWidget {\n"
"    #this does break dark mode stupid me\n"
"    #background-color: white;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(KeyPressWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(KeyPressWidget)
        self.label.setMinimumSize(QtCore.QSize(25, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ctrlMod = QtWidgets.QPushButton(KeyPressWidget)
        self.ctrlMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ctrlMod.setStyleSheet("QPushButton:selected {\n"
"        color: white;\n"
"}")
        self.ctrlMod.setCheckable(True)
        self.ctrlMod.setObjectName("ctrlMod")
        self.horizontalLayout.addWidget(self.ctrlMod)
        self.altMod = QtWidgets.QPushButton(KeyPressWidget)
        self.altMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.altMod.setCheckable(True)
        self.altMod.setObjectName("altMod")
        self.horizontalLayout.addWidget(self.altMod)
        self.shiftMod = QtWidgets.QPushButton(KeyPressWidget)
        self.shiftMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.shiftMod.setCheckable(True)
        self.shiftMod.setObjectName("shiftMod")
        self.horizontalLayout.addWidget(self.shiftMod)
        self.metaMod = QtWidgets.QPushButton(KeyPressWidget)
        self.metaMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.metaMod.setCheckable(True)
        self.metaMod.setObjectName("metaMod")
        self.horizontalLayout.addWidget(self.metaMod)
        self.keySequenceEdit = CKeySequenceEdit(KeyPressWidget)
        self.keySequenceEdit.setObjectName("keySequenceEdit")
        self.horizontalLayout.addWidget(self.keySequenceEdit)
        self.clearButton = QtWidgets.QPushButton(KeyPressWidget)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.clearButton.setIcon(icon)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.line_2 = QtWidgets.QFrame(KeyPressWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.moveUp = QtWidgets.QPushButton(KeyPressWidget)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.moveUp.setIcon(icon)
        self.moveUp.setObjectName("moveUp")
        self.horizontalLayout.addWidget(self.moveUp)
        self.moveDown = QtWidgets.QPushButton(KeyPressWidget)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.moveDown.setIcon(icon)
        self.moveDown.setObjectName("moveDown")
        self.horizontalLayout.addWidget(self.moveDown)
        self.line = QtWidgets.QFrame(KeyPressWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.delButton = QtWidgets.QPushButton(KeyPressWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.delButton.setIcon(icon)
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)

        self.retranslateUi(KeyPressWidget)
        self.clearButton.clicked.connect(self.keySequenceEdit.clear)
        self.delButton.clicked.connect(KeyPressWidget._remove)
        self.moveDown.clicked.connect(KeyPressWidget._moveDown)
        self.moveUp.clicked.connect(KeyPressWidget._moveUp)
        self.clearButton.clicked['bool'].connect(self.ctrlMod.setChecked)
        self.clearButton.clicked['bool'].connect(self.altMod.setChecked)
        self.clearButton.clicked['bool'].connect(self.shiftMod.setChecked)
        self.clearButton.clicked['bool'].connect(self.metaMod.setChecked)
        QtCore.QMetaObject.connectSlotsByName(KeyPressWidget)

    def retranslateUi(self, KeyPressWidget):
        _translate = QtCore.QCoreApplication.translate
        KeyPressWidget.setWindowTitle(_translate("KeyPressWidget", "Form"))
        self.label.setText(_translate("KeyPressWidget", "X."))
        self.ctrlMod.setText(_translate("KeyPressWidget", "Ctrl"))
        self.altMod.setText(_translate("KeyPressWidget", "Alt"))
        self.shiftMod.setText(_translate("KeyPressWidget", "Shift"))
        self.metaMod.setText(_translate("KeyPressWidget", "Meta"))
from gui.customwidgets import CKeySequenceEdit
