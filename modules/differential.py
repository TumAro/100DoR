from math import cos, sin

class DifferentialKinematics:
    def __init__(self, radius, axle_length):
        self.wl = 0    # left wheel velocity
        self.wr = 0    # right wheel velocity
        self.r = radius  # wheel radius
        self.l = axle_length


        # linear velocity of wheels
        self.vl = self.wl*radius
        self.vr = self.wr*radius

        self.v = (self.vl + self.vr) / 2
        self.w = (self.vr - self.vl) / self.l

        # pos
        self.x = 0
        self.y = 0
        self.a = 0

    def updateVel(self, wl, wr,):
         # linear velocity of wheels
        self.vl = wl*self.r
        self.vr = wr*self.r

        self.v = (self.vl + self.vr) / 2
        self.w = (self.vr - self.vl) / self.l


    def update(self, wl, wr, a, dt):
        self.updateVel(wl=wl, wr=wr)
        self.x = self.x + self.v * cos(a) * dt
        self.y = self.y + self.v * sin(a) * dt
        self.a = a + self.w * dt 

        return (self.x, self.y, self.a)