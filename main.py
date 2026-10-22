from units import Charge
from units import Acceleration
from units import Velocity
from hud import HUD
from units import Mass
from units import Meter
from simulator import Simulator
from objects import Objects

proton = Objects("positiveBall", {"x": Meter(10 ** -15), "y": Meter(0)}, Meter(0.84 * (10**-15)), Mass(1.673 * (10**-27)), Charge(1), color=(255,0,0))
electron = Objects("negativeBall", {"x": Meter(-(10 ** -15)), "y": Meter(0)}, Meter(10**-16), Mass(9.109 * (10**-31)), Charge(-1), color=(0,0,255))

electron.SetVelocity("y", Velocity(1))


simulator = Simulator(time_scale=1e-19, objects=[proton, electron], bounce=False, physics_dt=1e-21, background_color=(30,30,30), gravity=True, electromagnetic=True, width_px=1000, height_px=1000, pixels_per_meter=10e16)
simulator.run()