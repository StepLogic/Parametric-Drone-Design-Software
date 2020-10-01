from math import *
from scipy import interpolate
import matplotlib.pyplot as plt

from analysis.structural_analysis.DataStructure.PointMass import PointMass
from utils.MathLibrary import check_if_nan


class FStructureClass:
    def __init__(self, specification_section_list=None, x=None,mass=10):

        self.mass=mass
        x, y = self.interpolate_fuselage_coordinates(x_list=x, section_list=specification_section_list)
        z = y
        sum_of_areas, area_of_sections = self.approximate_area_of_each_section(x_list=x, section_list=z)
        initial_mass_list = self.calculate_initial_mass_per_boom(area_of_sections=area_of_sections, mass=self.mass,
                                                                 sum_of_areas=sum_of_areas)
        y_list, z_list, self.fuselage_point_mass_list = self.position_point_masses(mass_list=initial_mass_list, z=z, y=y,
                                                                              x=x)
        y_moments_list = self.sum_moment_arms(y_list, self.fuselage_point_mass_list)
        z_moments_list = self.sum_moment_arms(z_list, self.fuselage_point_mass_list)
        self.cg_x = self.approximate_cg_x(x=x)
        self.cg_y = self.approximate_cg_y(y_moments_list=y_moments_list, max_y_pos=self.get_maximum(y))
        self.cg_z = self.approximate_cg_z(z_moments_list=z_moments_list, max_z_pos=self.get_maximum(z))
        self.fuselage_point_mass_list = self.calculate_point_mass_moments(self.fuselage_point_mass_list, cg_x=self.cg_x,
                                                                          cg_y=self.cg_y,
                                                                          cg_z=self.cg_z)
        self.Ixx, self.Iyy, self.Izz, self.Ixz = self.calculate_total_fuselage_mass_moments(self.fuselage_point_mass_list)


    def sum_moment_arms(self, list=[], fuselage_point_mass_list=[]):
        sum_moments_1 = 0
        sum_moments_2 = 0
        sum_moments_3 = 0
        sum_moments_4 = 0
        sum_moments_5 = 0
        sum_moments_6 = 0
        sum_moments_7 = 0
        sum_moments_8 = 0
        moments_list = [0]

        for j in range(0, len(fuselage_point_mass_list)):
            l = fuselage_point_mass_list[j]
            arm = list[j]

            for i in range(1, int(len(l))):
                if i == 1:
                    sum_moments_1 += (l[i].mass * arm[i])
                elif i == 2:
                    sum_moments_2 += (l[i].mass * arm[i])
                elif i == 3:
                    sum_moments_3 += (l[i].mass * arm[i])
                elif i == 4:
                    sum_moments_4 += (l[i].mass * arm[i])
                elif i == 5:
                    sum_moments_2 += (l[i].mass * arm[i])
                elif i == 6:
                    sum_moments_3 += (l[i].mass * arm[i])
                elif i == 7:
                    sum_moments_4 += (l[i].mass * arm[i])
                elif i == 8:
                    sum_moments_8 += (l[i].mass * arm[i])
                else:
                    pass
        moments_list.append(sum_moments_1)
        moments_list.append(sum_moments_2)
        moments_list.append(sum_moments_3)
        moments_list.append(sum_moments_4)
        moments_list.append(sum_moments_5)
        moments_list.append(sum_moments_6)
        moments_list.append(sum_moments_7)
        moments_list.append(sum_moments_8)
        return moments_list

    def get_maximum(self, list=[]):
        max = 0
        for number in list:
            if number > max:
                max = number
        return max

    def interpolate_fuselage_coordinates(self, x_list, section_list):
        y_temp = []
        x_temp = []
        interp_func = interpolate.interp1d(x_list, section_list, kind="cubic")
        for l in x_list:
            if l < x_list[len(x_list) - 1] + 0.1:
                for count in range(0, 10):
                    count /= 10
                    if l + count < x_list[len(x_list) - 1] + 0.000001:
                        interp = interp_func(l + count)
                        x_temp.append(l + count)
                        y_temp.append(interp)
        return x_temp, y_temp

    def approximate_area_of_each_section(self, x_list=[], section_list=[]):
        sum_of_areas = 0
        area_of_sections = []
        for i in range(0, len(section_list)):
            if i == 0:
                length = 0
            else:
                length = x_list[i] - x_list[(i - 1)]

            area = pi * (section_list[i]) * (section_list[i]) * (length / self.get_maximum(x_list))
            sum_of_areas += area
            area_of_sections.append(area)
        return sum_of_areas, area_of_sections

    def calculate_initial_mass_per_boom(self, area_of_sections=[], mass=0, sum_of_areas=0):
        mass_list = []
        for i in area_of_sections:
            mpm = mass * (i / sum_of_areas)
            mass_list.append(mpm)
        return mass_list

    def position_point_masses(self, mass_list=[], z=[], y=[], x=[]):
        z_list = []
        y_list = []
        r_list = []
        theta_list = []
        alpha_list = []
        arc_list = []
        modified_point_mass_list = []
        fuselage_point_mass_list = []

        for i in range(0, len(mass_list)):
            circle = plt.Circle((0, 0), y[i])
            verts = circle.get_path().vertices
            trans = circle.get_patch_transform()
            points = trans.transform(verts)
            x_ = points[:, 0]
            y_d = points[:, 1]
            r = []
            x_main = []
            y_main = []

            for i in range(0, len(y_d), int(len(y_d) / 8)):
                rad = sqrt((y_d[i]) ** 2 + (x_[i]) ** 2)
                x_main.append(x_[i])
                y_main.append(y_d[i])
                r.append(rad)

            y_fus1 = y[i]
            y_fus2 = -y[i]

            z_fus1 = z[i]
            z_fus2 = 0
            z_fus3 = -z[i]
            rho_12 = 1
            rho_23 = 1
            r_1 = r[0]
            r_3 = r[1]
            r_2 = r[2]
            r_5 = r[3]
            r_4 = r[4]
            r_6 = r[5]
            r_7 = r[6]
            r_8 = r[7]

            theta_1 = atan(r_3 / r_1)
            theta_2 = radians(90) - theta_1
            theta_3 = -atan(r_5 / r_3)
            theta_4 = -(radians(90) - theta_3)
            theta_5 = theta_4
            theta_6 = theta_3
            theta_7 = theta_2
            theta_8 = theta_1

            temp_list = [0]
            temp_list.append(check_if_nan(theta_1))
            temp_list.append(check_if_nan(theta_2))
            temp_list.append(check_if_nan(theta_3))
            temp_list.append(check_if_nan(theta_4))
            temp_list.append(check_if_nan(theta_5))
            temp_list.append(check_if_nan(theta_6))
            temp_list.append(check_if_nan(theta_7))
            temp_list.append(check_if_nan(theta_8))
            theta_list.append(temp_list)
            alpha_1 = theta_1
            alpha_2 = (theta_1 + theta_2) / 2
            alpha_3 = (theta_1 + theta_2) / 2
            alpha_4 = (theta_3 + theta_4) / 2
            alpha_5 = theta_4
            alpha_6 = alpha_4
            alpha_7 = alpha_3
            alpha_8 = alpha_2

            temp_list = [0]
            temp_list.append(check_if_nan(alpha_1))
            temp_list.append(check_if_nan(alpha_2))
            temp_list.append(check_if_nan(alpha_3))
            temp_list.append(check_if_nan(alpha_4))
            temp_list.append(check_if_nan(alpha_5))
            temp_list.append(check_if_nan(alpha_6))
            temp_list.append(check_if_nan(alpha_7))
            temp_list.append(check_if_nan(alpha_8))
            alpha_list.append(temp_list)

            arc_1 = r_1 * alpha_1
            arc_2 = r_2 * alpha_2
            arc_3 = r_3 * alpha_3
            arc_4 = r_4 * alpha_4
            arc_5 = r_5 * alpha_5
            arc_6 = r_6 * alpha_6
            arc_7 = r_7 * alpha_7
            arc_8 = r_8 * alpha_8

            temp_list = [0]
            temp_list.append(check_if_nan(arc_1))
            temp_list.append(check_if_nan(arc_2))
            temp_list.append(check_if_nan(arc_3))
            temp_list.append(check_if_nan(arc_4))
            temp_list.append(check_if_nan(arc_5))
            temp_list.append(check_if_nan(arc_6))
            temp_list.append(check_if_nan(arc_7))
            temp_list.append(check_if_nan(arc_8))
            total_arc = 0
            for j in temp_list:
                total_arc += j
            arc_list.append(temp_list)

            y_cg1 = x_main[0]
            y_cg2 = x_main[1]
            y_cg3 = x_main[2]
            y_cg4 = x_main[3]
            y_cg5 = x_main[4]
            y_cg6 = x_main[5]
            y_cg7 = x_main[6]
            y_cg8 = x_main[7]
            temp_list = [0]

            temp_list.append(check_if_nan(y_cg1))
            temp_list.append(check_if_nan(y_cg2))
            temp_list.append(check_if_nan(y_cg3))
            temp_list.append(check_if_nan(y_cg4))
            temp_list.append(check_if_nan(y_cg5))
            temp_list.append(check_if_nan(y_cg6))
            temp_list.append(check_if_nan(y_cg7))
            temp_list.append(check_if_nan(y_cg8))

            y_list.append(temp_list)

            z_cg1 = y_main[0]
            z_cg2 = y_main[1]
            z_cg3 = y_main[2]
            z_cg4 = y_main[3]
            z_cg5 = y_main[4]
            z_cg6 = y_main[5]
            z_cg7 = y_main[6]
            z_cg8 = y_main[7]

            temp_list = [0]
            temp_list.append(check_if_nan(z_cg1))
            temp_list.append(check_if_nan(z_cg2))
            temp_list.append(check_if_nan(z_cg3))
            temp_list.append(check_if_nan(z_cg4))
            temp_list.append(check_if_nan(z_cg5))
            temp_list.append(check_if_nan(z_cg6))
            temp_list.append(check_if_nan(z_cg7))
            temp_list.append(check_if_nan(z_cg8))

            z_list.append(temp_list)

            mass_1 = self.modify_initial_mass(arc_of_point_mass=arc_1, total_arc=total_arc, initial_mass=mass_list[i])
            mass_2 = self.modify_initial_mass(arc_of_point_mass=arc_2, total_arc=total_arc, initial_mass=mass_list[i])
            mass_3 = self.modify_initial_mass(arc_of_point_mass=arc_3, total_arc=total_arc, initial_mass=mass_list[i])
            mass_4 = self.modify_initial_mass(arc_of_point_mass=arc_4, total_arc=total_arc, initial_mass=mass_list[i])
            mass_5 = self.modify_initial_mass(arc_of_point_mass=arc_5, total_arc=total_arc, initial_mass=mass_list[i])
            mass_6 = self.modify_initial_mass(arc_of_point_mass=arc_6, total_arc=total_arc, initial_mass=mass_list[i])
            mass_7 = self.modify_initial_mass(arc_of_point_mass=arc_7, total_arc=total_arc, initial_mass=mass_list[i])
            mass_8 = self.modify_initial_mass(arc_of_point_mass=arc_8, total_arc=total_arc, initial_mass=mass_list[i])

            temp_list = [0]
            temp_list.append(check_if_nan(mass_1))
            temp_list.append(check_if_nan(mass_2))
            temp_list.append(check_if_nan(mass_3))
            temp_list.append(check_if_nan(mass_4))
            temp_list.append(check_if_nan(mass_5))
            temp_list.append(check_if_nan(mass_6))
            temp_list.append(check_if_nan(mass_7))
            temp_list.append(check_if_nan(mass_8))
            modified_point_mass_list.append(temp_list)

        for y, z, mass, i in zip(y_list, z_list, modified_point_mass_list, range(0, len(mass_list))):
            x_v = x[i]
            area_1 = []
            area_1.append(PointMass(0, 0, 0, 0))
            for j in range(0, len(y)):
                point = PointMass(x_cg=x_v, y_cg=y[j], z_cg=z[j], mass=mass[j])
                area_1.append(point)
            fuselage_point_mass_list.append(area_1)
        return y_list, z_list, fuselage_point_mass_list

    def modify_initial_mass(self, arc_of_point_mass, total_arc, initial_mass):
        return initial_mass * (arc_of_point_mass / total_arc)

    def approximate_cg_x(self, x=[]):
        diffs = []
        for i in range(0, len(x)):
            pre_pivot_sum_of_moments_x = 0
            for j in range(0, i, 1):
                l = self.fuselage_point_mass_list[j]
                for k in l:
                    pre_pivot_sum_of_moments_x += k.mass * j

            post_pivot_sum_of_moments_x = 0

            for j in range(i, len(x)):
                l = self.fuselage_point_mass_list[j]

                for k in l:
                    post_pivot_sum_of_moments_x += k.mass * (j)

            x_dif = abs(pre_pivot_sum_of_moments_x) - abs(post_pivot_sum_of_moments_x)
            diffs.append(x_dif)

        cg_x_function = interpolate.interp1d(diffs, x, kind="linear")
        cg_x = cg_x_function(0.0)
        return cg_x

    def approximate_cg_y(self, y_moments_list=[], max_y_pos=None):
        y_pos = []
        max_y_pos = max_y_pos
        y_diffs = []
        y_center_value = 3

        for i in range(0, int(len(y_moments_list) / 2)):
            post_pivot_sum_of_moments_y = 0
            pre_pivot_sum_of_moments_y = 0
            for j in range(0, i):
                if j == 0 or j == int(len(y_moments_list) / 2):
                    pre_pivot_sum_of_moments_y += (y_moments_list[y_center_value + j])
                else:
                    pre_pivot_sum_of_moments_y += (
                                y_moments_list[y_center_value + j] + y_moments_list[y_center_value - j])

            for j in range(i, int(len(y_moments_list) / 2)):
                post_pivot_sum_of_moments_y += (y_moments_list[y_center_value + j] + y_moments_list[y_center_value - j])

            y_diff = pre_pivot_sum_of_moments_y - post_pivot_sum_of_moments_y
            y_diffs.append(y_diff)
            y_pos.append(max_y_pos + (i / int(len(y_moments_list) / 2)))
        cg_y_function = interpolate.interp1d(y_diffs, y_pos, kind="linear", fill_value="extrapolate")
        cg_y = cg_y_function(0.0)
        return cg_y

    def approximate_cg_z(self, z_moments_list=None, max_z_pos=None):
        z_pos = []

        z_diffs = []
        z_center_value = 5
        for i in range(0, int(len(z_moments_list) / 2)):
            post_pivot_sum_of_moments_z = 0
            pre_pivot_sum_of_moments_z = 0
            for j in range(0, i):
                if j == 0 or j == int(len(z_moments_list) / 2):
                    pre_pivot_sum_of_moments_z += (z_moments_list[z_center_value + j])
                else:
                    pre_pivot_sum_of_moments_z += (
                            z_moments_list[z_center_value + j] + z_moments_list[z_center_value - j])

            for j in range(i, int(len(z_moments_list) / 2)):
                if j == 0 or j == int(len(z_moments_list) / 2):
                    post_pivot_sum_of_moments_z += (
                            z_moments_list[z_center_value + j] + z_moments_list[z_center_value - j])
                else:
                    post_pivot_sum_of_moments_z += (z_moments_list[z_center_value + j])

            z_diff = pre_pivot_sum_of_moments_z - post_pivot_sum_of_moments_z
            z_diffs.append(z_diff)
            z_pos.append(max_z_pos + (i / int(len(z_moments_list) / 2)))

        cg_z_function = interpolate.interp1d(z_diffs, z_pos, kind="linear", fill_value="extrapolate")
        cg_z = cg_z_function(0.0)
        return cg_z

    def calculate_point_mass_moments(self, points_list, cg_x, cg_y, cg_z):
        for l in points_list:
            for k in l:
                k.Ixx = k.mass * ((k.y_cg - cg_y) ** 2 + (k.z_cg - cg_z) ** 2)
                k.Iyy = k.mass * ((k.z_cg - cg_z) ** 2 + (k.x_cg - cg_x) ** 2)
                k.Izz = k.mass * ((k.x_cg - cg_x) ** 2 + (k.y_cg - cg_y) ** 2)
                k.Ixz = k.mass * ((k.x_cg - cg_x) ** 2 + (k.z_cg - cg_z) ** 2)
        return points_list

    def calculate_total_fuselage_mass_moments(self, points_list):
        Ixx = 0.0
        Iyy = 0.0
        Izz = 0.0
        Ixz = 0.0
        for l in points_list:
            for k in l:
                Ixx += k.Ixx
                Iyy += k.Iyy
                Izz += k.Izz
                Ixz += k.Ixz
        return Ixx, Iyy, Izz, Ixz
