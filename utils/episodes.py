import json

from jobs import fetch_job

class Episode:
    def __init__(self, season: str, name: str, number: str, data: dict) -> None:
        self._data = data
        self._season = season
        self._name = name
        self._number = number
        self.name = data["name"]
        self.quote = data["quote"]
        self.rounds = data["rounds"]
        if type(data["maps"]) == list:
            self.maps = fetch_maps(data["maps"])
        else:
            self.maps = data["maps"]
        self.hard = data["hard"]
        self.special = data["special"]
        if name == "apocalpyse":
            self.jobs = {}
            self.sub = {}
            for map in self.maps:
                self.jobs[map.code] = []
                for d in data["maps"][map.code]["jobs"]["primary"]:
                    self.jobs[map.code].append(fetch_job(self, d))
                if data["maps"][map.code]["jobs"]["sub"] != []:
                    self.sub[map.code] = []
                    for d in data["maps"][map.code]["jobs"]["primary"]:
                        self.sub[map.code].append(fetch_job(self, d))
        else:
            for d in data["jobs"]["primary"]:
                self.jobs.append(fetch_job(self, d))
            if data["jobs"]["sub"] != []:
                self.sub = []
                for d in data["jobs"]["sub"]:
                    self.sub.append(fetch_job(self, d))


def fetch_episode(code: str) -> Episode:
    season, name, number = code.split("_")
    season = season.replace("_", "")
    name = name.replace("_", "")
    number = number.replace("_", "")
    data = json.load(open("src/episodes.json", "r", encoding="utf-8"))
    ep = Episode(season, name, number, data[season][name][number])
    return ep

def fetch_maps(maps: list) -> None:
    return