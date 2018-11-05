#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liwenjie'
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from cibaUI import Ui_CiBaTran

class Form(QtWidgets.QWidget, Ui_CiBaTran):
    def __init__(self):
        super(Form, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = Form()
    myshow.show()
    sys.exit(app.exec_())