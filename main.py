from units import Acceleration
from units import Velocity
from hud import HUD
from units import Mass
from units import Meter
from simulator import Simulator
from objects import Objects
ball = Objects("earth", {"x": Meter(0), "y": Meter(0)}, Meter(6.371e6), Mass( 5.972e24), color=(20,80,127))
ball2 = Objects("moon", {"x": Meter(3.844e8), "y": Meter(0)}, Meter(1.737e6), Mass(7.342e22), color=(100,100,100))

ball2.SetVelocity("y", Velocity(1022))



simulator = Simulator(time_scale=3600*24, objects=[ball, ball2], bounce=True, physics_dt=10, background_color=(30,30,30), gravity=True, width_px=1000, height_px=1000, pixels_per_meter=10**-6)
simulator.run()