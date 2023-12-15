from dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    name: str
    loc: str
    ang: float

    def absorb_positioning(self, neighbor):
        return Label(
            self.name,
            neighbor.loc if self.loc is None else self.loc,
            neighbor.ang if self.ang is None else self.ang,
        )

    def positioning_info(self):
        return [x for x in ["loc", "ang"] if getattr(self, x) is not None]
