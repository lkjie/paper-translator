# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cibaUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CiBaTran(object):
    def setupUi(self, CiBaTran):
        CiBaTran.setObjectName("CiBaTran")
        CiBaTran.resize(1200, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CiBaTran.sizePolicy().hasHeightForWidth())
        CiBaTran.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(CiBaTran)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_1 = QtWidgets.QTextEdit(CiBaTran)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit_1")
        self.gridLayout.addWidget(self.textEdit_1, 2, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(CiBaTran)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(CiBaTran)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.checkBox = QtWidgets.QCheckBox(CiBaTran)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_1.addWidget(self.checkBox)
        self.pushButton = QtWidgets.QPushButton(CiBaTran)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_1.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(CiBaTran)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_1.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.verticalLayout_1, 2, 1, 1, 1)
        self.textEdit_3 = QtWidgets.QTextEdit(CiBaTran)
        self.textEdit_3.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout.addWidget(self.textEdit_3, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(CiBaTran)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(CiBaTran)
        QtCore.QMetaObject.connectSlotsByName(CiBaTran)

    def retranslateUi(self, CiBaTran):
        _translate = QtCore.QCoreApplication.translate
        CiBaTran.setWindowTitle(_translate("CiBaTran", "Form"))
        self.label_2.setText(_translate("CiBaTran", "TextLabel"))
        self.checkBox.setText(_translate("CiBaTran", "CheckBox"))
        self.pushButton.setText(_translate("CiBaTran", "PushButton"))
        self.pushButton_2.setText(_translate("CiBaTran", "PushButton"))
        self.label.setText(_translate("CiBaTran", "TextLabel"))

