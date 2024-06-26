# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/commandWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CommandWidget(object):
    def setupUi(self, CommandWidget):
        CommandWidget.setObjectName("CommandWidget")
        CommandWidget.resize(726, 54)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CommandWidget.sizePolicy().hasHeightForWidth())
        CommandWidget.setSizePolicy(sizePolicy)
        CommandWidget.setMinimumSize(QtCore.QSize(0, 40))
        CommandWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        CommandWidget.setAutoFillBackground(True)
        CommandWidget.setStyleSheet("QWidget {\n"
"    #this does break dark mode stupid me\n"
"    #background-color: white;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(CommandWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CommandWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(20, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(CommandWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.commandEdit = QtWidgets.QLineEdit(CommandWidget)
        self.commandEdit.setClearButtonEnabled(True)
        self.commandEdit.setObjectName("commandEdit")
        self.horizontalLayout.addWidget(self.commandEdit)
        self.line_2 = QtWidgets.QFrame(CommandWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.moveUp = QtWidgets.QPushButton(CommandWidget)
        self.moveUp.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.moveUp.setIcon(icon)
        self.moveUp.setObjectName("moveUp")
        self.verticalLayout.addWidget(self.moveUp)
        self.moveDown = QtWidgets.QPushButton(CommandWidget)
        self.moveDown.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.moveDown.setIcon(icon)
        self.moveDown.setObjectName("moveDown")
        self.verticalLayout.addWidget(self.moveDown)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(CommandWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.delButton = QtWidgets.QPushButton(CommandWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.delButton.setIcon(icon)
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)

        self.retranslateUi(CommandWidget)
        self.delButton.clicked.connect(CommandWidget._remove) # type: ignore
        self.moveDown.clicked.connect(CommandWidget._moveDown) # type: ignore
        self.moveUp.clicked.connect(CommandWidget._moveUp) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CommandWidget)

    def retranslateUi(self, CommandWidget):
        _translate = QtCore.QCoreApplication.translate
        CommandWidget.setWindowTitle(_translate("CommandWidget", "Form"))
        self.label.setText(_translate("CommandWidget", "X."))
        self.label_2.setText(_translate("CommandWidget", "Command:"))
        self.commandEdit.setPlaceholderText(_translate("CommandWidget", "put command (e.g. konsole -e htop or cowsay \"nvidia sucks\")"))
