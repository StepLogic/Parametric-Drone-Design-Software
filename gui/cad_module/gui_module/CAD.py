import sys

import os

from PyQt5.QtWidgets import QMessageBox
import _thread
import concurrent.futures
import Helper
from analysis.aerodynamic_analysis.AerodyamicAnalyzer import run_analysis
from analysis.aerodynamic_analysis.Simulator import run_sandbox_simulation
from analysis.aerodynamic_analysis.analysis_module.AnalysisDialog import AnalysisDialog
from analysis.structural_analysis import StructuralAnalyzer
from analysis.structural_analysis.structure_module.StructureDialog import StructureDialog
from analysis.structural_analysis.structure_module.WeightDialog import WeightDialog
from gui.cad_module.control_surface_module.ControlSurfaceDialog import ControlSurfaceDialog
from gui.cad_module.engine_module.EngineDialog import EngineDialog
from gui.cad_module.fin_module.FinDialog import FinDialog
from gui.cad_module.fuselage_module.FuselageDialog import FuselageDialog
from gui.cad_module.gui_module import StructureView, Dialogs

from gui.cad_module.gui_module.Window import init_display
from gui.cad_module.landing_gear_module.LandingGearDialog import LandingGearDialog
from gui.cad_module.object_module import EngineObject, ControlSurfaceObject, LandingGearObject
from gui.cad_module.object_module.DrawObject import DrawObject
from gui.cad_module.object_module.FuselageObject import FuselageObject
from gui.cad_module.tailplane_module.TailPlaneDialog import TailPlaneDialog
from gui.cad_module.wing_module.WingDialog import WingDialog
from gui.report_module.PlotterModule import PlotterModule
from gui.report_module.TableModule import TableModule
from gui.report_module.TableReport import TableReport
from utils.Database import read_aircraft_specifications

from gui.report_module import Text_Report


