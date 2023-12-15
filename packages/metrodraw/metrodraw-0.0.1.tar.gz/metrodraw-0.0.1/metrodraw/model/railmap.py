from metrodraw.model.coord import Coord
from metrodraw.model.station import make_station
from .line import Line


class Railmap:
    def __init__(self):
        self.lines = []
        self.stations = []
        self.interlining_stations = []
        self.coord_to_station = {}
        self.neighboring_coords = set()

    def line(self, *args):
        self.lines.append(Line(self, *args))
        return self.lines[-1]

    def add_station(self, station):
        assert station.coord not in self.coord_to_station
        self.stations.append(station)
        self.coord_to_station[station.coord] = len(self.stations) - 1

    def add_neighboring(self, coord_a, coord_b):
        self.neighboring_coords.add((coord_a, coord_b))

    def add_interlining(self, orig, interlined):
        self.add_neighboring(orig, interlined)
        self.interlining_stations.append((interlined, self.station_at(orig)))

    @property
    def neighboring_stations(self):
        coord_to_stations = {}
        for station in self.stations:
            coord_to_stations.setdefault(station.coord, set()).add(station)
        result = {}
        for coord_a, coord_b in self.neighboring_coords:
            for station_a in coord_to_stations.get(
                coord_a, [make_station(coord_a, "dummy", loc=None)]
            ):
                for station_b in coord_to_stations.get(
                    coord_b, [make_station(coord_b, "dummy", loc=None)]
                ):
                    result.setdefault(station_a, set()).add(station_b)
                    result.setdefault(station_b, set()).add(station_a)
        return result

    def propagate_positioning_map(self):
        ns = self.neighboring_stations
        result = {station: station for station in ns}
        if not any(station.has_positioning() for station in result):
            info = sorted(
                {field for station in result for field in station.positioning_info()}
            )
            info_kwargs = {"loc": "l", "ang": 0}
            for field in info:
                info_kwargs[field] = None
            neighbor = make_station(Coord(0, 0), "dummy", **info_kwargs)
            result = {station: station.with_positioning(neighbor) for station in result}
        while True:
            dirty = False
            for station in result:
                dirty = dirty or not result[station].has_positioning()
                for neighbor in ns[station]:
                    if result[station].has_positioning():
                        break
                    result[station] = result[station].with_positioning(result[neighbor])
            if not dirty:
                break
        return result

    def propagate_positioning(self):
        positioning_map = self.propagate_positioning_map()
        self.stations = [positioning_map[station] for station in self.stations]

    def bounds(self, config, pad=0):
        xs = [station.coord.get_x(config) for station in self.stations]
        ys = [station.coord.get_y(config) for station in self.stations]

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        xmin -= pad
        xmax += pad
        ymin -= pad
        ymax += pad

        return xmin, xmax, ymin, ymax

    def station_at(self, coord):
        return self.stations[self.coord_to_station[coord]]
