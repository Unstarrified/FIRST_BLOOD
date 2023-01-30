import json
import random
from datetime import datetime, timezone

import disnake
from disnake.ext import commands


class Utility(commands.Cog, name="유틸리티"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    class MapSelect(disnake.ui.View):
        def __init__(self, inter: disnake.ApplicationCommandInteraction) -> None:
            super().__init__(timeout=60)
            self.inter = inter
            self.result = None
        
        async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
            return inter.author == self.inter.author

        @disnake.ui.select()
        async def _select(self, select: disnake.ui.Select, inter: disnake.MessageInteraction) -> None:
            await inter.response.edit_message(view=None)
            self.result = select.values[0]
            self.stop()

    @commands.slash_command(name="랜덤")
    async def random(self, inter: disnake.ApplicationCommandInteraction) -> None:
        return await inter.response.pong()
    
    @random.sub_command(name="직업", description="스토리 모드에서 사용할 직업을 골라줍니다.")
    async def _randomRole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        episode: str = commands.Param(name="에피소드", desc="플레이할 에피소드를 선택해주세요.", choices=[
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 제로", value="s1_original_ep0"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 1", value="s1_original_ep1"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 2", value="s1_original_ep2"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 3", value="s1_original_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 1", value="s1_heroes_ep1"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 2", value="s1_heroes_ep2"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 3", value="s1_heroes_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 4", value="s1_heroes_ep4"),
#            disnake.OptionChoice(name="아포칼립스", value="s1_apocalypse_ep1"),
#            disnake.OptionChoice(name="디비전 : 에피소드 1", value="s2_division_ep1"),
#            disnake.OptionChoice(name="디비전 : 에피소드 2", value="s2_division_ep2"),
#            disnake.OptionChoice(name="디비전 : 에피소드 3", value="s2_division_ep3"),
        ])
    ) -> None:
        await inter.response.defer(ephemeral=False)
        if episode in ["s1_heroes_ep4", "s1_apocalypse_ep1"]:
            return await inter.edit_original_message(content=":boom: > 해당 에피소드의 특수성으로 인해 아직 지원되지 않는 기능입니다.")
        season, name, number = episode.split("_")
        season = season.replace("_", "")
        name = name.replace("_", "")
        number = number.replace("_", "")
        data = json.load(open("src/episodes.json", "r", encoding="utf-8"))
        if name == "apocalypse":
            view = self.MapSelect(inter)
            await inter.edit_original_message(view=view)
            await view.wait()
            if view.result is None:
                return await inter.edit_original_message(content=":boom: > 선택 시간 초과로 인해 취소되었습니다.", view=None)
            jobs = data[season][name][number]["maps"][view.result]["jobs"]
        else:
            jobs = data[season][name][number]["jobs"]["primary"]
        sub = None
        if data[season][name][number]["jobs"]["sub"] != []:
            sub = data[season][name][number]["jobs"]["sub"]
        ep_name = data[season][name][number]["name"]
        quote = data[season][name][number]["quote"]
        data = json.load(open("src/jobs.json", "r", encoding="utf-8"))
        result = [random.choice(jobs)]
        if sub is not None:
            result = [random.choice(jobs), random.choice(sub)]

        job = data[season][name][number][result[0]]
        color = job["color"].replace("#", "")
        color = color.replace("0x", "")
        color = int(color, 16)
        embed = disnake.Embed(title=job["name"], description=job["description"], color=disnake.Colour(color), timestamp=datetime.now(timezone.utc))
        embed.set_author(name=f"불새위키 - {ep_name}", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
        embed.set_footer(text=quote, icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=job["image"])
        
        rd = random.randint(1, 100)
        text = f"> 랜덤 선택된 직업은 **{job['emote']} {job['name']}**입니다."
        if rd == 57:
            text = "> ... *(골라줬으니 귀찮게 하지 말고 꺼지라는 눈빛이다.)*"
        await inter.edit_original_message(content=text, embed=embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Utility(bot))