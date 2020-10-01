from PyQt5.QtWidgets import QMessageBox


def show_warning(text):
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Critical)
    dialog.setText(text)
    dialog.addButton(QMessageBox.Ok)
    dialog.exec()
def show_results(text):
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setText(text)
    dialog.addButton(QMessageBox.Ok)
    dialog.exec()