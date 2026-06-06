# Die Pacman-Umgebung wird importiert
from game_core.Pacman_Environment import Pacman_Environment

# Unsere Klassen aus Praktikum 3 importieren
from Backend.Student_Files.P3.Knoten import Knoten
from Backend.Student_Files.P3.Suche import Suche


"""
0: left
1: right
2: up
3: down
"""


class PacmanAgent:
    def __init__(self):
        # Pacman Environment initialisieren
        self.env = Pacman_Environment()

        self.is_running = False
        self.terminated = False
        self.truncated = False
        self.statistics = None
        self.is_last_step = False

        # Standardaktion, falls noch keine Suche ausgeführt wurde
        self.action = 1

        # Zielknoten der Suche
        self.loesungsknoten = None

        # Liste der Aktionen, die Pacman später abläuft
        self.action_path = []

    def render(self):
        self.env.render()

    def reset(self, seed, level):
        return self.env.reset(seed=seed, level=level)

    def baue_action_path(self, zielknoten):
        # Vom Zielknoten zurück zum Startknoten laufen
        aktionen = []
        aktueller_knoten = zielknoten

        while aktueller_knoten.parent is not None:
            aktionen.append(aktueller_knoten.action)
            aktueller_knoten = aktueller_knoten.parent

        # Weil wir von Ziel nach Start gelaufen sind,
        # müssen wir die Aktionen umdrehen.
        aktionen.reverse()

        return aktionen

    def step(self):

        if self.is_running and not (self.terminated or self.truncated):

            # Suche nur einmal starten
            if self.loesungsknoten is None:

                # Aktuelle Spielfeldsicht holen
                aktuelle_view = self.env.view

                # Pacman-Position holen
                pacman_position = self.env.pacman.get_position()

                # Startknoten erzeugen
                startknoten = Knoten(
                    aktuelle_view,
                    pacman_position
                )

                # Suche starten
                suche = Suche()
                self.loesungsknoten = suche.starte_Suchalgorithmus(startknoten)

                # Falls eine Lösung gefunden wurde
                if self.loesungsknoten is not None:
                    self.action_path = self.baue_action_path(self.loesungsknoten)
                    print("Action Path:", self.action_path)

                else:
                    print("Keine Lösung gefunden.")
                    self.action_path = []

            # Wenn es noch Aktionen gibt, nächste Aktion nehmen
            if len(self.action_path) > 0:
                self.action = self.action_path.pop(0)

            # Falls keine Aktionen mehr da sind, nichts Sinnvolles mehr zu tun
            else:
                print("Keine Aktion mehr im action_path.")
                self.is_last_step = True
                return self.statistics, self.is_last_step

            # Einen Schritt mit der berechneten Aktion ausführen
            observation, reward, self.terminated, self.truncated, self.statistics = self.env.step(self.action)

            print("Aktion:", self.action)
            print("Reward:", reward)

            # Spiel beendet oder abgebrochen
            if self.terminated or self.truncated:
                self.is_last_step = True
                self.statistics["view"] = observation
                return self.statistics, self.is_last_step

            else:
                # Spiel läuft weiter
                return self.statistics, self.is_last_step, observation

    def close(self):
        self.env.close()

    def is_game_over(self):
        return self.terminated or self.truncated