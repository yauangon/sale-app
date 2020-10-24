from PyQt5 import QtGui, QtWidgets

class NotEmptyValidator(QtGui.QValidator):
    def validate(self, text, pos):
        state = QtGui.QIntValidator.Acceptable if bool(text) else QtGui.QIntValidator.Invalid
        return state, text, pos

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QLineEdit("Hello World")
    validator = NotEmptyValidator(w)
    w.setValidator(validator)
    w.show()
    sys.exit(app.exec_())