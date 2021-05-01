import logging

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import surface_curve_type, objects, unconventional_design
from Utils.database import database


def get_sweep_and_dihedral(part=""):
    values = database.read_aircraft_specifications()[part]
    sweep_ = values[part + "_sweep"]
    dihedral_ = values.get(part + "_dihedral")
    return sweep_, dihedral_


def read_root_position(part=""):
    values = database.read_aircraft_specifications()[part]
    root_location_x_ = values[part + "_root_position_x"]
    root_location_y_ = values.get(part + "_root_position_y")
    root_location_z_ = values.get(part + "_root_position_z")
    return root_location_x_, root_location_y_, root_location_z_


def read_lifting_surface_params(values):
    if values is None:
        values = {}
    rot_x_ = values[rotation_x]
    rot_y_ = values[rotation_y]
    rot_z_ = values[rotation_z]
    surfaceType_ = values.get(surface_curve_type)

    root_le_pos_x_ = values[root_le_position_x]
    root_le_pos_y_ = values[root_le_position_y]
    root_le_pos_z_ = values[root_le_position_z]

    xz_mirror_ = values.get(xz_mirror)
    xy_mirror_ = values.get(xy_mirror)
    yz_mirror_ = values.get(yz_mirror)

    section_1_chord_ = values[section_1_chord]
    section_1_x_ = values[section_1_x]
    section_1_y_ = values[section_1_y]
    section_1_z_ = values[section_1_z]
    section_1_twist_angle_ = values[section_1_twist_angle]

    section_2_chord_ = values[section_2_chord]
    section_2_x_ = values[section_2_x]
    section_2_y_ = values[section_2_y]
    section_2_z_ = values[section_2_z]
    section_2_twist_angle_ = values[section_2_twist_angle]

    section_3_chord_ = values[section_3_chord]
    section_3_x_ = values[section_3_x]
    section_3_y_ = values[section_3_y]
    section_3_z_ = values[section_3_z]
    section_3_twist_angle_ = values[section_3_twist_angle]

    section_4_chord_ = values[section_4_chord]
    section_4_x_ = values[section_4_x]
    section_4_y_ = values[section_4_y]
    section_4_z_ = values[section_4_z]
    section_4_twist_angle_ = values[section_4_twist_angle]

    section_5_chord_ = values[section_5_chord]
    section_5_x_ = values[section_5_x]
    section_5_y_ = values[section_5_y]
    section_5_z_ = values[section_5_z]
    section_5_twist_angle_ = values[section_5_twist_angle]
    return surfaceType_, xz_mirror_, xy_mirror_, yz_mirror_ \
        , rot_x_, rot_y_, rot_z_, root_le_pos_x_, \
           root_le_pos_y_, root_le_pos_z_, section_1_x_, section_2_x_, \
           section_3_x_, section_4_x_, section_5_x_, section_1_y_, \
           section_2_y_, section_3_y_, section_4_y_, section_5_y_, \
           section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_ \
        , section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
           section_5_chord_, section_1_twist_angle_, section_2_twist_angle_, \
           section_3_twist_angle_, section_4_twist_angle_, section_5_twist_angle_


def read_w_h_v(values,part=""):

    if values is None:
        values = {}

    root_location_x = values[root_le_position_x]
    root_location_y = values.get(root_le_position_y)
    root_location_z = values.get(root_le_position_z)
    chord_ = values.get(chord)
    dihedral_ = values.get(dihedral)
    sweep_ = values.get(sweep)
    twist_ = values.get(twist)
    span_ = values.get(span)
    taper_ratio_ = values.get(taper_ratio)
    profile_ = values.get(profile)

    if part.__contains__(wing):
        winglet_width_ = values.get(winglet_width)
        winglet_center_translation_x_ = values.get(winglet_center_translation_x)
        winglet_center_translation_y_ = values.get(winglet_center_translation_y)
        winglet_center_translation_z_ = values.get(winglet_center_translation_z)
        winglet_rotation_ = values.get(winglet_rotation)

        return root_location_x, root_location_y, root_location_z, dihedral_, sweep_, twist_, span_, taper_ratio_, chord_, winglet_width_, winglet_rotation_, winglet_center_translation_x_, winglet_center_translation_y_, winglet_center_translation_z_, profile_
    else:
        return root_location_x, root_location_y, root_location_z, dihedral_, sweep_, twist_, span_, taper_ratio_, chord_, profile_


def get_surface_object_data(boom_name_=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][boom_name_][design_type]
    part_type_ = values[objects][boom_name_][surface_type]
    return design_type_, part_type_


def read_surface_data(surface_name=""):
    values = database.read_aircraft_specifications()
    design_type_ = values[objects][surface_name][design_type]
    surface_type_ = values[objects][surface_name][surface_type]
    print(design_type_,surface_type_)
    if design_type_ == unconventional_design:
            return read_lifting_surface_params(values[lifting_surface][surface_name])
    else:
            return read_w_h_v(values[lifting_surface][surface_name],part=surface_type_)


def write_lifting_surface_to_objects(surface_name="", surface_type_="", design_type_=""):
    data = database.read_aircraft_specifications()
    try:
        val = data[objects]
        val[surface_name] = {surface_type: surface_type_, design_type: design_type_}
    except Exception as e:
        logging.error(e)
        data.update({objects: {surface_name: {surface_type: surface_type_, design_type: design_type_}}})
    database.write_aircraft_specification(data)


def delete_lifting_surface_from_objects(surface_name=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[objects]
        array.pop(surface_name)
        data[objects] = array
    except:
        pass
    database.write_aircraft_specification(data)


def write_lifting_surface_objects(value=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[lifting_surface_objects]
        if not array.__contains__(value):
            array.append(value)
        data[lifting_surface_objects] = array
    except Exception as e:

        data.update({lifting_surface_objects: [value]})
    database.write_aircraft_specification(data)


def read_lifting_surface_objects():
    data = database.read_aircraft_specifications()
    return data[lifting_surface_objects]


def delete_lifting_surface_objects(value=""):
    data = database.read_aircraft_specifications()
    try:
        array = data[lifting_surface_objects]
        array.remove(value)
        data[lifting_surface_objects] = array
    except:
        pass
    database.write_aircraft_specification(data)
