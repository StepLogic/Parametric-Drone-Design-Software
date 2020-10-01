from math import *

from scipy import interpolate

from analysis.structural_analysis.DataStructure.PointMass import PointMass


class WStructureClass:
    def __init__(self, m=1, z_le=0.0
                 , x_le=0.0
                 , y_le=1
                 , dihedral_angle=0
                 , sweep_angle=0
                 , mass=10
                 , x_rs=0
                 , x_fs=0
                 , x_ms=0
                 , spar_mass=0
                 , rib_mass=0
                 , number_of_ribs=3
                 , t_on_c=0.25
                 , chord_length=1
                 , span=7
                 , root_chord=1
                 , taper_ratio=1):

        #####################assign masses######
        self.x_rs = x_rs
        self.x_fs = x_fs
        self.x_ms = x_ms
        f_rs = spar_mass
        f_ms = spar_mass
        f_fs = spar_mass
        f_ribs = rib_mass * number_of_ribs
        f_skin = mass - (f_fs + f_rs + f_ms + f_ribs) * (10 ** -3)

        self.z_le = z_le
        self.x_le = x_le
        self.y_le = y_le
        self.dihedral_angle = radians(dihedral_angle)
        self.sweep_angle = radians(sweep_angle)
        self.mass = mass
        self.f_skin = f_skin
        self.f_rs = f_rs
        self.f_ms = f_ms
        self.f_fs = f_fs
        self.f_ribs = f_ribs
        self.t_on_c = t_on_c
        self.chord_length = chord_length
        self.span = int(span)
        self.root_chord = root_chord
        self.taper_ratio = taper_ratio

        self.mirror = m
        self.number_of_stations = 5
        self.cg_x = 0.0
        self.Ixz = 0.0
        self.Izz = 0.0
        self.Iyy = 0.0
        self.Ixx = 0.0
        self.cg_z = 0.0
        self.cg_y = 0.0
        self.wings_point_mass_list = []
        self.y_cg_list = []
        self.z_cg_list = []
        self.x_cg_list = []
        self.ita = 1
        self.total_area_list = []
        self.c_n = self.root_chord * (1 - self.ita * (1 - self.taper_ratio))
        self.m = self.mass

        self.approximate_boom_area()
        self.create_y_cg_list()
        self.create_x_cg_list()
        self.create_z_cg_list()
        self.create_mass_list()
        self.fill_wings_point_mass_list()
        self.estimate_x_cg()
        self.estimate_y_cg()
        self.estimate_z_cg()
        self.calculate_mass_moments()

    def approximate_boom_area(self):
        for i in range(0, self.span):
            area_list = []

            start_values = [0, 0.5 * self.x_fs, 0.5 * (self.x_fs + self.x_ms), 0.5 * (self.x_ms + self.x_rs),
                            0.5 * (1 + self.x_rs)]
            end_values = [0.5 * self.x_fs, 0.5 * (self.x_fs + self.x_ms), 0.5 * (self.x_ms + self.x_rs),
                          0.5 * (1 + self.x_rs), 1]
            for k, j in zip(start_values, end_values):
                x = k
                total_area = 0
                while x < j:
                    total_area += (10 * self.c_n ** 2) * self.t_on_c * (
                            (0.197933 * x ** (3 / 2)) - (0.063 * x ** 2) - (0.1172 * x ** 3) + (0.071075 * x ** 4) - (
                            0.0203 * x ** 5))
                    x += 0.01
                area_list.append(total_area)
            self.total_area_list.append(area_list)

    def create_y_cg_list(self):
        ########YCG##########
        y_cg_list = []
        iter_number = len(self.total_area_list) + 1

        for i in range(1, iter_number):
            y_cg = self.y_le + (i / iter_number) * (self.span / 2) - (0.5) * ((self.span / 2) / iter_number)
            y_cg_list.append(y_cg)
        temp_list = y_cg_list

        for j in range(0, len(self.total_area_list)):
            container = []
            for i in range(0, len(self.total_area_list[0])):
                container.append(temp_list[j])
            self.y_cg_list.append(container)

    def create_z_cg_list(self):
        iter_number = len(self.total_area_list)
        for i in range(0, iter_number):
            z_cg = self.z_le + self.y_cg_list[i][0] * tan(self.dihedral_angle)
            self.z_cg_list.append(z_cg)
        temp_list = self.z_cg_list
        self.z_cg_list = []

        for j in range(0, len(self.total_area_list)):
            container = []
            for i in range(0, len(self.total_area_list[0])):
                container.append(temp_list[j])
            self.z_cg_list.append(container)

        #######################XCG####################

    def create_x_cg_list(self):
        self.iter_number = len(self.total_area_list)
        self.c_i_list = []
        self.lengths = []
        for j in range(0, self.iter_number):

            start_values = [0, 0.5 * self.x_fs, 0.5 * (self.x_fs + self.x_ms), 0.5 * (self.x_ms + self.x_rs),
                            0.5 * (1 + self.x_rs)]
            end_values = [0.5 * self.x_fs, 0.5 * (self.x_fs + self.x_ms), 0.5 * (self.x_ms + self.x_rs),
                          0.5 * (1 + self.x_rs), 1]
            x_apex = self.x_le + self.y_cg_list[j][0] * self.sweep_angle
            x_list = []
            self.c_i_s = []
            temp_l = []
            for i in range(1, len(self.total_area_list[0]) + 1):
                c_i = self.root_chord * (1 - ((i - 0.5) * (1 - self.taper_ratio)) / (len(self.total_area_list[0]) + 1))
                self.c_i_s.append(c_i)

                L = abs(start_values[i - 1] - end_values[i - 1])

                temp_l.append(L)
                if i == 1:
                    x_cg = x_apex + (L / 2) * c_i
                elif i == 2:
                    x_cg = x_apex + (self.x_fs) * c_i
                elif i == 3:
                    x_cg = x_apex + (self.x_ms) * c_i
                elif i == 4:
                    x_cg = x_apex + (self.x_rs) * c_i
                else:
                    x_cg = x_apex + ((L + 1) / 2) * c_i

                x_list.append(x_cg)
            self.x_cg_list.append(x_list)
            self.c_i_list.append(self.c_i_s)
            self.lengths.append(temp_l)
        ##############MASS###############################

    def create_mass_list(self):
        self.mass_list = []
        for i in range(0, self.iter_number):
            temp_list = []
            sum_of_c_i = 0
            for j in self.c_i_list[i]:
                sum_of_c_i += j
            for j in range(0, len(self.total_area_list[0])):
                a = -self.m * (((self.root_chord * (1 - self.taper_ratio)) / sum_of_c_i) / self.number_of_stations) ** 2
                c_1 = (2 / self.span) * ((self.m / 2) - ((self.span ** 2) / 8) * a)
                a_1 = ((self.span ** 2) / (4 * len(self.total_area_list[0]))) * (a / 2) + (
                        self.span / (2 * len(self.total_area_list[0]))) * c_1
                b_1 = (3 * (self.span ** 2) / (2 * len(self.total_area_list[0]))) * (a / 4) + (
                        self.span / (2 * len(self.total_area_list[0]))) * c_1
                PAR = b_1 - a_1
                L = self.lengths[i][j]
                sum_of_areas = 0
                for k in self.total_area_list[i]:
                    sum_of_areas += k
                if i == 0:
                    m = L * self.f_skin + (self.total_area_list[i][j] / sum_of_areas) * self.f_ribs + (
                            self.total_area_list[i][j] + PAR)
                elif i == 1:
                    m = (L - self.lengths[i][j - 1]) * self.f_skin + (self.total_area_list[i][j] / sum_of_areas) * (
                            self.f_ribs + self.f_fs) + (
                                self.total_area_list[i][j] + PAR)
                elif i == 3:
                    m = (L - self.lengths[i][j - 1]) * self.f_skin + (self.total_area_list[i][j] / sum_of_areas) * (
                            self.f_ribs + self.f_ms) + (
                                self.total_area_list[i][j] + PAR)
                elif i == 4:
                    m = (L - self.lengths[i][j - 1]) * self.f_skin + (self.total_area_list[i][j] / sum_of_areas) * (
                            self.f_ribs + self.f_rs) + (
                                self.total_area_list[i][j] + PAR)
                else:
                    m = (1 - self.lengths[i][j - 1]) * self.f_skin + (
                            self.total_area_list[i][j] / sum_of_areas) * self.f_ribs + (
                                self.total_area_list[i][j] + PAR)
                temp_list.append(m)
                self.mass_list.append(temp_list)

        ################Y_CG##############################

    def fill_wings_point_mass_list(self):
        self.wings_point_mass_list = []
        for x, y, z, mass_list in zip(self.x_cg_list, self.y_cg_list, self.z_cg_list, self.mass_list):
            temp_list = []
            for l, m, n, k in zip(x, y, z, mass_list):
                point = PointMass(x_cg=l, y_cg=self.mirror * m, z_cg=n, mass=k)
                temp_list.append(point)
            self.wings_point_mass_list.append(temp_list)

        #######X_CG##########################

    def estimate_x_cg(self):
        x_diffs = []
        x_lengths = []
        i = self.x_le
        max_count=self.x_le+self.chord_length

        while i < max_count :

            pre_pivot_sum_of_moments = 0
            post_pivot_sum_of_moments = 0
            for l in self.wings_point_mass_list:
                for k in l:

                    if k.x_cg < i:

                        pre_pivot_sum_of_moments += (k.mass * (i - k.x_cg))
                    else:
                        post_pivot_sum_of_moments += (k.mass * (i - k.x_cg))

            x_diff = pre_pivot_sum_of_moments + post_pivot_sum_of_moments

            x_diffs.append(x_diff)
            x_lengths.append(i)
            i += 0.01

        cg_x_function = interpolate.interp1d(x_diffs, x_lengths)
        self.cg_x = cg_x_function(0.0)

    #######X_CG##########################
    def estimate_y_cg(self):
        y_diffs = []
        y_lengths = []
        i = self.y_le
        while abs(i) < self.y_le+self.span:
            pre_pivot_sum_of_moments = 0
            post_pivot_sum_of_moments = 0
            for l in self.wings_point_mass_list:
                for k in l:
                    if k.y_cg < i:
                        pre_pivot_sum_of_moments += (k.mass * (i - k.y_cg))

                    else:

                        post_pivot_sum_of_moments += (k.mass * (i - k.y_cg))

            y_diff = pre_pivot_sum_of_moments + post_pivot_sum_of_moments
            y_diffs.append(y_diff)
            y_lengths.append(i)
            i += (self.mirror * 0.01)
        cg_y_function = interpolate.interp1d(y_diffs, y_lengths)
        self.cg_y = cg_y_function(0.0)

    #######Z_CG##########################
    def estimate_z_cg(self):
        z_diffs = []
        z_lengths = []
        max_count = self.z_le + (self.t_on_c * self.chord_length)
        i = -max_count
        while i < max_count:
            pre_pivot_sum_of_moments = 0
            post_pivot_sum_of_moments = 0
            for l in self.wings_point_mass_list:
                for k in l:
                    if k.z_cg < i:
                        pre_pivot_sum_of_moments += (k.mass * (i - k.z_cg))
                    else:
                        post_pivot_sum_of_moments += (k.mass * (i - k.z_cg))

            z_diff = pre_pivot_sum_of_moments + post_pivot_sum_of_moments
            z_diffs.append(z_diff)
            z_lengths.append(i)
            i += 0.01
        cg_z_function = interpolate.interp1d(z_diffs, z_lengths)
        self.cg_z = cg_z_function(0.0)

    def calculate_mass_moments(self):
        for l in self.wings_point_mass_list:
            for k in l:
                k.Ixx = k.mass * ((k.y_cg - self.cg_y) ** 2 + (k.z_cg - self.cg_z) ** 2)
                k.Iyy = k.mass * ((k.z_cg - self.cg_z) ** 2 + (k.x_cg - self.cg_x) ** 2)
                k.Izz = k.mass * ((k.x_cg - self.cg_x) ** 2 + (k.y_cg - self.cg_y) ** 2)
                k.Ixz = k.mass * ((k.x_cg - self.cg_x) + (k.z_cg - self.cg_z))
        for l in self.wings_point_mass_list:
            for k in l:
                self.Ixx += k.Ixx
                self.Iyy += k.Iyy
                self.Izz += k.Izz
                self.Ixz += k.Ixz
