#-*- coding:utf-8 -*-
'''
Basic Layout
'''
__author__ = 'Tony Zhu'
import sys
from PyQt5.QtGui import  QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QGroupBox, QPushButton, QLabel, QHBoxLayout,  QVBoxLayout, QGridLayout, QFormLayout, QLineEdit, QTextEdit

class TianGong(QWidget):
    def __init__(self):
        super(TianGong,self).__init__()
        self.initUi()

    def initUi(self):
        self.createGridGroupBox()
        self.creatVboxGroupBox()
        self.creatFormGroupBox()
        mainLayout = QVBoxLayout()
        hboxLayout = QHBoxLayout()
        hboxLayout.addStretch()
        hboxLayout.addWidget(self.gridGroupBox)
        hboxLayout.addWidget(self.vboxGroupBox)
        mainLayout.addLayout(hboxLayout)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)

    def createGridGroupBox(self):
        self.gridGroupBox = QGroupBox("Grid layout")
        layout = QGridLayout()

        nameLabel = QLabel("中文名称")
        nameLineEdit = QLineEdit("天宫二号")
        emitLabel = QLabel("发射地点")
        emitLineEdit = QLineEdit("酒泉中心")
        timeLabel = QLabel("发射时间")
        timeLineEdit = QLineEdit("9月15日")
        imgeLabel = QLabel()
        pixMap = QPixmap("tiangong.png")
        imgeLabel.setPixmap(pixMap)
        layout.setSpacing(10)
        layout.addWidget(nameLabel,1,0)
        layout.addWidget(nameLineEdit,1,1)
        layout.addWidget(emitLabel,2,0)
        layout.addWidget(emitLineEdit,2,1)
        layout.addWidget(timeLabel,3,0)
        layout.addWidget(timeLineEdit,3,1)
        layout.addWidget(imgeLabel,0,2,4,1)
        layout.setColumnStretch(1, 10)
        self.gridGroupBox.setLayout(layout)
        self.setWindowTitle('Basic Layout')

    def creatVboxGroupBox(self):
        self.vboxGroupBox = QGroupBox("Vbox layout")
        layout = QVBoxLayout()
        nameLabel = QLabel("科研任务：")
        bigEditor = QTextEdit()
        bigEditor.setPlainText("搭载了空间冷原子钟等14项应用载荷，以及失重心血管研究等航天医学实验设备 "
                "开展空间科学及技术试验.")
        layout.addWidget(nameLabel)
        layout.addWidget(bigEditor)
        self.vboxGroupBox.setLayout(layout)

    def creatFormGroupBox(self):
        self.formGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        performanceLabel = QLabel("性能特点：")
        performanceEditor = QLineEdit("舱内设计更宜居方便天宫生活")
        planLabel = QLabel("发射规划：")
        planEditor = QTextEdit()
        planEditor.setPlainText("2020年之前，中国计划初步完成空间站建设")
        layout.addRow(performanceLabel,performanceEditor)
        layout.addRow(planLabel,planEditor)

        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TianGong()
    ex.show()
    sys.exit(app.exec_())