from system import GravitationSystem
from units import Force, PIXELS_PER_METER
from units import Mass
import sys
import pygame
from units import Meter, Velocity, Acceleration, Second
from objects import Objects
from hud import HUD


# --- Konfigurasi ---
WIDTH, HEIGHT = 1000, 1000
TICK = 0.001
TIME_SCALE=3600*24
BG_COLOR = (30, 30, 30)
BALL_COLOR = (255, 87, 34)

# --- Init pygame ---
pygame.init()

font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation")
clock = pygame.time.Clock()

# --- Koordinat tengah layar dalam meter ---
CENTER_X = (WIDTH  / 2) / PIXELS_PER_METER   # meter
CENTER_Y = (HEIGHT / 2) / PIXELS_PER_METER   # meter

# Jarak orbit Bulan dari Bumi (rata-rata)
# ORBIT_DIST = 384400*(10**3)   # meter

ORBIT_DIST = 300000e3

# --- Buat objek Bumi (di tengah layar) ---
earth = Objects(
    coor={"x":Meter(CENTER_X), "y":Meter(CENTER_Y)},
    radius=Meter(6371e4),
    mass=Mass(5.972e24),
    dt=Second(TICK),
)

# --- Buat objek Bulan (di sebelah kanan Bumi, jarak orbit nyata) ---
moon = Objects(
    coor=dict(x=Meter(CENTER_X + ORBIT_DIST), y=Meter(CENTER_Y-200000e3)),
    radius=Meter(1737e4),
    mass=Mass(7.342e22),
    dt=Second(TICK),
)
# Kecepatan orbit Bulan agar mengorbit Bumi (kecepatan lingkaran)
moon.NewVelocity("y", Velocity(1022))   # ~1022 m/s tegak lurus jarak
    # Terapkan gaya gravitasi setiap frame
hud = HUD(screen, moon, label="Moon", x=10, y=10)

# --- Game loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        hud.handle_event(event)

    GravitationSystem([earth, moon])

    earth.Update()
    # earth.bounce(WIDTH, HEIGHT)

    moon.Update()
    # moon.bounce(WIDTH, HEIGHT)

    screen.fill(BG_COLOR)
    # Render Earth (biru)
    ex = earth.coor['x'].to_px()
    ey = HEIGHT - earth.coor['y'].to_px()
    pygame.draw.circle(screen, (33, 150, 243), (int(ex), int(ey)), max(1, int(earth.radius.to_px())))

    # Render Moon (abu-abu)
    mx = moon.coor['x'].to_px()
    my = HEIGHT - moon.coor['y'].to_px()
    pygame.draw.circle(screen, (180, 180, 180), (int(mx), int(my)), max(1, int(moon.radius.to_px())))

    hud.draw()
    pygame.display.flip()
    clock.tick(TICK*TIME_SCALE)
