import tigl3
from OCC.Bnd import Bnd_Box
from OCC._BRepBndLib import brepbndlib_Add

from utils import Database


class DrawObject():

    def __init__(self, params, aircraft, viewer, update, part=""):
        self.viewer = viewer
        self.aircraft = aircraft
        self.params = params
        self.update = update
        self.part = part
        self.cnt = 0

    def modify_parameters(self):
        loft = []
        if self.part == "vtp":
            loft = self.build_fin()
        if self.part == "htp":
            loft = self.build_tailplane()
        if self.part == "main":
            loft = self.build_wing()
        return loft

    def build_wing(self):

        loft = []
        profile = self.params["wing_main"]["wing_profile"]
        if self.update:
            wings = self.aircraft.get_wings()
            wing_main = wings.get_wing("wing_main")
            wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)

        else:
            wings = self.aircraft.get_wings()
            wing_main = wings.create_wing("wing_main", 3, "NACA{}".format(profile))
            wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
        profile = "naca" + self.params["wing_main"]["wing_profile"]
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01

        wing_main.set_root_leposition(tigl3.geometry.CTiglPoint(self.params["wing_main"]["wing_root_position_x"]
                                                                , self.params["wing_main"]["wing_root_position_y"]
                                                                , self.params["wing_main"]["wing_root_position_z"]))
        wing_main_half_span = self.params["wing_main"]["wing_span"] / 2
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
        root_width = self.params["wing_main"]["wing_chord"]
        root_height = self.params["wing_main"]["wing_chord"] * constant
        tip_width = self.params["wing_main"]["wing_chord"] / self.params["wing_main"]["wing_taper_ratio"]
        tip_height = tip_width * constant
        n_sections = wing_main.get_section_count()
        for idx in range(1, n_sections + 1):
            s = wing_main.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()

            theta = ce.get_center().y / wing_main_half_span

            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)

        wing_main.set_sweep(self.params["wing_main"]["wing_sweep"])
        wing_main.set_dihedral(self.params["wing_main"]["wing_dihedral"])

        # create winglet
        s = wing_main.get_section(tip_idx)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        pre_tip = wing_main.get_section(tip_idx - 1).get_section_element(1).get_ctigl_section_element().get_center()
        center = tigl3.geometry.CTiglPoint(self.params["wing_main"]["winglet_center_translation_x"]
                                           , self.params["wing_main"]["winglet_center_translation_y"]
                                           , self.params["wing_main"]["winglet_center_translation_z"])
        ce.set_center(pre_tip + center)
        s.set_rotation(tigl3.geometry.CTiglPoint(self.params["wing_main"]["winglet_rotation"], 0, 0))
        ce.set_width(self.params["wing_main"]["winglet_width"])
        parameters = {}
        parameters.update({"wing_reference_area": wing_main.get_reference_area(),

                           "wing_mac": wing_main.get_wing_mac()})

        try:
            Database.update_structure_specifications(key="wing_structure", value=parameters)
        except:
            Database.write_structures_specification({"wing_structure": parameters})
        loft.append(wing_main.get_loft())
        loft.append(wing_main.get_mirrored_loft())
        return loft

    def build_fin(self):
        # collect all relevant lofts of the airplane (fuselage, main wing, htp, vtp)
        lofts = []
        profile = self.params["wing_vtp"]["vtp_profile"]
        if self.update:
            wings = self.aircraft.get_wings()
            wing_vtp = wings.get_wing("wing_vtp")


        else:
            wings = self.aircraft.get_wings()
            wing_vtp = wings.create_wing("wing_vtp", 2, "NACA{}".format(profile))

        profile = "naca" + self.params["wing_vtp"]["vtp_profile"]
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01

        wing_vtp.set_root_leposition(tigl3.geometry.CTiglPoint(self.params["wing_vtp"]["vtp_root_position_x"]
                                                               , self.params["wing_vtp"]["vtp_root_position_y"]
                                                               , self.params["wing_vtp"]["vtp_root_position_z"]))

        wing_vtp.set_rotation(tigl3.geometry.CTiglPoint(90, 0, self.params["wing_vtp"]["vtp_twist"]))
        wing_vtp.set_half_span_keep_area(self.params["wing_vtp"]["vtp_span"])
        wing_vtp.set_sweep(self.params["wing_vtp"]["vtp_sweep"])
        root_width = self.params["wing_vtp"]["vtp_chord"]
        root_height = root_width * constant
        tip_width = self.params["wing_vtp"]["vtp_chord"] / self.params["wing_vtp"]["vtp_taper_ratio"]
        tip_height = tip_width * constant
        n_sections = wing_vtp.get_section_count()
        for idx in range(1, n_sections + 1):
            s = wing_vtp.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            theta = ce.get_center().y / (self.params["wing_vtp"]["vtp_span"] / 2)
            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)
        tip_idx = wing_vtp.get_section_count()
        s = wing_vtp.get_section(tip_idx)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        ce.set_width(self.params["wing_vtp"]["vtp_chord"] / self.params["wing_vtp"]["vtp_taper_ratio"])
        ce.set_height(self.params["wing_vtp"]["vtp_chord"] * 0.025)
        lofts.append(wing_vtp.get_loft())
        parameters = {}
        parameters.update({"vtp_reference_area": wing_vtp.get_reference_area(),

                           "vtp_mac": wing_vtp.get_wing_mac()})

        try:
            Database.update_structure_specifications(key="vtp_structure", value=parameters)
        except:
            Database.write_structures_specification({"vtp_structure": parameters})

        return lofts

    def build_tailplane(self):

        loft = []
        profile = self.params["wing_htp"]["htp_profile"]
        if self.update:
            wings = self.aircraft.get_wings()
            wing_htp = wings.get_wing("wing_htp")
            wing_htp.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)
        else:
            wings = self.aircraft.get_wings()
            wing_htp = wings.create_wing("wing_htp", 2, "NACA{}".format(profile))
            wing_htp.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)

        profile = "naca" + self.params["wing_htp"]["htp_profile"]
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01
        wing_htp.set_root_leposition(tigl3.geometry.CTiglPoint(self.params["wing_htp"]["htp_root_position_x"]
                                                               , self.params["wing_htp"]["htp_root_position_y"]
                                                               , self.params["wing_htp"]["htp_root_position_z"]))
        wing_htp.set_sweep(self.params["wing_htp"]["htp_sweep"])
        wing_htp.set_dihedral(self.params["wing_htp"]["htp_dihedral"])
        wing_htp.set_half_span_keep_area(self.params["wing_htp"]["htp_span"] / 2)

        root_width = self.params["wing_htp"]["htp_chord"]
        root_height = root_width * constant
        tip_width = self.params["wing_htp"]["htp_chord"] / self.params["wing_htp"]["htp_taper_ratio"]
        tip_height = tip_width * constant
        n_sections = wing_htp.get_section_count()
        for idx in range(1, n_sections + 1):
            s = wing_htp.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            theta = ce.get_center().y / (self.params["wing_htp"]["htp_span"] / 2)

            ce.set_width((1 - theta) * root_width + theta * tip_width)
            ce.set_height((1 - theta) * root_height + theta * tip_height)

        tip_idx = wing_htp.get_section_count()
        s = wing_htp.get_section(tip_idx)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        ce.set_width(tip_width)
        ce.set_height(tip_height)
        loft.append(wing_htp.get_loft())
        loft.append(wing_htp.get_mirrored_loft())

        parameters = {}
        parameters.update({"htp_reference_area": wing_htp.get_reference_area(),
                           "htp_mac": wing_htp.get_wing_mac()})

        try:
            Database.update_structure_specifications(key="htp_structure", value=parameters)
        except:
            Database.write_structures_specification({"htp_structure": parameters})

        return loft

    def show_lofts(self, prev_loft, lofts, cut_update=False, cut_loft=[]):
        self.cnt += 1
        if cut_update:
            for l in cut_loft:
                self.viewer.remove(l.shape())
        for loft in lofts:
            if (self.update):
                for l in prev_loft:
                    self.viewer.remove(l.shape())
                self.viewer.add(loft.shape())
            else:
                self.viewer.add(loft.shape())
                self.viewer._display.View.SetProj(-2, -1, 1)
                self.viewer._display.View.SetScale(90)

    def _display_lofts(self, prev_loft=None, cut_update=False, cut_loft=[]):
        if prev_loft is None:
            prev_loft = []
        loft = self.modify_parameters()
        self.show_lofts(prev_loft=prev_loft, lofts=loft, cut_update=cut_update, cut_loft=cut_loft)
        return loft
