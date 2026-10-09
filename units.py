PIXELS_PER_METER = 10**-6


class Unit:
    def __init__(self, nilai):
        self.nilai = float(nilai)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.nilai})"

    def _unwrap(self, other):
        return other.nilai if isinstance(other, Unit) else float(other)

    def __add__(self, other): return self.__class__(self.nilai + self._unwrap(other))
    def __sub__(self, other): return self.__class__(self.nilai - self._unwrap(other))
    def __mul__(self, other): return self.__class__(self.nilai * self._unwrap(other))
    def __rmul__(self, other): return self.__mul__(other)
    def __truediv__(self, other): return self.__class__(self.nilai / self._unwrap(other))
    def __neg__(self): return self.__class__(-self.nilai)
    def __iadd__(self, other): return self.__add__(other)


class Meter(Unit):
    def __str__(self): return f"{self.nilai} m"
    def to_px(self): return int(self.nilai * PIXELS_PER_METER)


class Velocity(Unit):
    def __str__(self): return f"{self.nilai} m/s"


class Acceleration(Unit):
    def __str__(self): return f"{self.nilai} m/s²"


class Second(Unit):
    def __init__(self, tick):
        self.nilai = 1 / tick  # detik per frame

    def __str__(self): return f"{self.nilai:.4f} s"

class Mass(Unit):
    def __init__(self, nilai):
        super().__init__(nilai)

    def __str__(self): return f"{self.nilai} kg"

class Force(Unit):
    def __init__(self, nilai):
        super().__init__(nilai)

    def __str__(self): return f"{self.nilai} N"

class Energy(Unit):
    def __init__(self, nilai):
        super().__init__(nilai)
    def __str__(self): return f"{self.nilai} J"
    
