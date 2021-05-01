import random

import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper

from GUI.window.cad.airconics_tools import make_ellipsoid
from Utils.database.geometry.boom_database import read_boom_data


class boom_model():
    def __init__(self, config=None, text="", boom_type_="", design_type_=""):
        super().__init__()
        self.text = text
        self.boom_type_ = boom_type_
        self.design_type_ = design_type_
        self.fuselage_diameter = 0
        self.fuselage_length = 0
        self.nose_radius_ = 0
        self.nose_length_ = 0
        self.iter = 0
        self.section_1_radius_ = 0
        self.section_1_length_ = 0
        self.section_2_radius_ = 0
        self.section_2_length_ = 0
        self.section_3_radius_ = 0
        self.section_3_length_ = 0
        self.tip_width_ = 0
        self.tail_width_ = 0
        self.tail_length_ = 0

        self.current_lofts = None
        self.update = False
        self.prev_name = ""

        self.fuselage_profile = "D150_VAMP_FL1_ProfSupEl6"
        self.fuselages =config.get_fuselages()
        self.fuselage = None

    def read_parameters(self):
        self.tail_profile_, self.nose_profile_, \
        self.section_1_profile_, self.section_2_profile_, \
        self.section_3_profile_, self.cockPitDesign, self.xz_mirror_, self.xy_mirror_, self.yz_mirror_, \
        self.root_position_x_, self.root_position_y_, self.root_position_z_, \
        self.nose_tip_position_, self.tail_tip_position_, \
        self.fuselage_diameter, self.fuselage_length, self.nose_width_, self.nose_height_, \
        self.cockpit_height_, self.cockpit_length_, self. cockpit_width_, \
        self.cockpit_position_x_, self.cockpit_position_y_, self.cockpit_position_z_, \
        self.nose_length_, self.nose_position_z_, self.section_1_width_, self.section_1_height_, \
        self.section_1_length_, self.section_1_position_z_, \
        self.section_2_width_, self.section_2_height_, self.section_2_length_, \
        self.section_2_position_z_, \
        self.section_3_width_, self.section_3_height_, \
        self.section_3_length_, \
        self.section_3_position_z_, \
        self.tip_width_, self.tail_height_, self.tail_width_, self.tip_height_,\
        self.tail_length_, self.tail_position_z_, \
            = read_boom_data(self.text)

    def get_current_loft(self):
        interval = 2
        self.read_parameters()
        sections = [self.root_position_x_,
                    self.root_position_x_+self.nose_length_,
                    self.root_position_x_+self.section_1_length_ + self.nose_length_,
                    self.root_position_x_+self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                    self.root_position_x_+self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                    self.root_position_x_+(self.tail_length_ / 2) + self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                    self.root_position_x_+(self.tail_length_) + self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                    ]

        width = [
            0.00,
            self.nose_width_,
            self.section_1_width_,
            self.section_2_width_,
            self.section_3_width_,
            self.tail_width_,
            self.tip_width_,
        ]

        height = [
            0.00,
            self.nose_height_,
            self.section_1_height_,
            self.section_2_height_,
            self.section_3_height_,
            self.tail_height_,
            self.tip_height_,
        ]

        z_position = [
            self.root_position_z_+self.nose_tip_position_,
            self.root_position_z_ +self.nose_position_z_,
            self.root_position_z_ +self.section_1_position_z_,
            self.root_position_z_ + self.section_2_position_z_,
            self.root_position_z_ + self.section_3_position_z_,
            self.root_position_z_ +self.tail_position_z_,
            self.root_position_z_ +self.tail_tip_position_]

        profiles=[self.nose_profile_,self.nose_profile_,
        self.section_1_profile_, self.section_2_profile_,
        self.section_3_profile_,self.tail_profile_,self.tail_profile_
                  ]


        n = random.random()
        self.fuselage = self.fuselages.create_fuselage(f"fuse{n}{self.iter}", len(sections), self.fuselage_profile)
        self.iter = +1

        for (x, w,h, z,profile, index) in zip(sections, width,height, z_position, profiles,range(1, len(sections)+1)):
            section = self.fuselage.get_section(index)
            sectionElement = section.get_section_element(1)
            sectionElement.set_profile_uid(profile)
            sectionElementCenter = sectionElement.get_ctigl_section_element()
            sectionElementCenter.set_center(tigl3.geometry.CTiglPoint(x
                                                                      ,self.root_position_y_
                                                                      ,z))


            sectionElementCenter.set_width(w)
            sectionElementCenter.set_height(h)

        loft=[]
        loft.append(self.fuselage.get_loft().shape())
        if self.cockPitDesign:
            WTBFZ = (self.fuselage_diameter / 2) + self.cockpit_position_z_  # 787: 0.2
            WTBFheight = self.cockpit_height_  # 787:2.7
            WTBFwidth = self.cockpit_width_
            WTBFXCentre = self.cockpit_position_x_  # 787: 23.8
            WTBFlength = self.cockpit_length_  # 787:26
            WBF_shape = make_ellipsoid([WTBFXCentre, self.cockpit_position_y_, WTBFZ], WTBFlength, WTBFwidth,
                                       WTBFheight)
            loft.append(WBF_shape)

        if self.xy_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xyplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.xz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.yz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_yzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        return loft


