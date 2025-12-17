import json
import os
from datetime import date, datetime, timedelta

STATS_FILE = "stats.json"
CALENDAR_FILE = "calendar.json"

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


class Calendar:
    def __init__(self):
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}
            self.save()

    def add_entry(self, day_str, happiness_value, notes=""):
        if day_str not in self.data:
            self.data[day_str] = {
                "date": day_str,
                "happiness": happiness_value,
                "notes": notes,
                "color": self._calculate_color(happiness_value)
            }
            self.save()

    def get_entry(self, day_str):
        return self.data.get(day_str)

    def update_entry(self, day_str, happiness_value, notes=""):
        self.data[day_str] = {
            "date": day_str,
            "happiness": happiness_value,
            "notes": notes,
            "color": self._calculate_color(happiness_value)
        }
        self.save()

    def _calculate_color(self, happiness_value):
        if happiness_value >= 70:
            return "green"
        elif happiness_value >= 40:
            return "yellow"
        else:
            return "red"

    def get_all(self):
        return self.data

    def save(self):
        with open(CALENDAR_FILE, "w") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


class Player:
    def __init__(self):
        self.stats = Stats()
        self.calendar = Calendar()
        self.actions_today = {}
