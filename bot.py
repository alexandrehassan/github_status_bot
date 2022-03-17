import os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GH_CHANNEL = int(os.getenv('GH_CHANNEL'))


client = commands.Bot(command_prefix='/')
# If you don't want the default help command and want to make by yourself, you can use this:
# client.remove_command('help')

# With this event, always when your bot is online, it will be printed on the terminal:
@client.event
async def on_ready():
    print('Bot Online!')

# This causes all files inside the folder with the ending .py to be loaded, without having to load one by one:
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)