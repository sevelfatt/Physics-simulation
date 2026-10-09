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
PHYSICS_DT = 1         # physics time step (detik per step) - kecil untuk akurasi orbit
TIME_SCALE = 3600*24     # skala waktu: 1 hari simulasi per detik real (86400)
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
MOON_ORBIT_DIST = 384400*(10**3)   # meter

# --- Buat objek Bumi (di tengah layar) ---
earth = Objects(
    coor={"x":Meter(CENTER_X), "y":Meter(CENTER_Y)},
    radius=Meter(6371e4),
    mass=Mass(5.972e24),
    dt=Second(PHYSICS_DT),
)

# --- Buat objek Bulan (di sebelah kanan Bumi, jarak orbit nyata) ---
moon = Objects(
    coor=dict(x=Meter(CENTER_X + MOON_ORBIT_DIST), y=Meter(CENTER_Y)),
    radius=Meter(1737e4),
    mass=Mass(7.342e22),
    dt=Second(PHYSICS_DT),
)
# Kecepatan orbit Bulan agar mengorbit Bumi (kecepatan lingkaran)
moon.NewVelocity("y", Velocity(1022))   # ~1022 m/s tegak lurus jarak

    # Terapkan gaya gravitasi setiap frame
hud = HUD(screen, moon, label="Moon", x=10, y=10, time_scale=TIME_SCALE)

# --- Game loop ---
sim_time = 0.0          # total simulation time advanced
last_real = pygame.time.get_ticks() / 1000.0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        hud.handle_event(event)

    # --- Fixed-timestep accumulator: jalankan physics steps hingga sim_time mengejar real_time * TIME_SCALE ---
    now = pygame.time.get_ticks() / 1000.0
    real_dt = now - last_real
    last_real = now
    target_sim_dt = real_dt * TIME_SCALE
    sim_time += target_sim_dt

    # Jalankan physics steps
    while sim_time >= PHYSICS_DT:
        GravitationSystem([earth, moon])
        earth.Update()
        moon.Update()
        sim_time -= PHYSICS_DT
    
    
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
    clock.tick(60)
