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
        KeyPressWidget.resize(814, 100)
        KeyPressWidget.setMinimumSize(QtCore.QSize(0, 100))
        KeyPressWidget.setMaximumSize(QtCore.QSize(16777215, 125))
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
        self.modBox = QtWidgets.QFrame(KeyPressWidget)
        self.modBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.modBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.modBox.setObjectName("modBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.modBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.modBoxButtons = QtWidgets.QHBoxLayout()
        self.modBoxButtons.setObjectName("modBoxButtons")
        self.ctrlMod = QtWidgets.QPushButton(self.modBox)
        self.ctrlMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ctrlMod.setStyleSheet("QPushButton:selected {\n"
"        color: white;\n"
"}")
        self.ctrlMod.setCheckable(True)
        self.ctrlMod.setObjectName("ctrlMod")
        self.modBoxButtons.addWidget(self.ctrlMod)
        self.shiftMod = QtWidgets.QPushButton(self.modBox)
        self.shiftMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.shiftMod.setCheckable(True)
        self.shiftMod.setObjectName("shiftMod")
        self.modBoxButtons.addWidget(self.shiftMod)
        self.altMod = QtWidgets.QPushButton(self.modBox)
        self.altMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.altMod.setCheckable(True)
        self.altMod.setObjectName("altMod")
        self.modBoxButtons.addWidget(self.altMod)
        self.metaMod = QtWidgets.QPushButton(self.modBox)
        self.metaMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.metaMod.setCheckable(True)
        self.metaMod.setObjectName("metaMod")
        self.modBoxButtons.addWidget(self.metaMod)
        self.customMod = QtWidgets.QPushButton(self.modBox)
        self.customMod.setFocusPolicy(QtCore.Qt.NoFocus)
        self.customMod.setCheckable(True)
        self.customMod.setObjectName("customMod")
        self.modBoxButtons.addWidget(self.customMod)
        self.verticalLayout_2.addLayout(self.modBoxButtons)
        self.customModBox = QtWidgets.QFrame(self.modBox)
        self.customModBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.customModBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.customModBox.setObjectName("customModBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.customModBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.customModBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.customSequenceEdit = CKeySequenceEdit(self.customModBox)
        self.customSequenceEdit.setObjectName("customSequenceEdit")
        self.horizontalLayout_2.addWidget(self.customSequenceEdit)
        self.clearButton2 = QtWidgets.QPushButton(self.customModBox)
        self.clearButton2.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.clearButton2.setIcon(icon)
        self.clearButton2.setFlat(True)
        self.clearButton2.setObjectName("clearButton2")
        self.horizontalLayout_2.addWidget(self.clearButton2)
        self.verticalLayout_2.addWidget(self.customModBox)
        self.horizontalLayout.addWidget(self.modBox)
        self.keyBox = QtWidgets.QFrame(KeyPressWidget)
        self.keyBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.keyBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.keyBox.setObjectName("keyBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.keyBox)
        self.verticalLayout.setContentsMargins(4, -1, 4, 1)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.keyBoxInput = QtWidgets.QHBoxLayout()
        self.keyBoxInput.setObjectName("keyBoxInput")
        self.keySequenceEdit = CKeySequenceEdit(self.keyBox)
        self.keySequenceEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.keySequenceEdit.setObjectName("keySequenceEdit")
        self.keyBoxInput.addWidget(self.keySequenceEdit)
        self.clearButton = QtWidgets.QPushButton(self.keyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.clearButton.setIcon(icon)
        self.clearButton.setFlat(True)
        self.clearButton.setObjectName("clearButton")
        self.keyBoxInput.addWidget(self.clearButton)
        self.verticalLayout.addLayout(self.keyBoxInput)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rawInputDescr = QtWidgets.QLabel(self.keyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawInputDescr.sizePolicy().hasHeightForWidth())
        self.rawInputDescr.setSizePolicy(sizePolicy)
        self.rawInputDescr.setObjectName("rawInputDescr")
        self.horizontalLayout_3.addWidget(self.rawInputDescr)
        self.rawInputLabel = QtWidgets.QLabel(self.keyBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawInputLabel.sizePolicy().hasHeightForWidth())
        self.rawInputLabel.setSizePolicy(sizePolicy)
        self.rawInputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rawInputLabel.setObjectName("rawInputLabel")
        self.horizontalLayout_3.addWidget(self.rawInputLabel)
        self.setNullKeyButton = QtWidgets.QPushButton(self.keyBox)
        self.setNullKeyButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setNullKeyButton.setText("")
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.setNullKeyButton.setIcon(icon)
        self.setNullKeyButton.setFlat(True)
        self.setNullKeyButton.setObjectName("setNullKeyButton")
        self.horizontalLayout_3.addWidget(self.setNullKeyButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.keyBox)
        self.moveUp = QtWidgets.QPushButton(KeyPressWidget)
        self.moveUp.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.moveUp.setIcon(icon)
        self.moveUp.setObjectName("moveUp")
        self.horizontalLayout.addWidget(self.moveUp)
        self.moveDown = QtWidgets.QPushButton(KeyPressWidget)
        self.moveDown.setFocusPolicy(QtCore.Qt.NoFocus)
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
        self.delButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.delButton.setIcon(icon)
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)

        self.retranslateUi(KeyPressWidget)
        self.delButton.clicked.connect(KeyPressWidget._remove)
        self.moveDown.clicked.connect(KeyPressWidget._moveDown)
        self.moveUp.clicked.connect(KeyPressWidget._moveUp)
        self.customMod.clicked['bool'].connect(self.customModBox.setVisible)
        self.clearButton2.clicked.connect(self.customSequenceEdit.clear)
        self.clearButton.clicked.connect(self.keySequenceEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(KeyPressWidget)

    def retranslateUi(self, KeyPressWidget):
        _translate = QtCore.QCoreApplication.translate
        KeyPressWidget.setWindowTitle(_translate("KeyPressWidget", "Form"))
        self.label.setText(_translate("KeyPressWidget", "X."))
        self.ctrlMod.setText(_translate("KeyPressWidget", "Ctrl"))
        self.shiftMod.setText(_translate("KeyPressWidget", "Shift"))
        self.altMod.setText(_translate("KeyPressWidget", "Alt"))
        self.metaMod.setText(_translate("KeyPressWidget", "Meta"))
        self.customMod.setText(_translate("KeyPressWidget", "Custom..."))
        self.label_2.setText(_translate("KeyPressWidget", "Custom Modifier: "))
        self.rawInputDescr.setText(_translate("KeyPressWidget", "raw:"))
        self.rawInputLabel.setText(_translate("KeyPressWidget", "--"))
        self.setNullKeyButton.setToolTip(_translate("KeyPressWidget", "set NULLKEY"))
from gui.customwidgets import CKeySequenceEdit
