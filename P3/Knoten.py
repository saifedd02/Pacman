from __future__ import annotations
from copy import deepcopy
from game_core.config import TILE_TYPES


class Knoten:
    # Ein Knoten repräsentiert einen Zustand des Spiels.

    def __init__(self, view, pacman_pos, parent=None, action=None, cost=0, eaten_dot=False):
        self.view = view
        self.pacman_pos = pacman_pos
        self.parent = parent
        self.action = action
        self.cost = cost

        # Wichtig für P3:
        # True bedeutet: Dieser Knoten ist entstanden,
        # weil Pacman gerade auf einen Dot gelaufen ist.
        self.eaten_dot = eaten_dot

    def expand(self) -> list["Knoten"]:
        # Erzeugt alle möglichen Nachfolgerknoten.

        kinder = []

        richtungen = {
            0: (0, -1),   # links
            1: (0, 1),    # rechts
            2: (-1, 0),   # oben
            3: (1, 0)     # unten
        }

        for action, (dx, dy) in richtungen.items():

            neue_x = self.pacman_pos[0] + dx
            neue_y = self.pacman_pos[1] + dy

            anzahl_zeilen = len(self.view)
            anzahl_spalten = len(self.view[0])

            # Wenn neue Position außerhalb der Map ist: überspringen.
            if not (0 <= neue_x < anzahl_zeilen and 0 <= neue_y < anzahl_spalten):
                continue

            zielfeld = self.view[neue_x][neue_y]

            # Wand darf Pacman nicht betreten.
            if zielfeld == TILE_TYPES["#"]:
                continue

            neue_view = deepcopy(self.view)

            alte_x, alte_y = self.pacman_pos

            # Alte Pacman-Position leer machen.
            neue_view[alte_x][alte_y] = TILE_TYPES[" "]

            # Neue Pacman-Position setzen.
            # Falls dort ein Dot war, wird er dadurch in der Suchkarte entfernt.
            neue_view[neue_x][neue_y] = TILE_TYPES["P"]

            kind = Knoten(
                neue_view,
                (neue_x, neue_y),
                parent=self,
                action=action,
                cost=self.cost + 1,
                eaten_dot=(zielfeld == TILE_TYPES["*"])
            )

            kinder.append(kind)

        return kinder