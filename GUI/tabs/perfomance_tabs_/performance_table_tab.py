from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.database.aerodynamics.loader import read_datcom_table_data, get_pandas_datcom_table, datcom_data, \
    get_pandas_sandbox_table, read_sandbox_table_data
from Utils.database.performance.loader import read_data


class performance_table_tab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        layout = QFormLayout(self)
        self.setWindowTitle(name)

        self.create_table(name)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def create_table(self, name):
        time,y = read_data(name)
        self.tableWidget = QTableWidget()

        # Row count
        self.tableWidget.setRowCount(len(y))

        # Column count
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("Time"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(name))
        for time, value, index in zip(time, y, range(1, len(y))):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(f"{time}"))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(f"{value}"))

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
