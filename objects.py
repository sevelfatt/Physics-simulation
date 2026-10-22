from units import Charge
from formula import electrostaticForce
from ast import Tuple
from units import Energy
from formula import gravityForce
import numpy as np
import math
from units import Force
from units import Mass
from units import Meter, Velocity, Acceleration, Second


class Objects:
    def __init__(self, name: str, coor: dict, radius: Meter, mass: Mass, charge: Charge, color: Tuple=(0,0,0)):
        self.color=color
        self.coor = coor
        self.radius = radius
        self.mass = mass
        self.charge = charge

        # Instance variable — setiap objek punya state sendiri
        self.a = dict(x=Acceleration(0), y=Acceleration(0))
        self.v = dict(x=Velocity(0), y=Velocity(0))
        self.f = dict(force=dict(x=Force(0), y=Force(0)))
        self.ke = 0
        self.name = name


    def bounce(self, width: int, height: int, pixel_per_meter):
        width /= 2
        height /= 2

        if (self.coor["x"] - self.radius).to_px(pixel_per_meter) < -width and self.v["x"].nilai < 0:
            self.coor["x"] = Meter(self.radius.nilai-(width/pixel_per_meter))           # snap ke kiri
            self.v["x"] = -self.v["x"]
        elif (self.coor["x"] + self.radius).to_px(pixel_per_meter) > width and self.v["x"].nilai > 0:
            self.coor["x"] = Meter(width / pixel_per_meter - self.radius.nilai)  # snap ke kanan
            self.v["x"] = -self.v["x"]

        if (self.coor["y"] - self.radius).to_px(pixel_per_meter) < -height and self.v["y"].nilai < 0:
            self.coor["y"] = Meter(self.radius.nilai-(height/pixel_per_meter))           # snap ke lantai
            self.v["y"] = -self.v["y"]
        elif (self.coor["y"] + self.radius).to_px(pixel_per_meter) > height and self.v["y"].nilai > 0:
            self.coor["y"] = Meter(height / pixel_per_meter - self.radius.nilai)  # snap ke langit-langit
            self.v["y"] = -self.v["y"]
            

    def Update(self, dt):
        self.ke = 0.5 * self.mass.nilai * self.speed() ** 2

        net_forces=self.get_net_force()

        for axis in self.coor:
            self.a[axis]=Acceleration(net_forces[axis].nilai/self.mass.nilai)
            self.v[axis] += self.a[axis] * dt
            self.coor[axis] += self.v[axis] * dt  
        

    def SetVelocity(self, axis: str, v: Velocity):
        self.v[axis] = v

    def SetAcceleration(self, axis: str, a: Acceleration):
        self.a[axis] = a
        
    def ApplyForce(self, label: str, axis: str, f: Force):
        # 1. Initialize the label with an empty dictionary ONLY if it doesn't exist yet
        if label not in self.f:
            self.f[label] = {}
            
        # 2. Add or update the specific axis safely
        self.f[label][axis] = f
        
        print(f"applying {f} {axis} to {label}")
                
    def GravitationForce(self, targetObject: Objects):
        force = gravityForce(self, targetObject)
        
        self.ApplyForce(targetObject.name + "'s gravitation", "x", force["x"])
        self.ApplyForce(targetObject.name + "'s gravitation", "y", force["y"])

    def ElectrostaticForce(self, targetObject: Objects):
        force = electrostaticForce(self, targetObject)
        
        self.ApplyForce(targetObject.name + "'s electrostatic", "x", force["x"])
        self.ApplyForce(targetObject.name + "'s electrostatic", "y", force["y"])

    def speed(self) -> float:
        return math.hypot(self.v["x"].nilai, self.v["y"].nilai)

    def get_net_force(self):
        net_force = {"x": Force(0), "y": Force(0)}
        
        for label, force_axes in self.f.items():
            net_force["x"] += force_axes["x"]
            net_force["y"] += force_axes["y"]
                
        return net_force


        
        
