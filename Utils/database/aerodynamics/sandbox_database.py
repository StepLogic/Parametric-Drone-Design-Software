import numpy as np
import pandas
from scipy.interpolate import interp1d

from Utils.data_objects.boom_placeholders import *
from Utils.data_objects.lifting_surface_placeholder import fin, tailplane
from Utils.database import database
from Utils.database.aerodynamics.settings_database import get_mach_number
from Utils.database.geometry.lifting_database import read_surface_data
divider=100

def get_parameters_for_fuselage(fuselage_name=''):
    values = database.read_aircraft_specifications()[boom][fuselage_name]
    fuselage_length = values.get("fuselage_length")
    fuselage_diameter = values.get("fuselage_diameter")
    root_position_x_ = 0
    root_position_y_ = 0
    root_position_z_ = 0

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
    radii =list(np.array([0, nose_radius_, section_1_radius_, section_2_radius_, section_3_radius_, tail_radius_, tip_radius_])/divider)
    z = list(np.array([nose_tip_position_, nose_position_z_, section_1_position_z_, section_2_position_z_, section_3_position_z_,
         tail_position_z_,
         tail_tip_position_])/divider)
    length_ = list(np.array([0, nose_length_, section_1_length_, section_2_length_, section_3_length_, tail_length_ / 2, tail_length_])/divider)
    temp = []
    x = []
    for x_ in length_:
        temp.append(x_)
        x.append(sum(temp))
    xz_mirror_ = False
    x=list(np.array(x)/divider)
    return radii, x, z, root_position_x_, root_position_y_, root_position_z_, xz_mirror_


def get_parameters_for_boom(boom_name=""):
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

    height_ = [0, nose_height_, section_1_height_, section_2_height_, section_3_height_, tail_height_, tip_height_]
    width_ = [0, nose_width_, section_1_width_, section_2_width_, section_3_width_, tail_width_, tip_width_]
    length_ = [0, nose_length_, section_1_length_, section_2_length_, section_3_length_, tail_length_ / 2, tail_length_]
    z = [nose_tip_position_, nose_position_z_, section_1_position_z_, section_2_position_z_, section_3_position_z_,
         tail_position_z_,
         tail_tip_position_]
    radii = []
    x = []
    for w, h in zip(width_, height_):
        radii.append(np.hypot(w, h))
    temp = []
    for x_ in length_:
        temp.append(x_)
        x.append(sum(temp))
    x__ = np.linspace(min(x), max(x), 8)
    radii_f = interp1d(x, radii, kind="cubic")
    radii__ = radii_f(x__)
    z_f = interp1d(x, z, kind="cubic")
    z__ = z_f(x__)
    print("radii__", radii__, "x__", x__, "z__", z__)
    return list(np.array(radii__)/divider), list(np.array(x__)/divider),list(np.array(z__)/divider), root_position_x_/divider, root_position_y_/divider, root_position_z_/divider, xz_mirror_


