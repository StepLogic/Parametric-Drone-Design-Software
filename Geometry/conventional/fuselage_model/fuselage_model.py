import random

import numpy as np
import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper

from GUI.window.cad.airconics_tools import make_ellipsoid
from Utils.data_objects.boom_placeholders import default_nose_position_x
from Utils.database.geometry.boom_database import read_boom_data
from Utils.maths import math_library


class fuselage_model():
    def __init__(self, config=None, text="", boom_type_="", design_type_=""):
        super().__init__()

        self.text = text
        self.boom_type_ = boom_type_
        self.design_type_ = design_type_
        self.fuselage_diameter = 0
        self.fuselage_length = 0
        self.nose_radius_ = 0
        self.nose_length_ = 0
        self.iter=0
        self.section_1_radius_ = 0
        self.section_1_length_ = 0
        self.section_2_radius_ = 0
        self.section_2_length_ = 0
        self.section_3_radius_ = 0
        self.section_3_length_ = 0
        self.tip_radius_ = 0
        self.tail_radius_ = 0
        self.tail_length_ = 0
        self.current_lofts = None
        self.update = False
        self.prev_name = ""
        self.fuselage_profile = "circularProfile"
        self.fuselages = config.get_fuselages()
        self.fuselage = None


    def read_parameters(self):
        self.cockitDesign,self.nose_tip_position_,self.tail_tip_position_,self.fuselage_diameter, self.fuselage_length, self.nose_radius_, \
        self.cockpit_height_, self.cockpit_length_, self.cockpit_width_, self.cockpit_position_x_, \
        self.cockpit_position_y_, self.cockpit_position_z_ ,\
        self.nose_length_, self.nose_position_z_, self.section_1_radius_, \
        self.section_1_length_, self.section_1_position_z_, \
        self.section_2_radius_, self.section_2_length_, \
        self.section_2_position_z_, \
        self.section_3_radius_, \
        self.section_3_length_, \
        self.section_3_position_z_, \
        self.tip_radius_, self.tail_radius_, \
        self.tail_length_, self.tail_position_z_ = \
            read_boom_data(self.text)

    def get_current_loft(self):
        interval=1
        self.read_parameters()
        sections=[self.nose_length_,
                  self.section_1_length_ + self.nose_length_,
                  self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                  self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                  (self.tail_length_/2) + self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                  self.tail_length_ + self.section_3_length_ + self.section_2_length_ + self.section_1_length_ + self.nose_length_,
                  ]

        radius=[
            0.00,
            self.nose_radius_,
            self.section_1_radius_,
            self.section_2_radius_,
            self.section_3_radius_,
            self.tail_radius_,
            self.tip_radius_,
        ]

        z_position=[
            self.nose_tip_position_,
            self.nose_position_z_,
            self.section_1_position_z_,
            self.section_2_position_z_,
            self.section_3_position_z_,
            self.tail_position_z_,
             self.tail_tip_position_]
        x_=[]
        x_.extend(np.linspace(default_nose_position_x,sections[0],num=interval))
        x_.extend(np.linspace(sections[0], sections[1],num=interval))
        x_.extend(np.linspace(sections[1], sections[2],num=interval))
        x_.extend(np.linspace(sections[2], sections[3],num=interval))
        x_.extend(np.linspace(sections[3], sections[4],num=interval))
        x_.extend(np.linspace(sections[4], sections[5],num=interval))

        radii=[]
        radii.extend(np.linspace(radius[0], radius[1],num=interval))
        radii.extend(np.linspace(radius[1], radius[2],num=interval))
        radii.extend(np.linspace(radius[2], radius[3],num=interval))
        radii.extend(np.linspace(radius[3], radius[4],num=interval))
        radii.extend(np.linspace(radius[4], radius[5],num=interval))
        radii.extend(np.linspace(radius[6],radius[5],num=interval))
        print(radius[6])
        z_ = []
        z_.extend(np.linspace(z_position[0], z_position[1],num=interval))
        z_.extend(np.linspace(z_position[1],z_position[2],num=interval))
        z_.extend(np.linspace(z_position[2], z_position[3],num=interval))
        z_.extend(np.linspace(z_position[3], z_position[4],num=interval))
        z_.extend(np.linspace(z_position[4], z_position[5],num=interval))
        z_.extend(np.linspace(z_position[5], z_position[6],num=interval,endpoint=True))
        n = random.random()
        self.fuselage = self.fuselages.create_fuselage(f"fuse{n}{self.iter}", len(x_), self.fuselage_profile)
        self.iter=+1

        for (x,rad,z,index) in zip(x_,radii,z_,range(1,len(x_)+1)):
            section = self.fuselage.get_section(index)
            sectionElement = section.get_section_element(1)
            sectionElementCenter = sectionElement.get_ctigl_section_element()
            sectionElementCenter.set_center(tigl3.geometry.CTiglPoint(x
                                                        , 0
                                                        , z))

            sectionElementCenter.set_area(math_library.getArea(rad))
        if self.cockitDesign:
            WTBFZ = (self.fuselage_diameter/2)+self.cockpit_position_z_  # 787: 0.2
            WTBFheight = self.cockpit_height_  # 787:2.7
            WTBFwidth = self.cockpit_width_
            WTBFXCentre = self.cockpit_position_x_# 787: 23.8
            WTBFlength = self.cockpit_length_  # 787:26
            WBF_shape = make_ellipsoid([WTBFXCentre, self.cockpit_position_y_, WTBFZ], WTBFlength, WTBFwidth, WTBFheight)
            return [self.fuselage.get_loft().shape(),WBF_shape]
        print(self.fuselage.get_loft().shape())
        return [self.fuselage.get_loft().shape()]




