from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel

import sys
import qdarkstyle
import sqlite3
import json

from form import Ui_Dialog as editDonHang
from filterForm import Ui_Dialog as filterWindow
from historyTable import Ui_Dialog as historyWindow
from phieuthu import Ui_Dialog as phieuthu

from ui_mainwindow import Ui_MainWindow
from datetime import datetime

#MODEL SECTION
class sqlQueryModel(QSqlQueryModel):

	header_labels = ['ID', 'Khách Hàng', 'Ngày Tạo', 'Người Tạo',\
	'Dịch vụ/Sản Phẩm', 'Thanh Toán', 'Trạng Thái' , "Discount", "Thuế", "Ghi chú"]

	def __init__(self):
		super(sqlQueryModel, self).__init__()

	def flags (self, index):
		if index.column() in [7, 8, 9]:
			return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

		return Qt.ItemIsSelectable | Qt.ItemIsEnabled

	def data(self, index, role = Qt.DisplayRole):
		value = QtSql.QSqlQueryModel.data(self, index, role)
		if value != None: #there are None value when printed out, I suspects it's the cause of weird check boxs in cell value
			if value == '':
				value = 0
			if index.column() == 0 or index.column() == 1:
				return "{:06d}".format(value)
			if index.column() == 3:
				return "{}".format(value)
			if index.column() == 5:
				return("{:,d} VND".format(int(value)))
			if index.column() == 6:
				if value%3 == 0:
					return("CHƯA THANH TOÁN")
				elif value%3 == 1:
					return("CÒN NỢ")
				elif value%3 == 2:
					return("ĐÃ XONG")

			if index.column() == 7:
				return "{:.0f}%".format(value)

			if index.column() == 8:
				return "{:.0f}%".format(value)
			else:
				return value

	def setData(self, index, value, role):
		key_id = self.index(index.row(), 0).data()
		if index.column() == 7: #discount EDIT
			value = float(value.replace('%', ''))
			q = QSqlQuery("UPDATE saleTable SET paymentDiscount = {} WHERE id = {}".format(value, key_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result

		if index.column() == 8:
			value = float(value.replace('%', ''))
			q = QSqlQuery("UPDATE saleTable SET paymentTax = {} WHERE id = {}".format(value, key_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result

		if index.column() == 9:
			q = QSqlQuery("UPDATE saleTable SET note = '{}' WHERE id  = '{}'".format(value, key_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result

		return QSqlQueryModel.setData(self, index, value, role)

	def setFilter(self, filter = None):
		text = self.query().lastQuery()
		if 'WHERE' in text:
			temp = text.find("WHERE")
			text = text[:temp - 1]
		if len(filter) > 0:
			text = (text + " WHERE " + filter)
		self.setQuery(text)
	
	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if role == Qt.DisplayRole and orientation == Qt.Horizontal:
			return self.header_labels[section]
		return QSqlQueryModel.headerData(self, section, orientation, role)

	def customer_idReturn(self, temp):
		return self.index(temp, 1).data()

	def idReturn(self, temp):
		return self.index(temp, 0).data()

	def statusReturn(self, temp):
		return self.index(temp, 6).data()

	def payReturn(self, temp):
		temp2 = self.index(temp, 5).data().replace(" VND", "")
		temp2 = temp2.replace(",", '')
		return int(temp2)

class sqlQueryModelTransaction(QSqlQueryModel):

	header_labels = ['ID', 'ProductID', 'Tên DV', 'Gía Thành', 'Số Lượng', "Tổng"]

	def __int__(self):
		super(sqlQueryModelTransaction, self).__init__()

	def flags(self, index):
		if index.column() in [3,4]: #price column
			return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

		return Qt.ItemIsSelectable | Qt.ItemIsEnabled

	def setData(self, index, value, role = Qt.EditRole):
		key_id = self.index(index.row(), 0).data()
		product_id = self.index(index.row(), 1).data()

		if index.column() == 3:
			q = QSqlQuery("UPDATE transactionTable SET pricePerProduct = '{}' WHERE id = '{}' AND product_id = '{}'".format(value, key_id, product_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result
		if index.column() == 4:
			q = QSqlQuery("UPDATE transactionTable SET amount = '{}' WHERE id = '{}' AND product_id = '{}'".format(value, key_id, product_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result

		return QSqlQueryModel.setData(self, index, value, role)

	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if role == Qt.DisplayRole and orientation == Qt.Horizontal:
			return self.header_labels[section]
		return QSqlQueryModel.headerData(self, section, orientation, role)

	def priceSum(self, newID):
		q = QSqlQuery("SELECT SUM(pricePerProduct*amount) FROM transactionTable WHERE id = {}".format(newID))
		q.exec_()
		while q.next():
			result = q.result().data(0)
		return result

class sqlQueryModelCustomer(QSqlQueryModel):
	header_labels = ["Customer ID", "Tên Khách Hàng", "Giới tính", "Tuổi", "Phone", "Địa Chỉ"]

	def __init__(self):
		super(sqlQueryModelCustomer, self).__init__()

	def flags(self, index):
		return Qt.ItemIsSelectable | Qt.ItemIsEnabled

	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if orientation == Qt.Horizontal:
			return self.header_labels[section]
		return QSqlQueryModel.headerData(self, section, orientation, role)

	def data(self, index, role = Qt.DisplayRole):
		value = QtSql.QSqlQueryModel.data(self, index, role)
		if value != None:
			if index.column() == 0:
				return "{:06d}".format(int(value))
			if index.column() == 2:
				if value == 0:
					return "Nam"
				else:
					return "Nữ"

			else:
				return value

	def customer_idReturn(self, temp):
		return self.index(temp, 0).data()

class sqlQueryModelHistory(QSqlQueryModel):
	header_labels = ["ID", "Bill", "Date Time", "Creator", "Pay"]

	def __init__(self):
		super(sqlQueryModelHistory, self).__init__()

	def flags(self, index):
		return Qt.ItemIsSelectable | Qt.ItemIsEnabled

	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if orientation == Qt.Horizontal:
			return self.header_labels[section]
		return QSqlQueryModel.headerData(self, section, orientation, role)

	def data(self, index, role = Qt.DisplayRole):
		value = QtSql.QSqlQueryModel.data(self, index, role)
		if value != None:
			if index.column() == 0:
				return "{:06d}".format(value)
			if index.column() == 4:
				return "{:,d} VND".format(int(value))

			else:
				return value

class sqlQueryModelProduct(QSqlQueryModel):
	header_labels = ["Product ID", "Name", "Price by default", "Description"]

	def __init__(self):
		super(sqlQueryModelProduct, self).__init__()

	def flags(self, index):
		if index.column() in [2, 3]:
			return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

		return Qt.ItemIsSelectable | Qt.ItemIsEnabled

	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if orientation == Qt.Horizontal:
			return self.header_labels[section]
		return QSqlQueryModel.headerData(self, section, orientation, role)

	def data(self, index, role = Qt.DisplayRole):
		value = QtSql.QSqlQueryModel.data(self, index, role)
		if value != None:
			if index.column() == 2:
				return "{:,d} VND".format(int(value))

			else:
				return value
	def setData(self, index, value, role = Qt.EditRole):
		product_id = self.index(index.row(), 0).data()

		if index.column() == 2:
			value.replace(" VND", "")
			value.replace(",", '')
			value = int(value)
			q = QSqlQuery("UPDATE productTable SET defaultPrice = '{}' WHERE product_id = '{}'".format(value, product_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result
		if index.column() == 3:
			q = QSqlQuery("UPDATE productTable SET description = '{}' WHERE product_id = '{}'".format(value, product_id))
			result = q.exec_()
			if result:
				self.query().exec_()
			else:
				print(self.query().lastError().text())
			return result

		return QSqlQueryModel.setData(self, index, value, role)

class customerSideModel(QtCore.QAbstractListModel):
	def __init__(self, data):
		super(customerSideModel, self).__init__()
		self.data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			value = self.data[index.row()]

			if index.row() == 0:
				return "Customer ID: {:06d}".format(value)
			if index.row() == 1:
				return "Tên KH: {}".format(value)
			if index.row() == 2:
				return "Giới tính: {}".format(value)
			if index.row() == 3:
				return "Tuổi: {}".format(value)
			if index.row() == 4:
				return "Phone: {}".format(value)
			if index.row() == 5:
				return "Địa Chỉ: {}".format(value)
			else:
				return value

	def rowCount(self, index):
		return len(self.data)

class serviceSideModel(QtCore.QAbstractListModel):
	def __init__(self, data):
		super(serviceSideModel, self).__init__()
		self.data = data

	def data(self, index, role):
		if role == Qt.DisplayRole:
			text = "{} : {:,.0f} x {:.0f} = {:,.0f} VND, NOTE: {}".format(self.data[index.row()][0], self.data[index.row()][1], \
				self.data[index.row()][2], self.data[index.row()][3], self.data[index.row()][4]) 
			return text

	def rowCount(self, index):
		return len(self.data)

#MAINWINDOW
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setStyleSheet(qdarkstyle.load_stylesheet())

		#SQL MANIPULATING
		self.q = sqlHandle()
		self.model = sqlQueryModel()
		self.model.setQuery(self.q.saleReading())
		self.customerTableModel = sqlQueryModelCustomer()
		self.customerTableModel.setQuery(self.q.customerTableReading())
		self.productModel = sqlQueryModelProduct()
		self.productModel.setQuery(self.q.productReading())
		#MVC  EDDTING
		self.orderTable.setModel(self.model)
		self.customerTable.setModel(self.customerTableModel)
		self.productTable.setModel(self.productModel)

		#TABLE VIEW GUI EDTTING
		self.orderTable.resizeColumnsToContents()
		self.orderTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		#self.customerTable.resizeColumnsToContents()
		#self.customerTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		#selection model for automatic retrieve infomation
		self.selection_Model = self.orderTable.selectionModel()
		self.selection_Model.selectionChanged.connect(self.sideViewConnect)
		self.customerSelectionModel = self.customerTable.selectionModel()


		#SHOWING
		self.show()
		#CONTROLER
		self.addButton.clicked.connect(self.openAddDialog)
		self.payButton.clicked.connect(self.changePayState)
		self.payButton.setShortcut("F1")
		self.filterButton.clicked.connect(self.openFilterDialog)
		self.filterButton.setShortcut("Ctrl+F")
		self.historyButton.clicked.connect(self.transacHistory)
		self.historyButton.setShortcut("Ctrl+H")

	'''def test(self):
			("CONNECTED")
		'''

	def sideViewConnect(self):
		indexes = self.orderTable.selectedIndexes()
		if indexes:
			index = indexes[0].row()

			temp = self.model.customer_idReturn(index) #temp store the customer_id returned from the sqlmodel
			query = QSqlQuery(self.q.customerReading(temp))
			text = []
			while query.next():
				for i in range(query.record().count()):
					text.append(query.result().data(i))

			self.customerModel = customerSideModel(text)
			self.sideView.setModel(self.customerModel)

			temp = self.model.idReturn(index)
			query = QSqlQuery(self.q.transactionReading(temp))
			list_1 = []
			while query.next():
				text = []
				for i in range(query.record().count()):
					text.append(query.result().data(i))
				list_1.append(text)

			self.serviceModel = serviceSideModel(list_1)
			self.sideView2.setModel(self.serviceModel)

	def openAddDialog(self):
		dialog = QtWidgets.QDialog()
		datetimeNow = datetime.now()
		cur_time = datetimeNow.strftime("%d/%m/%Y %H:%M:%S")
		dialog.qdatetime = QDateTime.fromString(cur_time, "dd/MM/yyyy h:mm:ss")

		#MODEL HANDLING
		dialog.newID = self.q.addSaleTable()
		dialog.maxCustomer = self.q.findMaxCustomerID()
		dialog.applyBoolean = 0
		dialog.transModel = sqlQueryModelTransaction()
		dialog.transModel.setQuery(self.q.editNewTransaction(dialog.newID))

		#setup UI
		dialog.ui = editDonHang()
		dialog.setStyleSheet(qdarkstyle.load_stylesheet())
		dialog.ui.setupUi(dialog)
		dialog.ui.dateTimeEdit.setDateTime(dialog.qdatetime)
		dialog.ui.idDisplay.setText("{:06d}".format(dialog.newID))
		dialog.ui.lineEdit.setPlaceholderText("Max customer id = {}".format(dialog.maxCustomer))
		#dialog.exec_() dont khow why this make the dialog bugged

		#table VIEW
		dialog.ui.tableView.setModel(dialog.transModel)
		dialog.ui.tableView.setColumnWidth(0, 10)
		dialog.ui.tableView.setColumnWidth(1, 60)
		dialog.ui.tableView.setColumnWidth(2, 90)
		dialog.ui.tableView.setColumnWidth(3, 90)

		#reg exp
		reg_exp_forNumbers = QRegExp("^[0-9]{1,11}$")
		phoneValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.phoneEdit)
		dialog.ui.phoneEdit.setValidator(phoneValid)

		searchValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.searchEdit)
		dialog.ui.searchEdit.setValidator(searchValid)

		ageValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.ageEdit)
		dialog.ui.ageEdit.setValidator(ageValid)

		idValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.lineEdit)
		dialog.ui.lineEdit.setValidator(idValid)

		reg_exp_forString = QRegExp("[^0-9]+")
		nameValid = QRegExpValidator(reg_exp_forString, dialog.ui.nameEdit)
		dialog.ui.nameEdit.setValidator(nameValid)

		creatorValid = QRegExpValidator(reg_exp_forString, dialog.ui.lineEdit_2)
		dialog.ui.lineEdit_2.setValidator(creatorValid)
		
		
		#initialize ui
		dialog.ui.nameEdit.setDisabled(True)
		dialog.ui.ageEdit.setDisabled(True)
		dialog.ui.phoneEdit.setDisabled(True)
		dialog.ui.addressEdit.setDisabled(True)
		dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

		def searchForCustomerID():
			phoneNumber = dialog.ui.searchEdit.text()
			query = QSqlQuery("SELECT customer_id FROM customerTable WHERE phone = '{}'".format(phoneNumber))
			temp = None
			while query.next():
				temp = query.result().data(0)

			dialog.ui.lineEdit.setText('{}'.format(temp))


		dialog.ui.searchButton.clicked.connect(searchForCustomerID)

		def checkEmptyLineEdit():
			if len(dialog.ui.lineEdit.text()) > 0:
				if dialog.ui.newIDButton.isChecked():
					if len(dialog.ui.nameEdit.text()) > 0\
					and len(dialog.ui.ageEdit.text()) > 0\
					and len(dialog.ui.phoneEdit.text()) > 0\
					and len(dialog.ui.addressEdit.text()) > 0\
					and len(dialog.ui.lineEdit_2.text()) > 0\
					and len(dialog.ui.saleEdit.text()) > 0\
					and len(dialog.ui.taxEdit.text()) > 0:
						dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
					else:
						pass
				else:
					if len(dialog.ui.lineEdit_2.text()) > 0\
					and len(dialog.ui.saleEdit.text()) > 0\
					and len(dialog.ui.taxEdit.text()) > 0:
						dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
					else:
						pass
			else:
				pass

		def newIDHandler():
			if dialog.ui.newIDButton.isChecked():
				dialog.ui.newIDButton.setText("Checked. Please fill in lines below")
				dialog.ui.nameEdit.setDisabled(False)
				dialog.ui.ageEdit.setDisabled(False)
				dialog.ui.phoneEdit.setDisabled(False)
				dialog.ui.addressEdit.setDisabled(False)
				dialog.ui.lineEdit.setText("{:06d}".format(int(dialog.maxCustomer) + 1))
			else:
				dialog.ui.newIDButton.setText("Unchecked. Please assigns id")
				dialog.ui.nameEdit.setDisabled(True)
				dialog.ui.ageEdit.setDisabled(True)
				dialog.ui.phoneEdit.setDisabled(True)
				dialog.ui.addressEdit.setDisabled(True)
				dialog.ui.lineEdit.setText("")
				dialog.ui.nameEdit.setText("")
				dialog.ui.ageEdit.setText("")
				dialog.ui.phoneEdit.setText("")
				dialog.ui.addressEdit.setText("")

		dialog.ui.newIDButton.setCheckable(True)
		dialog.ui.newIDButton.clicked.connect(newIDHandler)

		def setDefault(self):
			dialog.ui.saleEdit.setText('0')
			dialog.ui.taxEdit.setText("0")

		dialog.ui.defaultButton.clicked.connect(setDefault)
		dialog.show()
		dialog.ui.lineEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.nameEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.ageEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.phoneEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.addressEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.lineEdit_2.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.saleEdit.textChanged.connect(checkEmptyLineEdit)
		dialog.ui.taxEdit.textChanged.connect(checkEmptyLineEdit)

		#NOTE AREA TESTING
		dialog.ui.noteArea.setWidgetResizable(False)
		dialog.ui.scrollAreaWidgetContents.setMinimumSize(200, 500)
		dialog.ui.noteEdit = []
		dialog.ui.labelBox = []

		def applyEvent():
			dialog.applyBoolean = dialog.applyBoolean + 1
			result = dialog.transModel.priceSum(dialog.newID)
			text = dialog.ui.sumUpLabel.text()
			text = text[:14]
			dialog.ui.sumUpLabel.setText(text + " {:,.0f}VND".format(result))

			query = QSqlQuery("SELECT id, product_id, productName, pricePerProduct*amount, note FROM transactionTable\
				INNER JOIN productTable USING(product_id) WHERE id = '{}' AND pricePerProduct*amount > 0".format(dialog.newID))
			dialog.list_1 = []
			while query.next():
				text = []
				for i in range(query.record().count()):
					text.append(query.result().data(i))
				dialog.list_1.append(text)

			for i in range(len(dialog.list_1)):
				dialog.ui.labelBox.append(QLabel(dialog.ui.scrollAreaWidgetContents))
				dialog.ui.verticalLayout_3.addWidget(dialog.ui.labelBox[i])
				dialog.ui.labelBox[i].setText(dialog.list_1[i][2])
				
				dialog.ui.noteEdit.append(QTextEdit(dialog.ui.scrollAreaWidgetContents))
				dialog.ui.verticalLayout_3.addWidget(dialog.ui.noteEdit[i])
				dialog.ui.noteEdit[i].setMinimumSize(0, 50)


		dialog.ui.applyButton.clicked.connect(applyEvent)

		def saveTransacNote():
			for i in range(len(dialog.list_1)):
				text = dialog.ui.noteEdit[i].toPlainText()
				query = QSqlQuery("UPDATE transactionTable SET note = '{}' WHERE id = '{}' AND product_id = '{}'".format(text, int(dialog.list_1[i][0]), int(dialog.list_1[i][1])))
				query.exec_()

		def acceptEvent():
			customer_id = int(dialog.ui.lineEdit.text())
			if dialog.ui.newIDButton.isChecked(): #add customer
				if len(dialog.ui.nameEdit.text()) > 0: 
					name = dialog.ui.nameEdit.text()
				else: 
					name = "DEFAULT"
				if len(dialog.ui.nameEdit.text()) > 0:
					age = int(dialog.ui.ageEdit.text())
				else:
					age = 100
				if len(dialog.ui.phoneEdit.text()) > 0:
					phone = dialog.ui.phoneEdit.text()
				else:
					phone = "0999999999"
				if dialog.ui.addressEdit.text():
					address = dialog.ui.addressEdit.text()
				else:
					address = "VIETNAM"

				self.q.newCustomer(name, 0, age, phone, address)
				self.customerTableModel.setQuery(self.q.customerTableReading())
				self.customerTable.setModel(self.customerTable)

			if dialog.ui.lineEdit_2.text():
				creator = dialog.ui.lineEdit_2.text()
			else:
				creator = "DEFAULT"

			date = dialog.ui.dateTimeEdit.dateTime().toString('dd/MM/yyyy h:mm:ss')

			if dialog.ui.saleEdit.text():
				discount = float(dialog.ui.saleEdit.text())
			else:
				discount = 0.00
			if dialog.ui.taxEdit.text():
				tax = float(dialog.ui.taxEdit.text())
			else:
				tax = 0.00

			note = dialog.ui.textEdit.toPlainText()

			if dialog.applyBoolean == 0:
				applyEvent()
			else:
				pass
			saveTransacNote()

			pay = int(dialog.transModel.priceSum(dialog.newID))
			pay = pay*(1-discount)
			self.q.eraseZeroTrans(int(dialog.newID))
			self.q.setSaleValue(int(dialog.newID), customer_id, date, creator, discount, tax, note, pay)
			self.q.deleteUnknownSaleRow()

			self.model.setQuery(self.q.saleReading())
			self.orderTable.setModel(self.model)

		def rejectEvent():
			self.q.eraseBaseOnIDTrans(int(dialog.newID))
			self.q.deleteUnknownSaleRow()

		dialog.ui.buttonBox.accepted.connect(acceptEvent)
		dialog.ui.buttonBox.rejected.connect(rejectEvent)

	def openFilterDialog(self):
		if self.filterButton.isChecked(): #FILTER OPTION
			dialog = QtWidgets.QDialog()
			dialog.setStyleSheet(qdarkstyle.load_stylesheet())
			dialog.ui = filterWindow()
			dialog.ui.setupUi(dialog)
			#dialog.exec_()

			#VALIDATION WHITH REGULAR EXPRESSION
			reg_exp_forNumbers = QRegExp("^[0-9:/]{1,11}$")
			reg_exp_forString = QRegExp("[^0-9]+")

			idValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.idFilter)
			dialog.ui.idFilter.setValidator(idValid)

			customerValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.customerIDFilter)
			dialog.ui.customerIDFilter.setValidator(customerValid)

			dateValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.dateFilter)
			dialog.ui.dateFilter.setValidator(dateValid)

			creatorValid = QRegExpValidator(reg_exp_forString, dialog.ui.creatorFilter)
			dialog.ui.creatorFilter.setValidator(creatorValid)

			#ENSURE UNEMPTY LINE EDIT
			dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
			def enableOkButton():
				if len(dialog.ui.idFilter.text()) > 0 or\
				len(dialog.ui.customerIDFilter.text()) > 0 or\
				len(dialog.ui.dateFilter.text()) > 0 or\
				len(dialog.ui.creatorFilter.text()) > 0 or\
				len(dialog.ui.statusFilter.text()) > 0:
					dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)
				else:
					dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

			dialog.show()

			dialog.ui.idFilter.textChanged.connect(enableOkButton)
			dialog.ui.customerIDFilter.textChanged.connect(enableOkButton)
			dialog.ui.dateFilter.textChanged.connect(enableOkButton)
			dialog.ui.creatorFilter.textChanged.connect(enableOkButton)
			dialog.ui.statusFilter.textChanged.connect(enableOkButton)

			def acceptEvent():
				idFilter = dialog.ui.idFilter.text()
				customerIDFilter = dialog.ui.customerIDFilter.text()
				dateFilter = dialog.ui.dateFilter.text()
				creatorFilter = dialog.ui.creatorFilter.text()
				statusFilter = dialog.ui.statusFilter.text()
				text = ''
				if len(idFilter) > 0:
					text = text + "id = '{}' AND ".format(int(idFilter))
				if len(customerIDFilter) > 0:
					text = text + "customer_id = '{}' AND ".format(int(customerIDFilter))
				if len(dateFilter) > 0:
					text = text + "dateCreate LIKE '{}%' AND ".format(dateFilter)
				if len(creatorFilter) > 0:
					text = text + "creator = '{}' AND ".format(creatorFilter)
				if len(statusFilter) > 0:
					if statusFilter in ['ON DELIVERY', '1']:
						statusFilter = 1
					elif statusFilter in ['PENDING', '0']:
						statusFilter = 0
					else:
						statusFilter = 2
					text = text + "status = '{}' AND ".format(statusFilter)

				temp = text.rfind("AND ")
				text = text[:temp]
				self.model.setFilter(text)
			def rejectEnvent():
				pass
			dialog.ui.buttonBox.accepted.connect(acceptEvent)
			dialog.ui.buttonBox.rejected.connect(rejectEnvent)
		else:
			self.model.setFilter('')

	def transacHistory(self):
		dialog = QtWidgets.QDialog()

		indexes = self.customerTable.selectedIndexes()
		if indexes:
			index = indexes[0].row()
			temp = self.customerTableModel.customer_idReturn(index)
			query = QSqlQuery(self.q.historyReading(temp))
			dialog.balance = 0
			while query.next():
				if "HD" in query.result().data(1):
					dialog.balance = dialog.balance + query.result().data(4)
				elif "PT" in query.result().data(1):
					dialog.balance = dialog.balance - query.result().data(4)

		historyModel = sqlQueryModelHistory()
		historyModel.setQuery(query)
		

		
		dialog.ui = historyWindow()
		dialog.setStyleSheet(qdarkstyle.load_stylesheet())
		dialog.ui.setupUi(dialog)
		dialog.ui.historyTable.setModel(historyModel)
		#Balance Label setting
		text = dialog.ui.balanceLabel.text()
		text = text[0:7]
		dialog.ui.balanceLabel.setText(text + ' {:,d} VND'.format(int(dialog.balance)))


		dialog.show()
		dialog.exec_()

	def changePayState(self):
		indexes = self.orderTable.selectedIndexes()
		if indexes:
			index = indexes[0].row()

			dialog = QtWidgets.QDialog()
			dialog.setStyleSheet(qdarkstyle.load_stylesheet())

			dialog.id = self.model.idReturn(index) #temp store the customer_id returned from the sqlmodel
			dialog.cusid = self.model.customer_idReturn(index)
			dialog.pay = self.model.payReturn(index)

			datetimeNow = datetime.now()
			cur_time = datetimeNow.strftime("%d/%m/%Y %H:%M:%S")
			dialog.qdatetime = QDateTime.fromString(cur_time, "dd/MM/yyyy h:mm:ss")

			dialog.ui = phieuthu()
			dialog.ui.setupUi(dialog)
			#REGULAR EXPRESSION + VALIDATOR

			reg_exp_forString = QRegExp("[^0-9]+")
			creatorValid = QRegExpValidator(reg_exp_forString, dialog.ui.creatorEdit)
			dialog.ui.creatorEdit.setValidator(creatorValid)

			reg_exp_forNumbers = QRegExp("^[0-9]+$")
			payValid = QRegExpValidator(reg_exp_forNumbers, dialog.ui.payEdit)
			dialog.ui.payEdit.setValidator(payValid)

			#SETUP INFORMATION
			dialog.ui.dateTimeEdit.setDateTime(dialog.qdatetime)
			dialog.ui.idLabel.setText(dialog.id)
			dialog.ui.customer_idLabel.setText(dialog.cusid)
			dialog.ui.payLabel.setText("{:,d}".format(dialog.pay))

			#SETUP DISABLED BUTTON
			dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

			def checkEmpty():
				if len(dialog.ui.creatorEdit.text()) > 0\
				and len(dialog.ui.payEdit.text()) > 0:
					dialog.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(False)

			dialog.ui.creatorEdit.textChanged.connect(checkEmpty)
			dialog.ui.payEdit.textChanged.connect(checkEmpty)

			def setMoney():
				dialog.ui.payEdit.setText("{}".format(dialog.pay))

			dialog.ui.pushButton.clicked.connect(setMoney)
			dialog.show()

			def acceptEvent():
				date = dialog.ui.dateTimeEdit.dateTime().toString('dd/MM/yyyy h:mm:ss')
				creator = dialog.ui.creatorEdit.text()
				pay = int(dialog.ui.payEdit.text())
				self.q.addHistory(dialog.id, date, creator, pay)

				if dialog.pay - pay == 0:
					self.q.changeStatus(dialog.id)
					self.model.setQuery(self.q.saleReading())
					self.orderTable.setModel(self.model)

			def rejectEvent():
				pass

			dialog.ui.buttonBox.accepted.connect(acceptEvent)
			dialog.ui.buttonBox.rejected.connect(rejectEvent)
		else:
			pass
		
#SQL SECTION
class sqlHandle():
	def __init__(self):
		self.createConnection()
		self.createTable()

	def createConnection(self):
		db = QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName("data.db")
		if not db.open():
			print("Failed")
			return False
		return True

	def createTable(self):
		q = QSqlQuery()
		q.exec_(\
			"CREATE TABLE IF NOT EXISTS customerTable (customer_id INTEGER PRIMARY KEY,\
			name TEXT, sex INTEGER, age INTEGER, phone TEXT, address TEXT)")
		q.exec_(\
			"CREATE TABLE IF NOT EXISTS saleTable (id INTEGER PRIMARY KEY, \
			customer_id INTEGER, \
			paymentDiscount REAL,\
			paymentTax REAL, status INTEGER, note TEXT,\
			FOREIGN KEY (customer_id) \
			REFERENCES customerTable(customer_id) \
			ON UPDATE CASCADE)")
		q.exec_(\
			"CREATE TABLE IF NOT EXISTS productTable(product_id INTEGER PRIMARY KEY, \
			productName TEXT, defaultPrice REAL, description TEXT)")
		q.exec_(\
			"CREATE TABLE IF NOT EXISTS transactionTable(id INTEGER, product_id INTEGER, pricePerProduct REAL, amount REAL, note TEXT, \
			FOREIGN KEY(id) \
			REFERENCES saleTable(id) \
			ON UPDATE CASCADE\
			FOREIGN KEY (product_id)\
			REFERENCES productTable(product_id)\
			ON UPDATE CASCADE)")
		q.exec_(\
			"CREATE TABLE IF NOT EXISTS history(id INTEGER, type TEXT default 'HD', dateCreate TEXT, creator TEXT, pay REAL DEFAULT 0, \
			FOREIGN KEY(id) \
			REFERENCES saleTable(id)\
			ON UPDATE CASCADE)")

		q.exec_("CREATE VIEW IF NOT EXISTS table_View AS\
			SELECT saleTable.id, customer_id, history.dateCreate, history.creator, COUNT(product_id) AS productAmount, SUM(pricePerProduct*amount) AS priceSum , status, saleTable.note,\
			paymentDiscount, paymentTax\
			FROM saleTable\
			INNER JOIN transactionTable ON saleTable.id = transactionTable.id\
			INNER JOIN history ON saleTable.id = history.id\
			WHERE history.type = 'HD'\
			GROUP BY saleTable.id")

		q.exec_("CREATE VIEW IF NOT EXISTS customerSideView AS\
				SELECT DISTINCT customerTable.customer_id, name, sex, age, phone, address\
				FROM customerTable\
				INNER JOIN saleTable ON saleTable.customer_id = customerTable.customer_id")

#TAB ĐƠN HÀNG + SIDE VIEW CHO TAB KHÁCH HÀNG
	def saleReading(self):
		query = 'SELECT id, customer_id, dateCreate, creator, productAmount, \
		priceSum*(1-paymentDiscount/100)*(1+paymentTax/100) as finalPrice,\
		status, paymentDiscount, paymentTax, note FROM table_View'
		return query

	def customerReading(self, temp):
		query = 'SELECT * FROM customerSideView WHERE customer_id = {}'.format(temp)
		return query

	def transactionReading(self, temp):
		query = 'SELECT productName, pricePerProduct, amount, pricePerProduct*amount, note FROM transactionTable\
		INNER JOIN productTable USING(product_id) WHERE id = {}'.format(temp)
		return query
#OPEN-ADD-THANH-TOAN-DIALOG FUNCTION
	def addSaleTable(self): #initialize 1 new sale row and empty trans rows
		q = QSqlQuery()
		q.exec_("INSERT INTO saleTable DEFAULT VALUES")
		query = QSqlQuery("SELECT MAX(id) FROM saleTable")
		while query.next():
			temp = query.result().data(0)

		q.exec_("INSERT INTO transactionTable\
					SELECT id, product_id, defaultPrice, 0, ''\
					FROM saleTable\
					CROSS JOIN productTable\
					WHERE id = (\
					SELECT MAX(id) FROM saleTable);")
		q.exec_("INSERT INTO history(id) VALUES('{}')".format(temp))
		return temp


	def findMaxCustomerID(self):
		query = QSqlQuery("SELECT MAX(customer_id) FROM customerTable")
		while query.next():
			temp = query.result().data(0)
		return temp

	def newCustomer(self, name, sex, age, phone, address):
		q = QSqlQuery()
		q.exec_("INSERT INTO customerTable (name, sex, age, phone, address) VALUES('{}', '{}', '{}', '{}', '{}')".format(name, sex, age, phone, address))

	def eraseZeroTrans(self, newID):
		query = QSqlQuery("DELETE FROM transactionTable WHERE id = '{}' AND pricePerProduct*amount = 0".format(newID))
		query.exec_()

	def eraseBaseOnIDTrans(self, newID):
		query = QSqlQuery("DELETE FROM transactionTable WHERE id = '{}' ".format(newID))
		query.exec_()
		query = QSqlQuery("DELETE FROM history WHERE id = '{}'".format(newID))
		query.exec_()

	def setSaleValue(self, newID, customer_id, date, creator, discount, tax, note, pay): #CẦN SỬA GẤP
		query = QSqlQuery("UPDATE saleTable SET customer_id = '{}',\
		paymentDiscount = '{}', paymentTax = '{}', status = '{}',\
		note = '{}' WHERE id = '{}'".format(customer_id, discount, tax, 0, note, newID))

		query.exec_()

		query= QSqlQuery("UPDATE history SET dateCreate = '{}', creator = '{}', pay = '{}' WHERE id = '{}' AND type = 'HD'".format(date, creator, pay,newID))

		query.exec_()

	def editNewTransaction(self, newID):
		query = "SELECT id, product_id, productName, pricePerProduct, amount, pricePerProduct*amount FROM transactionTable\
			INNER JOIN productTable USING (product_id) WHERE id = '{}'".format(newID)
		return query

	def deleteUnknownSaleRow(self):
		q = QSqlQuery()
		q.exec_("DELETE FROM history WHERE id = (\
			SELECT id FROM saleTable WHERE customer_id IS NULL)")
		q.exec_("DELETE FROM history WHERE id IS NULL")

		q.exec_("DELETE FROM saleTable WHERE customer_id IS NULL")

	def addHistory(self, this_id, date, creator, pay):
		q = QSqlQuery()
		q.exec_("INSERT INTO history(id, type, dateCreate, creator, pay) VALUES('{}' , '{}', '{}', '{}', '{}')".format(this_id, "PT", date, creator, pay))

	def changeStatus(self, this_id):
		q = QSqlQuery()
		q.exec_("UPDATE saleTable SET status = 2 WHERE id = '{}'".format(this_id))
#TAB KHÁCH HÀNG
	def customerTableReading(self):
		query = "SELECT * FROM customerTable"
		return query

	def historyReading(self, temp):
		query = "SELECT saleTable.id, type, dateCreate, creator, pay FROM history INNER JOIN saleTable USING (id) WHERE customer_id = {}".format(temp)
		return query

#TAB SẢN PHẨM
	def productReading(self):
		query = "SELECT product_id, productName, defaultPrice, description FROM productTable"
		return query



if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	sys.exit(app.exec_())