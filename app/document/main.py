import sys

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

from datetime import datetime
import sqlite3
import json
import qdarkstyle

app = QApplication(sys.argv)

'''def adapt_list_to_JSON(lst):
    return json.dumps(lst).encode('utf8')

def convert_JSON_to_list(data):
    return json.loads(data.decode('utf8'))


conn = sqlite3.connect('data.db', detect_types = sqlite3.PARSE_DECLTYPES)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS saleTable(id INTEGER PRIMARY KEY, \
	customer_id INTEGER, dateCreate TEXT, creator TEXT, \
	services json, paymentMethod INTEGER, paymentDiscount REAL,\
	paymentTax REAL, paymentDebt REAL)")
c.close
conn.close()'''

window = MainWindow()
sys.exit(app.exec_())