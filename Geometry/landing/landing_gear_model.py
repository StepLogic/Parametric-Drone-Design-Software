from math import cos, sin

from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.BRepPrimAPI import (BRepPrimAPI_MakeCylinder,
                             BRepPrimAPI_MakeTorus)
from tigl3.geometry import CTiglTransformation

from Utils.database.geometry.landing_gear_database import read_landing_gear_values


class landing_gear_model():
    def __init__(self):
        pass

    def create_single_assembly(self, tire_radius, wheel_radius, struct_length, scale=1):
        tire_radius = tire_radius
        wheel_radius = wheel_radius
        struct_length = struct_length

        straight_arm_height = tire_radius * 1.5

        ring_radius = wheel_radius
        torus_radius = tire_radius
        torus = BRepPrimAPI_MakeTorus(torus_radius, ring_radius).Shape()

        straight_arm_radius = ring_radius / 2

        straight_arm = BRepPrimAPI_MakeCylinder(straight_arm_radius, straight_arm_height).Shape()

        angled_arm_radius = straight_arm_radius
        angled_arm_height = tire_radius * 1.5
        angle = -40

        angled_arm = BRepPrimAPI_MakeCylinder(angled_arm_radius, angled_arm_height).Shape()
        traf = CTiglTransformation()
        traf.add_rotation_x(angle)
        angled_arm = traf.transform(angled_arm)
        traf = CTiglTransformation()
        traf.add_translation(0, angled_arm_height * sin(angle), 0)
        angled_arm = traf.transform(angled_arm)

        traf = CTiglTransformation()
        traf.add_translation(0, angled_arm_height * cos(angle), angled_arm_height * sin(angle))
        straight_arm = traf.transform(straight_arm)
        arm_assembly = BRepAlgoAPI_Fuse(
            straight_arm, angled_arm
        ).Shape()

        traf = CTiglTransformation()
        traf.add_rotation_x(90)
        torus = traf.transform(torus)

        pin_radius = wheel_radius
        pin_height = tire_radius

        pin = BRepPrimAPI_MakeCylinder(pin_radius, pin_height).Shape()

        traf = CTiglTransformation()
        traf.add_translation(0, 0, -straight_arm_height + torus_radius / 2)
        torus = traf.transform(torus)

        traf = CTiglTransformation()
        traf.add_rotation_x(90)
        pin = traf.transform(pin)

        traf = CTiglTransformation()
        traf.add_translation(0, 0, -straight_arm_height + pin_radius)
        pin = traf.transform(pin)

        traf = CTiglTransformation()
        traf.add_mirroring_at_xzplane()
        mirrored_arm_assembly = traf.transform(arm_assembly)

        traf = CTiglTransformation()
        traf.add_mirroring_at_xzplane()
        mirrored_pin = traf.transform(pin)

        arm_assembly = BRepAlgoAPI_Fuse(mirrored_arm_assembly, arm_assembly).Shape()

        struct_radius = wheel_radius - 0.5 * wheel_radius
        struct_height = struct_length
        struct = BRepPrimAPI_MakeCylinder(struct_radius, struct_height).Shape()
        traf = CTiglTransformation()
        traf.add_translation(0, 0, torus_radius)
        struct = traf.transform(struct)

        pin = BRepAlgoAPI_Fuse(mirrored_pin, pin).Shape()
        part_1 = BRepAlgoAPI_Fuse(arm_assembly, pin).Shape()
        part_2 = BRepAlgoAPI_Fuse(part_1, struct).Shape()
        part_3 = BRepAlgoAPI_Fuse(part_2, pin).Shape()

        return BRepAlgoAPI_Fuse(part_3, torus).Shape()

    def position_gears(self, tire_diameter=0.4, wheel_diameter=0.2, struct_length=0.1, x=0, y=0, z=0, scale=1.0):
        gear = self.create_single_assembly(tire_diameter / 2, wheel_diameter / 2, struct_length)
        traf = CTiglTransformation()
        traf.add_translation(x, y, z)
        gear = traf.transform(gear)
        return gear

    def assemble_gears(self):
        landing_gear_type_, struct_length_main_gear_, struct_length_aux_, aux_gear_position_x_, aux_gear_position_y_, \
        aux_gear_position_z_, r_gear_position_x_, r_gear_position_y_, \
        r_gear_position_z_, wheel_diameter_, tire_diameter_ = \
            read_landing_gear_values()

        r_gear_position_x_ = r_gear_position_x_
        r_gear_position_y_ = r_gear_position_y_
        r_gear_position_z_ = r_gear_position_z_

        aux_gear = self.position_gears(struct_length=struct_length_aux_, x=aux_gear_position_x_, y=aux_gear_position_y_,
                                       z=aux_gear_position_z_, tire_diameter=tire_diameter_,
                                       wheel_diameter=wheel_diameter_)

        right_gear = self.position_gears(struct_length=struct_length_main_gear_, x=r_gear_position_x_,
                                         y=r_gear_position_y_,
                                         z=r_gear_position_z_, tire_diameter=tire_diameter_,
                                         wheel_diameter=wheel_diameter_)



        traf = CTiglTransformation()
        traf.add_mirroring_at_xzplane()
        left_gear = traf.transform(right_gear)

        lofts = [right_gear, left_gear, aux_gear]

        return lofts

    def get_current_loft(self):
        loft = self.assemble_gears()
        return loft
