from Backend.Student_Files.P3.Knoten import Knoten
from game_core.config import TILE_TYPES


class Suche:

    def ist_ziel(self, knoten):
        # Ziel ist erreicht, wenn keine Dots mehr im Spielfeld sind.
        for zeile in knoten.view:
            for feld in zeile:
                if feld == TILE_TYPES["*"]:
                    return False
        return True

    def zustand_als_key(self, knoten):
        # Macht die Map vergleichbar, damit closed_list prüfen kann,
        # ob ein Zustand schon besucht wurde.
        return tuple(tuple(zeile) for zeile in knoten.view)

    def loesungsweg(self, zielknoten):
        # Baut vom Zielknoten zurück zum Startknoten die Aktionen auf.
        aktionen = []
        aktueller_knoten = zielknoten

        while aktueller_knoten.parent is not None:
            aktionen.append(aktueller_knoten.action)
            aktueller_knoten = aktueller_knoten.parent

        aktionen.reverse()
        return aktionen

    def starte_Suchalgorithmus(self, node: Knoten) -> Knoten:
        """
        node: Startknoten
        return: Zielknoten oder None
        """

        open_list = [node]
        # Noch zu untersuchende Knoten.

        closed_list = set()
        # Bereits besuchte Zustände.

        while len(open_list) > 0:

            aktueller_knoten = open_list.pop(0)
            # Breitensuche: immer den ersten Knoten nehmen.

            zustand = self.zustand_als_key(aktueller_knoten)

            if zustand in closed_list:
                continue

            closed_list.add(zustand)

            if self.ist_ziel(aktueller_knoten):
                aktionen = self.loesungsweg(aktueller_knoten)

                print("Ziel gefunden!")
                print("OpenList:", len(open_list))
                print("ClosedList:", len(closed_list))
                print("Länge der Lösung:", len(aktionen))
                print("Aktionen:", aktionen)

                return aktueller_knoten

            kinder = aktueller_knoten.expand()

            for kind in kinder:
                open_list.append(kind)
                # Hinten einfügen = Breitensuche.

        print("Keine Lösung gefunden.")
        print("OpenList:", len(open_list))
        print("ClosedList:", len(closed_list))

        return None