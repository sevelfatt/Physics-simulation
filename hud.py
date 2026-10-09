import pygame
import math

pygame.font.init()

_FONT_S = None
_FONT_B = None


def _get_fonts():
    global _FONT_S, _FONT_B
    if _FONT_S is None:
        _FONT_S = pygame.font.SysFont("consolas", 13)
        _FONT_B = pygame.font.SysFont("consolas", 13, bold=True)
    return _FONT_S, _FONT_B


def fmt(val: float) -> str:
    """Format angka pendek: 1234 -> 1.23K, 0.0012 -> 1.23m, dll."""
    abs_val = abs(val)
    if abs_val >= 1e12:
        return f"{val/1e12:.2f}T"
    if abs_val >= 1e9:
        return f"{val/1e9:.2f}B"
    if abs_val >= 1e6:
        return f"{val/1e6:.2f}M"
    if abs_val >= 1e3:
        return f"{val/1e3:.2f}K"
    if abs_val >= 1:
        return f"{val:.2f}"
    if abs_val >= 1e-3:
        return f"{val*1e3:.2f}m"
    if abs_val >= 1e-6:
        return f"{val*1e6:.2f}µ"
    if abs_val >= 1e-9:
        return f"{val*1e9:.2f}n"
    if abs_val > 0:
        return f"{val:.2e}"
    return "0"


def fmt_time(seconds: float) -> str:
    """Format waktu: detik, menit, jam, hari."""
    abs_s = abs(seconds)
    if abs_s < 60:
        return f"{fmt(seconds)} s"
    minutes = seconds / 60
    if abs_s < 3600:
        return f"{fmt(minutes)} min"
    hours = seconds / 3600
    if abs_s < 86400:
        return f"{fmt(hours)} h"
    days = seconds / 86400
    return f"{fmt(days)} d"


