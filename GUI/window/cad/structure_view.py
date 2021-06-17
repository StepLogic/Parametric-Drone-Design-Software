import os

import tigl3.configuration
from tigl3 import tigl3wrapper
from tixi3 import tixi3wrapper

import Helper
from GUI.workflow.design_workflow import update_surface_lower_3d
from Utils.database.database import resource_dir_cpacs


def show_structure(display):
    display_wing_cell_geom(display, 0.1, 0.8)


def display_wing_cell_geom(display, start_eta, end_eta):
    display.eraseAll()
    tixi_h = tixi3wrapper.Tixi3()
    tigl_h = tigl3wrapper.Tigl3()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    tixi_h.open(resource_dir_cpacs + "/temp.xml")
    tigl_h.open(tixi_h, "")
    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
    config = mgr.get_configuration(tigl_h._handle.value)
    lifting_surfaces=update_surface_lower_3d(config)
    for part ,loft in lifting_surfaces.items():
        display.add(loft,color="blue" ,transparency=0.8)
def create_rib(uid_mgr):
    ribDef= tigl3.configuration.CPACSWingRibsDefinition(uid_mgr)