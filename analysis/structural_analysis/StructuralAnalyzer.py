

import matplotlib.pyplot as plt
import numpy as np

from analysis.structural_analysis.DataStructure.AircraftStructure import AircraftStructure
from utils import Database

x = []
y = []
z = []


def estimate_aircraft_structure():
    geometry_specs = Database.read_aircraft_specifications()
    structure_specs = Database.read_structures_specifications()
    weight_specs=Database.read_structures_specifications()["mass"]
    structure = AircraftStructure(geometry_specs=geometry_specs,structure_specs=structure_specs,weight_specs=weight_specs)

    results = {"Inertia": {"Ixx": structure.Ixx, "Iyy": structure.Iyy, "Izz": structure.Izz, "Ixz": structure.Ixz
                           ,"wing_loading":structure.wing_loading,
                           "cg_x": float(structure.cg_x.real), "cg_y": float(structure.cg_y.real),
                           "cg_z": float(structure.cg_z)}}

    points_list = structure.fuselage_structure.fuselage_point_mass_list
    for list in points_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.wing_structure_l.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.wing_structure_r.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.v_stab_structure_l.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.v_stab_structure_r.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.h_stab_structure_l.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)
    for list in structure.h_stab_structure_r.wings_point_mass_list:
        for point in list:
            x.append(point.x_cg)
            y.append(point.y_cg)
            z.append(point.z_cg)

    try:
        existing_value = Database.read_structures_specifications()
        existing_value.update(results)
        Database.write_structures_specification(existing_value)
    except:
        Database.write_structures_specification(results)

    return x,y,z,results




def show_payload_position_x_y(first=True, x_list=[], y_list=[], ):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = ax.scatter(x_list, y_list)
    if first:
        plt.show()
    else:
        data.set_ydata(np.array(y_list))
        data.set_xdata(np.array((x_list)))
        fig.canvas.draw()
        fig.canvas.flush_events()


def show_payload_position_z_y(first=True, z_list=[], y_list=[], ):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data = ax.scatter(y_list, z_list)
    if first:
        plt.show()
    else:
        data.set_ydata(np.array(z_list))
        data.set_xdata(np.array((y_list)))
        fig.canvas.draw()
        fig.canvas.flush_events()




