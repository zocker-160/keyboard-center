# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bene/Programmierkram/GitHub/G910-gui/src/gui/delayWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DelayWidget(object):
    def setupUi(self, DelayWidget):
        DelayWidget.setObjectName("DelayWidget")
        DelayWidget.resize(726, 53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DelayWidget.sizePolicy().hasHeightForWidth())
        DelayWidget.setSizePolicy(sizePolicy)
        DelayWidget.setMinimumSize(QtCore.QSize(0, 40))
        DelayWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        DelayWidget.setAutoFillBackground(True)
        DelayWidget.setStyleSheet("QWidget {\n"
"    #this does break dark mode stupid me\n"
"    #background-color: white;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(DelayWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(DelayWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(20, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(DelayWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox = QtWidgets.QSpinBox(DelayWidget)
        self.spinBox.setMaximum(10000)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.clearButton = QtWidgets.QPushButton(DelayWidget)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.clearButton.setIcon(icon)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.line_2 = QtWidgets.QFrame(DelayWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.moveUp = QtWidgets.QPushButton(DelayWidget)
        icon = QtGui.QIcon.fromTheme("go-up")
        self.moveUp.setIcon(icon)
        self.moveUp.setObjectName("moveUp")
        self.horizontalLayout.addWidget(self.moveUp)
        self.moveDown = QtWidgets.QPushButton(DelayWidget)
        icon = QtGui.QIcon.fromTheme("go-down")
        self.moveDown.setIcon(icon)
        self.moveDown.setObjectName("moveDown")
        self.horizontalLayout.addWidget(self.moveDown)
        self.line = QtWidgets.QFrame(DelayWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.delButton = QtWidgets.QPushButton(DelayWidget)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.delButton.setIcon(icon)
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)

        self.retranslateUi(DelayWidget)
        self.delButton.clicked.connect(DelayWidget._remove)
        self.moveDown.clicked.connect(DelayWidget._moveDown)
        self.moveUp.clicked.connect(DelayWidget._moveUp)
        QtCore.QMetaObject.connectSlotsByName(DelayWidget)

    def retranslateUi(self, DelayWidget):
        _translate = QtCore.QCoreApplication.translate
        DelayWidget.setWindowTitle(_translate("DelayWidget", "Form"))
        self.label.setText(_translate("DelayWidget", "X."))
        self.label_2.setText(_translate("DelayWidget", "Delay:"))
        self.spinBox.setSuffix(_translate("DelayWidget", " ms"))
