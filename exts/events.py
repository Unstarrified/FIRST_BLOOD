from disnake.ext import commands

class Events(commands.Cog, name="중계기"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def on_ready(self) -> None:
        print("FIRST BLOOD is now ready.")
    
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Events(bot))