from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

import sys





class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.centralwidget = QtWidgets.QWidget(self)
		_translate = QtCore.QCoreApplication.translate
		self.centralwidget.setObjectName("centralwidget")



		model = QSqlTableModel()
		model.setTable("employee")
		model.setEditStrategy(QSqlTableModel.OnManualSubmit)
		model.select()
		#model.removeColumn(0) # don't show the ID
		model.setHeaderData(0, Qt.Horizontal, QtCore.QCoreApplication.translate("NAME", "HUNG"))
		model.setHeaderData(1, Qt.Horizontal, QtCore.QCoreApplication.translate("SALARY", "HUNG"))
		print(model)
		print(model)

		view =  QTableView(self.centralwidget)
		view.setModel(model)
		view.
		
		self.show()


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())