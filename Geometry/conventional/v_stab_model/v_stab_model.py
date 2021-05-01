import random

import tigl3

from Utils.database.geometry.lifting_database import read_surface_data


class v_stab_model():
    def __init__(self,config,name="",surface_type_="",design_type_=""):
        super().__init__()
        self._name = name
        self.surface_type_=surface_type_
        self.design_type_=design_type_
        self.airfoil_type = "0012"
        self.current_loft = None
        self.aircraft = config
        self.wings = self.aircraft.get_wings()
        self.old_profile = ""
        self.v_stab = None
        self._observers = []
        self._wing_name = None
        self.iter=0
        self.root_position_x = 0
        self.root_position_y = 0
        self.root_position_z = 0
        self.dihedral = 0
        self.sweep = 0
        self.twist = 0
        self.span = 0
        self.taper_ratio = 0
        self.chord = 0

    def get_airfoil_notation(self):
        pass

    def read_parameters(self):
        try:
            self.root_location_x, self.root_location_y, self.root_location_z, self.dihedral, self.sweep, self.twist, self.span, self.taper_ratio, self.chord, self.airfoil_type = read_surface_data(self._name)
        except(Exception):
            self.airfoil_type = "0012"

    def get_current_loft(self):
        self.read_parameters()
        n = random.random()
        self.v_stab = self.wings.create_wing(f"v_stab{n}", 3, "NACA{}".format(self.airfoil_type))
        self.v_stab.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
        self.iter += 1

        self.v_stab.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_location_x
                                                                  , self.root_location_y
                                                                  , self.root_location_z))
        wing_main_half_span = self.span / 2
        try:
            self.v_stab.set_half_span_keep_area(wing_main_half_span)
        except(Exception):
            pass
        wing_main_half_span = self.span / 2
        try:
            self.v_stab.set_half_span_keep_area(wing_main_half_span)
        except(Exception):
            pass

        # move second to last section towards tip
        tip_idx = self.v_stab.get_section_count()
        tip = self.v_stab.get_section(tip_idx).get_section_element(1).get_ctigl_section_element().get_center()
        pre_tip = self.v_stab.get_section(tip_idx - 2).get_section_element(
            1).get_ctigl_section_element().get_center()
        s = self.v_stab.get_section(tip_idx - 1)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        center = ce.get_center()
        theta = 0.95
        center.x = theta * tip.x + (1 - theta) * pre_tip.x
        center.y = theta * tip.y + (1 - theta) * pre_tip.y
        center.z = theta * tip.z + (1 - theta) * pre_tip.z
        ce.set_center(center)

        profile = "naca" + self.airfoil_type
        constant = 0.0
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01
        # decrease section size towards wing tips
        root_width = self.chord
        root_height = self.chord * constant
        tip_width = self.chord / self.taper_ratio
        tip_height = tip_width * constant
        n_sections = self.v_stab.get_section_count()
        for idx in range(1, n_sections + 1):
            s = self.v_stab.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()

            theta = ce.get_center().y / wing_main_half_span

            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)

        self.v_stab.set_sweep(self.sweep)
        self.v_stab.set_dihedral(self.dihedral)
        self.v_stab.set_rotation(tigl3.geometry.CTiglPoint(90, 0, self.twist))
        self.current_loft = []

        self.current_loft.append(self.v_stab.get_loft().shape())
        self.old_profile = self.airfoil_type

        return self.current_loft


