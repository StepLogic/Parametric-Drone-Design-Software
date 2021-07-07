import random

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg

from Utils.database.performance.loader import read_data


class performance_plotter_tab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        layout = QFormLayout(self)
        self.setWindowTitle(name)
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        self.setLayout(layout)
        self.plot(name)

    def plot(self,name=""):
        time, y = read_data(name)
        self.graphWidget.setLabel('bottom', "time", units='s')
        self.graphWidget.setLabel('left', name)
        self.graphWidget.addLegend()

        try:
            self.graphWidget.plot(time, y[:len(time)],
                                  pen=pg.mkPen(color=(random.randint(0, 255),
                                                      random.randint(0, 255),
                                                      random.randint(0, 255))))
        except:
            pass


