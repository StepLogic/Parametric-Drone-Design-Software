from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox

from GUI.dialogs.aerodynamics_dialogs.settings_dialogs import settings_dialog
from GUI.dialogs.geometry_dialogs.boom_dialog_.boom_dialog import boom_dialog
from GUI.dialogs.geometry_dialogs.control_surface.control_surface_dialogs import control_surface_dialog
from GUI.dialogs.geometry_dialogs.landing_dialog.landing_gear_dialog import landing_gear_dialog
from GUI.dialogs.geometry_dialogs.lifting_surface_dialog_.lifting_surface_dialog import lifting_surface_dialog
from GUI.dialogs.propulsion_dialogs.propeller.propeller_dialog import propeller_dialog
from GUI.dialogs.propulsion_dialogs.propulsion_dialog import propulsion_dialog
from GUI.dialogs.propulsion_dialogs.shroud.shroud_dialog import shroud_dialog
from GUI.dialogs.structure_dialogs.structures_dialog import structures_dialog
from GUI.workflow.threads.geometry.GeometryThread import GeometryThread
from Structures.trimesh.trimeshWrapper import get_functions
from Utils.data_objects.workflow_placeholders import datcom_, sandbox_, update_surface_3D_, update_boom_3D_, build_cs, \
    build_landing_gear, start_multisandbox, build_shroud, build_propeller
from Utils.database.geometry.control_surface_database import read_control_surface_objects
from Utils.database.geometry.main_database import wipe_design_options, wipe_design


def setup_ui(workflow):
    def execute_command(command="", current_loft=None):
        workflow.events.set()
        workflow.sendTasks.send([command, current_loft])

    def setup_design_menu():
        workflow.add_menu("Design")
        workflow.add_function_to_menu("Design", start_new_design)
        workflow.add_function_to_menu("Design", design_overview)

    def setup_control_surface():
        def control_surface():
            dialog = control_surface_dialog(workflow=workflow)
            results = dialog.exec_()
            if results == 1:
                dialog.save_all()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow,command=build_cs)
                pool.start(runnable)

        workflow.add_function_to_menu("Geometry", control_surface)

    def setup_landing_gear():
        def landing_gear():
            dialog = landing_gear_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow, command=build_landing_gear)
                pool.start(runnable)

        workflow.add_function_to_menu("Geometry", landing_gear)

    def setup_propulsion_menu():
        workflow.add_menu("Propulsion")

        def enter_parameters():
            dialog = propulsion_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()

        def propeller():
            dialog = propeller_dialog(workflow=workflow)
            results = dialog.exec_()
            if results == 1:
                dialog.save_all()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow,command=build_propeller)
                pool.start(runnable)

        def shroud():
            dialog = shroud_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow, command=build_shroud)
                pool.start(runnable)

        workflow.add_function_to_menu("Propulsion", enter_parameters)
        workflow.add_function_to_menu("Propulsion", propeller)
        workflow.add_function_to_menu("Propulsion", shroud)

    def setup_performance_menu():
        workflow.add_menu("Performance")

        def enter_parameters():
            pass

        workflow.add_function_to_menu("Performance", enter_parameters)

    def setup_geometry_menu(workflow=workflow):
        workflow.add_menu("Geometry")

        def booms():
            dialog = boom_dialog(workflow=workflow)
            results = dialog.exec_()

            if results == 1:
                dialog.save_all()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow, command=update_boom_3D_)
                pool.start(runnable)

        def lifting_surfaces():
            dialog = lifting_surface_dialog(workflow=workflow)
            results = dialog.exec_()
            if results == 1:
                dialog.save_all()
                pool = QThreadPool.globalInstance()
                runnable = GeometryThread(workflow, command=update_surface_3D_)
                pool.start(runnable)

        workflow.add_function_to_menu("Geometry", booms)
        workflow.add_function_to_menu("Geometry", lifting_surfaces)

    def setup_structures_menu():
        workflow.add_menu("Structures")

        def structures():
            dialog = structures_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()

        workflow.add_function_to_menu("Structures", structures)
        func_ = get_functions(workflow)
        for l in func_:
            workflow.add_function_to_menu("Structures", l)

    def setup_aerodynamics_menu():
        workflow.add_menu("Aerodynamics")

        def sandbox():
            execute_command(command=sandbox_)

        def datcom():
            execute_command(command=datcom_)

        def multisandbox():
            execute_command(command=start_multisandbox)

        def settings():
            dialog = settings_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()

        workflow.add_function_to_menu("Aerodynamics", sandbox)
        workflow.add_function_to_menu("Aerodynamics", datcom)
        workflow.add_function_to_menu("Aerodynamics", multisandbox)
        workflow.add_function_to_menu("Aerodynamics", settings)

    def design_overview():
        workflow.design_window.exec_()

    def start_new_design():
        confirm = QMessageBox().question(None, "Prompt", "Are you want wipe the design?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
        if confirm == QMessageBox.Yes:
            wipe_design()
            wipe_design_options()
            workflow.viewer.eraseAll()
        else:
            pass

    setup_design_menu()
    setup_geometry_menu()
    setup_control_surface()
    setup_landing_gear()
    setup_structures_menu()
    setup_propulsion_menu()
    setup_aerodynamics_menu()
    setup_performance_menu()
