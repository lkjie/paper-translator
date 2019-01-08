#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'lkjie'
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from PaperTranUI import Ui_PaperTran

class Form(QtWidgets.QWidget, Ui_PaperTran):
    def __init__(self):
        super(Form, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Form()
    myshow.show()
    sys.exit(app.exec_())