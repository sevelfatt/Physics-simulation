import numpy as np
from units import Force
from units import Mass
from units import Meter
from constants import G, K

def gravityForce(object_1, object_2):
    """Gaya pada object_1 akibat object_2 (menarik object_1 ke arah object_2)."""
    mass1 = object_1.mass.nilai
    mass2 = object_2.mass.nilai

    dx = object_2.coor["x"].nilai - object_1.coor["x"].nilai
    dy = object_2.coor["y"].nilai - object_1.coor["y"].nilai

    r = np.hypot(dx, dy)
    if r == 0:
        raise ValueError("Kedua objek berada di posisi yang sama")

    result = G * mass1 * mass2 / r**2

    force_x = result * dx / r
    force_y = result * dy / r

    return {"x": Force(force_x), "y": Force(force_y)}

def electrostaticForce(object_1, object_2):
    charge1 = object_1.charge.toCoulombs()
    charge2 = object_2.charge.toCoulombs()

    dx = object_2.coor["x"].nilai - object_1.coor["x"].nilai
    dy = object_2.coor["y"].nilai - object_1.coor["y"].nilai

    r = np.hypot(dx, dy)
    if r == 0:
        raise ValueError("Kedua objek berada di posisi yang sama")

    result = K * charge1.nilai * charge2.nilai / r**2

    force_x = result * dx / r
    force_y = result * dy / r

    return {"x": Force(force_x), "y": Force(force_y)}