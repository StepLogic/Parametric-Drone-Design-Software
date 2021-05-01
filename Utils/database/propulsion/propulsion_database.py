import logging

#########GET PROPULSION PARAMETERS FROM JSON DATABASE##############
from Utils.data_objects.propulsion_keys import *
from Utils.database import database


def write_propulsion_parameters(data=None):
    if data is None:
        data = {}
    try:
        database.update_propulsion_specifications(key=propulsion, value=data[propulsion])
    except:
        database.write_propulsion_specifications(data)


def read_propulsion_parameters():
    values = database.read_propulsion_specifications()
    values = values[propulsion]
    voltage_ = values[voltage]
    max_thrust_ = values[max_thrust]
    battery_capacity_ = values[battery_capacity]
    discharge_rate_ = values[discharge_rate]
    max_current_ = values[max_current]
    return voltage_, max_thrust_, battery_capacity_, discharge_rate_, max_current_


def write_propeller_parameters(data):
    if data is None:
        data = {}
    try:
        database.update_propulsion_specifications(key=propeller, value=data[propeller])
    except:
        database.write_propulsion_specifications(data)


def write_propeller_objects(value=""):
    data = database.read_propulsion_specifications()
    try:
        array = data[propeller_objects]
        if not array.__contains__(value):
            array.append(value)
        data[propeller_objects] = array
    except Exception as e:
        logging.error(e)
        data.update({propeller_objects: [value]})
    database.write_propulsion_specifications(data)


def read_propeller_objects():
    data = database.read_propulsion_specifications()
    return data[propeller_objects]


def delete_propeller_objects(value=""):
    data = database.read_propulsion_specifications()
    try:
        array = data[propeller_objects]
        array.remove(value)
        data[propeller_objects] = array
    except:
        pass
    database.write_propulsion_specifications(data)


def read_propeller_parameters(name):
    values = database.read_propulsion_specifications()[propeller][name]
    if values is None:
        values = {}
    propeller_number_ = values[propeller_number]
    rot_x_ = values[rotation_x]
    rot_y_ = values[rotation_y]
    rot_z_ = values[pitch_angle]

    root_le_pos_x_ = values[hub_position_x]
    root_le_pos_y_ = values[hub_position_y]
    root_le_pos_z_ = values[hub_position_z]

    xz_mirror_ = values.get(xz_mirror)
    xy_mirror_ = values.get(xy_mirror)
    yz_mirror_ = values.get(yz_mirror)

    section_1_chord_ = values[section_1_chord]
    section_1_length_ = values[section_1_length]
    section_1_profile_ = values[section_1_profile]
    section_1_z_ = values[section_1_z]
    section_1_pitch_angle_ = values[section_1_pitch_angle]

    section_2_chord_ = values[section_2_chord]
    section_2_length_ = values[section_2_length]
    section_2_profile_ = values[section_2_profile]
    section_2_z_ = values[section_2_z]
    section_2_pitch_angle_ = values[section_2_pitch_angle]

    section_3_chord_ = values[section_3_chord]
    section_3_length_ = values[section_3_length]
    section_3_profile_ = values[section_3_profile]
    section_3_z_ = values[section_3_z]
    section_3_pitch_angle_ = values[section_3_pitch_angle]

    section_4_chord_ = values[section_4_chord]
    section_4_length_ = values[section_4_length]
    section_4_profile_ = values[section_4_profile]
    section_4_z_ = values[section_4_z]
    section_4_pitch_angle_ = values[section_4_pitch_angle]

    section_5_chord_ = values[section_5_chord]
    section_5_length_ = values[section_5_length]
    section_5_profile_ = values[section_5_profile]
    section_5_z_ = values[section_5_z]
    section_5_pitch_angle_ = values[section_5_pitch_angle]
    return propeller_number_, xz_mirror_, xy_mirror_, yz_mirror_ \
        , rot_x_, rot_y_, rot_z_, root_le_pos_x_, \
           root_le_pos_y_, root_le_pos_z_, section_1_length_, section_2_length_, \
           section_3_length_, section_4_length_, section_5_length_, section_1_profile_, \
           section_2_profile_, section_3_profile_, section_4_profile_, section_5_profile_, \
           section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_ \
        , section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
           section_5_chord_, section_1_pitch_angle_, section_2_pitch_angle_, \
           section_3_pitch_angle_, section_4_pitch_angle_, section_5_pitch_angle_


def read_shroud_parameters():
    values = database.read_propulsion_specifications()[propeller][shroud]
    if values is None:
        values = {}
    shroud_inner_diameter_ = values[shroud_inner_diameter]
    shroud_outer_diameter_ = values[shroud_outer_diameter]
    shroud_length_ = values[shroud_length]
    shroud_taper_ratio_ = values[shroud_taper_ratio]
    shroud_number_ = values[shroud_number]
    root_le_pos_x_ = values[hub_position_x]
    root_le_pos_y_ = values[hub_position_y]
    root_le_pos_z_ = values[hub_position_z]
    xz_mirror_ = values.get(xz_mirror)
    xy_mirror_ = values.get(xy_mirror)
    yz_mirror_ = values.get(yz_mirror)
    return shroud_length_, root_le_pos_x_, root_le_pos_y_, root_le_pos_z_, shroud_number_, shroud_taper_ratio_, shroud_inner_diameter_, shroud_outer_diameter_, xy_mirror_, xz_mirror_, yz_mirror_
