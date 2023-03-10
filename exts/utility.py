import random

import disnake
from disnake.ext import commands

from utils.episodes import Episode, episode_embed, fetch_episode
from utils.jobs import job_view


class Utility(commands.Cog, name="유틸리티"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    class MapSelection(disnake.ui.View):
        def __init__(self, episode: Episode, inter: disnake.ApplicationCommandInteraction) -> None:
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
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 ZERO", value="s1_original_ep0"),
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
    ) -> None:
        await inter.response.defer(ephemeral=False)
        if episode in ["s1_heroes_ep4", "s1_apocalypse_ep1"]:
            return await inter.edit_original_message(content=":boom: > 해당 에피소드의 특수성으로 인해 아직 지원되지 않는 기능입니다.")
        episode = fetch_episode(episode)
        jobs = episode.jobs
        sub = None
        if len(episode.sub) != 0:
            sub = episode.sub
        result = [random.choice(jobs)]
        if sub is not None:
            result = [random.choice(jobs), random.choice(sub)]

        embed, view = job_view(self.bot, result[0])
        view.inter = inter
        rd = random.randint(1, 100)
        text = f"> <:firebird_wiki:1069982735403319296> 랜덤 선택된 직업은 **{result[0].emote} {result[0].name}**입니다."
        if rd == 57:
            text = "> <:firebird_wiki:1069982735403319296> ... *(골라줬으니 귀찮게 하지 말고 꺼지라는 눈빛이다.)*"
        await inter.edit_original_message(content=text, embed=embed, view=view)

    @random.sub_command(name="에피소드", description="스토리 모드에서 플레이할 에피소드를 골라줍니다.")
    async def _randomEpisode(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.defer()
        episodes = ["s1_original_ep0", "s1_original_ep1", "s1_original_ep2", "s1_original_ep3", "s2_division_ep1", "s2_division_ep2", "s2_division_ep3"]
        code = random.choice(episodes)
        episode = fetch_episode(code)
        embed = episode_embed(self.bot, episode)
        rd = random.randint(1, 100)
        text = f"> <:firebird_wiki:1069982735403319296> 랜덤 선택된 에피소드는 **{episode.name}**입니다."
        if rd == 57:
            text = "> <:firebird_wiki:1069982735403319296> ... *(골라줬으니 귀찮게 하지 말고 꺼지라는 눈빛이다.)*"
        await inter.edit_original_message(content=text, embed=embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Utility(bot))
