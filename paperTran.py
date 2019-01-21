# -*- coding: utf-8 -*-

import time, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
import requests
import json
import os
import re

import ico
from PaperTranUI import Ui_PaperTran
from Translator import Translator
from configures import *

FILE_PATH = os.path.split(os.path.realpath(__file__))[0]


class PaperTran(QtWidgets.QWidget, Ui_PaperTran):
    fontRegular = False  # 字体不需要设置
    current_id = -1
    translator = Translator()


    def __init__(self):
        super(PaperTran, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':ico/translator.ico'))
        QtCore.QMetaObject.connectSlotsByName(self)
        desktop = QtWidgets.QApplication.desktop()
        x = (desktop.width() - self.width())
        y = (desktop.height() - self.height())
        self.move(x, y)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |  # 使能最小化按钮
                            QtCore.Qt.WindowCloseButtonHint |  # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint)  # 窗体总在最前端

        self.pushButton.clicked.connect(self.buttonTrans)
        self.pushButton_2.clicked.connect(self.textEdit_1.clear)
        self.timer = MyTimer(self.textEdit_1, parent=self)
        self.timer.tranTrigger.connect(lambda s: self.trans(textData=s))
        self.timer.wordTrigger.connect(self.setWordText)
        self.checkBox.toggle()
        self.checkBox.stateChanged.connect(self.timer.changeDetect)
        self.pushButton_3.clicked.connect(self.nextItem)
        self.pushButton_4.clicked.connect(self.lastItem)
        self.comboBox.activated.connect(self.onComboboxFunc)
        self.RES_PATH = FILE_PATH + os.sep + 'sourceList.json'

        # cut combo strings
        self.strcut = lambda str1: str1[:COMBO_STRLEN - 3] + '...' if len(str1) > COMBO_STRLEN else str1
        self.strscut = lambda strs: [self.strcut(str1) for str1 in strs]

        self.sourceList = []
        self.sourceList_cut = []
        try:
            self.sourceList = json.load(open(self.RES_PATH, encoding='utf8'))
            self.sourceList_cut = self.strscut(self.sourceList)
            self.comboBox.addItems(self.sourceList_cut)
        except Exception as e:
            pass
        # char format
        self.defaultCharFormat = self.textEdit_1.currentCharFormat()

        # setting translate engine
        self.comboBox_2.addItems(self.translator.engine_name_dict.keys())
        self.comboBox_2.activated.connect(self.selectEngine)

    def retranslateUi(self, PaperTran):
        _translate = QtCore.QCoreApplication.translate
        PaperTran.setWindowTitle(_translate("PaperTran", "论文翻译"))
        self.label.setText(_translate("PaperTran", "请输入要翻译的字段"))
        self.pushButton.setText(_translate("PaperTran", "(&T)点击翻译"))
        self.pushButton_2.setText(_translate("PaperTran", "(&C)清空"))
        self.label_2.setText(_translate("PaperTran", "翻译结果"))
        self.checkBox.setText(_translate("PaperTran", "检测剪切板"))
        self.label_3.setText(_translate("PaperTran", "选择条目"))
        self.pushButton_4.setText(_translate("PaperTran", "(&L)上一条"))
        self.pushButton_3.setText(_translate("PaperTran", "(&N)下一条"))
        self.label_4.setText(_translate("PaperTran", "翻译引擎："))

    def setTransText(self, str1):
        self.textEdit_2.clear()
        self.textEdit_2.append(str1)
        if self.fontRegular:
            self.changeFontSize(self.textEdit_2)

    def setSourceText(self, str1):
        self.textEdit_1.clear()
        if self.textEdit_1.currentCharFormat() != self.defaultCharFormat:
            self.textEdit_1.setCurrentCharFormat(self.defaultCharFormat)
        self.textEdit_1.append(str1)
        if self.fontRegular:
            self.changeFontSize(self.textEdit_1)

    def setWordText(self, str1):
        self.textEdit_3.clear()
        self.textEdit_3.append(str1)
        if self.fontRegular:
            self.changeFontSize(self.textEdit_3, 10)

    def buttonTrans(self):
        textData = self.textEdit_1.toPlainText()
        self.trans(textData)

    def lastItem(self):
        if self.comboBox.currentIndex() > 0:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() - 1)
            self.onComboboxFunc()

    def nextItem(self):
        if self.comboBox.currentIndex() < len(self.sourceList) - 1:
            self.comboBox.setCurrentIndex(self.comboBox.currentIndex() + 1)
            self.onComboboxFunc()

    def onComboboxFunc(self):
        self.trans(transId=self.comboBox.currentIndex())

    def selectEngine(self):
        engine = self.comboBox_2.currentText()
        self.translator.engine = self.translator.engine_name_dict.get(engine, 'ciba')

    def trans(self, textData='', transId=None):
        '''
        translate function, all translate must use this func
        transId first
        '''
        if isinstance(transId, int) and transId >= 0:
            transText = self.sourceList[transId]
            self.comboBox.setCurrentIndex(transId)
        elif textData:
            if len(self.sourceList) > COMBO_SIZE:
                self.restore(path=self.RES_PATH + 'backup')
                sourceList = self.sourceList[:-int(COMBO_SIZE * 0.5)]
                self.comboSetItems(sourceList)
            else:
                self.comboDropItem(textData)
                self.comboAddItem(textData)
            transText = textData
        else:
            return
        self.setSourceText(transText)
        tranTxt = self.translator.translate(transText)
        self.setTransText(tranTxt)

    def changeFontSize(self, edit, fontsize=15):
        cursor = edit.textCursor()
        edit.selectAll()
        edit.setFontPointSize(fontsize)
        edit.setTextCursor(cursor)

    def restore(self, path=None):
        if path:
            json.dump(self.sourceList, open(path, 'w'), ensure_ascii=False, indent=4)
        else:
            json.dump(self.sourceList, open(self.RES_PATH, 'w'), ensure_ascii=False, indent=4)

    def comboSetItems(self, sourceList):
        self.sourceList = sourceList
        self.sourceList_cut = self.strscut(self.sourceList)
        self.comboBox.clear()
        self.comboBox.addItems(self.sourceList_cut)

    def comboAddItem(self, textData):
        self.sourceList.append(textData)
        self.sourceList_cut.append(self.strcut(textData))
        self.comboBox.addItem(self.strcut(textData))
        self.comboBox.setCurrentIndex(len(self.sourceList) - 1)

    def comboDropItem(self, textData):
        if textData not in self.sourceList:
            return
        idx = self.sourceList.index(textData)
        self.sourceList.pop(idx)
        self.sourceList_cut.pop(idx)
        self.comboBox.clear()
        self.comboBox.addItems(self.sourceList_cut)


