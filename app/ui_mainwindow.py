# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1198, 807)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.menuWidgets = QtWidgets.QListWidget(self.centralwidget)
        self.menuWidgets.setMinimumSize(QtCore.QSize(191, 768))
        self.menuWidgets.setMaximumSize(QtCore.QSize(191, 16777215))
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.p2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.orderTable = QtWidgets.QTableView(self.p2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orderTable.sizePolicy().hasHeightForWidth())
        self.orderTable.setSizePolicy(sizePolicy)
        self.orderTable.setMinimumSize(QtCore.QSize(800, 0))
        self.orderTable.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.orderTable.setFont(font)
        self.orderTable.setStyleSheet("")
        self.orderTable.setFrameShape(QtWidgets.QFrame.Box)
        self.orderTable.setLineWidth(0)
        self.orderTable.setAlternatingRowColors(False)
        self.orderTable.setShowGrid(True)
        self.orderTable.setGridStyle(QtCore.Qt.SolidLine)
        self.orderTable.setObjectName("orderTable")
        self.orderTable.horizontalHeader().setCascadingSectionResizes(False)
        self.orderTable.horizontalHeader().setDefaultSectionSize(100)
        self.orderTable.horizontalHeader().setMinimumSectionSize(31)
        self.horizontalLayout_3.addWidget(self.orderTable)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sideView = QtWidgets.QListView(self.p2)
        self.sideView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sideView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.sideView.setObjectName("sideView")
        self.verticalLayout_2.addWidget(self.sideView)
        self.sideView2 = QtWidgets.QListView(self.p2)
        self.sideView2.setMaximumSize(QtCore.QSize(16777215, 500))
        self.sideView2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sideView2.setLineWidth(0)
        self.sideView2.setObjectName("sideView2")
        self.verticalLayout_2.addWidget(self.sideView2)
        self.filterButton = QtWidgets.QPushButton(self.p2)
        self.filterButton.setCheckable(True)
        self.filterButton.setObjectName("filterButton")
        self.verticalLayout_2.addWidget(self.filterButton)
        self.payButton = QtWidgets.QPushButton(self.p2)
        self.payButton.setObjectName("payButton")
        self.verticalLayout_2.addWidget(self.payButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addButton = QtWidgets.QPushButton(self.p2)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QPushButton(self.p2)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.stackedWidgets.addWidget(self.p2)
        self.p3 = QtWidgets.QWidget()
        self.p3.setObjectName("p3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.p3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.customerTable = QtWidgets.QTableView(self.p3)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.customerTable.setFont(font)
        self.customerTable.setFrameShape(QtWidgets.QFrame.Box)
        self.customerTable.setObjectName("customerTable")
        self.verticalLayout_3.addWidget(self.customerTable)
        self.debtButton = QtWidgets.QPushButton(self.p3)
        self.debtButton.setObjectName("debtButton")
        self.verticalLayout_3.addWidget(self.debtButton)
        self.historyButton = QtWidgets.QPushButton(self.p3)
        self.historyButton.setCheckable(True)
        self.historyButton.setObjectName("historyButton")
        self.verticalLayout_3.addWidget(self.historyButton)
        self.stackedWidgets.addWidget(self.p3)
        self.p4 = QtWidgets.QWidget()
        self.p4.setObjectName("p4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.p4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.productTable = QtWidgets.QTableView(self.p4)
        self.productTable.setObjectName("productTable")
        self.verticalLayout_4.addWidget(self.productTable)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1198, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.stackedWidgets.setCurrentIndex(2)
        self.menuWidgets.currentRowChanged['int'].connect(self.stackedWidgets.setCurrentIndex)
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
        self.filterButton.setText(_translate("MainWindow", "Filter/Search (Ctrl+F)"))
        self.payButton.setText(_translate("MainWindow", "Thanh Toán (F1)"))
        self.addButton.setText(_translate("MainWindow", "AddButton"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.debtButton.setText(_translate("MainWindow", "Nợ Cần Thu (Ctrl+D)"))
        self.historyButton.setText(_translate("MainWindow", "Lịch Sử Giao Dịch (Ctrl+H)"))
        self.label_5.setText(_translate("MainWindow", "Page 5"))
        self.label_6.setText(_translate("MainWindow", "Page 6"))
