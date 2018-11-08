# -*- coding: utf-8 -*-

import time, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyperclip
import requests
import json
import os

from PaperTranUI import Ui_PaperTran

try:
    translated = json.load(open('translated.json'))
except Exception as e:
    translated = {}


class Form(QtWidgets.QWidget, Ui_PaperTran):
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
        self.timer.source_trigger.connect(self.setSourceText)
        self.timer.tran_trigger.connect(self.setTransText)
        self.timer.word_trigger.connect(self.setWordText)
        self.checkBox.toggle()
        self.checkBox.stateChanged.connect(self.timer.changeDetect)

    def retranslateUi(self, PaperTran):
        _translate = QtCore.QCoreApplication.translate
        PaperTran.setWindowTitle(_translate("PaperTran", "论文翻译"))
        self.label.setText(_translate("PaperTran", "请输入要翻译的英文"))
        self.pushButton.setText(_translate("PaperTran", "点击翻译"))
        self.pushButton_2.setText(_translate("PaperTran", "清空"))
        self.label_2.setText(_translate("PaperTran", "翻译结果"))
        self.checkBox.setText(_translate("PaperTran", "检测剪切板"))
        self.label_3.setText(_translate("PaperTran", "选择条目翻译结果"))

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
        source, tran_txt = translateByPaper(textData)
        self.setTransText(tran_txt)
        self.setSourceText(source)

    def changeFontSize(self, edit, fontsize=15):
        pass
        # cursor = edit.textCursor()
        # edit.selectAll()
        # edit.setFontPointSize(fontsize)
        # edit.setTextCursor(cursor)


def translateByPaper(textData):
    try:
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
            os.rename('translated.json', 'translated.json.bak')
            translated.clear()
        translated[textData] = tran_txt
        json.dump(translated, open('translated.json', 'w'), ensure_ascii=False, indent=4)
        return results, tran_txt
    except Exception as e:
        return '', str(e)

class MyTimer(QtWidgets.QWidget):
    source_trigger = pyqtSignal(str)
    tran_trigger = pyqtSignal(str)
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
        self.lastTran = ''
        self.lastTranWord = ''

    # 定义槽
    def onTimerOut(self):
        if not self.detect:
            return
        self.translateWord()
        self.translateSentence()

    def translateWord(self):
        cursor = self.editor.textCursor()
        textSelected = cursor.selectedText()
        if textSelected and self.lastTranWord != textSelected:
            source1, tran_txt1 = translateByPaper(textSelected)
            self.lastTranWord = textSelected
            self.word_trigger.emit(tran_txt1)

    def translateSentence(self):
        clipText = pyperclip.paste()
        if not clipText or clipText == self.lastTran:
            return
        self.lastTran = clipText
        source, tran_txt = translateByPaper(clipText)
        self.source_trigger.emit(source)
        self.tran_trigger.emit(tran_txt)

    def changeDetect(self):
        self.detect = not self.detect


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Form()
    myshow.show()
    sys.exit(app.exec_())
