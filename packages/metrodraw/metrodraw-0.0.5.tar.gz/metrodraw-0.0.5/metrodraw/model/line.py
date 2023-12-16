from metrodraw.model.coord import Coord, InterliningCoord
from metrodraw.model.station import make_station


class LineSegment:
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def coords(self, config):
        return [self.start.get_x(config), self.end.get_x(config)], [
            self.start.get_y(config),
            self.end.get_y(config),
        ]


class Line:
    def __init__(self, railmap, start, color, name):
        self.railmap = railmap
        self.last = start
        self.segment_basis = start
        self.color = color
        self.name = name
        self.segments = []
        self.grid_size = 1
        self._interlining = None

    def stations(self, *names, **kwargs):
        return [self.station(name, **kwargs) for name in names]

    def segment(self, direction, label=None):
        coord = self.last
        original = self.segment_basis
        coord = coord.move(direction, scale=self.grid_size)
        self.goto(coord)
        coord = self.with_interlining(coord)
        self.segments.append(LineSegment(original, coord, label))
        self.railmap.add_neighboring(original, coord)
        return coord

    def station(
        self,
        name,
        direction=None,
        *,
        loc=None,
        ang=None,
        kind="basic",
        segment_label=None
    ):
        if direction is not None:
            self.segment(direction, segment_label)
        station_loc = self.with_interlining(self.last)
        self.railmap.add_station(
            make_station(station_loc, name, loc, ang=ang, kind=kind)
        )
        return station_loc

    def goto(self, coord):
        self.last = coord
        self.segment_basis = self.with_interlining(coord)

    def grid(self, size):
        self.grid_size = size

    def interlining(self, direction):
        self._interlining = direction

    def no_interlining(self, keep_pos=False):
        self._interlining = None
        if keep_pos:
            self.last = self.segment_basis

    def with_interlining(self, coord):
        if self._interlining is None:
            return coord
        wi = InterliningCoord(coord, self._interlining)
        self.railmap.add_interlining(coord, wi)
        return wi
