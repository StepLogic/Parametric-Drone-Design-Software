from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMessageBox

from GUI.dialogs.aerodynamics_dialogs.report_dialogs.plotter_dialog import plotter_dialog
from GUI.dialogs.aerodynamics_dialogs.report_dialogs.table_dialog import table_dialog
from GUI.dialogs.aerodynamics_dialogs.settings_dialogs import settings_dialog
from GUI.dialogs.geometry_dialogs.boom_dialog_.boom_dialog import boom_dialog
from GUI.dialogs.geometry_dialogs.control_surface.control_surface_dialogs import control_surface_dialog
from GUI.dialogs.geometry_dialogs.landing_dialog.landing_gear_dialog import landing_gear_dialog
from GUI.dialogs.geometry_dialogs.lifting_surface_dialog_.lifting_surface_dialog import lifting_surface_dialog
from GUI.dialogs.propulsion_dialogs.propeller.propeller_dialog import propeller_dialog
from GUI.dialogs.propulsion_dialogs.propulsion_dialog import propulsion_dialog
from GUI.dialogs.propulsion_dialogs.shroud.shroud_dialog import shroud_dialog
from GUI.dialogs.structure_dialogs.structures_dialog import structures_dialog
from GUI.window.cad.structure_view import show_structure
from GUI.workflow.design_workflow import export_files
from GUI.workflow.threads.aerodynamics.AerodynamicsThread import AerodynamicThread

from GUI.workflow.threads.geometry.GeometryThread import GeometryThread
from Structures.trimesh.trimeshWrapper import get_functions
from Utils.data_objects.workflow_placeholders import datcom_, sandbox_, update_surface_3D_, update_boom_3D_, build_cs, \
    build_landing_gear, start_multisandbox, build_shroud, build_propeller, done_
from Utils.database.geometry.control_surface_database import read_control_surface_objects
from Utils.database.geometry.main_database import wipe_design_options, wipe_design


def setup_ui(workflow):

    def show_objects(trig):
        for name, loft in trig.items():
            workflow.viewer.update_object(part_name=name, lofts=loft)
        workflow.update_progress(done_)



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
                thread = GeometryThread()
                thread.trigger.connect(show_objects)  # connect to it's signal
                thread.setup(workflow, command=build_cs)  # just setting up a parameter
                thread.start()
                workflow.threads.append(thread)

        workflow.add_function_to_menu("Geometry", control_surface)

    def setup_landing_gear():
        def landing_gear():
            dialog = landing_gear_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()
                thread = GeometryThread()
                thread.trigger.connect(show_objects)  # connect to it's signal
                thread.setup(workflow, command=build_landing_gear)  # just setting up a parameter
                thread.start()
                workflow.threads.append(thread)
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
                thread = GeometryThread()
                thread.trigger.connect(show_objects)  # connect to it's signal
                thread.setup(workflow, command=build_propeller)  # just setting up a parameter
                thread.start()
                workflow.threads.append(thread)

        def shroud():
                dialog = shroud_dialog()
                results = dialog.exec_()
                if results == 1:
                    dialog.tab.init_action()
                    thread = GeometryThread()
                    thread.trigger.connect(show_objects)  # connect to it's signal
                    thread.setup(workflow, command=build_shroud)  # just setting up a parameter
                    thread.start()
                    workflow.threads.append(thread)

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
                thread = GeometryThread()
                thread.trigger.connect(show_objects)  # connect to it's signal
                thread.setup(workflow, command=update_boom_3D_)  # just setting up a parameter
                thread.start()
                workflow.threads.append(thread)

        def lifting_surfaces():
            dialog = lifting_surface_dialog(workflow=workflow)
            results = dialog.exec_()
            if results == 1:
                dialog.save_all()
                thread = GeometryThread()
                thread.trigger.connect(show_objects)  # connect to it's signal
                thread.setup(workflow, command=update_surface_3D_)  # just setting up a parameter
                thread.start()
                workflow.threads.append(thread)

        workflow.add_function_to_menu("Geometry", booms)
        workflow.add_function_to_menu("Geometry", lifting_surfaces)

    def setup_structures_menu():
        workflow.add_menu("Structures")

        def structures():
            dialog = structures_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()
        def show_internals():
            show_structure(workflow.viewer)
        workflow.add_function_to_menu("Structures", structures)
        workflow.add_function_to_menu("Structures", show_internals)
        func_ = get_functions(workflow)
        for l in func_:
            workflow.add_function_to_menu("Structures", l)
    def setup_cad_menu():
        workflow.add_menu("Cad")
        def localize_camera():
            workflow.viewer.localize_camera()
        def top_view():
            workflow.viewer.top_view()
        def side_view():
            workflow.viewer.side_view()
        def end_view():
            workflow.viewer.end_view()

        workflow.add_function_to_menu("Cad", localize_camera)
        workflow.add_function_to_menu("Cad", top_view)
        workflow.add_function_to_menu("Cad", side_view)
        workflow.add_function_to_menu("Cad", end_view)

    def setup_aerodynamics_menu():
        workflow.add_menu("Aerodynamics")

        def sandbox():
            pool = QThreadPool.globalInstance()
            runnable = AerodynamicThread(workflow,command=sandbox_)
            pool.start(runnable)

        def datcom():
            pool = QThreadPool.globalInstance()
            runnable = AerodynamicThread(workflow, command=datcom_)
            pool.start(runnable)

        def multisandbox():
            pool = QThreadPool.globalInstance()
            runnable = AerodynamicThread(workflow, command=start_multisandbox)
            pool.start(runnable)
        def plot_graphs():
            dialog = plotter_dialog()
            results = dialog.exec_()
        def show_tables():
            dialog = table_dialog()
            results = dialog.exec_()


        def settings():
            dialog = settings_dialog()
            results = dialog.exec_()
            if results == 1:
                dialog.tab.init_action()

        workflow.add_function_to_menu("Aerodynamics", sandbox)
        workflow.add_function_to_menu("Aerodynamics", datcom)
        workflow.add_function_to_menu("Aerodynamics", multisandbox)
        workflow.add_function_to_menu("Aerodynamics", plot_graphs)
        workflow.add_function_to_menu("Aerodynamics", show_tables)
        workflow.add_function_to_menu("Aerodynamics", settings)
    def setup_simulation_menu():
        workflow.add_menu("Simulation")
        def start_simulation():
            thread = ExportThread()
            thread.setup(workflow)  # just setting up a parameter
            thread.start()
            workflow.threads.append(thread)
        workflow.add_function_to_menu("Simulation",start_simulation)
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
    setup_cad_menu()
    setup_geometry_menu()
    setup_control_surface()
    setup_landing_gear()
    setup_structures_menu()
    setup_propulsion_menu()
    setup_aerodynamics_menu()
    setup_simulation_menu()
    setup_performance_menu()
