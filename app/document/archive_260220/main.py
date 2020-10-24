from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
import qdarkstyle
import sqlite3
import json
from form import Ui_Dialog as editDonHang
from ui_mainwindow import Ui_MainWindow
from datetime import datetime

class saleTable(QtCore.QAbstractTableModel):

    header_labels = ['ID', 'Khách Hàng', 'Ngày Tạo', 'Người Tạo',\
    'Dịch vụ/Sản Phẩm', 'Thanh Toán', 'Trạng Thái', 'Ghi Chú', 'H']

    def __init__(self, data):
        super(saleTable, self).__init__()
        self._data = data


    def data(self, index, role):
        value = self._data[index.row()][index.column()]

        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d")

            if index.column() == 0:
            	return '{:06d}'.format(value)

            if index.column() == 5:
            	return "{:,d} VND".format(int(value))

            if index.column() == 6:
                if value == 0: 
                    return "PENDING"
                elif value == 1: 
                    return "DELIVERING"
                elif value == 2: 
                    return "GOOD" 

            return value

    def setData(self, index, value, role = Qt.EditRole):
        if index.column() == 3:
            key_id = self.index(index.row(), 2).data()
            print(key_id)
            print(value)



    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role = Qt.DisplayRole):
    	if role == Qt.DisplayRole and orientation == Qt.Horizontal:
    	    return self.header_labels[section]
    	return QAbstractTableModel.headerData(self, section, orientation, role)

    def flags(self, index):
        if index.column() == 3:
            return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class customerSideModel(QtCore.QAbstractListModel):
	def __init__(self, data):
		super(customerSideModel, self).__init__()
		self.data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			text = self.data[index.row()]
			return text

	def rowCount(self, index):
		return len(self.data)

class serviceSideModel(QtCore.QAbstractListModel):
	def __init__(self, data):
		super(serviceSideModel, self).__init__()
		self.data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			text = "{} : {:,.0f}VND".format(self.data[index.row()][0], self.data[index.row()][1]) 
			return text

	def rowCount(self, index):
		return len(self.data)




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        #SQL MANIPULATING
        self.data = sqlHandle()

        #MVC  EDDTING
        self.model = saleTable(self.data.saleReading())
        self.orderTable.setModel(self.model)        

        #TABLE VIEW GUI EDTTING
        self.orderTable.resizeColumnsToContents()
        self.orderTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        editMode = self.orderTable.itemDelegate()
        print(editMode)
        #editMode.setModelData()

        #selection model for automatic retrieve infomation
        self.selection_Model = self.orderTable.selectionModel()
        self.selection_Model.selectionChanged.connect(self.sideViewConnect)

        #SHOWING
        self.show()

        
        #CONTROLER
        self.addButton.clicked.connect(self.openDialog)

    def test(self):
    	print("CONNECTED")
    	print(self.model._data)

    def sideViewConnect(self):
    	indexes = self.orderTable.selectedIndexes()
    	if indexes:
    		index = indexes[0]
    		temp = self.model._data[index.row()][1] # temp = customer_id in currently selected row 
    		self.customerModel = customerSideModel(self.data.customerConditionalReading(temp)[0]) # index 0 as it's a list of tuple
    		self.sideView.setModel(self.customerModel)

    		temp = self.model._data[index.row()][0] # temp = id in currently selected row
    		self.serviceModel = serviceSideModel(self.data.serviceConditionalReading(temp)) #index 0 as it's a list of tuple
    		self.sideView2.setModel(self.serviceModel)

    def dataGenerate(self):
        row_data = 9
        col_data = 9 
        data = []
        for i in range (row_data):
            new = []
            for j in range (col_data):
            	if j == 0:
            		new.append(i + 105)
            	elif j == 1:
            		new.append("Hưng")
            	elif j == 2:
            		new.append(datetime(2001, 10, 18))
            	elif j == 3:
            		new.append("Thuận")
            	elif j == 4:
            		temp = [[19, "hung"], [20, 'me']]
            		new.append(temp)
            	else:
                    new.append(None)
            data.append(new)
        return data

    def openDialog(self):
    	dialog = QtWidgets.QDialog()
    	dialog.ui = editDonHang()
    	dialog.setStyleSheet(qdarkstyle.load_stylesheet())
    	dialog.ui.setupUi(dialog)

    	dialog.exec_()
    	dialog.show()




