from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AnalysisDialog(QDialog):
    def __init__(self, parent=None):
        super(AnalysisDialog, self).__init__(parent)
        scroll = QScrollArea(self)
        layout = QFormLayout(self)
        self.parameters = {}
        self.setWindowTitle("Enter Simulation Parameters")

        ##########################################################################
        ##################################################################################

        self.alpha_label = QLabel("Angle Of Attack")
        self.alpha_text = QLineEdit()
        layout.addRow(self.alpha_label, self.alpha_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.beta_label = QLabel("Sideslip Angle")
        self.beta_text = QLineEdit()
        layout.addRow(self.beta_label, self.beta_text)

        ##################################################################################

        ##############################################################################
        self.velocity_label = QLabel("Free Stream Velocity")
        self.velocity_text = QLineEdit()
        layout.addRow(self.velocity_label, self.velocity_text)

        self.density_label = QLabel("Density")
        self.density_text = QLineEdit()
        layout.addRow(self.density_label, self.density_text)

        ##########################################################################################
        self.toolbox_ = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget = QWidget(self)
        widget.setLayout(layout)
        scroll.setWidget(widget)
        temp_layout = QVBoxLayout(self)
        temp_layout.addWidget(scroll)
        self.setLayout(temp_layout)

    ############################################################################
    def init_action(self):
        self.parameters = {
            "parameter": {
                "alpha": float(self.alpha_text.text()),
                "beta": float(self.beta_text.text()),
                "velocity": float(self.velocity_text.text()),
                "density": float(self.density_text.text()),

            }}
        return self.parameters

    @staticmethod
    def get_params():
        dialog = AnalysisDialog(None)
        result = dialog.exec_()
        if result == 1:
            try:
                params = dialog.init_action()
                return params, QDialog.Accepted
            except Exception:
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Critical)
                dialog.setText("Incorrect or No Values Entered")
                dialog.addButton(QMessageBox.Ok)
                dialog.exec()
                return [], QDialog.Rejected
        else:
            return [], QDialog.Rejected
