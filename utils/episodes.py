import json
from datetime import datetime, timezone

import disnake
from disnake.ext import commands

from .jobs import fetch_job

class Episode:
    def __init__(self, season: str, name: str, number: str, data: dict) -> None:
        self._data = data
        self._season = season
        self._name = name
        self._number = number
        self.name = data["name"]
        self.quote = data["quote"]
        self.rounds = data["rounds"]
        self.image = data.get("image")
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
                self.sub[map.code] = []
                for d in data["maps"][map.code]["jobs"]["primary"]:
                    self.sub[map.code].append(fetch_job(self, d))
        else:
            self.jobs = []
            self.sub = []
            for d in data["jobs"]["primary"]:
                self.jobs.append(fetch_job(self, d))
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

def episode_embed(bot: commands.Bot, episode: Episode) -> disnake.Embed:
    embed = disnake.Embed(title=episode.name, description=episode.quote, color=0x000001, timestamp=datetime.now(timezone.utc))
    embed.set_author(name="시나리오 플레이어", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
    embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=bot.user.display_avatar.url)
    if episode.image is not None:
        embed.set_image(url=episode.image)
    embed.add_field(name="스토리 분기", value=episode._season.replace("s", "스토리 시즌 "), inline=False)
    embed.add_field(name="라운드 수 (0라운드 제외)", value=f"총 {episode.rounds} 라운드")
    if type(episode.maps) == list:
        embed.add_field(name="총 맵 개수", value= f"{len(episode.maps)}개", inline=False)
    else:
        embed.add_field(name="총 맵 개수", value= f"{episode.maps}개", inline=False)
    embed.add_field(name="주요 역할군 개수", value=f"{len(episode.jobs)}개")
    embed.add_field(name="보조 역할군 개수", value=f"{len(episode.sub)}개")
    embed.add_field(name="하드 모드 여부", value="네" if episode.hard is True else "아니오", inline=False)
    if len(episode.special) != 0:
        specs = ""
        for spec in episode.special:
            if spec == "":
                specs += "\n**하드 모드 한정**\n"
                continue
            specs += f"{spec}\n"
        embed.add_field(name="특수사항", value=specs, inline=False)
    return embed