import sys

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QApplication, QTableView

db_file = "test.db"


def create_connection(file_path):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(file_path)
    if not db.open():
        print("Cannot establish a database connection to {}!".format(file_path))
        return False
    return True


def fill_tables():
    q = QSqlQuery()
    q.exec_("DROP TABLE IF EXISTS Manufacturers;")
    q.exec_("CREATE TABLE Manufacturers (Company TEXT, Country TEXT);")
    q.exec_("INSERT INTO Manufacturers VALUES ('VW', 'Germany');")
    q.exec_("INSERT INTO Manufacturers VALUES ('Honda' , 'Japan');")

    q.exec_("DROP TABLE IF EXISTS Cars;")
    q.exec_("CREATE TABLE Cars (Company TEXT, Model TEXT, Year INT);")
    q.exec_("INSERT INTO Cars VALUES ('Honda', 'Civic', 2009);")
    q.exec_("INSERT INTO Cars VALUES ('VW', 'Golf', 2013);")
    q.exec_("INSERT INTO Cars VALUES ('VW', 'Polo', 1999);")


class SqlQueryModel(QSqlQueryModel):
    def flags(self, index):
        fl = QSqlQueryModel.flags(self, index)
        if index.column() == 1:
            fl |= Qt.ItemIsEditable
        return fl

    def setData(self, index, value, role=Qt.EditRole):
        if index.column() == 1:
            company = self.index(index.row(), 2).data()
            print(company)
            q = QSqlQuery("UPDATE Manufacturers SET Country = '{}' WHERE Company =  '{}'".format(value, company))
            result = q.exec_()
            if result:
                self.query().exec_()
            else:
                print(self.query().lastError().text())
            return result
        return QSqlQueryModel.setData(self, index, value, role)

    def setFilter(self, filter):
        text = (self.query().lastQuery() + " WHERE " + filter)
        self.setQuery(text)


query = '''
        SELECT (comp.company || " " || cars.model) as Car,
                comp.Country,
                cars.company,
                (CASE WHEN cars.Year > 2000 THEN 'yes' ELSE 'no' END) as this_century
        from manufacturers comp left join cars
            on comp.company = cars.company
        '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not create_connection(db_file):
        sys.exit(-1)

    fill_tables()

    view = QTableView()

    model = SqlQueryModel()
    q = QSqlQuery(query)
    model.setQuery(q)
    model.setFilter("cars.Company = 'VW'")
    view.setModel(model)
    view.hideColumn(2)
    view.show()
    sys.exit(app.exec_())