from PyQt5 import Qt
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QFormLayout, QScrollArea, QTextEdit


class Text_Report(QDialog):
    def __init__(self, parent=None):
        super(Text_Report, self).__init__(parent)
        scroll=QScrollArea(self)
        layout = QFormLayout(self)
        self.setWindowTitle("Report")
        self.text= QTextEdit()
        layout.addWidget(self.text)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget=QWidget(self)
        widget.setLayout(layout)
        scroll.setWidget(widget)
        temp_layout=QVBoxLayout(self)
        temp_layout.addWidget(scroll)
        self.setLayout(temp_layout)
    def set_text(self,info=""):
         self.text.setText(info)
    ############################################################################

