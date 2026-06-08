from game_core.Pacman_Environment import Pacman_Environment
from Backend.Student_Files.P3.Knoten import Knoten
from Backend.Student_Files.P3.Suche import Suche


class PacmanAgent:

    def __init__(self):
        self.env = Pacman_Environment()

        self.is_running = False
        self.terminated = False
        self.truncated = False
        self.statistics = {}
        self.is_last_step = False

        self.action = 1
        self.strategie = "Greedy"

        self.loesungsknoten = None
        self.action_path = []

        # Damit Frontend den letzten Dot noch anzeigen/aktualisieren kann
        self.finish_next_call = False

    def render(self):
        self.env.render()

    def reset(self, seed, level):
        self.terminated = False
        self.truncated = False
        self.statistics = {}
        self.is_last_step = False
        self.finish_next_call = False

        self.action = 1
        self.loesungsknoten = None
        self.action_path = []

        return self.env.reset(seed=seed, level=level)

    def baue_action_path(self, zielknoten):
        aktionen = []
        aktueller = zielknoten

        while aktueller.parent is not None:
            aktionen.append(aktueller.action)
            aktueller = aktueller.parent

        aktionen.reverse()
        return aktionen

    def baue_statistics(self, view=None):
        if view is None:
            view = self.env.view

        return {
            "view": view,
            "turns": self.env.turn,
            "remainingDots": self.env.remainingDots,
            "collectedDots": self.env.totalDots - self.env.remainingDots
        }

    def suche_starten(self):
        startknoten = Knoten(
            self.env.view,
            self.env.pacman.get_position()
        )

        suche = Suche()
        ziel = suche.starte_Suchalgorithmus(startknoten, self.strategie)

        if ziel is not None:
            self.action_path = self.baue_action_path(ziel)
            print("Action Path:", self.action_path)
        else:
            print("Keine Lösung gefunden.")
            self.action_path = []

    def step(self):

        # Nach dem letzten sichtbaren Schritt sauber beenden
        if self.finish_next_call:
            self.is_last_step = True
            return self.baue_statistics(), self.is_last_step

        if self.is_running and not (self.terminated or self.truncated):

            if len(self.action_path) == 0:

                if self.env.remainingDots == 0:
                    self.finish_next_call = True
                    return self.baue_statistics(), False

                print("Nächsten Dot suchen")
                self.suche_starten()

            if len(self.action_path) == 0:
                return self.baue_statistics(), False

            self.action = self.action_path.pop(0)

            observation, reward, self.terminated, self.truncated, info = self.env.step(self.action)

            print("Aktion:", self.action)
            print("Reward:", reward)

            self.statistics = self.baue_statistics(observation)

            # WICHTIG:
            # Bei Reward 10 erst noch einmal die letzte View ans Frontend senden.
            if self.terminated or self.truncated:
                self.finish_next_call = True
                return self.statistics, False, observation

            return self.statistics, self.is_last_step, observation

        return self.baue_statistics(), self.is_last_step

    def close(self):
        self.env.close()

    def is_game_over(self):
        return self.terminated or self.truncated