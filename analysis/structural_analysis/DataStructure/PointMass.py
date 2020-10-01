class PointMass():
    def __init__(self,x_cg,y_cg,z_cg,mass):
        self.x_cg=x_cg
        self.y_cg=y_cg
        self.z_cg=z_cg
        self.mass=mass
        self.Ixx=0
        self.Iyy=0
        self.Izz=0
        self.Ixz=0