def get_parameters_for_conventional(surface_name="", part=""):
    x = []
    y = []
    z = []
    x_1 = []
    z_1 = []
    chords = []
    twist = []
    interval = 5

    if part == fin:
        root_location_x, root_location_y, root_location_z, \
        dihedral_, sweep_, twist_, span_, taper_ratio_, chord_, profile_ = read_surface_data(surface_name)
        y.extend(list(np.linspace(0, span_, interval)))
        x.extend(list(np.linspace(0, (span_ * (np.tan(90 + sweep_))), interval)))
        z.extend(list(np.linspace(0, (span_ * (np.tan(dihedral_))), interval)))
        for x_, z_ in zip(x, z):
            x_1.append(0 if np.isnan(x_) or np.isinf(x_) else x_)
            z_1.append(0 if np.isnan(z_) or np.isinf(z_) else z_)

        chords.extend(list(np.linspace(chord_ / taper_ratio_, chord_, interval)))
        chords.reverse()


    elif part == tailplane:
        root_location_x, root_location_y, root_location_z, \
        dihedral_, sweep_, twist_, span_, taper_ratio_, chord_, profile_ = read_surface_data(surface_name)
        y.extend(list(np.linspace(0, span_, interval)))
        x.extend(list(np.linspace(0, (span_ * (np.tan(sweep_))), interval)))
        z.extend(list(np.linspace(0, (span_ * (np.tan(dihedral_))), interval)))
        for x_, z_ in zip(x, z):
            x_1.append(0 if np.isnan(x_) or np.isinf(x_) else x_)
            z_1.append(0 if np.isnan(z_) or np.isinf(z_) else z_)
        chords.extend(list(np.linspace(chord_ / taper_ratio_, chord_, interval)))
        chords.reverse()
    else:
        root_location_x, root_location_y, root_location_z, \
        dihedral_, sweep_, twist_, span_, taper_ratio_, chord_, \
        winglet_width_, winglet_rotation_, winglet_center_translation_x_, \
        winglet_center_translation_y_, winglet_center_translation_z_, profile_ = read_surface_data(surface_name)

        a = pandas.Series(list(np.linspace(0, span_, interval)))
        a.interpolate(method="polynomial", order=2)
        y.extend(a.to_list())
        a = pandas.Series(list(np.linspace(0, (span_ * (np.tan(-sweep_))), interval)))
        a.interpolate(method="polynomial", order=2)
        x.extend(a.to_list())
        a = pandas.Series(list(np.linspace(0, (span_ * (np.tan(dihedral_))), interval)))
        a.interpolate(method="polynomial", order=2)
        z.extend(a.to_list())

        for x_, z_ in zip(x, z):
            x_1.append(0 if np.isnan(x_) or np.isinf(x_) else x_)
            z_1.append(0 if np.isnan(z_) or np.isinf(z_) else z_)

        a = pandas.Series(list(np.linspace(chord_ / taper_ratio_, chord_, interval)))
        a.interpolate(method="polynomial", order=2)
        chords.extend(a.to_list())
        chords.reverse()
    return list(np.array(x_1)/divider), list(np.array(y)/divider), list(np.array(z_1)/divider),list(np.array(chords)/divider), twist_, profile_,root_location_x/divider,root_location_y/divider, root_location_z/divider


def get_parameters_for_unconventional(surface_name="", part=""):
    airfoil,surfaceType_, xz_mirror_, xy_mirror_, yz_mirror_ \
        , rot_x_, rot_y_, rot_z_, root_le_pos_x_, \
    root_le_pos_y_, root_le_pos_z_, section_1_x_, section_2_x_, \
    section_3_x_, section_4_x_, section_5_x_, section_1_y_, \
    section_2_y_, section_3_y_, section_4_y_, section_5_y_, \
    section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_ \
        , section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
    section_5_chord_, section_1_twist_angle_, section_2_twist_angle_, \
    section_3_twist_angle_, section_4_twist_angle_, section_5_twist_angle_ = read_surface_data(
        surface_name=surface_name)

    x_1 = [section_1_x_, section_2_x_, section_3_x_, section_4_x_, section_5_x_]
    y_1 = [section_1_y_, section_2_y_, section_3_y_, section_4_y_, section_5_y_]
    z_1 = [section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_]
    chords = [section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, section_5_chord_]
    twist_angle = [int(section_1_twist_angle_),
                   int(section_2_twist_angle_),
                   int(section_3_twist_angle_),
                   int(section_4_twist_angle_),
                   int(section_5_twist_angle_)]
    y__ = np.linspace(min(y_1), max(y_1), 10)
    x_f = interp1d(y_1, x_1, kind="cubic")
    x__ = x_f(y__)
    z_f = interp1d(y_1, z_1, kind="cubic")
    z__ = z_f(y__)
    chords_f = interp1d(y_1, chords, kind="cubic")
    chords__ = chords_f(y__)
    twist_angle_f = interp1d(y_1, twist_angle, kind="cubic")
    twist_angle__ = twist_angle_f(y__)
    x = []
    y = []
    z = []
    profile_ = "0012"

    from scipy.spatial.transform import Rotation as R
    r = R.from_euler('zyx', [rot_z_, rot_y_, rot_x_], degrees=True)
    for x_, y_, z_ in zip(x__, y__, z__):
        point = list(r.apply([z_, y_, x_]))
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])

    return list(np.array(x)/divider),list(np.array(y)/divider),list(np.array(z)/divider),list(np.array(chords)/divider), twist_angle__, profile_, root_le_pos_x_/divider, root_le_pos_y_/divider, root_le_pos_z_/divider, xz_mirror_


def get_free_stream_velocity_range():
    value = np.array(get_mach_number()) * 341
    return [value]
