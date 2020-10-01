from scipy import interpolate

from analysis.structural_analysis.DataStructure.FStructureClass import FStructureClass
from analysis.structural_analysis.DataStructure.HStructureClass import HStructureClass
from analysis.structural_analysis.DataStructure.VStructureClass import VStructureClass
from analysis.structural_analysis.DataStructure.WStructureClass import WStructureClass
from utils.MathLibrary import *


class AircraftStructure:
    def __init__(self, geometry_specs,weight_specs,structure_specs):

        wing_root_location_x, wing_root_location_y, wing_root_location_z, wing_dihedral, wing_sweep, wing_twist, wing_span, wing_taper_ratio, wing_chord, winglet_width, winglet_rotation, winglet_center_translation_x, winglet_center_translation_y, winglet_center_translation_z = read_w_h_v(
            values=geometry_specs, part="wing")
        htp_root_location_x, htp_root_location_y, htp_root_location_z, htp_dihedral, htp_sweep, htp_twist, htp_span, htp_taper_ratio, htp_chord, z1, z2, z3, z4, z5 = read_w_h_v(
            values=geometry_specs, part="htp")
        vtp_root_location_x, vtp_root_location_y, vtp_root_location_z, vtp_dihedral, vtp_sweep, vtp_twist, vtp_span, vtp_taper_ratio, vtp_chord, z1, z2, z3, z4, z5 = read_w_h_v(
            values=geometry_specs, part="vtp")

        wing_span = wing_span / 2
        fuselage_diameter, fuselage_length, nose_radius, nose_position_x, nose_position_y, nose_position_z, section_2_radius, section_2_center_position_x, section_2_center_position_y, section_2_center_position_z, section_3_radius, section_3_center_position_x, section_3_center_position_y, section_3_center_position_z, section_4_radius, section_4_center_position_x, section_4_center_position_y, section_4_center_position_z, tail_angle, tail_radius, tail_position_x, tail_position_y, tail_position_z = read_fuselage_values(
            values=geometry_specs)
        we_chord = effective_chord(wing_chord, wing_chord * wing_taper_ratio)
        wing_a = planform_area(wing_span, we_chord)
        ve_chord = effective_chord(wing_chord, wing_chord * wing_taper_ratio)
        vtail_a = planform_area(vtp_span, ve_chord)
        he_chord = effective_chord(htp_chord, htp_chord * htp_taper_ratio)
        htp_a = planform_area(htp_span, he_chord)

        self.wing_loading=weight_specs["maximum_take_off_mass"]/wing_a
        specification_section_list = [nose_radius, section_2_radius, section_3_radius, section_4_radius, tail_radius]
        x = [nose_position_x, section_2_center_position_x, section_3_center_position_x, section_4_center_position_x,
             tail_position_x]
        m_wing, m_fuselage, m_hstap, m_vstap = self.estimate_mass_of_airframe_parts(diameter_fuselage=fuselage_diameter,
                                                                                    length_fuselage=fuselage_length
                                                                                    , mtom=weight_specs["maximum_take_off_mass"], wing_area=wing_a,
                                                                                    htail_area=htp_a,
                                                                                    vtail_area=vtail_a,
                                                                                    aspect_ratio=wing_span / we_chord)
        wing_structure=structure_specs["wing_structure"]
        htp_structure=structure_specs["htp_structure"]
        vtp_structure = structure_specs["vtp_structure"]
        wing_sweep =quater_chord_sweep_to_leading_edge(sweep=wing_sweep,taper_ratio=wing_taper_ratio,area=wing_structure["wing_reference_area"])
        vtp_sweep=quater_chord_sweep_to_leading_edge(sweep=vtp_sweep,taper_ratio=vtp_taper_ratio,area=vtp_structure["vtp_reference_area"])
        htp_sweep = quater_chord_sweep_to_leading_edge(sweep=htp_sweep, taper_ratio=htp_taper_ratio,
                                                       area=htp_structure["htp_reference_area"])
        self.fuselage_structure = FStructureClass(specification_section_list=specification_section_list, x=x,
                                                  mass=m_fuselage
                                                  )
        self.wing_structure_r = WStructureClass(mass=m_wing, x_le=wing_root_location_x, y_le=wing_root_location_y,
                                                z_le=wing_root_location_z,dihedral_angle=wing_dihedral,sweep_angle=wing_sweep
                                                ,x_fs=wing_structure["spar_1_position"],x_ms=wing_structure["spar_2_position"],
                                                x_rs=wing_structure["spar_3_position"],taper_ratio=wing_taper_ratio,chord_length=wing_chord
                                                ,span=wing_span,root_chord=wing_chord,number_of_ribs=3)
        self.v_stab_structure_r = VStructureClass(mass=m_vstap, x_le=vtp_root_location_x, y_le=-vtp_root_location_y,
                                                  z_le=vtp_root_location_z,dihedral_angle=vtp_dihedral,sweep_angle=vtp_sweep
                                                ,x_fs=vtp_structure["spar_1_position"],x_ms=vtp_structure["spar_2_position"],
                                                x_rs=vtp_structure["spar_3_position"],taper_ratio=vtp_taper_ratio,chord_length=vtp_chord
                                                ,span=vtp_span,root_chord=vtp_chord,number_of_ribs=3,rib_mass=vtp_structure["rib_mass"]
                                                  ,spar_mass=vtp_structure["spar_mass"])
        self.h_stab_structure_r = HStructureClass(mass=m_hstap, x_le=htp_root_location_x, y_le=htp_root_location_y,
                                                  z_le=htp_root_location_z,dihedral_angle=htp_dihedral,sweep_angle=htp_sweep
                                                ,x_fs=htp_structure["spar_1_position"],x_ms=htp_structure["spar_2_position"],
                                                x_rs=htp_structure["spar_3_position"],taper_ratio=htp_taper_ratio,chord_length=htp_chord
                                                ,span=htp_span,root_chord=htp_chord,number_of_ribs=3,rib_mass=htp_structure["rib_mass"]
                                                  ,spar_mass=htp_structure["spar_mass"])

        self.v_stab_structure_l = VStructureClass(m=-1, mass=m_vstap, x_le=vtp_root_location_x,
                                                  y_le=-vtp_root_location_y, z_le=vtp_root_location_z,dihedral_angle=vtp_dihedral,sweep_angle=vtp_sweep
                                                ,x_fs=vtp_structure["spar_1_position"],x_ms=vtp_structure["spar_2_position"],
                                                x_rs=vtp_structure["spar_3_position"],taper_ratio=vtp_taper_ratio,chord_length=vtp_chord
                                                ,span=vtp_span,root_chord=vtp_chord,number_of_ribs=3,rib_mass=vtp_structure["rib_mass"]
                                                  ,spar_mass=vtp_structure["spar_mass"])


        self.wing_structure_l = WStructureClass(m=-1, mass=m_wing, x_le=wing_root_location_x,
                                                y_le=-wing_root_location_y, z_le=wing_root_location_z,dihedral_angle=wing_dihedral,sweep_angle=wing_sweep
                                                ,x_fs=wing_structure["spar_1_position"],x_ms=wing_structure["spar_2_position"],
                                                x_rs=wing_structure["spar_3_position"],taper_ratio=wing_taper_ratio,chord_length=wing_chord
                                                ,span=wing_span,root_chord=wing_chord,number_of_ribs=3,rib_mass=wing_structure["rib_mass"]
                                                  ,spar_mass=wing_structure["spar_mass"])


        self.h_stab_structure_l = HStructureClass(m=-1, mass=m_hstap, x_le=htp_root_location_x,
                                                  y_le=-htp_root_location_y, z_le=htp_root_location_z,dihedral_angle=htp_dihedral,sweep_angle=htp_sweep
                                                ,x_fs=htp_structure["spar_1_position"],x_ms=htp_structure["spar_2_position"],
                                                x_rs=htp_structure["spar_3_position"],taper_ratio=htp_taper_ratio,chord_length=htp_chord
                                                ,span=htp_span,root_chord=htp_chord,number_of_ribs=3,rib_mass=htp_structure["rib_mass"]
                                                  ,spar_mass=htp_structure["spar_mass"])

        self.cg_x = 0
        self.cg_y = 0
        self.cg_z = 0
        self.Ixx = 0
        self.Iyy = 0
        self.Izz = 0
        self.Ixz = 0
        self.fuselage_diameter = fuselage_diameter
        self.wing_span=wing_span
        self.vtp_span=vtp_span
        self.fuselage_length = fuselage_length
        self.estimate_Inertia()

    def estimate_cg_x(self):
        length_value = []
        moment_difference = []
        i = 0
        while i < self.fuselage_length:
            pre_pivot_moment = 0
            post_pivot_moment = 0
            if self.v_stab_structure_r.cg_x < i:
                pre_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_x ))
            else:
                post_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_x ))

            if self.h_stab_structure_r.cg_x < i:
                pre_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_x ))
            else:
                post_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_x ))

            if self.wing_structure_r.cg_x < i:
                pre_pivot_moment += (self.wing_structure_r.mass * (i-self.wing_structure_r.cg_x ))
            else:
                post_pivot_moment += (self.wing_structure_r.mass * (i-self.wing_structure_r.cg_x ))

            if self.v_stab_structure_l.cg_x < i:
                pre_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_x ))
            else:
                post_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_x ))

            if self.h_stab_structure_l.cg_x < i:
                pre_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_x ))
            else:
                post_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_x ))

            if self.wing_structure_l.cg_x < i:
                pre_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_x ))
            else:
                post_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_x ))

            if self.fuselage_structure.cg_x < i:
                pre_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_x))
            else:
                post_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_x))
            length_value.append(i)
            moment_diff = pre_pivot_moment + post_pivot_moment
            moment_difference.append(moment_diff)
            i += 0.01

        cg_x_function = interpolate.interp1d(moment_difference, length_value, fill_value="extrapolate")
        self.cg_x = cg_x_function(0.0)

    def estimate_mass_of_airframe_parts(self, length_fuselage=None, mtom=None, aspect_ratio=None,
                                        diameter_fuselage=None, wing_area=None, vtail_area=None, htail_area=None):
        m_wing = 2.2001003 * (10 ** (-4)) * (401.146 * (wing_area ** (1.31)) + mtom ** 1.1038) * aspect_ratio
        m_fuselage = ((12.7 * (length_fuselage * diameter_fuselage) ** 1.2932) * (1 - (
                -0.008 * ((length_fuselage / diameter_fuselage) ** 2) + (
                0.1664 * (length_fuselage / diameter_fuselage)) - 0.8501 * (
                        mtom * (diameter_fuselage / diameter_fuselage))))) / 10000
        m_vstap = 25.056 * vtail_area ** (1.003) / 100
        m_hstap = 12.908 * htail_area ** (1.1868) / 100
        return m_wing, m_fuselage, m_hstap, m_vstap

    def estimate_cg_y(self):
        length_value = []
        moment_difference = []
        i = -self.wing_span

        while i < self.wing_span:
            pre_pivot_moment = 0
            post_pivot_moment = 0

            if self.v_stab_structure_r.cg_y < i:
                pre_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_y))
            else:
                post_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_y))

            if self.h_stab_structure_r.cg_y < i:
                pre_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_y))
            else:
                post_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_y))

            if self.wing_structure_r.cg_y < i:
                pre_pivot_moment += (self.wing_structure_r.mass * (i-self.wing_structure_r.cg_y))
            else:
                post_pivot_moment += (self.wing_structure_r.mass * (i-self.wing_structure_r.cg_y))

            if self.v_stab_structure_l.cg_y < i:
                pre_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_y))
            else:
                post_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_y))

            if self.h_stab_structure_l.cg_y < i:
                pre_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_y))
            else:
                post_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_y))

            if self.wing_structure_l.cg_y < i:
                pre_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_y))
            else:
                post_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_y))

            if self.fuselage_structure.cg_y < i:
                pre_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_y))
            else:
                post_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_y))
            length_value.append(i)

            moment_diff = pre_pivot_moment + post_pivot_moment
            moment_difference.append(moment_diff)
            i += 0.01
        cg_y_function = interpolate.interp1d(moment_difference, length_value)

        self.cg_y = cg_y_function(0.0)

    def estimate_cg_z(self):
        length_value = []
        moment_difference = []
        i = -self.fuselage_diameter/2


        while i < (self.fuselage_diameter/2)+self.vtp_span:
            pre_pivot_moment = 0
            post_pivot_moment = 0
            if self.v_stab_structure_r.cg_z < i:
                pre_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_z))
            else:
                post_pivot_moment += (self.v_stab_structure_r.mass * (i-self.v_stab_structure_r.cg_z))

            if self.h_stab_structure_r.cg_z < i:
                pre_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_z))
            else:
                post_pivot_moment += (self.h_stab_structure_r.mass * (i-self.h_stab_structure_r.cg_z))

            if self.wing_structure_r.cg_z < i:
                pre_pivot_moment += (self.wing_structure_r.mass *(i-self.wing_structure_r.cg_z))
            else:
                post_pivot_moment += (self.wing_structure_r.mass * (i-self.wing_structure_r.cg_z))

            if self.v_stab_structure_l.cg_z < i:
                pre_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_z))
            else:
                post_pivot_moment += (self.v_stab_structure_l.mass * (i-self.v_stab_structure_l.cg_z))

            if self.h_stab_structure_l.cg_z < i:
                pre_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_z))
            else:
                post_pivot_moment += (self.h_stab_structure_l.mass * (i-self.h_stab_structure_l.cg_z))

            if self.wing_structure_l.cg_z < i:
                pre_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_z))
            else:
                post_pivot_moment += (self.wing_structure_l.mass * (i-self.wing_structure_l.cg_z))

            if self.fuselage_structure.cg_z < i:
                pre_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_z))
            else:
                post_pivot_moment += (self.fuselage_structure.mass * (i-self.fuselage_structure.cg_z))
            length_value.append(i)

            moment_diff = pre_pivot_moment + post_pivot_moment
            moment_difference.append(moment_diff)
            i += 0.01

        cg_z_function = interpolate.interp1d(moment_difference, length_value)
        self.cg_z = cg_z_function(0.0)


    def estimate_cg(self):
        self.estimate_cg_z()
        self.estimate_cg_x()
        self.estimate_cg_y()

        return self.cg_x, self.cg_y, self.cg_z

    def estimate_Inertia(self):
        x, y, z = self.estimate_cg()

        I_x_vstab_l = self.v_stab_structure_l.Ixx + self.v_stab_structure_l.mass * (
                (self.v_stab_structure_l.cg_y - y) ** 2 + (self.v_stab_structure_l.cg_z - z) ** 2)
        I_y_vstab_l = self.v_stab_structure_l.Iyy + self.v_stab_structure_l.mass * (
                (self.v_stab_structure_l.cg_x - x) ** 2 + (self.v_stab_structure_l.cg_z - z) ** 2)
        I_z_vstab_l = self.v_stab_structure_l.Izz + self.v_stab_structure_l.mass * (
                (self.v_stab_structure_l.cg_x - x) ** 2 + (self.v_stab_structure_l.cg_y - y) ** 2)
        I_z_x_vstab_l = self.v_stab_structure_l.Ixz + self.v_stab_structure_l.mass * (
                (self.v_stab_structure_l.cg_x - x) + (self.v_stab_structure_l.cg_z - z))

        I_x_hstab_l = self.h_stab_structure_l.Ixx + self.h_stab_structure_l.mass * (
                (self.h_stab_structure_l.cg_y - y) ** 2 + (self.h_stab_structure_l.cg_z - z) ** 2)
        I_y_hstab_l = self.h_stab_structure_l.Iyy + self.h_stab_structure_l.mass * (
                (self.h_stab_structure_l.cg_x - x) ** 2 + (self.h_stab_structure_l.cg_z - z) ** 2)
        I_z_hstab_l = self.h_stab_structure_l.Izz + self.h_stab_structure_l.mass * (
                (self.h_stab_structure_l.cg_x - x) ** 2 + (self.h_stab_structure_l.cg_y - y) ** 2)
        I_z_x_hstab_l = self.h_stab_structure_l.Ixz + self.h_stab_structure_l.mass * (
                (self.h_stab_structure_l.cg_x - x) + (self.h_stab_structure_l.cg_z - z))

        I_x_wing_l = self.wing_structure_l.Ixx + self.wing_structure_l.mass * (
                (self.wing_structure_l.cg_y - y) ** 2 + (self.wing_structure_l.cg_z - z) ** 2)
        I_y_wing_l = self.wing_structure_l.Iyy + self.wing_structure_l.mass * (
                (self.wing_structure_l.cg_x - x) ** 2 + (self.wing_structure_l.cg_z - z) ** 2)
        I_z_wing_l = self.wing_structure_l.Izz + self.wing_structure_l.mass * (
                (self.wing_structure_l.cg_x - x) ** 2 + (self.wing_structure_l.cg_y - y) ** 2)
        I_z_x_wing_l = self.wing_structure_l.Ixz + self.wing_structure_l.mass * (
                (self.wing_structure_l.cg_x - x) + (self.wing_structure_l.cg_z - z))

        I_x_vstab_r = self.v_stab_structure_r.Ixx + self.v_stab_structure_r.mass * (
                (self.v_stab_structure_r.cg_y - y) ** 2 + (self.v_stab_structure_r.cg_z - z) ** 2)
        I_y_vstab_r = self.v_stab_structure_r.Iyy + self.v_stab_structure_r.mass * (
                (self.v_stab_structure_r.cg_x - x) ** 2 + (self.v_stab_structure_r.cg_z - z) ** 2)
        I_z_vstab_r = self.v_stab_structure_r.Izz + self.v_stab_structure_r.mass * (
                (self.v_stab_structure_r.cg_x - x) ** 2 + (self.v_stab_structure_r.cg_y - y) ** 2)
        I_z_x_vstab_r = self.v_stab_structure_r.Ixz + self.v_stab_structure_r.mass * (
                (self.v_stab_structure_r.cg_x - x) + (self.v_stab_structure_r.cg_z - z))

        I_x_hstab_r = self.h_stab_structure_r.Ixx + self.h_stab_structure_r.mass * (
                (self.h_stab_structure_r.cg_y - y) ** 2 + (self.h_stab_structure_r.cg_z - z) ** 2)
        I_y_hstab_r = self.h_stab_structure_r.Iyy + self.h_stab_structure_r.mass * (
                (self.h_stab_structure_r.cg_x - x) ** 2 + (self.h_stab_structure_r.cg_z - z) ** 2)
        I_z_hstab_r = self.h_stab_structure_r.Izz + self.h_stab_structure_r.mass * (
                (self.h_stab_structure_r.cg_x - x) ** 2 + (self.h_stab_structure_r.cg_y - y) ** 2)
        I_z_x_hstab_r = self.h_stab_structure_r.Ixz + self.h_stab_structure_r.mass * (
                (self.h_stab_structure_r.cg_x - x) + (self.h_stab_structure_r.cg_z - z))

        I_x_wing_r = self.wing_structure_r.Ixx + self.wing_structure_r.mass * (
                (self.wing_structure_r.cg_y - y) ** 2 + (self.wing_structure_r.cg_z - z) ** 2)
        I_y_wing_r = self.wing_structure_r.Iyy + self.wing_structure_r.mass * (
                (self.wing_structure_r.cg_x - x) ** 2 + (self.wing_structure_r.cg_z - z) ** 2)
        I_z_wing_r = self.wing_structure_r.Izz + self.wing_structure_r.mass * (
                (self.wing_structure_r.cg_x - x) ** 2 + (self.wing_structure_r.cg_y - y) ** 2)
        I_z_x_wing_r = self.wing_structure_r.Ixz + self.wing_structure_r.mass * (
                (self.wing_structure_r.cg_x - x) + (self.wing_structure_r.cg_z - z))

        I_x_fuselage = self.fuselage_structure.Ixx + self.fuselage_structure.mass * (
                (self.fuselage_structure.cg_y - y) ** 2 + (self.fuselage_structure.cg_z - z) ** 2)
        I_y_fuselage = self.fuselage_structure.Iyy + self.fuselage_structure.mass * (
                (self.fuselage_structure.cg_x - x) ** 2 + (self.fuselage_structure.cg_z - z) ** 2)
        I_z_fuselage = self.fuselage_structure.Izz + self.fuselage_structure.mass * (
                (self.fuselage_structure.cg_x - x) ** 2 + (self.fuselage_structure.cg_y - y) ** 2)
        I_z_x_fuselage = self.fuselage_structure.Ixz + self.fuselage_structure.mass * (
                (self.fuselage_structure.cg_x - x) + (self.fuselage_structure.cg_z - z))

        self.Ixx = I_x_wing_r + I_x_hstab_r + I_x_wing_l + I_x_hstab_l + I_x_fuselage + I_x_vstab_r + I_x_vstab_l
        self.Iyy = I_y_wing_r + I_y_hstab_r + I_y_wing_l + I_y_hstab_l + I_y_fuselage + I_y_vstab_r + I_y_vstab_l
        self.Izz = I_z_wing_r + I_z_hstab_r + I_z_wing_l + I_z_hstab_l + I_z_fuselage + I_z_vstab_r + I_z_vstab_l
        self.Ixz = I_z_x_wing_r + I_z_x_hstab_r + I_z_x_wing_l + I_z_x_hstab_l + I_z_x_fuselage + I_z_x_vstab_r + I_z_x_vstab_l


