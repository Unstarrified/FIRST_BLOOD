import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(
            status=disnake.Status.idle,
            activity=disnake.Activity(name="연구 보고", type=disnake.ActivityType.listening),
            command_prefix=">",
            intents=intents,
            case_insensitive=True,
            allowed_mentions=disnake.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
            help_command=None
        )
    
    def prepare(self):
        for f in os.listdir("./exts"):
            if not f.endswith(".py"):
                continue
            try:
                self.load_extension(f"exts.{f[:-3]}")
            except Exception as e:
                print(e)
                pass
    
    def run(self):
        super().run(os.getenv("FIRST_BLOOD_TOKEN"), reconnect=True)

if __name__ == "__main__":
    bot = Bot()
    bot.prepare()
    bot.run()