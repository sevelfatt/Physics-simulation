from formula import gravityForce
import numpy as np
from units import Force
from units import Mass
from units import Meter, Velocity, Acceleration, Second


class Objects:
    def __init__(self, coor: dict, radius: Meter, mass: Mass, dt: Second):
        self.coor = coor
        self.radius = radius
        self.mass = mass
        self.dt = dt
        # Instance variable — setiap objek punya state sendiri
        self.a = {"x": Acceleration(0), "y": Acceleration(0)}
        self.v = {"x": Velocity(0), "y": Velocity(0)}
        self.f = {"x": Force(0), "y": Force(0)}

    def bounce(self, width: int, height: int):
        from units import PIXELS_PER_METER

        if (self.coor["x"] - self.radius).to_px() < 0 and self.v["x"].nilai < 0:
            self.coor["x"] = Meter(self.radius.nilai)           # snap ke kiri
            self.v["x"] = -self.v["x"]
        elif (self.coor["x"] + self.radius).to_px() > width and self.v["x"].nilai > 0:
            self.coor["x"] = Meter(width / PIXELS_PER_METER - self.radius.nilai)  # snap ke kanan
            self.v["x"] = -self.v["x"]

        if (self.coor["y"] - self.radius).to_px() < 0 and self.v["y"].nilai < 0:
            self.coor["y"] = Meter(self.radius.nilai)           # snap ke lantai
            self.v["y"] = -self.v["y"]
        elif (self.coor["y"] + self.radius).to_px() > height and self.v["y"].nilai > 0:
            self.coor["y"] = Meter(height / PIXELS_PER_METER - self.radius.nilai)  # snap ke langit-langit
            self.v["y"] = -self.v["y"]
            

    def Update(self):
        for i in self.f:
            self.f[i] = self.a[i] * self.mass
        for i in self.coor:
            self.v[i] += self.a[i] * self.dt   # kecepatan dulu
            self.coor[i] += self.v[i] * self.dt  # baru posisi
        

    def NewVelocity(self, axis: str, v: Velocity):
        self.v[axis] = v

    def NewAcc(self, axis: str, a: Acceleration):
        self.a[axis] = a
        self.f[axis] = self.a[axis] * self.mass  # = bukan +=
        
    def NewForce(self, axis: str, f: Force):
        self.f[axis] = f
        self.a[axis] = Acceleration(f.nilai / self.mass.nilai)  # F = ma → a = F/m

    def GravitationForce(self, targetObject: Objects):
        forces = gravityForce(self, targetObject)

        for axis in self.f:
            self.NewForce(axis, forces[axis])

            
    
        
        
