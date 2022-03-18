import os
from discord.ext import commands
from dotenv import load_dotenv
import logging

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    logging.info("Bot is up and running")


for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        logging.info("Loading " + filename)
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)