class CAD:
    def __init__(self, configuration):
        self.geometry_done = False
        self.structures_done = False
        self.aerodynamics_done = False
        self.prev_fuse_loft = []
        self.prev_wing_loft = []
        self.prev_htp_loft = []
        self.prev_vtp_loft = []
        self.prev_engine_loft = []
        self.prev_aileron_loft = []
        self.prev_rudder_loft = []
        self.prev_elevator_loft = []
        self.prev_landing_gear_loft = []
        self.report_list = {}
        self.total_lofts = []
        self.fin_update = False
        self.engine_update = False
        self.landing_gear_update = False
        self.aircraft_specs = {}
        self.tail_update = False
        self.fuselage_update = False
        self.wing_update = False
        self.weight_update = False
        self.aileron_update = False
        self.rudder_update = False
        self.elevator_update = False
        self.wing_structure_update = False
        self.vtp_structure_update = False
        self.htp_structure_update = False
        self.aircraft = configuration
        self.viewer, self.display, self.start_display, self.add_menu, self.add_function_to_menu, self.add_sub_menu_to_menu, self.add_function_to_sub_menu, self.add_text_to_console = init_display(
            "qt-pyqt5")

    def switch_to_structure_view(self):
        self.display.EraseAll()
        StructureView.show_structure(self.viewer)

    def switch_to_normal_view(self):
        self.display.EraseAll()
        lofts = [self.prev_htp_loft, self.prev_vtp_loft, self.prev_fuse_loft, self.prev_wing_loft]
        for lofts_list in lofts:
            for loft in lofts_list:
                self.viewer.add(loft.shape)

    def run(self):
        self.add_text_to_console("Caution!! Enter All Inputs First")
        self.add_menu('File')
        self.add_function_to_menu('File', self.start_new_design)
        self.add_function_to_menu('File', self.export_model)
        self.add_function_to_menu('File', self.quit)
        self.add_menu('CAD')
        self.add_function_to_menu('CAD', self.top_view)
        self.add_function_to_menu('CAD', self.side_view)
        self.add_function_to_menu('CAD', self.end_view)
        self.add_function_to_menu('CAD', self.switch_to_normal_view)
        self.add_function_to_menu('CAD', self.switch_to_structure_view)
        self.add_menu('Geometry')
        self.add_function_to_menu('Geometry', self.build_or_modify_fuselage)
        self.add_function_to_menu('Geometry', self.build_or_modify_wing)
        self.add_function_to_menu('Geometry', self.build_or_modify_fin)
        self.add_function_to_menu('Geometry', self.build_or_modify_tail_plane)
        self.add_function_to_menu('Geometry', self.build_or_modify_engine)
        self.add_function_to_menu('Geometry', self.build_or_modify_landing_gear)
        self.add_sub_menu_to_menu('build or modify control surfaces', 'Geometry')
        self.add_function_to_menu('build or modify control surfaces', self.build_or_modify_aileron)
        self.add_function_to_menu('build or modify control surfaces', self.build_or_modify_elevator)
        self.add_function_to_menu('build or modify control surfaces', self.build_or_modify_rudder)

        self.add_menu('Structures')
        self.add_function_to_menu("Structures", self.weight_entry)
        self.add_function_to_menu("Structures", self.setup_wing_structure)
        self.add_function_to_menu("Structures", self.setup_fin_structure)
        self.add_function_to_menu("Structures", self.setup_tailplane_structure)
        self.add_function_to_menu("Structures", self.analyze_structure)
        self.add_function_to_menu('Structures', self.show_lumped_mass_distribution)
        self.add_menu('Aerodynamics')
        self.add_function_to_menu('Aerodynamics', self.vlm_multiple_analysis)
        self.add_function_to_menu('Aerodynamics', self.vortex_lattice_method)
        self.add_sub_menu_to_menu("show graphs", 'Aerodynamics')
        self.add_function_to_menu("show graphs", self.plot_cl_against_alpha)
        self.add_function_to_menu("show graphs", self.plot_cd_against_alpha)
        self.add_function_to_menu("show graphs", self.plot_cm_against_alpha)
        self.add_function_to_menu("show graphs", self.plot_cd_against_cl)
        self.add_function_to_menu("show graphs", self.plot_cy_against_beta)
        self.add_sub_menu_to_menu("show tables", 'Aerodynamics')
        self.add_function_to_menu("show tables", self.show_cm_against_alpha_table)
        self.add_function_to_menu("show tables", self.show_cl_against_alpha_table)
        self.add_function_to_menu("show tables", self.show_cd_against_alpha_table)
        self.add_function_to_menu("show tables", self.show_cy_against_beta_table)
        self.add_menu('Tools')
        self.add_function_to_menu('Tools', self.show_multiple_simulation_graph_results)
        self.add_function_to_menu('Tools', self.show_multiple_simulation_text_results)

        self.start_display()
    def show_cy_against_beta_table(self):
        tableReport = TableReport()
        tableReport.show_cy_against_beta_table()
    def show_cd_against_alpha_table(self):
        tableReport = TableReport()
        tableReport.show_cd_against_alpha_table()
    def show_cl_against_alpha_table(self):
        tableReport = TableReport()
        tableReport.show_cl_against_alpha_table()
    def show_cm_against_alpha_table(self):
        tableReport = TableReport()
        tableReport.show_cm_against_alpha_table()

    def setup_wing_structure(self):
        self.update()
        if self.geometry_done:
            ok, params = StructureDialog.get_params(part="wing")
            if ok:
                self.wing_structure_update = True

    def setup_fin_structure(self):
        self.update()
        if self.geometry_done:
            ok, params = StructureDialog.get_params(part="vtp")
            if ok:
                self.vtp_structure_update = True

    def setup_tailplane_structure(self):
        self.update()
        if self.geometry_done:
            ok, params = StructureDialog.get_params(part="htp")
            if ok:
                self.htp_structure_update = True

    def show_aerodynamic_plots(self):
        try:
            self.analyze_aircraft_for_results()
            plotter = PlotterModule()
            plotter.plot_common()
        except Exception:
            Dialogs.show_warning("Not All Inputs Are Available Enter or Check Values")

    def show_lumped_mass_distribution(self):
        try:
            if self.geometry_done and self.weight_update:
                x, y, z = StructuralAnalyzer.estimate_aircraft_structure()
                PlotterModule.plot_scatter_3D(x, y, z)
        except Exception:
            Dialogs.show_warning("Not All Inputs Are Available Enter or Check Values")

    def analyze_structure(self):
        self.update()
        if self.geometry_done and self.weight_update:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                thread = executor.submit(StructuralAnalyzer.estimate_aircraft_structure)
                x, y, z, val = thread.result()
                val = val["Inertia"]

            info = "Results For Simulation\nCG_x={}\nCG_y={}\nCG_z={}\nIxx={}\nIyy={}\nIzz={}\nIxz={}".format(
                val["cg_x"],
                val["cg_y"],
                val["cg_z"],
                val["Ixx"],
                val["Iyy"],
                val["Izz"],
                val["Ixz"]
            )
            Dialogs.show_results(info)

    def analyze_aircraft_for_results(self):
        self.update()
        if self.geometry_done and self.weight_update and self.structures_done:
            _thread.start_new_thread(run_sandbox_simulation, ())
            _thread.start_new_thread(StructuralAnalyzer.estimate_aircraft_structure, ())
        else:
            Dialogs.show_warning("Not All Inputs Are Available Enter or Check Values")

    def build_or_modify_wing(self):
        params, ok = WingDialog.get_Wing_Params()

        if (ok):
            wing_object = DrawObject(params, self.aircraft, self.viewer, self.wing_update, "main")
            temp_var = wing_object._display_lofts(prev_loft=self.prev_wing_loft, cut_update=self.aileron_update,
                                                  cut_loft=self.prev_aileron_loft)
            self.add_text_to_console("Wing Parameters Captured!!")
            self.prev_wing_loft = temp_var
            self.aileron_update = False
            if self.wing_update:
                pass
            else:
                self.wing_update = True
        else:
            pass

    def build_or_modify_landing_gear(self):
        params, ok = LandingGearDialog.get_params()

        if ok:
            self.prev_landing_gear_loft = LandingGearObject.get_landing_gear_loft(params=params, display=self.viewer,
                                                                                  update=self.landing_gear_update,
                                                                                  prev_loft=self.prev_landing_gear_loft)
            if self.landing_gear_update:
                pass
            else:
                self.landing_gear_update = True

        else:
            pass

    def build_or_modify_engine(self):
        params, ok = EngineDialog.get_params()

        if ok:

            self.prev_engine_loft = EngineObject.get_engine_loft(params=params, display=self.viewer,
                                                                 update=self.engine_update,
                                                                 prev_loft=self.prev_engine_loft)
            if self.engine_update:
                pass
            else:
                self.engine_update = True
        else:
            pass

    def build_or_modify_fin(self):

        params, ok = FinDialog.get_params()

        if ok:
            fin_object = DrawObject(params, self.aircraft, self.viewer, self.fin_update, "vtp")
            temp_var = fin_object._display_lofts(prev_loft=self.prev_vtp_loft, cut_update=self.rudder_update,
                                                 cut_loft=self.prev_rudder_loft)
            self.rudder_update = False
            self.prev_vtp_loft = temp_var

            if self.fin_update:
                pass
            else:
                self.fin_update = True
        else:
            pass

    def build_or_modify_tail_plane(self):
        params, ok = TailPlaneDialog.get_params()
        if (ok):
            tailplane_object = DrawObject(params, self.aircraft, self.viewer, self.tail_update, "htp")
            temp_var = tailplane_object._display_lofts(prev_loft=self.prev_htp_loft, cut_update=self.elevator_update,
                                                       cut_loft=self.prev_elevator_loft)
            self.elevator_update = False
            self.prev_htp_loft = temp_var
            if self.tail_update:
                pass
            else:
                self.tail_update = True

        else:
            pass

    def build_or_modify_fuselage(self):
        params, ok = FuselageDialog.get_params()
        if (ok):
            Fuselage_object = FuselageObject(params, self.aircraft, self.viewer, self.fuselage_update)
            temp_var = Fuselage_object._display_lofts(self.prev_fuse_loft)
            self.prev_fuse_loft = temp_var

            if self.fuselage_update:
                pass
            else:
                self.fuselage_update = True

        else:
            pass

    def build_or_modify_aileron(self):
        part = "aileron"
        params, ok = ControlSurfaceDialog.get_params(part=part)

        if ok and self.wing_update:
            self.prev_aileron_loft = ControlSurfaceObject.draw_control_surface(display=self.viewer, params=params,
                                                                               part=part,
                                                                               prev_wing_loft=self.prev_wing_loft,
                                                                               prev_cs_loft=self.prev_aileron_loft,
                                                                               update=self.aileron_update)

            if self.aileron_update:
                pass
            else:
                self.aileron_update = True
        else:
            pass

    def build_or_modify_rudder(self):
        part = "rudder"
        params, ok = ControlSurfaceDialog.get_params(part=part)

        if ok and self.fin_update:
            self.prev_rudder_loft = ControlSurfaceObject.draw_control_surface(display=self.viewer, params=params,
                                                                              part=part,
                                                                              prev_wing_loft=self.prev_vtp_loft,
                                                                              prev_cs_loft=self.prev_rudder_loft,
                                                                              update=self.rudder_update)

            if self.rudder_update:
                pass
            else:
                self.rudder_update = True
        else:
            pass

    def build_or_modify_elevator(self):
        part = "elevator"
        params, ok = ControlSurfaceDialog.get_params(part=part)

        if ok and self.tail_update:
            self.prev_elevator_loft = ControlSurfaceObject.draw_control_surface(display=self.viewer, params=params,
                                                                                part=part,
                                                                                prev_wing_loft=self.prev_htp_loft,
                                                                                prev_cs_loft=self.prev_elevator_loft,
                                                                                update=self.elevator_update)

            if self.elevator_update:
                pass
            else:
                self.elevator_update = True
        else:
            pass

    def top_view(self):
        self.viewer._display.View.SetProj(0, 0, 1)
        self.viewer._display.View.SetScale(90)

    def side_view(self):
        self.viewer._display.View.SetProj(0, -1, 0)
        self.viewer._display.View.SetScale(90)

    def end_view(self):
        self.viewer._display.View.SetProj(-1, 0, 0)
        self.viewer._display.View.SetScale(90)

    def start_new_design(self):
        self.display.EraseAll()

    def quit(self):
        sys.exit()

    def vortex_lattice_method(self):
        self.update()
        if self.structures_done and self.geometry_done:
            params, ok = AnalysisDialog.get_params()
            if ok:
                try:
                    values = read_aircraft_specifications()
                    alpha = params["parameter"]["alpha"]
                    beta = params["parameter"]["beta"]
                    velocity = params["parameter"]["velocity"]
                    fast_track = False
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        thread = executor.submit(run_analysis, values, alpha, beta, velocity, fast_track)
                        val = thread.result()
                    info = "Results For Simulation\nCl={}\nCm={}\nCn={}\nCL={}\nCD={}\nCY={}".format(val["Cl"],
                                                                                                     val["Cm"],
                                                                                                     val["Cn"],
                                                                                                     val["CL"],
                                                                                                     val["CD"],
                                                                                                     val["CY"]
                                                                                                     )
                    Dialogs.show_results(info)

                except Exception:
                    pass

    def fly_model(self):
        self.update()
        if self.structures_done and self.geometry_done:
            self.export_model()
            command = "python flight.py run".format(os.path.abspath(__file__))
            os.system("python flight.py run")

    def export_model(self):
        if self.fin_update and self.tail_update and self.fuselage_update and self.wing_update:
            _thread.start_new_thread(self.save_model, ())

    def weight_entry(self):
        ok, params = WeightDialog.get_params()
        if ok:
            self.weight_update = True

    def vlm_multiple_analysis(self):
        self.update()

        _thread.start_new_thread(run_sandbox_simulation, ())

    def show_multiple_simulation_graph_results(self):
        self.update()
        if self.structures_done and self.geometry_done:
            pl = PlotterModule()

    def plot_cl_against_alpha(self):
        pl = PlotterModule()
        pl.plot_cl_against_alpha()

    def plot_cd_against_cl(self):
        pl = PlotterModule()
        pl.plot_cd_against_cl()

    def plot_cy_against_p(self):
        pl = PlotterModule()
        pl.plot_cy_against_p()

    def plot_cy_against_alpha(self):
        pl = PlotterModule()
        pl.plot_cy_against_alpha()

    def plot_cl_roll_against_aileron_deflection(self):
        pl = PlotterModule()
        pl.plot_cl_roll_against_aileron_deflection()

    def plot_cl_roll_against_beta(self):
        pl = PlotterModule()
        pl.plot_cl_roll_against_beta()

    def plot_cl_roll_against_p(self):
        pl = PlotterModule()
        pl.plot_cl_roll_against_p()

    def plot_cl_roll_against_r(self):
        pl = PlotterModule()
        pl.plot_cl_roll_against_r()

    def plot_cm_against_q(self):
        pl = PlotterModule()
        pl.plot_cm_against_q()

    def plot_cm_against_elevator_deflection(self):
        pl = PlotterModule()
        pl.plot_cm_against_elevator_deflection()

    def plot_cn_against_beta(self):
        pl = PlotterModule()
        pl.plot_cn_against_beta()

    def plot_cn_against_r(self):
        pl = PlotterModule()
        pl.plot_cn_against_r()

    def plot_cm_against_alpha(self):
        pl = PlotterModule()
        pl.plot_cm_against_alpha()

    def plot_cy_against_beta(self):
        pl = PlotterModule()
        pl.plot_cy_against_beta()

    def plot_cd_against_alpha(self):
        pl = PlotterModule()
        pl.plot_cd_against_alpha()

    def plot_cd_against_aileron_deflection(self):
        pl = PlotterModule()
        pl.plot_cd_against_aileron_deflection()

    def show_multiple_simulation_text_results(self):
        self.update()
        if self.structures_done and self.geometry_done:
            text = Text_Report()
            text.exec()

    def save_model(self):
        lofts = [self.prev_htp_loft, self.prev_vtp_loft, self.prev_fuse_loft, self.prev_wing_loft,
                 self.prev_engine_loft, self.prev_landing_gear_loft, self.prev_aileron_loft, self.prev_elevator_loft,
                 self.prev_rudder_loft]
        if self.fin_update and self.tail_update and self.fuselage_update and self.wing_update:
            from OCC.StlAPI import StlAPI_Writer

            stl_writer = StlAPI_Writer()
            stl_writer.SetASCIIMode(True)
            for lofts in lofts:
                for loft in lofts:
                    stl_writer.Write(loft.shape(), "model.stl")

            os.system("meshio-convert model.stl model.obj ")

            os.replace("model.obj",
                       Helper.resource_path(Helper.absolute_path + "/resources/results/3D/model.obj"))
            os.replace("model.stl",
                       Helper.resource_path(Helper.absolute_path + "/resources/results/3D/model.stl"))



        else:
            dialog = QMessageBox()
            dialog.setIcon(QMessageBox.Critical)
            dialog.setText("Missing Parts")
            dialog.addButton(QMessageBox.Ok)
            dialog.exec()

    def update(self):
        if self.wing_structure_update and self.vtp_structure_update and self.htp_structure_update and self.weight_update:
            self.structures_done = True

        if self.fin_update and self.tail_update and self.fuselage_update and self.wing_update:
            self.geometry_done = True
