import os

import tigl3.configuration
from tigl3 import tigl3wrapper
from tixi3 import tixi3wrapper

import Helper


def show_structure(display):
    tixi_h = tixi3wrapper.Tixi3()
    tigl_h = tigl3wrapper.Tigl3()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    tixi_h.open(Helper.resource_path(Helper.absolute_path + "/resources/temp.xml"))
    tigl_h.open(tixi_h, "")

    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()

    config = mgr.get_configuration(tigl_h._handle.value)

    display_wing_cell_geom(config, display, 0.1, 0.8)


def display_wing_cell_geom(configuration, display, start_eta, end_eta):
    uid_mgr = configuration.get_uidmanager()
    wing = uid_mgr.get_geometric_component("Wing")

    componentSegment = wing.get_component_segment(1)
    structure = componentSegment.get_structure()
    ribStartPoint = structure.get_ribs_definition(1).get_ribs_positioning_choice1().get_start_curve_point_choice2()
    ribEndPoint = structure.get_ribs_definition(1).get_ribs_positioning_choice1().get_end_curve_point_choice2()
    ribEndPoint.set_eta(end_eta)
    ribStartPoint.set_eta(start_eta)
    structure.get_ribs_definition(1).get_ribs_positioning_choice1().set_end_curve_point(ribEndPoint)
    structure.get_ribs_definition(1).get_ribs_positioning_choice1().set_start_curve_point(ribStartPoint)

    display.add(wing.get_loft().shape(), transparency=0.7)

    # display cell geometry
    cell = uid_mgr.get_geometric_component("Wing_CS_upperShell_Cell1")
    display.add(cell.get_loft().shape(), transparency=0.3)

    # display ribs and spar

    rib1 = uid_mgr.get_geometric_component("Wing_CS_RibDef1")

    display.add(rib1.get_loft().shape(), color="blue")

    spar1 = uid_mgr.get_geometric_component("Wing_CS_spar1")
    display.add(spar1.get_loft().shape(), color="blue")

    spar2 = uid_mgr.get_geometric_component("Wing_CS_spar2")

    display.add(spar2.get_loft().shape(), color="green")

    spar3 = uid_mgr.get_geometric_component("Wing_CS_spar3")
    display.add(spar3.get_loft().shape(), color="blue")
