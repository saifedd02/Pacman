from Backend.Student_Files.P3.Knoten import Knoten
from game_core.config import TILE_TYPES


class Suche:
    # Diese Klasse enthält alle Suchstrategien aus Praktikum 3.
    # Wichtig: Wir suchen jetzt NICHT mehr direkt nach "alle Dots weg",
    # sondern nach dem nächsten gefressenen Dot.
    # Danach startet PacmanAgent wieder eine neue Suche.

    def ist_ziel(self, knoten):
        # Ziel dieses Suchlaufs:
        # Pacman hat in diesem Knoten gerade einen Dot gefressen.
        return knoten.eaten_dot

    def zustand_als_key(self, knoten):
        # Macht den Zustand vergleichbar für die Closed-List.
        return tuple(tuple(zeile) for zeile in knoten.view)

    def loesungsweg(self, zielknoten):
        # Vom Zielknoten zurück zum Start laufen.
        aktionen = []
        aktueller_knoten = zielknoten

        while aktueller_knoten.parent is not None:
            aktionen.append(aktueller_knoten.action)
            aktueller_knoten = aktueller_knoten.parent

        # Umkehren: Wir wollen vom Start zum Ziel laufen.
        aktionen.reverse()
        return aktionen

    def heuristik(self, knoten):
        # Manhattan-Distanz zum nächsten Dot.
        pacman_x, pacman_y = knoten.pacman_pos
        kleinste_distanz = None

        for x, zeile in enumerate(knoten.view):
            for y, feld in enumerate(zeile):
                if feld == TILE_TYPES["*"]:
                    distanz = abs(pacman_x - x) + abs(pacman_y - y)

                    if kleinste_distanz is None or distanz < kleinste_distanz:
                        kleinste_distanz = distanz

        if kleinste_distanz is None:
            return 0

        return kleinste_distanz

    def bewertung(self, knoten, strategie):
        # Bewertung für UCS, Greedy und A*
        if strategie == "UCS":
            return knoten.cost

        if strategie == "Greedy":
            return self.heuristik(knoten)

        if strategie == "A-Stern":
            return knoten.cost + self.heuristik(knoten)

        return 0

    def insert(self, open_list, kind, strategie):
        # INSERT bestimmt die Suchstrategie.

        if strategie == "Tiefensuche":
            # Stack-Prinzip: vorne einfügen.
            open_list.insert(0, kind)

        elif strategie == "Breitensuche":
            # Queue-Prinzip: hinten anhängen.
            open_list.append(kind)

        else:
            # UCS, Greedy, A*: nach Bewertung sortiert einfügen.
            wert = self.bewertung(kind, strategie)
            position = 0

            while position < len(open_list) and self.bewertung(open_list[position], strategie) <= wert:
                position += 1

            open_list.insert(position, kind)

    def starte_Suchalgorithmus(self, node: Knoten, strategie="Breitensuche") -> Knoten:
        """
        node: Startknoten
        strategie: Breitensuche | Tiefensuche | UCS | Greedy | A-Stern
        return: Zielknoten oder None
        """

        open_list = [node]
        closed_list = set()

        while len(open_list) > 0:

            aktueller_knoten = open_list.pop(0)

            zustand = self.zustand_als_key(aktueller_knoten)

            if zustand in closed_list:
                continue

            closed_list.add(zustand)

            if self.ist_ziel(aktueller_knoten):
                aktionen = self.loesungsweg(aktueller_knoten)

                print("Strategie:", strategie)
                print("Nächster Dot gefunden!")
                print("OpenList:", len(open_list))
                print("ClosedList:", len(closed_list))
                print("Laenge der Loesung:", len(aktionen))
                print("Aktionen:", aktionen)

                return aktueller_knoten

            kinder = aktueller_knoten.expand()

            for kind in kinder:
                self.insert(open_list, kind, strategie)

        print("Strategie:", strategie)
        print("Kein Dot gefunden.")
        print("OpenList:", len(open_list))
        print("ClosedList:", len(closed_list))

        return None