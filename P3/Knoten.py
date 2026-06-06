from __future__ import annotations
# Erlaubt die Verwendung von "Knoten" als Rückgabetyp
# bevor die Klasse vollständig definiert ist.

from copy import deepcopy
# deepcopy erstellt eine echte Kopie eines Objekts.
# Wir brauchen das, damit jede Map unabhängig bleibt.

from game_core.config import TILE_TYPES
# Enthält die Spielfeldwerte des Servers.
# Beispiel: Wand, Pacman, Dot usw.


class Knoten:
    # Ein Knoten repräsentiert einen Zustand des Spiels.

    def __init__(self, view, pacman_pos, parent=None, action=None, cost=0):

        self.view = view
        # Aktuelles Spielfeld (Map)

        self.pacman_pos = pacman_pos
        # Position von Pacman
        # Beispiel: (5, 3)

        self.parent = parent
        # Vorgängerknoten
        # Damit kann später der Lösungsweg rekonstruiert werden.

        self.action = action
        # Welche Aktion führte zu diesem Knoten?
        # 0=links, 1=rechts, 2=oben, 3=unten

        self.cost = cost
        # Bisherige Wegkosten
        # Bei jedem Schritt +1


    def expand(self) -> list["Knoten"]:
        # Erzeugt alle möglichen Nachfolgerknoten.

        kinder = []
        # Hier speichern wir alle erzeugten Kindknoten.

        richtungen = {
            0: (0, -1),   # links
            1: (0, 1),    # rechts
            2: (-1, 0),   # oben
            3: (1, 0)     # unten
        }

        # Für jede mögliche Bewegung
        for action, (dx, dy) in richtungen.items():

            neue_x = self.pacman_pos[0] + dx
            # Neue Zeile berechnen

            neue_y = self.pacman_pos[1] + dy
            # Neue Spalte berechnen

            # Prüfen ob dort KEINE Wand ist
            if self.view[neue_x][neue_y] != TILE_TYPES["#"]:

                neue_view = deepcopy(self.view)
                # Neue unabhängige Kopie der Map erstellen

                alte_x, alte_y = self.pacman_pos
                # Aktuelle Position von Pacman

                neue_view[alte_x][alte_y] = TILE_TYPES[" "]
                # Altes Feld wird leer

                neue_view[neue_x][neue_y] = TILE_TYPES["P"]
                # Pacman auf neue Position setzen

                kind = Knoten(
                    neue_view,
                    (neue_x, neue_y),
                    parent=self,
                    action=action,
                    cost=self.cost + 1
                )

                # Neuer Kindknoten:
                # neue Map
                # neue Position
                # Vorgänger = aktueller Knoten
                # ausgeführte Aktion speichern
                # Kosten erhöhen

                kinder.append(kind)
                # Kindknoten zur Liste hinzufügen

        return kinder
        # Alle erzeugten Kindknoten zurückgeben