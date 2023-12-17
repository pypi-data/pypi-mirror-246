from metrodraw.model.label import Label
from metrodraw.model.coord import Coord, InterliningCoord
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
        lookup_coord = station.coord
        if isinstance(lookup_coord, InterliningCoord):
            lookup_coord = lookup_coord.coord

        if lookup_coord in self.coord_to_station:
            old_station = self.stations[self.coord_to_station[lookup_coord]]
            new_label = station.label
            old_label = old_station.label
            assert (
                new_label.name == old_label.name
            ), f"Attempted to add station {new_label.name} at {lookup_coord} but already have station {old_label.name} at that location"
            merged_label = merge_labels(new_label, old_label)
            merged_kind = old_station.kind
            if station.kind != old_station.kind:
                err = f"Attempted to add station {new_label.name} at {lookup_coord} with kind {station.kind} but already have station {old_label.name} at that location with kind {old_station.kind}"
                assert station.kind is None or old_station.kind is None, err
                merged_kind = station.kind or old_station.kind
            self.stations[self.coord_to_station[lookup_coord]] = old_station.with_label(
                merged_label
            ).with_kind(merged_kind)
        else:
            self.stations.append(station)
            self.coord_to_station[lookup_coord] = len(self.stations) - 1

    def add_neighboring(self, coord_a, coord_b):
        self.neighboring_coords.add((coord_a, coord_b))

    def add_interlining(self, orig, interlined):
        self.add_neighboring(orig, interlined)
        sa = self.station_at(orig)
        if sa is None:
            return
        self.interlining_stations.append((interlined, sa))

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
        if coord not in self.coord_to_station:
            return None
        return self.stations[self.coord_to_station[coord]]


def merge_labels(a, b):
    if a.name != b.name:
        raise ValueError(f"Cannot merge labels {a.name} and {b.name}")
    loc = a.loc if a.loc is not None else b.loc
    if a.loc != b.loc:
        assert (
            a.loc is None or b.loc is None
        ), f"Cannot merge labels with different locs: {a.loc} and {b.loc}"

    ang = a.ang if a.ang is not None else b.ang
    if a.ang != b.ang:
        assert (
            a.ang is None or b.ang is None
        ), f"Cannot merge labels with different angs: {a.ang} and {b.ang}"

    return Label(a.name, loc, ang)
