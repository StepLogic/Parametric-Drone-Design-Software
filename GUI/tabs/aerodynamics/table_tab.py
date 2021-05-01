from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.database.aerodynamics.loader import read_datcom_table_data, get_pandas_datcom_table, datcom_data, \
    get_pandas_sandbox_table


class table_tab(QWidget):
    def __init__(self, type_="", major_key="", name=""):
        super().__init__()
        layout = QFormLayout(self)
        self.setWindowTitle(name)
        self.tableWidget = QLabel(
            get_pandas_datcom_table(type_, major_key, name) if type_ == datcom_data else get_pandas_sandbox_table())
        layout.addWidget(self.tableWidget)

        self.toolbox_ = QHBoxLayout()

        layout.addWidget(self.tableWidget)

        self.setLayout(layout)