class HUD:
    """
    Panel HUD kecil yang bisa di-drag, terikat ke satu objek fisika.

    Cara pakai:
        hud = HUD(screen, ball, label="Ball 1", x=10, y=10)

        # dalam event loop:
        hud.handle_event(event)

        # dalam draw loop:
        hud.draw()
    """

    W   = 300
    PAD = 6
    ROW = 20   # tinggi per baris
    HDR = 20   # tinggi header (area drag)

    BG      = (15, 18, 30, 200)
    BORDER  = (70, 100, 210)
    HDR_CLR = (30, 40, 80)
    LBL_CLR = (130, 150, 200)
    VAL_CLR = (220, 230, 255)
    TTL_CLR = (200, 215, 255)

    # (label singkat, unit, getter x, getter y)
    ROWS = [
        ("pos", "m",    lambda o: o.coor["x"].nilai, lambda o: o.coor["y"].nilai),
        ("vel", "m/s",  lambda o: o.v["x"].nilai,    lambda o: o.v["y"].nilai),
        ("acc", "m/s²", lambda o: o.a["x"].nilai,    lambda o: o.a["y"].nilai),
        ("F",   "N",    lambda o: o.f["x"].nilai,     lambda o: o.f["y"].nilai),

    ]

    def _speed(self, o):
        return o.speed()

    def _accel_mag(self, o):
        return math.hypot(o.a["x"].nilai, o.a["y"].nilai)

    def _kinetic_energy(self, o):
        return o.ke

    def __init__(self, screen: pygame.Surface, obj,
                 label: str = "Object", x: int = 10, y: int = 10,
                 dt: float = 0.0, time_scale: float = 1.0):
        self.screen = screen
        self.obj    = obj
        self.label  = label
        self.x      = x
        self.y      = y
        self._drag  = False
        self._ox    = 0
        self._oy    = 0
        self._time_scale = time_scale  # skala waktu: detik simulasi per detik real
        self._sim_time = 0.0
        self._last_real_time = pygame.time.get_ticks() / 1000.0

    # ── tinggi total panel ──────────────────────────────────────────────────
    @property
    def _height(self):
        return self.HDR + self.PAD + (len(self.ROWS) + 10) * self.ROW + self.PAD

    def _header_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.W, self.HDR)

    # ── drag ────────────────────────────────────────────────────────────────
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._header_rect().collidepoint(event.pos):
                self._drag = True
                self._ox   = event.pos[0] - self.x
                self._oy   = event.pos[1] - self.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._drag = False
        elif event.type == pygame.MOUSEMOTION and self._drag:
            self.x = event.pos[0] - self._ox
            self.y = event.pos[1] - self._oy

    # ── gambar ──────────────────────────────────────────────────────────────
    def draw(self):
        font_s, font_b = _get_fonts()
        o = self.obj
        h = self._height

        # update simulation time based on real elapsed time
        now = pygame.time.get_ticks() / 1000.0
        real_dt = now - self._last_real_time
        self._last_real_time = now
        self._sim_time += real_dt * self._time_scale

        # surface panel
        surf = pygame.Surface((self.W, h), pygame.SRCALPHA)
        surf.fill(self.BG)
        pygame.draw.rect(surf, self.BORDER, (0, 0, self.W, h), 1, border_radius=5)

        # header (area drag)
        pygame.draw.rect(surf, self.HDR_CLR, (1, 1, self.W - 2, self.HDR - 1),
                         border_top_left_radius=5, border_top_right_radius=5)
        title = font_b.render(f"▣ {self.label}", True, self.TTL_CLR)
        surf.blit(title, (self.PAD, (self.HDR - title.get_height()) // 2))

        # baris data
        oy = self.HDR + self.PAD
        for lbl, unit, gx, gy in self.ROWS:
            vx = gx(o); vy = gy(o)
            l = font_s.render(f"{lbl}", True, self.LBL_CLR)
            v = font_s.render(f"  x={fmt(vx)}  y={fmt(vy)}  {unit}", True, self.VAL_CLR)
            surf.blit(l, (self.PAD, oy))
            surf.blit(v, (self.PAD + l.get_width(), oy))
            oy += self.ROW

        # speed (magnitude of velocity)
        spd = self._speed(o)
        l = font_s.render("spd", True, self.LBL_CLR)
        v = font_s.render(f"  {fmt(spd)} m/s", True, self.VAL_CLR)
        surf.blit(l, (self.PAD, oy))
        surf.blit(v, (self.PAD + l.get_width(), oy))
        oy += self.ROW

        # acceleration magnitude
        acc_mag = self._accel_mag(o)
        l = font_s.render("acc", True, self.LBL_CLR)
        v = font_s.render(f"  {fmt(acc_mag)} m/s²", True, self.VAL_CLR)
        surf.blit(l, (self.PAD, oy))
        surf.blit(v, (self.PAD + l.get_width(), oy))
        oy += self.ROW

        # kinetic energy
        ke = self._kinetic_energy(o)
        l = font_s.render("KE  ", True, self.LBL_CLR)
        v = font_s.render(f"  {fmt(ke)} J", True, self.VAL_CLR)
        surf.blit(l, (self.PAD, oy))
        surf.blit(v, (self.PAD + l.get_width(), oy))
        oy += self.ROW

        # simulation time
        l = font_s.render("time", True, self.LBL_CLR)
        v = font_s.render(f"  {fmt_time(self._sim_time)}", True, self.VAL_CLR)
        surf.blit(l, (self.PAD, oy))
        surf.blit(v, (self.PAD + l.get_width(), oy))
        oy += self.ROW

        # massa (satu nilai, tidak ada x/y)
        lm = font_s.render("m  ", True, self.LBL_CLR)
        vm = font_s.render(f"  {fmt(o.mass.nilai)} kg", True, self.VAL_CLR)
        surf.blit(lm, (self.PAD, oy))
        surf.blit(vm, (self.PAD + lm.get_width(), oy))

        self.screen.blit(surf, (self.x, self.y))
