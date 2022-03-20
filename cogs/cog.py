from discord.ext import commands, tasks
import os
import requests
from logger import log


to_ignore = ["Visit www.githubstatus.com for more information"]
COMPONENT_URL = "https://www.githubstatus.com/api/v2/components.json"
STATUS_URL = "https://www.githubstatus.com/api/v2/status.json"

watching = dict()


def get_gh_status() -> str:
    response_json = requests.get(STATUS_URL).json()
    if response_json["status"]["indicator"] != "none":
        return get_gh_comp()
    else:
        return None


def set_watching() -> None:
    response_json = requests.get(COMPONENT_URL).json()
    c_name = ""
    for component in response_json["components"]:
        c_name = component["name"]
        c_status = component["status"]
        if c_status == "operational" and c_name not in to_ignore:
            watching[c_name] = c_status


def get_gh_comp() -> str:
    response_json = requests.get(COMPONENT_URL).json()
    return_str = ""
    c_name = ""
    for component in response_json["components"]:
        c_name = component["name"]
        c_status = component["status"]
        if c_name not in watching and c_name not in to_ignore:
            watching[c_name] = ""
            print("Was missing - " + c_name)

        if c_name in watching and c_status != watching[c_name]:
            watching[c_name] = c_status
            return_str += f'**{c_name}** - {c_status.replace("_", " ")}\n'

    if return_str != "":
        return return_str + to_ignore[0]
    else:
        return None


class GithubCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        set_watching()
        self.channelNum = int(os.environ["GH_CHANNEL"])
        self.channel = None
        self.periodic.start()
        log("INFO", "Github Cog loaded")

    @commands.command(name="gh_status", help="Gets the status of Github")
    async def gh_status(self, ctx):
        status = get_gh_status()
        log("INFO", "Manual check triggered")
        if status is None:
            log("INFO", "No reported issues")
            await ctx.send("No reported issues")
        else:
            log("INFO", status)
            await ctx.send(status)

    @tasks.loop(minutes=1)
    async def periodic(self):
        await self.bot.wait_until_ready()
        log("DEBUG", "Periodic check triggered")
        if self.channel is None:
            self.channel = self.bot.get_channel(self.channelNum)

        status = get_gh_status()
        if status is not None:
            log("INFO", status)
            await self.channel.send(status)


def setup(bot):
    bot.add_cog(GithubCog(bot))
