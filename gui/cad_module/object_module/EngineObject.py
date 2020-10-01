import os
from math import cos, sin

import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper
import tixi3.tixi3wrapper
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Display.SimpleGui import init_display
import OCC.Quantity
from OCC.StlAPI import StlAPI_Reader
from OCC.TopLoc import TopLoc_Location
from OCC.TopoDS import TopoDS_Shape
from OCC.gp import gp_Trsf, gp_Pnt
from tigl3.geometry import CNamedShape
import Helper
from utils import MathLibrary
from utils.Database import read_aircraft_specifications
import tigl3.geometry
from tigl3.geometry import CTiglTransformation
def modify_parameters(aircraft, wing_span, chord, length, taper_ratio, radius_center, x, y, z, number,pos="n"):
    lofts = []
    fuselages = aircraft.get_fuselages()
    fuselage = fuselages.create_fuselage("fuselage{}".format(y), 4, "fuselageCircleProfileuID")
    fuselage.set_length(length)
    l1 = length / 4
    l2 = l1 + l1
    l3 = l1 + l2

    # shrink nose to a point
    s1 = fuselage.get_section(1)
    s1e1 = s1.get_section_element(1)
    s1e1ce = s1e1.get_ctigl_section_element()
    s1e1ce.set_center(tigl3.geometry.CTiglPoint(x, y, z))
    s1e1ce.set_area(MathLibrary.getArea(0.003))

    # move second section towards the nose
    s2 = fuselage.get_section(2)
    s2e1 = s2.get_section_element(1)
    s2e1ce = s2e1.get_ctigl_section_element()
    s2e1ce.set_center(tigl3.geometry.CTiglPoint(x + l1, y, z))
    s2e1ce.set_area(MathLibrary.getArea(radius_center))

    # move second section towards the nose
    s3 = fuselage.get_section(3)
    s3e1 = s3.get_section_element(1)
    s3e1ce = s3e1.get_ctigl_section_element()
    s3e1ce.set_center(tigl3.geometry.CTiglPoint(x + l2, y, z))
    s3e1ce.set_area(MathLibrary.getArea(radius_center))

    # move fourth section towards the tail
    s4 = fuselage.get_section(4)
    s4e1 = s4.get_section_element(1)
    s4e1ce = s4e1.get_ctigl_section_element()
    s4e1ce.set_center(tigl3.geometry.CTiglPoint(x + l3, y, z))
    s4e1ce.set_area(MathLibrary.getArea(radius_center - 0.3))



    angle = 0
    for i in range(0, number+1):
        lofts.append(
            create_wing(aircraft, angle=angle, wing_span=wing_span, chord=chord, taper_ratio=taper_ratio, x=x+(l1/2), y=y,
                        z=z,pos=pos))
        angle = (i / 3) * 360

    lofts.append(fuselage.get_loft())


    return lofts


def create_wing(aircraft, angle, wing_span, chord, taper_ratio, x, y, z,pos="n"):

    prop_object = TopoDS_Shape()
    stl_reader = StlAPI_Reader()
    location = os.path.abspath(Helper.absolute_path + "/resources/model/blade.stl")
    stl_reader.Read(prop_object, location)

    trafo = CTiglTransformation()
    trafo.add_scaling(chord,wing_span,chord*0.25)
    prop_object = trafo.transform(prop_object)

    trafo = CTiglTransformation()
    trafo.add_rotation_y(90)
    prop_object = trafo.transform(prop_object)

    trafo = CTiglTransformation()
    trafo.add_rotation_x(angle)
    prop_object=trafo.transform(prop_object)

    trafo = CTiglTransformation()
    trafo.add_translation(x,y,z)
    prop_object = trafo.transform(prop_object)





    return CNamedShape(prop_object, "prop")


def show_lofts(viewer, prev_loft, lofts, update):
    for loft in lofts:
        if update:
            for l in prev_loft:
                viewer.remove(l.shape())
            viewer.add(loft.shape())
        else:
            viewer.add(loft.shape())
            viewer._display.View.SetProj(-2, -1, 1)
            viewer._display.View.SetScale(90)


def get_engine_loft(params, display, update, prev_loft):
    t_h_1 = tixi3.tixi3wrapper.Tixi3()
    t_h_1.open(Helper.resource_path(Helper.absolute_path + "/resources/empty.cpacs3.xml"))
    tg_h_1 = tigl3.tigl3wrapper.Tigl3()
    tg_h_1.open(t_h_1, "")
    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
    aircraft = mgr.get_configuration(tg_h_1._handle.value)
    length = params["engine"]["cover_length"]
    radius_center = params["engine"]["cover_radius"]
    span = params["engine"]["propeller_diameter"] / 2
    chord = params["engine"]["propeller_chord"]
    x = params["engine"]["engine_position_x"]
    y = params["engine"]["engine_position_y"]
    z = params["engine"]["engine_position_z"]
    number = params["engine"]["propeller_number"]
    engine_position=params["engine"]["engine_position"]
    values = read_aircraft_specifications()
    loft=[]
    loft2 = []
    if (engine_position == "w"):
        part = "wing"
        root_location_x = values.get(part + "_root_position_x")
        root_location_y = values.get(part + "_root_position_y")
        root_location_z = values.get(part + "_root_position_z")
        dihedral = values.get(part + "_dihedral")
        sweep = values.get(part + "_sweep")

        taper_ratio = values.get(part + "_taper_ratio")
        engine_position_y = y + root_location_y
        engine_position_x =x  + root_location_x
        engine_position_z = z+root_location_z
        loft = modify_parameters(aircraft, length=length, taper_ratio=0.3,
                                 radius_center=radius_center, wing_span=span,
                                 chord=chord, x=engine_position_x, y=engine_position_y, z=engine_position_z,
                                 number=number,pos="w")
        loft2=modify_parameters(aircraft, length=length, taper_ratio=1,
                                 radius_center=radius_center, wing_span=span,
                                 chord=chord, x=engine_position_x, y=-engine_position_y, z=engine_position_z,
                                 number=number,pos="w")



    elif (engine_position == "n"):
        nose_position_x = values.get("nose_center_position_x")
        nose_position_y = values.get("nose_center_position_y")
        nose_position_z = values.get("nose_center_position_z")
        engine_position_x = nose_position_x
        engine_position_y = nose_position_y
        engine_position_z = nose_position_z
        loft = modify_parameters(aircraft, length=length, taper_ratio=0.3,
                                 radius_center=radius_center, wing_span=span,
                                 chord=chord, x=engine_position_x, y=engine_position_y, z=engine_position_z, number=number,pos="n")



    loft.extend(loft2)
    show_lofts(viewer=display, prev_loft=prev_loft, lofts=loft, update=update)
    return loft
