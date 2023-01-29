import json
import random
from datetime import datetime, timezone

import disnake
from disnake.ext import commands


class Utility(commands.Cog, name="유틸리티"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.slash_command(name="랜덤")
    async def random(self, inter: disnake.ApplicationCommandInteraction) -> None:
        return await inter.response.pong()
    
    @random.sub_command(name="직업")
    async def _randomRole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        episode: Optional[str] = commands.Param(default="s2_division_ep3", name="에피소드", desc="", choices=[
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 제로", value="s1_original_ep0"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 1", value="s1_original_ep1"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 2", value="s1_original_ep2"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 3", value="s1_original_ep3"),
            disnake.OptionChoice(name="히어로즈 : 에피소드 1", value="s1_heroes_ep1"),
            disnake.OptionChoice(name="히어로즈 : 에피소드 2", value="s1_heroes_ep2"),
            disnake.OptionChoice(name="히어로즈 : 에피소드 3", value="s1_heroes_ep3"),
            disnake.OptionChoice(name="히어로즈 : 에피소드 4", value="s1_heroes_ep4"),
            disnake.OptionChoice(name="아포칼립스", value="s1_apocalypse_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 1", value="s2_division_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 2", value="s2_division_ep2"),
            disnake.OptionChoice(name="디비전 : 에피소드 3", value="s2_division_ep3"),
        ])
    ):
        await inter.response.defer(ephemeral=False)
        season, name, number = episode.split("_")
        season = season.replace("_", "")
        name = name.replace("_", "")
        number = number.replace("_", "")
        if name == "apocalypse":
            view = MapSelect(inter)
            await inter.edit_original_message(view=view)
            await view.wait()
            if view.result is None:
                return await inter.edit_original_message(content="선택 시간 초과로 인해 취소되었습니다.", view=None)
            jobs = data[season][name][number]["maps"][view.result]["jobs"]
        else:
            jobs = data[season][name][number]["jobs"]["primary"]
            sub = data[season][name][number]["jobs"]["sub"]
        data = None # Jobs data
        result = [random.choice(jobs)]
        if sub is not None:
            result = [random.choice(jobs), random.choice(sub)]

        selected = []
        for job in result:
            job = data[season][name][number][job]
            embed = disnake.Embed(name=job["name"], description=job["description"], color=job["color"], timestamp=datetime.now(timezone.utc))
            embed.set_author(name="불새위키", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
            selected.append(embed)
        
        rd = random.randint(1, 100)
        text = "랜덤 선택된 직업은 **{job['emote']}**입니다."
        if rd == 57:
            text = "... (골라줬으니 귀찮게 하지 말고 꺼지라는 눈빛이다.)"
        await inter.edit_original_message(content=text, embeds=selected)

def setup(bot: commands.Bot) -> None: