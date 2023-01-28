import os

import disnake
from disnake import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.default()
        intents.members = True
        super().__init__(
            status=disnake.Status.idle,
            activity=disnake.Activity(name="연구 보고", type=disnake.ActivityType.listening),
            command_prefix=">",
            intents=intents,
        )
    
    def prepare(self):
        for f in os.listdir("./exts"):
            if not f.endswith(".py"):
                continue
            self.load_extension(f"exts.{f[:-3]}")
    
    def run(self):
        super().run(token, reconnect=True)

if __name__ == "__main__":
    bot = Bot()
    bot.prepare()
    bot.run()