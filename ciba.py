# -*- coding: utf-8 -*-

import time, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyperclip
import requests
import json

try:
    translated = json.load(open('translated.json'))
except Exception as e:
    translated = {}

# size
LABEL_STRAT_X = 20
LABEL_STRAT_Y = 20
LABEL_WIDTH = 200
LABEL_HEIGTH = 20
TEXTSOURCE_WIDTH = 600
TEXTSOURCE_HEIGTH = 200
BUTTON_WIDTH = 150
BUTTON_HEIGTH = 80
TEXTTRANS_WIDTH = TEXTSOURCE_WIDTH + BUTTON_WIDTH * 1.2
TEXTTRANS_HEIGTH = TEXTSOURCE_HEIGTH + BUTTON_HEIGTH * 1.2


class Form(QtWidgets.QWidget):
    def __init__(self):
        super(Form, self).__init__()
        self.setupUi(self)
        self.timer = MyTimer(self.textEdit_1)
        self.timer.trigger.connect(self.setSourceAndTransText)
        self.timer.word_trigger.connect(self.setWordText)

    def setupUi(self, Form):
        # # move window
        # window = QtWidgets.QWidget()
        # desktop = QtWidgets.QApplication.desktop()
        # x = (desktop.width() - window.width())
        # y = 0
        # CiBaTran.move(x, y)
        # # move window end

        Form.setObjectName("CiBaTran")
        Form.resize(1200, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_1 = QtWidgets.QTextEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_1.setFont(font)
        self.textEdit_1.setObjectName("textEdit_1")
        self.gridLayout.addWidget(self.textEdit_1, 2, 0, 1, 1)
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.textEdit_2, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.pushButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_1.addWidget(self.pushButton, alignment=QtCore.Qt.AlignCenter)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMaximumSize(QtCore.QSize(120, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_1.addWidget(self.pushButton_2, alignment=QtCore.Qt.AlignCenter)
        self.gridLayout.addLayout(self.verticalLayout_1, 2, 1, 1, 1)
        self.textEdit_3 = QtWidgets.QTextEdit(Form)
        self.textEdit_3.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setObjectName("textEdit_3")
        self.gridLayout.addWidget(self.textEdit_3, 6, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(Form.trans)
        self.pushButton_2.clicked.connect(self.textEdit_1.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            QtCore.Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端

    def retranslateUi(self, CiBaTran):
        _translate = QtCore.QCoreApplication.translate
        CiBaTran.setWindowTitle(_translate("CiBaTran", "词霸翻译"))
        self.label.setText(_translate("CiBaTran", "请输入要翻译的英文"))
        self.pushButton.setText(_translate("CiBaTran", "点击翻译"))
        self.pushButton_2.setText(_translate("CiBaTran", "清空"))
        self.label_2.setText(_translate("CiBaTran", "翻译结果"))

    def setTransText(self, str1):
        self.textEdit_2.clear()
        self.textEdit_2.append(str1)
        self.changeFontSize(self.textEdit_2)

    def setSourceText(self, str1):
        self.textEdit_1.clear()
        self.textEdit_1.append(str1)
        self.changeFontSize(self.textEdit_1)

    def setSourceAndTransText(self, source, tran_txt):
        self.setTransText(tran_txt)
        self.setSourceText(source)

    def setWordText(self, str1):
        self.textEdit_3.clear()
        self.textEdit_3.append(str1)
        self.changeFontSize(self.textEdit_3, 10)

    def trans(self):
        textData = self.textEdit_1.toPlainText()
        source, tran_txt = translateByCiBa(textData)
        self.setTransText(tran_txt)
        self.setSourceText(source)

    def changeFontSize(self, edit, fontsize=15):
        cursor = edit.textCursor()
        edit.selectAll()
        edit.setFontPointSize(fontsize)
        edit.setTextCursor(cursor)


def translateByCiBa(textData):
    results = textData.replace('\n', ' ').replace('- ', '')
    if results in translated:
        return results, translated[textData]
    res_tran = requests.post('http://fy.iciba.com/ajax.php?a=fy', data={'w': results}).json()
    content = res_tran.get('content', {})
    if 'out' in content.keys():
        tran_txt = content['out']
    elif 'word_mean' in content.keys():
        tran_txt = '\n'.join(content['word_mean'])
    else:
        return results, ''
    if len(translated.keys()) > 100000:
        translated.clear()
    translated[textData] = tran_txt
    json.dump(translated, open('translated.json', 'w'), ensure_ascii=False, indent=4)
    return results, tran_txt


class MyTimer(QtWidgets.QWidget):
    trigger = pyqtSignal(str, str)
    word_trigger = pyqtSignal(str)

    def __init__(self, sender, parent=None):
        super().__init__(parent)
        self.editor = sender
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)

    # 定义槽
    def onTimerOut(self):
        textData = self.editor.toPlainText()
        clipText = pyperclip.paste()
        cursor = self.editor.textCursor()
        textSelected = cursor.selectedText()
        source1, tran_txt1 = translateByCiBa(textSelected)
        self.word_trigger.emit(tran_txt1)
        if not textData and not clipText or clipText in translated.keys() and textData in translated.keys():
            return
        if not textData or (clipText and clipText not in translated.keys()):
            textData = clipText
            self.editor.append(textData)
        source, tran_txt = translateByCiBa(textData)
        # 等待5秒后，给触发信号，并传递test
        self.trigger.emit(source, tran_txt)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Form()
    myshow.show()
    sys.exit(app.exec_())
