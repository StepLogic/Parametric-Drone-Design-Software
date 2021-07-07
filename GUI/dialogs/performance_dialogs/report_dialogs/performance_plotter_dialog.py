from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


from GUI.tabs.perfomance_tabs_.performance_plotter_tab import performance_plotter_tab
from Utils.database import database


class performance_plotter_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        mainTabs = QTabWidget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.asbTabs = QTabWidget()
        self.datcomTabs = QTabWidget()
        mainTabs.addTab(self.asbTabs,"Performance")
        self.layout.addRow(mainTabs)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.load_tabs()
    def load_tabs(self):
        for key in database.read_performance_specifications().keys():
            self.asbTabs.addTab(performance_plotter_tab(name=key), key)
