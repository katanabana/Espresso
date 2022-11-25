import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('coffee.sqlite')
        query = 'SELECT * FROM coffee'
        data = con.cursor().execute(query).fetchall()
        rows = len(data)
        cols = len(data[0]) if data else 0
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())