def read_w_h_v(part="", values={}):
    root_location_x = values.get(part + "_root_position_x")
    root_location_y = values.get(part + "_root_position_y")
    root_location_z = values.get(part + "_root_position_z")
    chord = values.get(part + "_chord")
    dihedral = values.get(part + "_dihedral")
    sweep = values.get(part + "_sweep")
    twist = values.get(part + "_twist")
    span = values.get(part + "_span")
    taper_ratio = values.get(part + "_taper_ratio")
    if part == "wing":
        winglet_width = values.get("winglet_width")
        winglet_center_translation_x = values.get("winglet_center_translation_x")
        winglet_center_translation_y = values.get("winglet_center_translation_y")
        winglet_center_translation_z = values.get("winglet_center_translation_z")
        winglet_rotation = values.get("winglet_rotation")
    else:
        winglet_width = 0
        winglet_center_translation_x = 0
        winglet_center_translation_y = 0
        winglet_center_translation_z = 0
        winglet_rotation = 0

    return root_location_x, root_location_y, root_location_z, dihedral, sweep, twist, span, taper_ratio, chord, winglet_width, winglet_rotation, winglet_center_translation_x, winglet_center_translation_y, winglet_center_translation_z


def read_fuselage_values(values={}):
    fuselage_length = values.get("fuselage_length")
    fuselage_diameter = values.get("fuselage_diameter")
    nose_radius = values.get("nose_radius")
    nose_position_x = values.get("nose_center_position_x")
    nose_position_y = values.get("nose_center_position_y")
    nose_position_z = values.get("nose_center_position_z")
    tail_radius = values.get("tail_radius")
    tail_position_x = values.get("tail_center_position_x")
    tail_position_y = values.get("tail_center_position_y")
    tail_position_z = values.get("tail_center_position_z")
    tail_angle = values.get("tail_angle")
    section_2_center_position_x = values.get("section_2_center_position_x")
    section_2_center_position_y = values.get("section_2_center_position_y")
    section_2_center_position_z = values.get("section_2_center_position_z")
    section_2_radius = values.get("section_2_radius")
    section_3_radius = values.get("section_3_radius")
    section_3_center = values.get("section_3_center")
    section_3_center_position_x = values.get("section_3_center_position_x")
    section_3_center_position_y = values.get("section_3_center_position_y")
    section_3_center_position_z = values.get("section_3_center_position_z")
    section_4_center = values.get("section_4_center")
    section_4_center_position_x = values.get("section_4_center_position_x")
    section_4_center_position_y = values.get("section_4_center_position_y")
    section_4_center_position_z = values.get("section_4_center_position_z")
    section_4_radius = values.get("section_4_radius")
    return fuselage_diameter, fuselage_length, nose_radius, nose_position_x, nose_position_y, nose_position_z, section_2_radius, section_2_center_position_x, section_2_center_position_y, section_2_center_position_z, section_3_radius, section_3_center_position_x, section_3_center_position_y, section_3_center_position_z, section_4_radius, section_4_center_position_x, section_4_center_position_y, section_4_center_position_z, tail_angle, tail_radius, tail_position_x, tail_position_y, tail_position_z
