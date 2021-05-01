import random

import tigl3
import tigl3.surface_factories

from Utils.database.geometry.lifting_database import read_surface_data


class wing_model:
    def __init__(self, config=None, name="", surface_type_="", design_type_=""):
        super().__init__()
        self._name = name
        self.surface_type_ = surface_type_
        self.design_type_ = design_type_
        self.profile = "0012"
        self.current_loft = None
        self.aircraft = config
        self.wings = self.aircraft.get_wings()
        self.old_profile = ""

        self.iter = 0
        self._wing_name = None
        self.root_location_x = 0
        self.root_location_y = 0
        self.root_location_z = 0
        self.dihedral = 0
        self.sweep = 0
        self.twist = 0
        self.span = 0
        self.taper_ratio = 1
        self.chord = 0
        self.winglet_width = 0
        self.winglet_rotation = 0
        self.winglet_center_translation_x = 0
        self.winglet_center_translation_y = 0
        self.winglet_center_translation_z = 0
        self.update = False

    def get_airfoil_notation(self):
        pass

    def read_parameters(self):

        self.root_location_x, self.root_location_y, self.root_location_z, self.dihedral, \
        self.sweep, self.twist, self.span, self.taper_ratio, \
        self.chord, self.winglet_width, self.winglet_rotation, self.winglet_center_translation_x, \
        self.winglet_center_translation_y, self.winglet_center_translation_z, self.profile = read_surface_data(
            self._name)

    def get_current_loft(self):
        self.read_parameters()
        return self.straight_surface()

    def straight_surface(self):
        self.read_parameters()
        loft = []
        profile = self.profile
        wings = self.aircraft.get_wings()
        n = random.random()
        wing_main = wings.create_wing(f"wing_main{n}", 3, "NACA{}".format(profile))
        wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
        self.iter += 1

        profile = "naca" + self.profile
        constant = 1
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01

        wing_main.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_location_x
                                                                , self.root_location_y
                                                                , self.root_location_z))
        wing_main_half_span = self.span / 2
        try:
            wing_main.set_half_span_keep_area(wing_main_half_span)
        except(Exception):
            pass

        # move second to last section towards tip
        tip_idx = wing_main.get_section_count()
        tip = wing_main.get_section(tip_idx).get_section_element(1).get_ctigl_section_element().get_center()
        pre_tip = wing_main.get_section(tip_idx - 2).get_section_element(1).get_ctigl_section_element().get_center()
        s = wing_main.get_section(tip_idx - 1)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        center = ce.get_center()
        theta = 0.95
        center.x = theta * tip.x + (1 - theta) * pre_tip.x
        center.y = theta * tip.y + (1 - theta) * pre_tip.y
        center.z = theta * tip.z + (1 - theta) * pre_tip.z
        ce.set_center(center)

        # decrease section size towards wing tips
        root_width = self.chord
        root_height = self.chord * constant
        tip_width = self.chord / self.taper_ratio
        tip_height = tip_width * constant
        n_sections = wing_main.get_section_count()
        for idx in range(1, n_sections + 1):
            s = wing_main.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()

            theta = ce.get_center().y / wing_main_half_span

            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)

        wing_main.set_sweep(self.sweep)
        wing_main.set_dihedral(self.dihedral)

        # create winglet
        s = wing_main.get_section(tip_idx)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        pre_tip = wing_main.get_section(tip_idx - 1).get_section_element(1).get_ctigl_section_element().get_center()
        center = tigl3.geometry.CTiglPoint(self.winglet_center_translation_x
                                           , self.winglet_center_translation_y
                                           , self.winglet_center_translation_z)
        ce.set_center(pre_tip + center)
        s.set_rotation(tigl3.geometry.CTiglPoint(self.winglet_rotation, 0, 0))
        ce.set_width(self.winglet_width)

        loft.append(wing_main.get_loft().shape())
        loft.append(wing_main.get_mirrored_loft().shape())
        return loft
