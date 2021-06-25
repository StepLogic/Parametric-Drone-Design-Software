import sys

import tigl3.configuration
import tigl3.tigl3wrapper
import tixi3.tixi3wrapper
from PyQt5.QtWidgets import QMessageBox

from Aerodynamics.sandbox.multi_sandbox import run_sandbox_simulation
from Geometry.control_surface.control_surface_model import control_surface_model
from Geometry.conventional.fuselage_model.fuselage_model import fuselage_model
from Geometry.conventional.h_stab_model.h_stab_model import h_stab_model
from Geometry.conventional.v_stab_model.v_stab_model import v_stab_model
from Geometry.conventional.wing_model.wing_model import wing_model
from Geometry.landing.landing_gear_model import landing_gear_model
from Geometry.propulsion.propeller_model import propeller_model
from Geometry.propulsion.shroud_model import shroud_model
from Geometry.unconventional.boom.boom_model import boom_model
from Geometry.unconventional.lifting_surface.lifting_surface_model import lifting_surface_model
from Utils.data_objects.boom_placeholders import fuselage, boom
from Utils.data_objects.landing_gear_key import landing_gear
from Utils.data_objects.lifting_surface_placeholder import fin, wing, tailplane
from Utils.data_objects.placeholder import conventional_design
from Utils.data_objects.placeholder import unconventional_design
from Utils.data_objects.propulsion_keys import shroud
from Utils.data_objects.workflow_placeholders import *
from Utils.database.database import resource_dir_cpacs
from Utils.database.geometry.boom_database import get_boom_object_data, read_boom_objects
from Utils.database.geometry.control_surface_database import read_control_surface_objects, get_parent_name
from Utils.database.geometry.lifting_database import read_lifting_surface_objects, get_surface_object_data
from Utils.database.propulsion.propulsion_database import read_propeller_objects


def start(e, receiveTasks, sendLofts):
    filename = resource_dir_cpacs + "/empty.cpacs3.xml"
    tixi_h = tixi3.tixi3wrapper.Tixi3()
    tixi_h.open(filename)
    tigl_h = tigl3.tigl3wrapper.Tigl3()
    tigl_h.open(tixi_h, "")
    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
    config = mgr.get_configuration(tigl_h._handle.value)
    while 1:
        e.wait()
        res = receiveTasks.recv()
        command = res[0]
        if command == datcom_:
            from Aerodynamics.datcom.datcom import run_datcom
            run_datcom()
            sendLofts.send(done)
        elif command == sandbox_:
            from Aerodynamics.sandbox.sandbox import run_analysis
            run_analysis()
            sendLofts.send(done)
        elif command == shutdown_:
            sys.exit()
        elif command == update_boom_3D_:
            sendLofts.send(update_boom_3d(config=config))  # pass workflow monitor
        elif command == update_surface_3D_:
            sendLofts.send(update_surface_3d(config=config))
        if command == build_cs:
            sendLofts.send(generate_control_surfaces(config=config))
        elif command == build_landing_gear:
            sendLofts.send(update_landing_gear())
        elif command == start_multisandbox:
            run_sandbox_simulation()
            sendLofts.send(done)
        elif command == build_shroud:
            sendLofts.send({shroud: shroud_model(config=config).get_current_loft()})
        elif command == build_propeller:
            sendLofts.send(update_propeller(config=config))


def update_propeller(config=None):
    loft = {}
    propeller_list = read_propeller_objects()
    for l in propeller_list:
        loft.update({l: propeller_model(name=l, config=config).get_current_loft()})
    return loft


def update_landing_gear():
    return {landing_gear: landing_gear_model().get_current_loft()}


def update_control_surfaces(config=None, res=None):
    if res is None:
        res = []
    lofts = {}
    surface_list = read_control_surface_objects()
    loft_table = res[1]

    for surface in surface_list:
        for name, loft in loft_table.items():
            if name == get_parent_name(surface):
                lofts.update(
                    {name: control_surface_model(name=surface, config=config, part_loft=loft).get_current_loft()})

    return lofts


