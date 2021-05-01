
import random

import numpy as np
import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper

from GUI.window.cad.airconics_tools import boolean_cut
from Utils.database.propulsion.propulsion_database import read_shroud_parameters
from Utils.maths.math_library import getArea


class shroud_model():
    def __init__(self, config=None):
        self.config = config

    def get_current_loft(self):
        shroud_length_, root_le_pos_x_, root_le_pos_y_, root_le_pos_z_, shroud_number_, shroud_taper_ratio_, shroud_inner_diameter_, shroud_outer_diameter_, xy_mirror_, xz_mirror_, yz_mirror_\
            = read_shroud_parameters()

        interval = 5


        sections = [root_le_pos_x_,
                    root_le_pos_x_ +shroud_length_]
        cutout_sections = [root_le_pos_x_-(shroud_length_/2),
                    root_le_pos_x_ + (shroud_length_+(shroud_length_/2))]

        cutout_radius = [
            shroud_inner_diameter_/2,
            shroud_inner_diameter_/(2*shroud_taper_ratio_)]
        outer_radius = [
            shroud_outer_diameter_ / 2,
            shroud_outer_diameter_ /(2*shroud_taper_ratio_)]

        x_ = []
        x_.extend(np.linspace(sections[0], sections[1], num=interval))
        x_cut=[]
        x_cut.extend(np.linspace(cutout_sections[0], cutout_sections[1], num=interval))
        cutout_radii = []
        cutout_radii.extend(np.linspace(cutout_radius[0], cutout_radius[1], num=interval))

        outer_radii = []
        outer_radii.extend(np.linspace(outer_radius[0], outer_radius[1], num=interval))


        print(x_,cutout_radii)

        n = random.random()
        cut_out = self.config.get_fuselages().create_fuselage(f"shroud{n}", len(x_), "fuselageCircleProfileuID")
        for (x, rad, index) in zip(x_cut, cutout_radii, range(1, len(x_) + 1)):
            section = cut_out.get_section(index)
            sectionElement = section.get_section_element(1)
            sectionElementCenter = sectionElement.get_ctigl_section_element()
            sectionElementCenter.set_center(tigl3.geometry.CTiglPoint(x
                                                                      ,root_le_pos_y_
                                                                      ,root_le_pos_z_))

            sectionElementCenter.set_area(getArea(rad))

        n = random.random()
        outer = self.config.get_fuselages().create_fuselage(f"shroud{n}", len(x_),
                                                                       "fuselageCircleProfileuID")
        for (x, rad, index) in zip(x_,outer_radii, range(1, len(x_) + 1)):
            section = outer.get_section(index)
            sectionElement = section.get_section_element(1)
            sectionElementCenter = sectionElement.get_ctigl_section_element()
            sectionElementCenter.set_center(tigl3.geometry.CTiglPoint(x
                                                                      , root_le_pos_y_
                                                                      , root_le_pos_z_))

            sectionElementCenter.set_area(getArea(rad))
        loft=[]
        loft.append(boolean_cut(outer.get_loft().shape(),cut_out.get_loft().shape()))
        if xy_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xyplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif xz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif yz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_yzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        print(loft)
        return loft