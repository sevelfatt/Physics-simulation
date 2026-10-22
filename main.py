from units import Charge, Velocity, Mass, Meter
from simulator import Simulator
from objects import Objects

# ── Hydrogen atom constants ───────────────────────────────────────────────────
BOHR_RADIUS  = 5.29e-11   # meters  (ground-state orbital radius)
V_ORBITAL    = 2.187e6    # m/s     (speed for circular orbit at Bohr radius)
#              v = sqrt(k·e² / m_e·r₀)

# ── Particles ─────────────────────────────────────────────────────────────────
proton = Objects(
    "proton",
    {"x": Meter(0), "y": Meter(0)},
    Meter(0.84e-11),          # radius
    Mass(1.673e-27),          # kg
    Charge(1),                # +1 e
    color=(255, 100, 80),
)

# Electron starts at Bohr radius on the +x axis, velocity pointing +y → circular orbit
electron = Objects(
    "electron",
    {"x": Meter(BOHR_RADIUS), "y": Meter(0)},
    Meter(1e-12),             # radius (visual only)
    Mass(9.109e-31),          # kg
    Charge(-1),               # −1 e
    color=(80, 160, 255),
)
electron.SetVelocity("y", Velocity(V_ORBITAL))

# ── Simulator ─────────────────────────────────────────────────────────────────
# Orbital period T = 2π·r₀ / v ≈ 1.52e-16 s
# time_scale = 1e-15  →  one orbit takes ~0.15 real seconds (~6-7 orbits/s)
# physics_dt = 1e-18  →  ~150 physics steps per orbit (good Euler accuracy)
# pixels_per_meter = 1e12  →  Bohr radius ≈ 53 px on screen
simulator = Simulator(
    time_scale=1e-17,
    objects=[proton, electron],
    bounce=False,
    physics_dt=1e-18,
    background_color=(8, 8, 18),
    gravity=False,             # gravity negligible at atomic scale
    electromagnetic=True,
    width_px=1000,
    height_px=1000,
    pixels_per_meter=10e11,
)
simulator.run()