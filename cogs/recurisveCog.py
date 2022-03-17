from discord.ext import commands, tasks
from dotenv import load_dotenv
import os


def get_gh_status():
    return None
    # response_json = requests.get(
    #     "https://www.githubstatus.com/api/v2/status.json").json()
    # if response_json["status"]["indicator"] != "none":
    #     return response_json["page"]["url"]
    # else:
    #     return None


class MainCog(commands.Cog):
    def __init__(self, client):
        # self.author = None
        self.client = client
        self.periodic.start()
        load_dotenv()
        self.channel = int(os.getenv('GH_CHANNEL'))

    @tasks.loop(seconds=10.0)
    async def periodic(self):
        await self.client.wait_until_ready()
        print("Loaded")
        channel = self.client.get_channel(self.channel)
        # await channel.send("periodic")
        status = get_gh_status()
        if status == None:
            print("periodic")
            # await channel.send("periodic")
        else:
            print("status")
            # await channel.send(status)


def setup(client):
    client.add_cog(MainCog(client))