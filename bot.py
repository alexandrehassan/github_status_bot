import os
from discord.ext import commands
from discord import Intents
from logger import log


log("INFO", "Starting Bot")
TOKEN = os.environ["DISCORD_TOKEN"]
client = commands.Bot(command_prefix="/", intents=Intents.GUILD_MESSAGES)


@client.event
async def on_ready():
    log("INFO", "Bot is up and running")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        log("INFO", "Loading " + filename)
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
