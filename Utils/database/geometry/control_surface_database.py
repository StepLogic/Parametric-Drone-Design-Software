import logging

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import objects, unconventional_design
from Utils.database import database


def get_parent_name(surface_name = ""):
    values = database.read_aircraft_specifications()[control_surface][surface_name]
    return values.get(parent_)


def get_surface_type(surface_name = ""):
    _type=""
    values = get_parent_name(surface_name)
    surface_type_=database.read_aircraft_specifications()[values][surface_type]
    if surface_type_==wing:
        _type=aileron_
    elif surface_type_==tailplane:
        _type=elevator_
    elif surface_type_==fin:
        _type=rudder_

    return _type



def read_parent_data(surface_name="",key=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][surface_name][design_type]
    surface_type_ = values[objects][surface_name][surface_type]
    if design_type_ == unconventional_design:
            return values[lifting_surface][surface_name][key]

    else:
            return values[lifting_surface][surface_name][key]


def get_surface_object_data(boom_name_=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][boom_name_][design_type]
    part_type_ = values[objects][boom_name_][surface_type]
    return design_type_, part_type_


def read_surface_data(surface_name=""):
    values=database.read_aircraft_specifications()[control_surface][surface_name]
    root_location_x_ = values.get(root_le_position_x)
    root_location_y_ = values.get(root_le_position_y)
    root_location_z_ = values.get(root_le_position_z)
    rot_x_ = values.get(rotation_x)
    rot_y_ = values.get(rotation_y)
    rot_z_ = values.get(rotation_z)
    parent__=values.get(parent_)
    span_ = values.get(span)
    chord_ = values.get(chord)
    return root_location_x_, root_location_y_, root_location_z_, rot_x_, rot_y_, rot_z_, span_, chord_,parent__




def write_control_surface_to_objects(surface_name="",parent__=""):
    data = database.read_aircraft_specifications()
    try:
        val = data[objects]
        val[surface_name] = {surface_name: {parent_:parent__}}
    except Exception as e:
        logging.error(e)
        data.update({objects: {surface_name: {parent_:parent__}}})
    database.write_aircraft_specification(data)


def delete_control_surface_from_objects(surface_name=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[objects]
        array.pop(surface_name)
        data[objects] = array
    except:
        pass
    database.write_aircraft_specification(data)


def write_control_surface_objects(value=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[control_surface_objects]
        if not array.__contains__(value):
            array.append(value)
        data[control_surface_objects] = array
    except Exception as e:

        data.update({control_surface_objects: [value]})
    database.write_aircraft_specification(data)


def read_control_surface_objects():
    data = database.read_aircraft_specifications()
    return data[control_surface_objects]


def delete_control_surface_objects(value=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[control_surface_objects]
        array.remove(value)
        data[control_surface_objects] = array
    except:
        pass
    database.write_aircraft_specification(data)
