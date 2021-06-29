import random

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg

from Utils.data_objects.aerodynamics_placeholders import alpha
from Utils.database.aerodynamics.loader import read_datcom_table_data, get_pandas_datcom_table, datcom_data, \
    read_sandbox_table_data


class plotter_tab(QWidget):
    def __init__(self,type_="",major_key="",name=""):
        super().__init__()
        layout = QFormLayout(self)
        self.setWindowTitle(name)
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)


        self.setLayout(layout)
        self.plot(type_,major_key,name)

    def plot(self, type_="",major_key="",name=""):
        alpha_, velocity_, y =  read_datcom_table_data(type_, major_key, name) if type_ == datcom_data else read_sandbox_table_data(type_, major_key, name)
        self.graphWidget.setLabel('bottom', alpha, units='degrees')
        self.graphWidget.setLabel('left',name)
        self.graphWidget.addLegend()
        try:
                self.graphWidget.plot(alpha_, y[0][:len(alpha_)],
                                      pen=pg.mkPen(color=(random.randint(0, 255),
                                                          random.randint(0, 255),
                                                          random.randint(0, 255))))
        except:
                print(y,alpha_)


