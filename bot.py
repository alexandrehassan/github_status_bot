import os
from discord.ext import commands
# from discord import Intents
from logger import log


log("INFO", "Starting Bot")
TOKEN = os.environ["DISCORD_TOKEN"]
bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    log("INFO", "Bot is up and running")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        log("INFO", "Loading " + filename)
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)
