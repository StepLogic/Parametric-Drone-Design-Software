import functools
import logging
import random
import time

import tigl3

from GUI.window.cad.geometry_tools import cut_wing
from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import conventional_design, unconventional_design
from Utils.database.geometry.control_surface_database import read_parent_data, read_surface_data


class control_surface_model():

    def __init__(self, name=None, config=None, part_loft=None):
        super().__init__()
        self.profile = "naca4412"
        self.aircraft = config
        self.part_loft = part_loft
        self.wings = self.aircraft.get_wings()
        self.name = name
        self.iter = 0
        self.update = False

    def read_parameters(self):
        self.root_location_x_, self.root_location_y_, self.root_location_z_, self.rot_x, self.rot_y, self.rot_z, \
        self.span_, self.chord_, self.parent__ = read_surface_data(
            surface_name=self.name)

    def create_aileron(self, height=1):
        self.read_parameters()
        loft = []
        profile = self.profile
        wings = self.aircraft.get_wings()
        try:
            wing_main = wings.create_wing(f"{self.name}{self.iter}", 3, "naca4412")
        except:
            n = random.random()
            wing_main = wings.create_wing(f"{self.name}{n}{self.iter}", 3, "naca4412")

        self.iter += 1

        profile = "naca4412"
        constant = 1
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01
        wing_main_half_span = self.span_ / 2
        wing_main.set_half_span_keep_area(wing_main_half_span)

        # decrease section size towards wing tips
        root_width = self.chord_
        root_height = self.chord_ * constant * height
        tip_width = self.chord_
        tip_height = tip_width * constant * height
        n_sections = wing_main.get_section_count()
        for idx in range(1, n_sections + 1):
            s = wing_main.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            theta = ce.get_center().y / wing_main_half_span
            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)
        root_location_x_ = read_parent_data(self.parent__, key=root_le_position_x)
        root_location_y_ = read_parent_data(self.parent__, key=root_le_position_y)
        root_location_z_ = read_parent_data(self.parent__, key=root_le_position_z)
        if read_parent_data(self.parent__, key=design_type) == conventional_design:
            sweep_ = read_parent_data(self.parent__, key=sweep)
            dihedral_ = read_parent_data(self.parent__, key=dihedral)
            if sweep_>0.0:
                wing_main.set_sweep(sweep_)
            if dihedral_>0.0:
                wing_main.set_sweep(dihedral_)
        if read_parent_data(self.parent__, key=surface_type) == fin and read_parent_data(self.parent__,
                                                                                         key=design_type) == conventional_design:
            wing_main.set_rotation(tigl3.geometry.CTiglPoint(90, 0, 0))
        elif read_parent_data(self.parent__, key=design_type) == unconventional_design:
            wing_main.set_rotation(tigl3.geometry.CTiglPoint(
                self.rot_x + float(read_parent_data(self.parent__, key=rotation_x)),
                self.rot_y + float(read_parent_data(self.parent__, key=rotation_y)),
                self.rot_z + float(read_parent_data(self.parent__, key=rotation_z))))


        if read_parent_data(self.parent__,key=design_type) == conventional_design:
            wing_main.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_location_x_+ root_location_x_
                                                                    , self.root_location_y_ + root_location_y_
                                                                    , self.root_location_z_ + root_location_z_))
        elif read_parent_data(self.parent__, key=design_type) == unconventional_design:
            wing_main.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_location_x_ + root_location_x_
                                                                    , self.root_location_y_ + root_location_y_
                                                                    , self.root_location_z_ + root_location_z_))


        loft.append(wing_main.get_loft().shape())
        if read_parent_data(self.parent__, key=design_type) == unconventional_design:
            if read_parent_data(self.parent__, key=xz_mirror):
                wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
            elif read_parent_data(self.parent__, key=xy_mirror):
                wing_main.set_symmetry(tigl3.geometry.TIGL_X_Y_PLANE)
            elif read_parent_data(self.parent__, key=yz_mirror):
                wing_main.set_symmetry(tigl3.geometry.TIGL_Y_Z_PLANE)
            else:
                return loft
        if read_parent_data(self.parent__, key=surface_type) == fin and read_parent_data(self.parent__,
                                                                                         key=design_type) == conventional_design:
            return loft
        else:
            wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
            loft.append(wing_main.get_mirrored_loft().shape())

        return loft


    def get_current_loft(self):
        lofts = self.part_loft
        surfaces = self.create_aileron()
        cut_shapes = self.create_aileron(10)
        logging.info(time.strftime('%X'))
        wing_1 = cut_wing(lofts[0], cut_shapes[0])
        logging.info(time.strftime('%X'))
        ret_loft = []
        if read_parent_data(self.parent__, key=design_type)==conventional_design:
            if read_parent_data(self.parent__, key=surface_type) == fin:
                ret_loft = [wing_1, surfaces[0]]
            else:
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1, surfaces[0], surfaces[1]]

        else:
            if read_parent_data(self.parent__, key=xz_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1, surfaces[0], surfaces[1]]
            elif read_parent_data(self.parent__, key=xy_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xyplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1, surfaces[0], surfaces[1]]
            elif read_parent_data(self.parent__, key=yz_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_yzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1, surfaces[0], surfaces[1]]
            else:

                ret_loft=[wing_1,surfaces[0]]


        return ret_loft


    def get_surface_loft(self):
        lofts = self.part_loft
        surfaces = self.create_aileron()
        ret_loft = {}
        if read_parent_data(self.parent__, key=design_type) == conventional_design:
            if read_parent_data(self.parent__, key=surface_type) == fin:
                ret_loft = {self.name:surfaces[0]}
            else:
                ret_loft = {self.name+"Left": surfaces[0],self.name+"Right": surfaces[1]}


        else:
            if read_parent_data(self.parent__, key=xz_mirror):
                ret_loft = {self.name + "Left": surfaces[0], self.name + "Right": surfaces[1]}
            elif read_parent_data(self.parent__, key=xy_mirror):
                ret_loft = {self.name + "Left": surfaces[0], self.name + "Right": surfaces[1]}
            elif read_parent_data(self.parent__, key=yz_mirror):
                ret_loft = {self.name + "Left": surfaces[0], self.name + "Right": surfaces[1]}

        return ret_loft

    @functools.lru_cache(maxsize=512)
    def get_wing_loft(self):
        lofts = self.part_loft
        surfaces = self.create_aileron()
        cut_shapes = self.create_aileron(10)

        logging.info(time.strftime('%X'))
        wing_1 = cut_wing(lofts[0], cut_shapes[0])
        logging.info(time.strftime('%X'))
        ret_loft = []
        if read_parent_data(self.parent__, key=design_type) == conventional_design:
            if read_parent_data(self.parent__, key=surface_type) == fin:
                ret_loft = [wing_1]
            else:
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1]

        else:
            if read_parent_data(self.parent__, key=xz_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1]
            elif read_parent_data(self.parent__, key=xy_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_xyplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1]
            elif read_parent_data(self.parent__, key=yz_mirror):
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_mirroring_at_yzplane()
                wing_2 = tigl3.geometry.CNamedShape(trafo.transform(wing_1), "cut").shape()
                ret_loft = [wing_2, wing_1]
            else:
                ret_loft = [wing_1, surfaces[0]]

        return ret_loft
