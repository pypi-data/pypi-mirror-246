from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    x: float
    y: float

    def off(self, dx, dy):
        return type(self)(self.x + dx, self.y + dy)

    def move(self, direct, scale=1, length=None):
        if isinstance(direct, Coord):
            return direct
        direct = direct.lower()
        dx = 0
        dy = 0
        dy += direct.count("u")
        dy -= direct.count("d")
        dx += direct.count("r")
        dx -= direct.count("l")
        if length is not None:
            assert scale == 1
            scale = length / (dx ** 2 + dy ** 2) ** 0.5
        dx, dy = dx * scale, dy * scale
        return self.off(dx, dy)

    def get_x(self, config):
        return self.x

    def get_y(self, config):
        return self.y


@dataclass(frozen=True)
class InterliningCoord:
    coord: Coord
    interlining_direction: str

    def off(self, dx, dy):
        return InterliningCoord(self.coord.off(dx, dy), self.interlining_direction)

    def move(self, direct, scale=1, length=None):
        return InterliningCoord(
            self.coord.move(direct, scale=scale, length=length),
            self.interlining_direction,
        )

    def get_x(self, config):
        return self.coord.move(
            self.interlining_direction,
            scale=config["interlining_offset"],
        ).x

    def get_y(self, config):
        return self.coord.move(
            self.interlining_direction,
            scale=config["interlining_offset"],
        ).y
