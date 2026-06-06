
from __future__ import annotations
# Erlaubt, dass wir in der Klasse schon "Knoten" als Typ benutzen dürfen:
# def expand(self) -> list[Knoten]

from copy import deepcopy
# Wir brauchen deepcopy, damit wir eine echte Kopie vom Level machen.
# Ohne deepcopy würden wir aus Versehen das originale Level verändern.


class Knoten:
    # Diese Klasse beschreibt EINEN Zustand vom Pacman-Spiel.

    def __init__(self, level, pacman_pos_x, pacman_pos_y, parent=None):
        # __init__ wird automatisch ausgeführt, wenn wir einen neuen Knoten erstellen.
        # level = aktuelle Map
        # pacman_pos_x = Zeile, wo Pacman steht
        # pacman_pos_y = Spalte, wo Pacman steht
        # parent = vorheriger Knoten, von dem dieser Knoten kommt

        self.level = level
        # Speichert die aktuelle Map im Knoten.

        self.pacman_pos_x = pacman_pos_x
        # Speichert die aktuelle Zeile von Pacman.

        self.pacman_pos_y = pacman_pos_y
        # Speichert die aktuelle Spalte von Pacman.

        self.parent = parent
        # Speichert den vorherigen Knoten.
        # Das hilft später, den Weg zurückzuverfolgen.


    def expand(self) -> list[Knoten]:
        # expand erzeugt alle möglichen nächsten Zustände.
        # Rückgabe ist eine Liste von Kindknoten.

        kinder = []
        # Hier speichern wir alle neuen Kindknoten.

        richtungen = [
            (0, -1),  # links: gleiche Zeile, eine Spalte nach links
            (0, 1),   # rechts: gleiche Zeile, eine Spalte nach rechts
            (-1, 0),  # oben: eine Zeile nach oben, gleiche Spalte
            (1, 0)    # unten: eine Zeile nach unten, gleiche Spalte
        ]

        for dx, dy in richtungen:
            # Wir probieren jede Richtung einzeln aus.

            neue_x = self.pacman_pos_x + dx
            # Neue Zeile berechnen.

            neue_y = self.pacman_pos_y + dy
            # Neue Spalte berechnen.

            if self.level[neue_x][neue_y] != "#":
                # Wenn dort KEINE Wand ist, darf Pacman dorthin gehen.

                neues_level = deepcopy(self.level)
                # Wir kopieren die Map, damit der alte Zustand unverändert bleibt.

                neues_level[self.pacman_pos_x][self.pacman_pos_y] = " "
                # Alte Pacman-Position wird leer gemacht.

                neues_level[neue_x][neue_y] = "P"
                # Neue Pacman-Position wird gesetzt.

                kind = Knoten(neues_level, neue_x, neue_y, self)
                # Neuer Knoten wird erstellt.
                # parent ist self, weil dieser neue Knoten aus dem aktuellen kommt.

                kinder.append(kind)
                # Kindknoten wird in die Liste eingefügt.
        return kinder
        # Am Ende geben wir alle möglichen Kindknoten zurück.
