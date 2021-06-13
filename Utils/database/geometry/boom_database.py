import logging

from Utils.data_objects.boom_placeholders import *
from Utils.data_objects.placeholder import objects, design_type, unconventional_design
from Utils.database import database


def read_boom_data(boom_name_=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][boom_name_][design_type]
    part = values[objects][boom_name_][boom_type]
    if design_type_ == unconventional_design:
            return read_boom_values(values[part][boom_name_])
    else:
            return read_fuselage_values(values["boom"][boom_name_])


def get_boom_object_data(boom_name_=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][boom_name_][design_type]
    boom_type_ = values[objects][boom_name_][boom_type]
    return design_type_, boom_type_


def write_boom_objects(value=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[boom_objects]
        if not array.__contains__(value):
            array.append(value)
        data[boom_objects] = array
    except:
        data.update({boom_objects: [value]})
    database.write_aircraft_specification(data)


def delete_boom_objects(value=""):
    data = database.read_aircraft_specifications()
    array = data[boom_objects]
    array.remove(value)
    data[boom_objects] = array
    print(database.read_aircraft_specifications())
    database.write_aircraft_specification(data)



def write_boom_to_objects(boom_name="", boom_type_="", design_type_=""):
    data = database.read_aircraft_specifications()
    try:
        val = data[objects]
        val[boom_name] = {boom_type: boom_type_, design_type: design_type_}
    except Exception as e:
        logging.error(e)
        data.update({objects: {boom_name: {boom_type: boom_type, design_type: design_type_}}})
    database.write_aircraft_specification(data)


def read_fuselage_values(values={}):
    fuselage_length = values.get("fuselage_length")
    fuselage_diameter = values.get("fuselage_diameter")

    nose_radius_ = values.get(nose_width)
    nose_length_ = values.get(nose_length)
    nose_position_z_ = values.get(nose_position_z)

    cockpit_height_ = values.get(cockpit_height)
    cockpit_length_ = values.get(cockpit_length)
    cockpit_width_ = values.get(cockpit_width)
    cockpit_position_x_ = values.get(cockpit_position_x)
    cockpit_position_y_ = values.get(cockpit_position_y)
    cockpit_position_z_ = values.get(cockpit_position_z)

    tail_tip_position_ = values.get(tail_tip_position)
    nose_tip_position_ = values.get(nose_tip_position)

    tail_radius_ = values.get(tail_width)
    tail_length_ = values.get(tail_length)
    tip_radius_ = values.get(tip_width)
    tail_position_z_ = values.get(tail_position_z)

    section_1_length_ = values.get(section_1_length)
    section_1_radius_ = values.get(section_1_width)
    section_1_position_z_ = values.get(section_1_position_z)

    section_2_radius_ = values.get(section_2_width)
    section_2_length_ = values.get(section_2_length)
    section_2_position_z_ = values.get(section_2_position_z)

    section_3_length_ = values.get(section_3_length)
    section_3_radius_ = values.get(section_3_width)
    section_3_position_z_ = values.get(section_3_position_z)
    return values[design_cockpit], nose_tip_position_, tail_tip_position_, \
           fuselage_diameter, fuselage_length, nose_radius_, \
           cockpit_height_, cockpit_length_, cockpit_width_, \
           cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, \
           nose_length_, nose_position_z_, section_1_radius_, \
           section_1_length_, section_1_position_z_, \
           section_2_radius_, section_2_length_, \
           section_2_position_z_, \
           section_3_radius_, \
           section_3_length_, \
           section_3_position_z_, \
           tip_radius_, tail_radius_, \
           tail_length_, tail_position_z_


def delete_boom_from_objects(surface_name=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[objects]
        array.pop(surface_name)
        data[objects] = array
    except:
        pass
    database.write_aircraft_specification(data)


def read_boom_values(values={}):
    fuselage_length = values.get(boom_length)
    fuselage_diameter = values.get(boom_diameter)
    root_position_x_ = values.get(root_position_x)
    root_position_y_ = values.get(root_position_y)
    root_position_z_ = values.get(root_position_z)

    nose_width_ = values.get(nose_width)
    nose_height_ = values.get(nose_height)
    nose_length_ = values.get(nose_length)
    nose_position_z_ = values.get(nose_position_z)

    xz_mirror_ = values.get(xz_mirror)
    xy_mirror_ = values.get(xy_mirror)
    yz_mirror_ = values.get(yz_mirror)

    cockpit_height_ = values.get(cockpit_height)
    cockpit_length_ = values.get(cockpit_length)
    cockpit_width_ = values.get(cockpit_width)
    cockpit_position_x_ = values.get(cockpit_position_x)
    cockpit_position_y_ = values.get(cockpit_position_y)
    cockpit_position_z_ = values.get(cockpit_position_z)

    tail_tip_position_ = values.get(tail_tip_position)
    nose_tip_position_ = values.get(nose_tip_position)

    tail_profile_ = values.get(tail_profile)
    nose_profile_ = values.get(nose_profile)
    section_1_profile_ = values.get(section_1_profile)
    section_2_profile_ = values.get(section_2_profile)
    section_3_profile_ = values.get(section_3_profile)


    tail_length_ = values.get(tail_length)
    tail_width_ = values.get(tail_width)
    tip_width_ = values.get(tip_width)
    tail_height_ = values.get(tail_height)
    tip_height_ = values.get(tip_height)
    tail_position_z_ = values.get(tail_position_z)

    section_1_length_ = values.get(section_1_length)
    section_1_width_ = values.get(section_1_width)
    section_1_height_ = values.get(section_1_height)
    section_1_position_z_ = values.get(section_1_position_z)

    section_2_width_ = values.get(section_2_width)
    section_2_height_ = values.get(section_2_height)
    section_2_length_ = values.get(section_2_length)
    section_2_position_z_ = values.get(section_2_position_z)

    section_3_length_ = values.get(section_3_length)
    section_3_width_ = values.get(section_3_width)
    section_3_height_ = values.get(section_3_height)
    section_3_position_z_ = values.get(section_3_position_z)
    return tail_profile_, nose_profile_, \
           section_1_profile_, section_2_profile_, \
           section_3_profile_, values[design_cockpit], xz_mirror_, xy_mirror_, yz_mirror_, \
           root_position_x_, root_position_y_, root_position_z_, \
           nose_tip_position_, tail_tip_position_, \
           fuselage_diameter, fuselage_length, nose_width_, nose_height_, \
           cockpit_height_, cockpit_length_, cockpit_width_, \
           cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, \
           nose_length_, nose_position_z_, section_1_width_, section_1_height_, \
           section_1_length_, section_1_position_z_, \
           section_2_width_, section_2_height_, section_2_length_, \
           section_2_position_z_, \
           section_3_width_, section_3_height_, \
           section_3_length_, \
           section_3_position_z_, \
           tip_width_,tail_height_, tail_width_,tip_height_, \
           tail_length_, tail_position_z_


def read_boom_objects():
    data = database.read_aircraft_specifications()
    print("reading_objects")
    return data[boom_objects]
