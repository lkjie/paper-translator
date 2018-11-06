# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PaperUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PaperTran(object):
    def setupUi(self, PaperTran):
        PaperTran.setObjectName("PaperTran")
        PaperTran.resize(1200, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PaperTran.sizePolicy().hasHeightForWidth())
        PaperTran.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(PaperTran)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_1 = QtWidgets.QTextEdit(PaperTran)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit_1")
        self.gridLayout.addWidget(self.textEdit_1, 2, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(PaperTran)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(PaperTran)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.checkBox = QtWidgets.QCheckBox(PaperTran)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_1.addWidget(self.checkBox)
        self.pushButton = QtWidgets.QPushButton(PaperTran)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_1.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(PaperTran)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_1.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.verticalLayout_1, 2, 1, 1, 1)
        self.textEdit_3 = QtWidgets.QTextEdit(PaperTran)
        self.textEdit_3.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout.addWidget(self.textEdit_3, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(PaperTran)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(PaperTran)
        QtCore.QMetaObject.connectSlotsByName(PaperTran)

    def retranslateUi(self, PaperTran):
        _translate = QtCore.QCoreApplication.translate
        PaperTran.setWindowTitle(_translate("PaperTran", "Form"))
        self.label_2.setText(_translate("PaperTran", "TextLabel"))
        self.checkBox.setText(_translate("PaperTran", "CheckBox"))
        self.pushButton.setText(_translate("PaperTran", "PushButton"))
        self.pushButton_2.setText(_translate("PaperTran", "PushButton"))
        self.label.setText(_translate("PaperTran", "TextLabel"))

