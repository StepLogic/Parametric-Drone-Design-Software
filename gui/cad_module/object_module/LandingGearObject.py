from utils.Database import read_aircraft_specifications

from math import atan, cos, sin, pi

from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.BRepBuilderAPI import (BRepBuilderAPI_Transform, BRepBuilderAPI_MakeWire,
                                BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace)
from OCC.BRepFeat import BRepFeat_MakeCylindricalHole
from OCC.BRepPrimAPI import (BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder,
                             BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeRevol)
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Ax1, gp_Trsf, gp_Vec

from OCC.Display.SimpleGui import init_display
from tigl3.geometry import CTiglTransformation, CNamedShape


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


def create_single_assembly(tire_radius, wheel_radius, struct_length, scale=1):
    tire_radius= tire_radius / scale
    wheel_radius= wheel_radius / scale
    struct_length=struct_length/scale

    straight_arm_height =tire_radius*1.5

    ring_radius = wheel_radius
    torus_radius = tire_radius
    torus = BRepPrimAPI_MakeTorus(torus_radius, ring_radius).Shape()

    straight_arm_radius = ring_radius/2

    straight_arm = BRepPrimAPI_MakeCylinder(straight_arm_radius, straight_arm_height).Shape()



    angled_arm_radius = straight_arm_radius
    angled_arm_height =tire_radius*1.5
    angle=-40

    angled_arm = BRepPrimAPI_MakeCylinder(angled_arm_radius, angled_arm_height).Shape()
    traf = CTiglTransformation()
    traf.add_rotation_x(angle)
    angled_arm=traf.transform(angled_arm)
    traf = CTiglTransformation()
    traf.add_translation(0,angled_arm_height * sin(angle),0)
    angled_arm=traf.transform(angled_arm)

    traf = CTiglTransformation()
    traf.add_translation(0,angled_arm_height * cos(angle),angled_arm_height*sin(angle))
    straight_arm=traf.transform(straight_arm)
    arm_assembly = BRepAlgoAPI_Fuse(
        straight_arm, angled_arm
    ).Shape()




    traf = CTiglTransformation()
    traf.add_rotation_x(90)
    torus=traf.transform(torus)

    pin_radius =wheel_radius
    pin_height =tire_radius

    pin = BRepPrimAPI_MakeCylinder(pin_radius, pin_height).Shape()

    traf = CTiglTransformation()
    traf.add_translation(0,0,-straight_arm_height+torus_radius/2)
    torus=traf.transform(torus)

    traf = CTiglTransformation()
    traf.add_rotation_x(90)
    pin = traf.transform(pin)

    traf = CTiglTransformation()
    traf.add_translation(0, 0, -straight_arm_height + pin_radius)
    pin = traf.transform(pin)

    traf = CTiglTransformation()
    traf.add_mirroring_at_xzplane()
    mirrored_arm_assembly=traf.transform(arm_assembly)





    traf = CTiglTransformation()
    traf.add_mirroring_at_xzplane()
    mirrored_pin=traf.transform(pin)



    arm_assembly = BRepAlgoAPI_Fuse(mirrored_arm_assembly, arm_assembly).Shape()

    struct_radius =wheel_radius-0.5*wheel_radius
    struct_height =struct_length
    struct = BRepPrimAPI_MakeCylinder(struct_radius, struct_height).Shape()
    traf = CTiglTransformation()
    traf.add_translation(0, 0,torus_radius)
    struct=traf.transform(struct)

    pin = BRepAlgoAPI_Fuse(mirrored_pin, pin).Shape()
    part_1 = BRepAlgoAPI_Fuse(arm_assembly, pin).Shape()
    part_2 = BRepAlgoAPI_Fuse(part_1, struct).Shape()
    part_3 = BRepAlgoAPI_Fuse(part_2, pin).Shape()

    return BRepAlgoAPI_Fuse(part_3, torus).Shape()

def position_gears(tire_diameter=0.4, wheel_diameter=0.2, struct_length=0.1,x=0,y=0,z=0,scale=1.0):
    gear = create_single_assembly(tire_diameter/2, wheel_diameter/2, struct_length,scale)
    traf = CTiglTransformation()
    traf.add_translation(x,y,z)
    gear = traf.transform(gear)
    return CNamedShape(gear,"gear")



def assemble_gears(values):
    values = values["landing_gear"]
    landing_gear_type = values["landing_gear_type"]
    struct_length_main_gear = values["struct_length_main_gear"]
    struct_length_aux = values["struct_length_aux"]
    r_gear_position_x = values["rol_gear_position_x"]
    r_gear_position_y = values["rol_gear_position_y"]
    r_gear_position_z = values["rol_gear_position_z"]
    aux_gear_position_x = values["aux_gear_position_x"]
    aux_gear_position_y = values["aux_gear_position_y"]
    aux_gear_position_z = values["aux_gear_position_z"]

    values = read_aircraft_specifications()
    part = "wing"
    root_location_x = values.get(part + "_root_position_x")
    root_location_y = values.get(part + "_root_position_y")
    root_location_z = values.get(part + "_root_position_z")

    r_gear_position_x = r_gear_position_x + (root_location_x)-struct_length_main_gear
    r_gear_position_y = (r_gear_position_y + root_location_y)-struct_length_main_gear
    r_gear_position_z = r_gear_position_z + root_location_z-struct_length_main_gear

    l_gear_position_x = r_gear_position_x
    l_gear_position_y = -abs(r_gear_position_y)
    l_gear_position_z = r_gear_position_z
    aux=None
    if (landing_gear_type == "c"):
        nose_position_x = values.get("nose_center_position_x")
        nose_position_y = values.get("nose_center_position_y")
        nose_position_z = values.get("nose_center_position_z")
        aux_gear_position_x = nose_position_x + aux_gear_position_x-struct_length_aux
        aux_gear_position_y = nose_position_y + aux_gear_position_y-struct_length_aux
        aux_gear_position_z = nose_position_z + aux_gear_position_z-struct_length_aux
        aux_gear = position_gears(struct_length=struct_length_aux, x=aux_gear_position_x, y=aux_gear_position_y,
                                  z=aux_gear_position_z, scale=1.5)

    elif landing_gear_type == "t":
        tail_center_position_x = values.get("tail_center_position_x")
        tail_center_position_y = values["tail_center_position_y"]
        tail_center_position_z = values.get("tail_center_position_z")
        aux_gear_position_x = tail_center_position_x + aux_gear_position_x-struct_length_aux
        aux_gear_position_y = tail_center_position_y + aux_gear_position_y-struct_length_aux
        aux_gear_position_z = tail_center_position_z + aux_gear_position_z-struct_length_aux
        aux_gear = position_gears(struct_length=struct_length_aux, x=aux_gear_position_x, y=aux_gear_position_y,
                                  z=aux_gear_position_z, scale=3)

    right_gear=position_gears(struct_length=struct_length_main_gear,x=r_gear_position_x,y=r_gear_position_y,z=r_gear_position_z,scale=1.5)
    left_gear=position_gears(struct_length=struct_length_main_gear,x=l_gear_position_x,y=l_gear_position_y,z=l_gear_position_z,scale=1.5)

    lofts=[]
    lofts.append(right_gear)
    lofts.append(left_gear)
    lofts.append(aux_gear)
    return lofts

def get_landing_gear_loft(params, display, update, prev_loft):
    loft = assemble_gears(params)
    show_lofts(viewer=display, prev_loft=prev_loft, lofts=loft, update=update)
    return loft
