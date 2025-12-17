import json
import os

STATS_FILE = "stats.json"

class Stats:
    def __init__(self):
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r") as f:
                self.values = json.load(f)
        else:
            self.values = {
                "salud": 60,
                "estudios": 55,
                "amistades": 60,
                "economia": 50,
                "disciplina": 50,
                "familia": 65,
                "relacion": 80,
                "felicidad": 70
            }
            self.save()

    def get(self, key):
        return self.values.get(key, 0)

    def modify(self, key, amount):
        self.values[key] = max(0, min(100, self.values.get(key, 0) + amount))
        self.recalculate_happiness()
        self.save()

    def recalculate_happiness(self):
        core = (
            self.values["salud"] +
            self.values["relacion"] +
            self.values["amistades"] +
            self.values["disciplina"]
        ) / 4

        penalty = 0
        if self.values["salud"] < 30:
            penalty += 10
        if self.values["disciplina"] < 30:
            penalty += 10

        self.values["felicidad"] = max(0, min(100, int(core - penalty)))

    def save(self):
        with open(STATS_FILE, "w") as f:
            json.dump(self.values, f, indent=2)


class Player:
    def __init__(self):
        self.stats = Stats()
        self.actions_today = {}
