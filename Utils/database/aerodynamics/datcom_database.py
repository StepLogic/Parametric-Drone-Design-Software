import numpy as np

from Utils.data_objects.boom_placeholders import *
from Utils.data_objects.lifting_surface_placeholder import *
from Utils.database import database


divider=100

def get_area(width=0, height=0):
    return width * height


def get_parameters_from_unconventional_boom(boom_name=""):
    values = database.read_aircraft_specifications()[boom][boom_name]
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
    s = list(np.array([get_area(nose_width_,nose_height_),get_area(section_1_width_,section_1_height_),get_area(section_2_width_,section_2_height_)
         ,get_area(section_3_width_,section_3_height_),get_area(tail_width_,tail_height_)])/divider)
    x = list(np.array([nose_length_, sum([nose_length_, section_1_length_, section_2_length_]),
         sum([nose_length_, section_1_length_, section_2_length_, section_3_length_]),
         sum([nose_length_, section_1_length_, section_2_length_, section_3_length_, tail_length_])])/divider)
    return s,x


def get_parameters_from_conventional_boom(boom_name=""):
    values = database.read_aircraft_specifications()[boom][boom_name]
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
    radii = list(np.array([nose_radius_, section_1_radius_, section_2_radius_, section_3_radius_, tail_radius_])/divider)
    x = list(np.array([nose_length_, sum([nose_length_, section_1_length_, section_2_length_]),
         sum([nose_length_, section_1_length_, section_2_length_, section_3_length_]),
         sum([nose_length_, section_1_length_, section_2_length_, section_3_length_, tail_length_])])/divider)
    z = list(np.array([nose_position_z_, section_1_position_z_, section_2_position_z_, section_3_position_z_, tail_position_z_]) / 2000)
    return radii, x, z


def get_parameters_from_conventional_wing(surface_name=""):
    values = database.read_aircraft_specifications()[lifting_surface][surface_name]
    root_chord = values.get(chord)
    dihedral_ = values.get(dihedral)
    sweep_ = values.get(sweep)
    twist_ = values.get(twist)
    span_ = values.get(span)
    taper_ratio_ = values[taper_ratio]
    profile_ = values.get(profile)
    tip_chord = root_chord / taper_ratio_
    return span_/divider, tip_chord/divider, root_chord/divider, dihedral_, sweep_,profile_


def get_parameters_from_sections_lifting_surface(surface_name=""):
    values = database.read_aircraft_specifications()
    parameters = values[lifting_surface][surface_name]
    profile_=values[lifting_surface][surface_name]
    x_list = [parameters[section_1_x], parameters[section_2_x], parameters[section_3_x], parameters[section_4_x],
              parameters[section_5_x]]
    y_list = [parameters[section_1_y], parameters[section_2_y], parameters[section_3_y], parameters[section_4_y],
              parameters[section_5_y]]
    chords = [parameters[section_1_chord], parameters[section_2_chord], parameters[section_3_chord],
              parameters[section_4_chord], parameters[section_5_chord]]
    z_list = [[parameters[section_1_z], parameters[section_2_z], parameters[section_3_z],
               parameters[section_4_z], parameters[section_5_z]]]
    avg_chord = np.average(np.array(chords))
    y = np.array(y_list, dtype=float)
    z = np.array(z_list, dtype=float)
    x = np.array([0., 1., 1.5, 3.5, 4., 6.], dtype=float)
    dihedral_ = 0
    try:
        dihedral_ = np.arctan(max([np.gradient(z, y)]))
    except:
        pass
    sweep_ = max(np.arctan(np.gradient(y_list, x_list)))
    span_ = max(y_list)
    tip_chord = min(chords)
    root_chord = max(chords)
    return span_/divider, tip_chord/divider, root_chord/divider, dihedral_, sweep_,profile_
