from matplotlib import pyplot as plt
import numpy as np
from metrodraw.model.coord import Coord
from metrodraw.utils.data_linewidth_plot import data_linewidth_plot


class Renderer:
    def __init__(self, scheme, dpi=200, lw=0.2, font_size=4):
        self.lw = lw
        self.dpi = dpi
        self.ax = None
        self.font_size = font_size
        self._handles = []
        self.scheme = scheme
        self.original_rcparams = None

    def __enter__(self):
        self.original_rcparams = {
            k: plt.rcParams[k] for k in self.scheme.rcparams().keys()
        }
        for k, v in self.scheme.rcparams().items():
            plt.rcParams[k] = v
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del exc_type, exc_value, traceback
        assert self.original_rcparams is not None, "Renderer.__enter__ was not called"
        for k, v in self.original_rcparams.items():
            plt.rcParams[k] = v
        self.original_rcparams = None

    @property
    def coord_config(self):
        return dict(interlining_offset=self.lw)

    def line(self, line):
        for seg in line.segments:
            xs, ys = seg.coords(self.coord_config)
            self._handles += [
                data_linewidth_plot(
                    xs,
                    ys,
                    ax=self.ax,
                    linewidth=self.lw,
                    solid_capstyle="round",
                    # solid_joinstyle="miter",
                    color=self.scheme.get_color(line.color),
                )
            ]
            assert len(xs) == 2
            assert len(ys) == 2

            cx = (xs[0] + xs[1]) / 2
            cy = (ys[0] + ys[1]) / 2
            angle = np.rad2deg(np.arctan2(ys[1] - ys[0], xs[1] - xs[0]))

            self.ax.text(
                x=cx,
                y=cy,
                s=seg.label,
                ha="center",
                va="center",
                rotation=angle,
                fontsize=self.lw * 30,
                color=self.scheme.get_color("bg"),
            )

    def station(self, station, no_label=False):
        # draw circle at station
        x, y = station.coord.get_x(self.coord_config), station.coord.get_y(
            self.coord_config
        )
        r = self.lw / 2
        for i, mark in enumerate(
            station.get_markers(
                x,
                y,
                r,
                black=self.scheme.get_color("fg"),
                white=self.scheme.get_color("bg"),
            )
        ):
            # bring to front
            mark.zorder = 10 + i / 10
            self.ax.add_artist(mark)

        if not no_label:
            self.label(x, y, r, station.font_size, station.label)

    def interlining(self, coord, station):
        self.station(station.with_coord(coord), no_label=True)
        x1, y1 = station.coord.get_x(self.coord_config), station.coord.get_y(
            self.coord_config
        )
        x2, y2 = coord.get_x(self.coord_config), coord.get_y(self.coord_config)

        self._handles += [
            data_linewidth_plot(
                [x1, x2],
                [y1, y2],
                ax=self.ax,
                linewidth=self.lw / 4,
                solid_capstyle="round",
                # solid_joinstyle="miter",
                color=self.scheme.get_color("white"),
            )
        ]

    def label(self, x, y, r, font_size, label):
        # draw station name
        loc = label.loc  # one of l, r, u, d, ul, ur, dl, dr

        loc_new = Coord(x, y).move(loc, length=r * 3)

        loc = "".join(sorted(loc))  # normalize

        ha, va = {
            "l": ("right", "center"),
            "r": ("left", "center"),
            "u": ("center", "bottom"),
            "d": ("center", "top"),
            "lu": ("right", "bottom"),
            "ru": ("left", "bottom"),
            "dl": ("right", "top"),
            "dr": ("left", "top"),
        }[loc]

        self.ax.text(
            loc_new.x,
            loc_new.y,
            self.scheme.modify_label(label.name),
            ha=ha,
            va=va,
            rotation=label.ang,
            fontsize=font_size * self.font_size,
            color=self.scheme.get_color("fg"),
        )

    def railmap(self, railmap):
        xlow, xhigh, ylow, yhigh = railmap.bounds(self.coord_config, 1)

        size = xhigh - xlow, yhigh - ylow
        plt.figure(dpi=self.dpi, facecolor=self.scheme.get_color("bg"), figsize=size)
        self.ax = plt.gca()

        for line in railmap.lines:
            self.line(line)
        for station in set(railmap.stations):
            self.station(station)
        for coord, station in railmap.interlining_stations:
            self.interlining(coord, station)

        self.ax.axis("square")
        self.ax.axis("off")
        self.ax.set_xlim(xlow, xhigh)
        self.ax.set_ylim(ylow, yhigh)


def render(railmap, path, **kwargs):
    with Renderer(**kwargs) as renderer:
        renderer.railmap(railmap)
        plt.savefig(path)
        plt.savefig(path)