def generate_control_surfaces(config=None):
    lofts = {}
    try:
        surface_list = read_control_surface_objects()
        for surface in surface_list:
            lofts.update(control_surface_model(name=surface, config=config, part_loft=None).get_surface_loft())

    except:
        pass
    try:
        surface_list = read_control_surface_objects()
        loft_table = update_surface_3d(config)
        for surface in surface_list:
            for name, loft in loft_table.items():
                if name == get_parent_name(surface):
                    lofts.update(
                        {name: control_surface_model(name=surface, config=config, part_loft=loft).get_wing_loft()})
    except:
        lofts = update_surface_3d(config)
    return lofts


def update_boom_3d(config=None):
    boom_list = read_boom_objects()
    lofts = {}
    for l in boom_list:
        design_type_, boom_type_ = get_boom_object_data(l)
        print(l)
        lofts.update({l: generate_boom_3D_model(config, name=l, boom_type_=boom_type_, design_type_=design_type_)})
    return lofts


def export_files(config=None):
    loft={}
    try:
     booms =update_boom_3d(config=config)
     loft.update(booms)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Error")
        msg.setInformativeText("ERROR! Exporting Boom")
        msg.setWindowTitle("Aerosoft")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    try:
     wing =generate_control_surfaces(config=config)
     loft.update(wing)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Error")
        msg.setInformativeText("ERROR! Exporting Wing")
        msg.setWindowTitle("Aerosoft")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    return loft


def update_surface_3d(config=None):
    surface_list = read_lifting_surface_objects()
    lofts = {}
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        lofts.update({l: generate_wing_3D(config, l, surface_type_, design_type_)})
    return lofts


def generate_boom_3D_model(config=None, name="", boom_type_="", design_type_=""):
    if design_type_ == conventional_design:
        return fuselage_model(config=config, text=name,
                              boom_type_=boom_type_,
                              design_type_=design_type_).get_current_loft()
    elif design_type_ == unconventional_design:
        return boom_model(config=config, text=name,
                          boom_type_=boom_type_,
                          design_type_=design_type_).get_current_loft()


def generate_wing_3D(config=None, name="", surface_type_="", design_type_=""):
    if surface_type_ == fin and design_type_ == conventional_design:
        return v_stab_model(config=config, name=name,
                            surface_type_=surface_type_,
                            design_type_=design_type_).get_current_loft()
    elif surface_type_ == fin and design_type_ == unconventional_design:
        return lifting_surface_model(config=config, name=name,
                                     surface_type_=surface_type_,
                                     design_type_=design_type_).get_current_loft()
    elif surface_type_ == wing and design_type_ == conventional_design:
        return wing_model(config=config, name=name,
                          surface_type_=surface_type_,
                          design_type_=design_type_).get_current_loft()
    elif surface_type_ == wing and design_type_ == unconventional_design:
        return lifting_surface_model(config=config, name=name,
                                     surface_type_=surface_type_,
                                     design_type_=design_type_).get_current_loft()
    elif surface_type_ == tailplane and design_type_ == conventional_design:
        return h_stab_model(config=config, name=name,
                            surface_type_=surface_type_,
                            design_type_=design_type_).get_current_loft()
    elif surface_type_ == tailplane and design_type_ == unconventional_design:
        return lifting_surface_model(config=config, name=name,
                                     surface_type_=surface_type_,
                                     design_type_=design_type_).get_current_loft()


def update_surface_lower_3d(config=None):
    surface_list = read_lifting_surface_objects()
    lofts = {}
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        lofts.update({l: generate_wing_lower_3D(config, l, surface_type_, design_type_)})
    return lofts


def generate_wing_lower_3D(config=None, name="", surface_type_="", design_type_=""):
    if surface_type_ == wing and design_type_ == unconventional_design:
        return lifting_surface_model(config=config, name=name,
                                     surface_type_=surface_type_,
                                     design_type_=design_type_).get_lower_surface()
