import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem, QPushButton, QHBoxLayout, QTableWidget, QLineEdit, \
    QMessageBox


def get_column_names(cursor, table_name):
    query = f'PRAGMA table_info({table_name})'
    data = cursor.execute(query).fetchall()
    ans = [i[1] for i in data]
    return ans


class EditingDataForm(QWidget):
    def __init__(self, parent):
        super(EditingDataForm, self).__init__()
        self.parent = parent
        uic.loadUi('addEditCoffeeForm.ui', self)
        columns = get_column_names(parent.cursor, parent.table_name)
        self.les = [QLineEdit() for i in range(len(columns))]
        [self.formLayout.addRow(label, le) for label, le in zip(columns, self.les)]
        self.pushButton.clicked.connect(self.edit)
        self.pushButton_2.clicked.connect(self.add)

    def get_values(self):
        values = [i.text() for i in self.les]
        values = [values[i] if i in [1, 4] else int(values[i]) for i in range(len(values))]
        return values

    def add(self):
        n = len(get_column_names(self.parent.cursor, self.parent.table_name))
        a = ", ".join(["?" for _ in range(n)])
        query = f'INSERT INTO {self.parent.table_name} VALUES ({a})'
        try:
            self.perform(query, self.get_values())
        except Exception:
            self.raise_error()

    def edit(self):
        query = f'UPDATE {self.parent.table_name} SET '
        cols = get_column_names(self.parent.cursor, self.parent.table_name)[1:]
        query += ', '.join(i + ' = ?' for i in cols)
        query += ' WHERE id = ?'
        try:
            values = self.get_values()
            q = f'SELECT id FROM {self.parent.table_name} WHERE id = ?'
            if not self.parent.cursor.execute(q, [values[0]]).fetchall():
                raise Exception
            values = values[1:] + [values[0]]
            self.perform(query, values)
        except Exception:
            self.raise_error()

    def perform(self, query, values):
        self.parent.cursor.execute(query, values)
        self.parent.connection.commit()
        self.parent.update_table()

    def raise_error(self):
        d = QMessageBox(self, text='Некорректный ввод')
        d.exec()


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.table_name = 'coffee'
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect('coffee.sqlite')
        self.cursor = self.connection.cursor()
        self.update_table()
        self.editing_data_form = EditingDataForm(self)
        self.layout().addWidget(self.editing_data_form)

    def update_table(self):
        query = 'SELECT * FROM ' + self.table_name
        data = self.cursor.execute(query).fetchall()
        rows = len(data)
        cols = len(data[0]) if data else 0
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setHorizontalHeaderLabels(get_column_names(self.cursor, self.table_name))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