class MyTimer(QtWidgets.QWidget):
    tranTrigger = pyqtSignal(str)
    wordTrigger = pyqtSignal(str)
    detect = True

    def __init__(self, sender, parent=None):
        super().__init__(parent)
        self.editor = sender
        self.form = parent
        self.timer = QTimer()
        self.timer.setInterval(TRANS_INTERVAL)
        self.timer.start()
        # 信号连接到槽
        self.timer.timeout.connect(self.onTimerOut)
        self.lastTran = ''
        self.lastTranWord = ''
        self.clipboard = QApplication.clipboard()

        self.storeTimer = QTimer()
        self.storeTimer.setInterval(STORE_INTERVAL)
        self.storeTimer.start()
        self.timer.timeout.connect(self.restoreTimeOut)

    # 定义槽
    def onTimerOut(self):
        self.translateWord()
        if self.detect:
            self.translateSentence()

    def restoreTimeOut(self):
        self.form.restore()
        self.form.translator.restore()

    def translateWord(self):
        cursor = self.editor.textCursor()
        textSelected = cursor.selectedText()
        if textSelected and self.lastTranWord != textSelected:
            tranTxt = self.form.translator.translate(textSelected)
            self.lastTranWord = textSelected
            self.wordTrigger.emit(tranTxt)

    def translateSentence(self):
        '''
        condition: 
        not clipText 剪切板为空
        clipText == self.lastTran 剪切板无变化
        self.isActiveWindow() 当前窗口为活动窗口
        :return: 
        '''
        clipText = self.clipboard.text()
        clipText = self.form.translator.textClean(clipText)
        if not clipText or clipText in self.lastTran or self.isActiveWindow():
            return
        self.lastTran = clipText
        self.tranTrigger.emit(clipText)

    def changeDetect(self):
        self.detect = not self.detect


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = PaperTran()
    myshow.show()
    sys.exit(app.exec_())
