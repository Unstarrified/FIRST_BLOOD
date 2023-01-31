import disnake
from disnake.ext import commands

from utils.episodes import episode_embed, fetch_episode
from utils.jobs import job_view

class Information(commands.Cog, name="정보제공"):
    class JobSelection(disnake.ui.View):
        class JobSelect(disnake.ui.StringSelect):
            def __init__(self, episode):
                super().__init__(
                    placeholder="열람할 직업을 선택해주세요.",
                    options=[
                        disnake.SelectOption(label=job.name, value=str(episode.jobs.index(job)), description=job.description, emoji=job.emote)
                        for job in episode.jobs
                    ],
                    min_values=1,
                    max_values=1,
                )
                self.episode = episode
            
            async def callback(self, inter: disnake.MessageInteraction) -> None:
                embed, view = job_view(self.view.inter.bot, self.episode.jobs[int(self.values[0])])
                view.inter = self.view.inter
                await inter.response.edit_message(content="", embed=embed, view=view)
                self.view.stop()
        
        def __init__(self, inter, episode):
            super().__init__()
            self.inter = inter
            self.episode = episode
            self.add_item(self.JobSelect(episode))
        
        async def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
            return inter.user == self.inter.user
        
        async def on_timeout(self) -> None:
            embed = disnake.Embed(description="> ⏱️ 시간 초과로 인해 취소되었습니다.", color=0xFF0000)
            embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=self.inter.bot.user.display_avatar.url)
            await self.inter.edit_original_message(content="", embed=embed, view=None)
            msg = await self.inter.original_response()
            await msg.delete(delay=1)
        
        @disnake.ui.button(label="취소하기", style=disnake.ButtonStyle.red, emoji="⏹️", row=1)
        async def _cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction) -> None:
            embed = disnake.Embed(description="> ⏹️ 사용자가 작업을 취소했습니다.", color=0xFF0000)
            embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=self.inter.bot.user.display_avatar.url)
            await self.inter.edit_original_message(content="", embed=embed, view=None)
            msg = await self.inter.original_response()
            await msg.delete(delay=1)

    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.slash_command(name="정보")
    async def info(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.pong()
    
    @info.sub_command(name="모드", description="좀비고등학교의 게임 모드에 대한 정보를 표시합니다.")
    async def _infoMode(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.send_message("> <:smasher:1068904705167732737> 이 기능은 아직 준비 중입니다.", ephemeral=True)

    @info.sub_command(name="에피소드", description="스토리 모드의 에피소드에 대한 정보를 표시합니다.")
    async def _infoEpisode(self,
        inter: disnake.ApplicationCommandInteraction,
        episode: str = commands.Param(name="에피소드", desc="정보를 열람할 에피소드를 선택해주세요.", choices=[
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 ZERO", value="s1_original_ep0"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 1", value="s1_original_ep1"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 2", value="s1_original_ep2"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 3", value="s1_original_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 1", value="s1_heroes_ep1"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 2", value="s1_heroes_ep2"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 3", value="s1_heroes_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 4", value="s1_heroes_ep4"),
#            disnake.OptionChoice(name="아포칼립스", value="s1_apocalypse_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 1", value="s2_division_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 2", value="s2_division_ep2"),
            disnake.OptionChoice(name="디비전 : 에피소드 3", value="s2_division_ep3"),
        ])
    ) -> None:
        await inter.response.defer()
        episode = fetch_episode(episode)
        embed = episode_embed(self.bot, episode)
        await inter.edit_original_message(embed=embed)
    
    @info.sub_command(name="직업", description="스토리 모드의 역할군에 대한 정보를 표시합니다.")
    async def _infoJob(
        self,
        inter: disnake.ApplicationCommandInteraction,
        episode: str = commands.Param(name="에피소드", desc="정보를 열람할 에피소드를 선택해주세요.", choices=[
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 ZERO", value="s1_original_ep0"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 1", value="s1_original_ep1"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 2", value="s1_original_ep2"),
            disnake.OptionChoice(name="진격의 좀비 : 에피소드 3", value="s1_original_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 1", value="s1_heroes_ep1"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 2", value="s1_heroes_ep2"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 3", value="s1_heroes_ep3"),
#            disnake.OptionChoice(name="히어로즈 : 에피소드 4", value="s1_heroes_ep4"),
#            disnake.OptionChoice(name="아포칼립스", value="s1_apocalypse_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 1", value="s2_division_ep1"),
            disnake.OptionChoice(name="디비전 : 에피소드 2", value="s2_division_ep2"),
            disnake.OptionChoice(name="디비전 : 에피소드 3", value="s2_division_ep3"),
        ])
    ) -> None:
        await inter.response.defer()
        episode = fetch_episode(episode)
        view = self.JobSelection(inter, episode)
        await inter.edit_original_message(content="열람할 직업을 아래 목록에서 선택해주세요.", view=view)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Information(bot))