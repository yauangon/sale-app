from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class main_window(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        # Create QLineEdit
        le_username = QLineEdit(self)
        le_username.setPlaceholderText("Enter username")
        le_password = QLineEdit(self)
        le_password.setPlaceholderText("Enter password")

        # Create QLabel
        lb_username = QLabel("Username: ")
        lb_password = QLabel("Password: ")

        # Adding a layout
        self.setLayout(QVBoxLayout())


        # Adding widgets to layout
        self.layout().addWidget(lb_username)
        self.layout().addWidget(le_username)


        self.layout().addWidget(lb_password)
        self.layout().addWidget(le_password)


        #!! ReGex implementation !!
        # For more details about ReGex search on google: regex rules or something similar 
        reg_ex = QRegExp("[a-z-A-Z_]+")
        le_username_validator = QRegExpValidator(reg_ex, le_username)
        le_username.setValidator(le_username_validator)
        #!! ReGex implementation End !!


        #.......
        self.setMinimumWidth(200)
        self.setWindowTitle("ReGEX Validator in Python with Qt Framework")

app = QApplication(sys.argv)
dialog = main_window()
dialog.show()
sys.exit(app.exec_())