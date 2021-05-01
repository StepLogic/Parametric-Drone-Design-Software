from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.aerodynamics.table_tab import table_tab
from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database


class table_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        mainTabs = QTabWidget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.asbTabs = QTabWidget()
        self.datcomTabs = QTabWidget()
        mainTabs.addTab(self.asbTabs, sandbox_data)
        mainTabs.addTab(self.datcomTabs, datcom_data)
        self.layout.addRow(mainTabs)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.load_tabs()
    def load_tabs(self):
        for major_key in database.read_stability_specifications().keys():
            for key in database.read_stability_specifications()[major_key].keys():
               self.asbTabs.addTab(table_tab(type_=sandbox_data,major_key=major_key,name=key), key)
        for major_key in database.read_datcom_stability_specifications().keys():
            for key in database.read_datcom_stability_specifications()[major_key].keys():
                self.datcomTabs.addTab(table_tab(type_=datcom_data,major_key=major_key,name=key), key)
