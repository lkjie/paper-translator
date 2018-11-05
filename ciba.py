# -*- coding: utf-8 -*-

import time, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyperclip
import requests
import json
import os

from cibaUI import Ui_CiBaTran


try:
    translated = json.load(open('translated.json'))
except Exception as e:
    translated = {}


class Form(QtWidgets.QWidget, Ui_CiBaTran):

    def __init__(self):
        super(Form, self).__init__()
        self.setupUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - self.width())
        y = (desktop.height() - self.height())
        self.move(x, y)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            QtCore.Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端

        self.pushButton.clicked.connect(self.trans)
        self.pushButton_2.clicked.connect(self.textEdit_1.clear)
        self.timer = MyTimer(self.textEdit_1)
        self.timer.trigger.connect(self.setSourceAndTransText)
        self.timer.word_trigger.connect(self.setWordText)
        self.checkBox.toggle()
        self.checkBox.stateChanged.connect(self.timer.changeDetect)

    def retranslateUi(self, CiBaTran):
        _translate = QtCore.QCoreApplication.translate
        CiBaTran.setWindowTitle(_translate("CiBaTran", "词霸翻译"))
        self.label.setText(_translate("CiBaTran", "请输入要翻译的英文"))
        self.pushButton.setText(_translate("CiBaTran", "点击翻译"))
        self.pushButton_2.setText(_translate("CiBaTran", "清空"))
        self.label_2.setText(_translate("CiBaTran", "翻译结果"))
        self.checkBox.setText(_translate("CiBaTran", "检测剪切板"))

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
    # keep faster
    if len(translated.keys()) > 100000:
        os.rename('translated.json','translated.json.bak')
        translated.clear()
    translated[textData] = tran_txt
    json.dump(translated, open('translated.json', 'w'), ensure_ascii=False, indent=4)
    return results, tran_txt


class MyTimer(QtWidgets.QWidget):
    trigger = pyqtSignal(str, str)
    word_trigger = pyqtSignal(str)
    detect = True

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
        if not self.detect:
            return
        textData = self.editor.toPlainText()
        clipText = pyperclip.paste()
        cursor = self.editor.textCursor()
        textSelected = cursor.selectedText()
        source1, tran_txt1 = translateByCiBa(textSelected)
        self.word_trigger.emit(tran_txt1)
        if not textData and not clipText:
            return
        if not textData or (clipText and clipText not in translated.keys()):
            textData = clipText
            self.editor.append(textData)
        source, tran_txt = translateByCiBa(textData)
        self.trigger.emit(source, tran_txt)

    def changeDetect(self):
        self.detect = not self.detect


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Form()
    myshow.show()
    sys.exit(app.exec_())
