from ast import List
from hud import HUD
from objects import Objects
from system import GravitationSystem
from units import Mass
import sys
import pygame
from units import Meter, Velocity, Acceleration, Second

class Simulator:
    def __init__(self, time_scale: float, objects: List[Objects], width_px: int = 1000, height_px: int = 1000, physics_dt: float = 1, background_color: tuple = (30, 30, 30), colors: dict = {"earth": (33, 150, 243), "moon": (180, 180, 180)}, bounce: bool = True, gravity: bool = True, pixels_per_meter: float = 1):
        self.time_scale = time_scale
        self.objects = objects
        self.time = 0
        self.width_px = width_px
        self.height_px = height_px
        self.physics_dt = physics_dt
        self.background_color = background_color
        self.bounce = bounce
        self.gravity = gravity
        self.pixels_per_meter = pixels_per_meter
        self.huds = []
        o = 1
        for object in objects:
            self.huds.append(HUD(object,object.name,time_scale=time_scale, x=10*o))
            o+=1

    def add_object(self, obj: Objects):
        self.objects.append(obj)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width_px, self.height_px))
        pygame.display.set_caption("Physics Simulation")
        clock = pygame.time.Clock()

        # --- Game loop ---
        sim_time = 0.0          # total simulation time advanced
        last_real = pygame.time.get_ticks() / 1000.0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            for hud in self.huds:
                hud.handle_event(event)

            # --- Fixed-timestep accumulator: jalankan physics steps hingga sim_time mengejar real_time * TIME_SCALE ---
            now = pygame.time.get_ticks() / 1000.0
            real_dt = now - last_real
            last_real = now
            target_sim_dt = real_dt * self.time_scale
            sim_time += target_sim_dt

            # Jalankan physics steps
            while sim_time >= self.physics_dt:
                if self.gravity:
                    GravitationSystem(self.objects)
                for obj in self.objects:
                    obj.Update(self.physics_dt)
                    if self.bounce:
                        obj.bounce(self.width_px, self.height_px, self.pixels_per_meter)
                sim_time -= self.physics_dt
            
            screen.fill(self.background_color)
            for obj in self.objects:
                ox = (self.width_px/2) + obj.coor['x'].to_px(self.pixels_per_meter)
                oy = (self.height_px/2) - obj.coor['y'].to_px(self.pixels_per_meter)
                r = obj.radius.to_px(self.pixels_per_meter)

                pygame.draw.circle(screen, obj.color, (int(ox), int(oy)), max(1, int(r)))
            for hud in self.huds:
                hud.draw(screen)
            pygame.display.flip()
            clock.tick(60)
                
                

            
        
