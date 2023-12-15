from abc import ABC, abstractmethod
from dataclasses import dataclass

from matplotlib import pyplot as plt

from .coord import Coord
from .label import Label


@dataclass(frozen=True)
class Station(ABC):
    coord: Coord
    label: Label

    def with_coord(self, coord):
        return type(self)(coord, self.label)

    @abstractmethod
    def get_markers(self, x, y, r, black, white):
        pass

    def with_positioning(self, neighbor):
        return type(self)(
            self.coord,
            self.label.absorb_positioning(neighbor.label),
        )

    def has_positioning(self):
        return self.label.positioning_info() == ["loc", "ang"]

    def positioning_info(self):
        return self.label.positioning_info()


@dataclass(frozen=True)
class BasicStation(Station):
    def get_markers(self, x, y, r, black, white):
        return [
            plt.Circle((x, y), r * 0.5, color=white),
        ]

    @property
    def font_size(self):
        return 1


@dataclass(frozen=True)
class MajorStation(Station):
    def get_markers(self, x, y, r, black, white):
        return [
            plt.Circle((x, y), r * 0.65, color=black),
            plt.Circle((x, y), r * 0.4, color=white),
        ]

    @property
    def font_size(self):
        return 1.5


def make_station(coord, name, loc, ang=0, kind="basic"):
    if kind == "basic":
        typ = BasicStation
    elif kind == "major":
        typ = MajorStation
    else:
        raise ValueError(f"unknown station kind: {kind}")
    return typ(coord, Label(name=name, loc=loc, ang=ang))
