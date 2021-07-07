import trimesh
from PyQt5.QtWidgets import QMessageBox

from Utils.database.database import model_filepath
from Utils.database.structures.structures_database import set_center_of_mass, set_moments_of_inertia


def get_functions(workflow):
    def maximum_takeoff_mass():
        pass

    def centerMass():
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
        workflow.viewer.save_model()
        mesh = trimesh.load(model_filepath)
        set_moments_of_inertia({"Ixx":round(list(mesh.center_mass)[0][0],2),
                                "Ixy":-round(list(mesh.center_mass)[0][1],2),
                                "Ixz":-round(list(mesh.center_mass)[0][2],2),
                                "Iyy":round(list(mesh.center_mass)[1][1],2),
                                "Iyz":-round(list(mesh.center_mass)[1][2],2),
                                "Izz":-round(list(mesh.center_mass)[2][2],2)})
        dialog = QMessageBox()
        dialog.setWindowTitle("Moment Of Inertia")
        dialog.setIcon(QMessageBox.Information)
        dialog.setText(f" \n{list(mesh.moment_inertia)[0]}  \n{list(mesh.moment_inertia)[1]}   \n{list(mesh.moment_inertia)[2]}")
        dialog.addButton(QMessageBox.Ok)
        dialog.exec()

    return maximum_takeoff_mass,centerMass,moment_of_inertia