class sqlHandle():
    def __init__(self):
        self.conn = sqlite3.connect('data.db', detect_types = sqlite3.PARSE_DECLTYPES)

        self.c = self.conn.cursor()

        #customer table define
        self.c.execute("CREATE TABLE IF NOT EXISTS customerTable (customer_id INTEGER PRIMARY KEY,\
        	name TEXT, age INTEGER, phone TEXT, address TEXT)")

        #sale Table define
        self.c.execute("CREATE TABLE IF NOT EXISTS saleTable (id INTEGER PRIMARY KEY, \
        customer_id INTEGER, dateCreate TEXT, creator TEXT, \
        paymentMethod INTEGER, paymentDiscount REAL,\
        paymentTax REAL, paymentDebt REAL, status INTEGER, note TEXT,\
        FOREIGN KEY (customer_id) \
        REFERENCES customerTable(customer_id) \
        ON UPDATE CASCADE)")

        #product table define
        self.c.execute("CREATE TABLE IF NOT EXISTS productTable(product_id INTEGER PRIMARY KEY, \
        	productName TEXT)")

        #transaction table
        self.c.execute("CREATE TABLE IF NOT EXISTS transactionTable(id INTEGER, product_id INTEGER, price REAL,\
        	FOREIGN KEY(id) \
        	REFERENCES saleTable(id) \
        	ON UPDATE CASCADE\
        	FOREIGN KEY (product_id)\
        	REFERENCES productTable(product_id)\
        	ON UPDATE CASCADE)")

        self.createView()

    def createView(self):
    	self.c.execute(\
    		"""CREATE VIEW IF NOT EXISTS table_View AS
    		SELECT saleTable.id, customer_id, dateCreate, creator, COUNT(product_id), SUM(price), status, note
    		FROM saleTable
    		INNER JOIN transactionTable ON saleTable.id = transactionTable.id
    		GROUP BY saleTable.id
    		""")

    	self.c.execute(\
    		"""CREATE VIEW IF NOT EXISTS customerSideView AS
    		SELECT customerTable.customer_id, name, age, phone, address, paymentMethod, paymentDiscount, paymentTax, paymentDebt
    		FROM customerTable
    		INNER JOIN saleTable ON saleTable.customer_id = customerTable.customer_id
    		""")

    	self.conn.commit()

    def closing(self):
        self.c.close
        self.conn.close()

    def saleReading(self):
        self.c.execute("SELECT * FROM table_View")
        data = self.c.fetchall()
        return data

    def customerReading(self):
    	self.c.execute("SELECT * FROM customerSideView")
    	customerData = self.c.fetchall()
    	return customerData

    def customerConditionalReading(self, temp):
        self.c.execute("SELECT * FROM customerSideView WHERE customer_id = {}".format(temp))
        return self.c.fetchall()

    def serviceConditionalReading(self, temp):
    	self.c.execute("SELECT productName, price FROM transactionTable\
    	INNER JOIN productTable USING(product_id) WHERE id = {}".format(temp))
    	return self.c.fetchall()

    def dataWritting(self, value, key_id):
        self.c.execute("UPDATE saleTable SET creator = {} WHERE ID = {}".format(value, key_id))
        self.conn.commit()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    def adapt_list_to_JSON(lst):
        return json.dumps(lst).encode('utf8')

    def convert_JSON_to_list(data):
        return json.loads(data.decode('utf8'))

    sqlite3.register_adapter(list, adapt_list_to_JSON)
    sqlite3.register_converter("json", convert_JSON_to_list)

    window = MainWindow()
    sys.exit(app.exec_())
    window.data.closing() #closing sql table