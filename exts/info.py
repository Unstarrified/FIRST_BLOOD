# import disnake
from disnake.ext import commands

class Information(commands.Cog, name="정보제공"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Information(bot))