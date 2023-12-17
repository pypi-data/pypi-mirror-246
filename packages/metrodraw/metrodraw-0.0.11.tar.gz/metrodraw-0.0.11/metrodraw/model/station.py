from abc import ABC, abstractmethod
from dataclasses import dataclass

from matplotlib import pyplot as plt

from .coord import Coord
from .label import Label


@dataclass(frozen=True)
class Station:
    coord: Coord
    label: Label
    kind: str
    kind_kwargs: dict = None

    def with_coord(self, coord):
        return type(self)(coord, self.label, self.kind)

    @property
    def prototype(self):
        if self.kind == "basic" or self.kind is None:
            typ = BasicStation
        elif self.kind == "major":
            typ = MajorStation
        else:
            raise ValueError(f"unknown station kind: {self.kind}")
        return typ(**self.kind_kwargs) if self.kind_kwargs else typ()

    def with_label(self, label):
        return type(self)(self.coord, label, self.kind)

    def with_kind(self, kind):
        return type(self)(self.coord, self.label, kind)

    def with_positioning(self, neighbor):
        return type(self)(
            self.coord,
            self.label.absorb_positioning(neighbor.label),
            self.kind,
        )

    def has_positioning(self):
        return self.label.positioning_info() == ["loc", "ang"]

    def positioning_info(self):
        return self.label.positioning_info()


class StationPrototype(ABC):
    @abstractmethod
    def get_markers(self, x, y, r, black, white):
        pass

    @property
    @abstractmethod
    def font_size(self):
        pass


@dataclass(frozen=True)
class BasicStation(StationPrototype):
    def get_markers(self, x, y, r, black, white):
        return [
            plt.Circle((x, y), r * 0.5, color=white),
        ]

    @property
    def font_size(self):
        return 1


@dataclass(frozen=True)
class MajorStation(StationPrototype):
    def get_markers(self, x, y, r, black, white):
        return [
            plt.Circle((x, y), r * 0.65, color=black),
            plt.Circle((x, y), r * 0.4, color=white),
        ]

    @property
    def font_size(self):
        return 1.5


def make_station(coord, name, loc, ang=0, kind=None):
    return Station(coord, Label(name=name, loc=loc, ang=ang), kind)
