import trimesh
from PyQt5.QtWidgets import QMessageBox

from Utils.database.database import model_filepath


def get_functions(workflow):
    def maximum_takeoff_mass():
        pass

    def center_mass():
        workflow.viewer.save_model()
        mesh = trimesh.load(model_filepath)
        dialog = QMessageBox()
        dialog.setWindowTitle("Center of Mass")
        dialog.setIcon(QMessageBox.Information)
        dialog.setText(f"x: {list(mesh.center_mass)[0]} y: {list(mesh.center_mass)[1]}  z: {list(mesh.center_mass)[2]}")
        dialog.addButton(QMessageBox.Ok)
        dialog.exec()

    def moment_of_inertia():
        workflow.viewer.save_model()
        mesh = trimesh.load(model_filepath)
        dialog = QMessageBox()
        dialog.setWindowTitle("Moment Of Inertia")
        dialog.setIcon(QMessageBox.Information)
        dialog.setText(f" \n{list(mesh.moment_inertia)[0]}  \n{list(mesh.moment_inertia)[1]}   \n{list(mesh.moment_inertia)[2]}")
        dialog.addButton(QMessageBox.Ok)
        dialog.exec()

    return maximum_takeoff_mass,center_mass,moment_of_inertia

