import trimesh
from PyQt5.QtWidgets import QMessageBox

from GUI.alerts.information_dialog import information_dialog
from Utils.database.database import model_filepath
from Utils.database.structures.structures_database import set_center_of_mass, set_moments_of_inertia


def get_functions(workflow):
    def maximum_takeoff_mass():
        pass

    def centerMass():
        dialog = information_dialog()
        results = dialog.exec_()
        if results == 1:
            workflow.viewer.save_model()
            mesh = trimesh.load(model_filepath)
            set_center_of_mass({"x":round(list(mesh.center_mass)[0],2),"y":round(list(mesh.center_mass)[1],2),"z":round(list(mesh.center_mass)[2],2)})
            dialog = QMessageBox()
            dialog.setWindowTitle("Center of Mass")
            dialog.setIcon(QMessageBox.Information)
            dialog.setText(f"x: {round(list(mesh.center_mass)[0],2)} y: {round(list(mesh.center_mass)[1],2)} z: {round(list(mesh.center_mass)[2],2)}")
            dialog.addButton(QMessageBox.Ok)
            dialog.exec()

    def moment_of_inertia():
        dialog = information_dialog()
        results = dialog.exec_()
        if results == 1:
            workflow.viewer.save_model()
            mesh = trimesh.load(model_filepath)
            print(round(list(mesh.moment_inertia)[0][0],2))
            set_moments_of_inertia({"Ixx":list(mesh.moment_inertia)[0][0],
                                    "Ixy":-float(list(mesh.moment_inertia)[0][1]),
                                    "Ixz":-float(list(mesh.moment_inertia)[0][2]),
                                    "Iyy":float(list(mesh.moment_inertia)[1][1]),
                                    "Iyz":-float(list(mesh.moment_inertia)[1][2]),
                                    "Izz":-float(list(mesh.moment_inertia)[2][2])})
            dialog = QMessageBox()
            dialog.setWindowTitle("Moment Of Inertia")
            dialog.setIcon(QMessageBox.Information)
            dialog.setText(f" \n{list(mesh.moment_inertia)[0]}  \n{list(mesh.moment_inertia)[1]}   \n{list(mesh.moment_inertia)[2]}")
            dialog.addButton(QMessageBox.Ok)
            dialog.exec()

    return maximum_takeoff_mass,centerMass,moment_of_inertia

