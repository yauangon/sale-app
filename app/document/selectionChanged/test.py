import sys

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QAbstractItemView, QApplication, QTableView

names = ["Adam", "Brian", "Carol", "David", "Emily"]

def selection_changed():
    selected_names = [names[idx.row()] for idx in table_view.selectedIndexes()]
    print("Selection changed:", selected_names)

app = QApplication(sys.argv)
table_view = QTableView()
model = QStandardItemModel()
table_view.setModel(model)

for name in names:
    item = QStandardItem(name)
    model.appendRow(item)

table_view.setSelectionMode(QAbstractItemView.ExtendedSelection)  # <- optional
selection_model = table_view.selectionModel()
selection_model.selectionChanged.connect(selection_changed)

table_view.show()
app.exec_()