from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel, 
                         QSqlRelationalTableModel, QSqlRelation)
from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.Qt import QSortFilterProxyModel
import sys

db_file = "test.db"

def create_connection(db_file):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_file)
    if not db.open():
        print("Cannot establish a database connection to {}!".format(db_file))
        return False
    return db


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


class CarTable(QTableView):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.create_model()

    def create_model(self):
        query = """
        SELECT (comp.company || " " || cars.model) as Car,
                comp.Country,
                (CASE WHEN cars.Year > 2000 THEN 'yes' ELSE 'no' END) as this_century
        from manufacturers comp left join cars
            on comp.company = cars.company
        """
        raw_model = QSqlTableModel()
        q = QSqlQuery()
        q.exec_(query)
        self.check_error(q)
        raw_model.setQuery(q)

        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(raw_model)
        self.setModel(self.model)

        # filtering:
        self.model.setFilterKeyColumn(0)
        self.model.setFilterFixedString('VW')

    def init_UI(self):
        self.resize(500,300)

    def check_error(self, q):
        lasterr = q.lastError()
        if lasterr.isValid():
            print(lasterr.text())
            exit(1)


def main():
    mydb = create_connection(db_file)
    if not mydb:
        sys.exit(-1)
    fill_tables()
    app = QApplication(sys.argv)
    ex = CarTable()
    ex.show()
    result = app.exec_()

    if (mydb.open()):
        mydb.close()

    sys.exit(result)


if __name__ == '__main__':
    main()