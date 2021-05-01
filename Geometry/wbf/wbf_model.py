from DPS_cad_system.airconics.airconics_tools import make_ellipsoid
from DPS_data_objects.placeholders.geometry_placeholder import *
from tigl3.geometry import CNamedShape
from utils.database.geometry_database import read_w_h_v, read_fuselage_values


class wbf_model:
    def __init__(self):
      pass


    def get_current_loft(self):
        self.wingroot_location_x, self.root_location_y, self.root_location_z, self.dihedral, \
        self.sweep, self.twist, self.span, self.taper_ratio, \
        self.chord, self.winglet_width, self.winglet_rotation, self.winglet_center_translation_x, \
        self.winglet_center_translation_y, self.winglet_center_translation_z, self.profile = read_w_h_v(
            part=wing)
        self.cockpitDesign,self.nose_tip_position_,self.tail_tip_position_,self.fuselage_diameter, self.fuselage_length, self.nose_radius_, \
        self.cockpit_height_, self.cockpit_length_, self.cockpit_width_, self.cockpit_position_x_, \
        self.cockpit_position_y_,self.cockpit_position_z_ ,       \
        self.nose_length_, self.nose_position_z_, self.section_1_radius_, \
        self.section_1_length_, self.section_1_position_z_, \
        self.section_2_radius_, self.section_2_length_, \
        self.section_2_position_z_, \
        self.section_3_radius_, \
        self.section_3_length_, \
        self.section_3_position_z_, \
        self.tip_radius_, self.tail_radius_, \
        self.tail_length_, self.tail_position_z_ = \
            read_fuselage_values()

        WTBFZ = self.chord * 0.009  # 787: 0.2
        WTBFheight = 0.3* self.chord  # 787:2.7
        WTBFwidth = 0.8*self.fuselage_diameter
        WTBFXCentre = self.wingroot_location_x  # 787: 23.8
        WTBFlength = 1.167 * self.chord  # 787:26

        WBF_shape =make_ellipsoid([WTBFXCentre, 0, WTBFZ], WTBFlength, WTBFwidth, WTBFheight)
        return [CNamedShape(WBF_shape, "loft")]

