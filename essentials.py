from units import Meter, Velocity


def bounce(x: Meter, y: Meter, radius: Meter,
           vx: Velocity, vy: Velocity,
           width: int, height: int):
    """Balik kecepatan jika ball menyentuh batas layar."""
    if (x - radius).to_px() < 0 and vx.nilai < 0:
        vx = -vx
    elif (x + radius).to_px() > width and vx.nilai > 0:
        vx = -vx

    if (y - radius).to_px() < 0 and vy.nilai < 0:
        vy = -vy
    elif (y + radius).to_px() > height and vy.nilai > 0:
        vy = -vy

    return vx, vy
