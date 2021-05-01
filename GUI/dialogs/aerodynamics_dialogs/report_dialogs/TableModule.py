from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TableModule(QDialog):
    def __init__(self, parent=None,title="",y=[],x=[],y_label="",x_label=""):
        super(TableModule, self).__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle(title)
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setRowCount(len(y))
        self.tableWidget.setColumnCount(2)
        column_1=0
        column_2=1
        self.tableWidget.setItem(0, column_2, QTableWidgetItem(y_label))
        self.tableWidget.setItem(0, column_1, QTableWidgetItem(x_label))
        self.tableWidget.setMaximumSize(self.getQTableWidgetSize())
        self.tableWidget.setMinimumSize(self.getQTableWidgetSize())
        for i in range(1,len(y)):
          self.tableWidget.setItem(i,column_2, QTableWidgetItem(str(y[i])))
        for l in x:
            self.tableWidget.setItem(x.index(l)+1,column_1, QTableWidgetItem(str(l)))

        self.tableWidget.move(0, 0)


        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.toolbox_ = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        widget = QWidget(self)
        widget.setLayout(layout)

        temp_layout = QVBoxLayout(self)
        temp_layout.addWidget(widget)
        self.setLayout(temp_layout)






    def getQTableWidgetSize(self):
        w = self.tableWidget.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.tableWidget.columnCount()):
            w += self.tableWidget.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.tableWidget.horizontalHeader().height() + 4
        for i in range(self.tableWidget.rowCount()):
            h += self.tableWidget.rowHeight(i)
        return QtCore.QSize(w, h)

