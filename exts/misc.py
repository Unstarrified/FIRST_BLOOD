import os
from datetime import datetime, timezone

import disnake
import humanize
import psutil
from disnake.ext import commands

humanize.i18n.activate("ko_KR")

class Misc(commands.Cog, name="일반"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command(name="핑", description="정동석이 여기서부터 저기까지 찍고 오는데 얼마나 걸리나요?")
    async def _pingPong(self, inter: disnake.ApplicationCommandInteraction) -> None:
        start = datetime.now()
        await inter.response.defer()
        end = datetime.now()
        delay = round((float(str(end - start)[6:]) * 1000), 2)
        late = round(self.bot.latency * 1000, 2)
        uptime = datetime.now() - datetime.fromtimestamp(psutil.Process(os.getpid()).create_time())
        uptime = humanize.precisedelta(uptime, minimum_unit="seconds", format="%0.0f").replace("and ", "").replace(",", "")
        embed = disnake.Embed(description=f"""
> 🔭 {late}ms
> ✉️ {delay}ms
> ⏰️ {uptime}
        """, color=0x000001, timestamp=datetime.now(timezone.utc))
        embed.set_author(name="정동석에 대하여", icon_url="https://cdn.discordapp.com/attachments/1068907896882089994/1069235582175281203/IMG_2647.jpg")
        embed.set_footer(text="FIRST BLOOD 프로젝트", icon_url=self.bot.user.display_avatar.url)
        await inter.edit_original_message(content="", embed=embed)
    
    @commands.slash_command(name="문의", description="하긴... 제가 봐도 쟤 인성이...")
    async def _inquiry(self, inter: disnake.ApplicationCommandInteraction) -> None:
        await inter.response.send_message("> <:medic:1068899454603755621> 사용이 어렵거나, 사용 중에 문제가 발생했다면 아래 서버로 알려주세요!\n> https://discord.gg/ap3DXd9Hdc", ephemeral=True)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Misc(bot))

