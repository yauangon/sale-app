# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(50,90)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1201, 789)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.menuWidgets = QtWidgets.QListWidget(self.centralwidget)
        self.menuWidgets.setMinimumSize(QtCore.QSize(191, 768))
        self.menuWidgets.setMaximumSize(QtCore.QSize(191, 768))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.menuWidgets.setFont(font)
        self.menuWidgets.setStyleSheet("QListView {\n"
"    show-decoration-selected: 0; /* make the selection span the entire width of the view */\n"
"    background-color: #6e5773;\n"
"    color: #e9e1cc;\n"
"}\n"
"\n"
"QListView::item:alternate {\n"
"    background: #EEEEEE;\n"
"}\n"
"\n"
"QListView::item:selected {\n"
"    border: 1px solid #6a6ea9;\n"
"}\n"
"\n"
"QListView::item:selected:!active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #ABAFE5, stop: 1 #8588B2);\n"
"}\n"
"\n"
"QListView::item:selected:active {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #6a6ea9, stop: 1 #888dd9);\n"
"}\n"
"\n"
"QListView::item:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}")
        self.menuWidgets.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.menuWidgets.setFrameShadow(QtWidgets.QFrame.Plain)
        self.menuWidgets.setAlternatingRowColors(False)
        self.menuWidgets.setFlow(QtWidgets.QListView.TopToBottom)
        self.menuWidgets.setProperty("isWrapping", False)
        self.menuWidgets.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.menuWidgets.setGridSize(QtCore.QSize(0, 30))
        self.menuWidgets.setSelectionRectVisible(False)
        self.menuWidgets.setObjectName("menuWidgets")
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.menuWidgets.addItem(item)
        self.horizontalLayout_2.addWidget(self.menuWidgets)
        self.stackedWidgets = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidgets.setMinimumSize(QtCore.QSize(780, 0))
        self.stackedWidgets.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidgets.setLineWidth(1)
        self.stackedWidgets.setMidLineWidth(0)
        self.stackedWidgets.setObjectName("stackedWidgets")
        self.p1 = QtWidgets.QWidget()
        self.p1.setObjectName("p1")
        self.label = QtWidgets.QLabel(self.p1)
        self.label.setGeometry(QtCore.QRect(30, 20, 131, 101))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setObjectName("label")
        self.stackedWidgets.addWidget(self.p1)
        self.p2 = QtWidgets.QWidget()
        self.p2.setObjectName("p2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.p2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.orderTable = QtWidgets.QTableView(self.p2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orderTable.sizePolicy().hasHeightForWidth())
        self.orderTable.setSizePolicy(sizePolicy)
        self.orderTable.setFrameShape(QtWidgets.QFrame.Box)
        self.orderTable.setAlternatingRowColors(False)
        self.orderTable.setObjectName("orderTable")
        self.orderTable.horizontalHeader().setCascadingSectionResizes(False)
        self.orderTable.horizontalHeader().setDefaultSectionSize(100)
        self.orderTable.horizontalHeader().setMinimumSectionSize(31)
        self.verticalLayout.addWidget(self.orderTable)
        self.stackedWidgets.addWidget(self.p2)
        self.p3 = QtWidgets.QWidget()
        self.p3.setObjectName("p3")
        self.label_3 = QtWidgets.QLabel(self.p3)
        self.label_3.setGeometry(QtCore.QRect(150, 90, 131, 101))
        self.label_3.setFrameShape(QtWidgets.QFrame.Box)
        self.label_3.setObjectName("label_3")
        self.stackedWidgets.addWidget(self.p3)
        self.p4 = QtWidgets.QWidget()
        self.p4.setObjectName("p4")
        self.label_4 = QtWidgets.QLabel(self.p4)
        self.label_4.setGeometry(QtCore.QRect(350, 90, 131, 101))
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setObjectName("label_4")
        self.stackedWidgets.addWidget(self.p4)
        self.p5 = QtWidgets.QWidget()
        self.p5.setObjectName("p5")
        self.label_5 = QtWidgets.QLabel(self.p5)
        self.label_5.setGeometry(QtCore.QRect(160, 140, 131, 101))
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setObjectName("label_5")
        self.stackedWidgets.addWidget(self.p5)
        self.p6 = QtWidgets.QWidget()
        self.p6.setObjectName("p6")
        self.label_6 = QtWidgets.QLabel(self.p6)
        self.label_6.setGeometry(QtCore.QRect(30, 50, 131, 101))
        self.label_6.setFrameShape(QtWidgets.QFrame.Box)
        self.label_6.setObjectName("label_6")
        self.stackedWidgets.addWidget(self.p6)
        self.horizontalLayout_2.addWidget(self.stackedWidgets)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sideView = QtWidgets.QListView(self.centralwidget)
        self.sideView.setMaximumSize(QtCore.QSize(239, 600))
        self.sideView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sideView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sideView.setObjectName("sideView")
        self.verticalLayout_2.addWidget(self.sideView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        #addButton
        self.addButton = PicButton(QPixmap('.\\img\\addButton.png'), QPixmap('.\\img\\addButton.png'),QPixmap('.\\img\\addButton.png'), self)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        #deleteButton
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1201, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.stackedWidgets.setCurrentIndex(1)
        self.menuWidgets.currentRowChanged['int'].connect(self.stackedWidgets.setCurrentIndex)
        self.deleteButton.clicked.connect(self.orderTable.clearSelection)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.menuWidgets.isSortingEnabled()
        self.menuWidgets.setSortingEnabled(False)
        item = self.menuWidgets.item(0)
        item.setText(_translate("MainWindow", "Tổng Quan"))
        item = self.menuWidgets.item(1)
        item.setText(_translate("MainWindow", "Đơn Hàng"))
        item = self.menuWidgets.item(2)
        item.setText(_translate("MainWindow", "Khách Hàng"))
        item = self.menuWidgets.item(3)
        item.setText(_translate("MainWindow", "Sản Phẩm/Dịch Vụ"))
        item = self.menuWidgets.item(4)
        item.setText(_translate("MainWindow", "Thống Kê/Báo Cáo"))
        item = self.menuWidgets.item(5)
        item.setText(_translate("MainWindow", "Sổ Quỹ"))
        self.menuWidgets.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("MainWindow", "Page 1"))
        self.label_3.setText(_translate("MainWindow", "Page3"))
        self.label_4.setText(_translate("MainWindow", "Page 4"))
        self.label_5.setText(_translate("MainWindow", "Page 5"))
        self.label_6.setText(_translate("MainWindow", "Page 6"))
        self.addButton.setText(_translate("MainWindow", "AddButton"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
