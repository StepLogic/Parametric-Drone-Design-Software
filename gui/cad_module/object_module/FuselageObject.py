import numpy as np

import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper
from utils import MathLibrary


class FuselageObject():
    def __init__(self,params,aircraft,viewer,update):
        self.params=params
        self.aircraft=aircraft
        self.viewer = viewer
        self.update=update



    def modify_parameters(self):

        lofts = []
        # create main wing and display for a few frames
        if self.update:
            fuselages = self.aircraft.get_fuselages()
            fuselage = fuselages.get_fuselage("fuselage")
        else:
            fuselages = self.aircraft.get_fuselages()
            fuselage = fuselages.create_fuselage("fuselage", 5, "fuselageCircleProfileuID")

        fuselage.set_length(self.params["fuselage"]["fuselage_length"])

        # shrink nose to a point
        s1 = fuselage.get_section(1)
        s1e1 = s1.get_section_element(1)
        s1e1ce = s1e1.get_ctigl_section_element()
        s1e1ce.set_center(tigl3.geometry.CTiglPoint(self.params["fuselage"]["nose_center_position_x"]
                                                    ,self.params["fuselage"]["nose_center_position_y"]
                                                    ,self.params["fuselage"]["nose_center_position_z"]))
        s1e1ce.set_area(MathLibrary.getArea(self.params["fuselage"]["nose_radius"]))

        # move second section towards the nose
        s2 = fuselage.get_section(2)
        s2e1 = s2.get_section_element(1)
        s2e1ce = s2e1.get_ctigl_section_element()
        s2e1ce.set_center(tigl3.geometry.CTiglPoint(self.params["fuselage"]["section_2_center_position_x"]
                                                    ,self.params["fuselage"]["section_2_center_position_y"]
                                                    ,self.params["fuselage"]["section_2_center_position_z"]))
        s2e1ce.set_area(MathLibrary.getArea(self.params["fuselage"]["section_2_radius"]))

        # move second section towards the nose
        s3 = fuselage.get_section(3)
        s3e1 = s3.get_section_element(1)
        s3e1ce = s3e1.get_ctigl_section_element()
        s3e1ce.set_center(tigl3.geometry.CTiglPoint(self.params["fuselage"]["section_3_center_position_x"]
                                                    ,self.params["fuselage"]["section_3_center_position_y"]
                                                    ,self.params["fuselage"]["section_3_center_position_z"]))
        s3e1ce.set_area(self.params["fuselage"]["section_3_radius"])

        # move fourth section towards the tail
        s4 = fuselage.get_section(4)
        s4e1 = s4.get_section_element(1)
        s4e1ce = s4e1.get_ctigl_section_element()
        s4e1ce.set_center(tigl3.geometry.CTiglPoint(self.params["fuselage"]["section_4_center_position_x"]
                                                    ,self.params["fuselage"]["section_4_center_position_y"]
                                                    ,self.params["fuselage"]["section_4_center_position_z"]))
        s4e1ce.set_area(self.params["fuselage"]["section_4_radius"])

        # transform the tail
        tail_idx = fuselage.get_section_count()
        st = fuselage.get_section(tail_idx)
        ste1 = st.get_section_element(1)
        ste1ce = ste1.get_ctigl_section_element()
        ste1ce.set_center(tigl3.geometry.CTiglPoint(self.params["fuselage"]["tail_center_position_x"]
                                                    ,self.params["fuselage"]["tail_center_position_y"]
                                                    ,self.params["fuselage"]["tail_center_position_z"]))
        tail_angle = np.deg2rad(self.params["fuselage"]["tail_angle"])
        ste1ce.set_normal(tigl3.geometry.CTiglPoint(np.cos(tail_angle), 0, np.sin(tail_angle)))
        ste1ce.set_width(self.params["fuselage"]["tail_radius"])
        ste1ce.set_height(self.params["fuselage"]["tail_radius"])
        lofts.append(fuselage.get_loft())
        return lofts
    def show_lofts(self,prev_loft, lofts):
        for loft in lofts:
            if (self.update):
                for l in prev_loft:
                    self.viewer.remove(l.shape())
                self.viewer.add(loft.shape())
            else:
                self.viewer.add(loft.shape())
                self.viewer._display.View.SetProj(-2, -1, 1)
                self.viewer._display.View.SetScale(90)

    def _display_lofts(self,prev_loft=[]):

        lofts = self.modify_parameters()
        self.show_lofts(prev_loft, lofts)

        return lofts
