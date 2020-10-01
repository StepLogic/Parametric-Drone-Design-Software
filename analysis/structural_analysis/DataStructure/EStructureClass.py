class EStructureClass:
    def __init__(self, mass=10, x=0, y=0, z=0, height=0, width=0, length=0):
        self.cg_x = x
        self.cg_y = y
        self.cg_z = z
        self.mass = mass
        self.width = width
        self.height = height
        self.length = length
        self.Ixx = 0.0
        self.Iyy = 0.0
        self.Izz = 0.0
        self.Ixz = 0.0
    def setXYZ(self, x, y, z):
        self.cg_x = x
        self.cg_y = y
        self.cg_z = z

    def estimate_inertia(self):
        self.Ixx = (self.mass * (self.length - self.height) / 12)
        self.Iyy = (self.mass * (self.length - self.width) / 12)
        self.Izz = (self.mass * (self.height - self.width) / 12)
        self.Ixz = 0.0
