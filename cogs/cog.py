from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import requests
import json

to_ignore = ["Visit www.githubstatus.com for more information"]
COMPONENT_URL ="https://www.githubstatus.com/api/v2/components.json"
STATUS_URL = "https://www.githubstatus.com/api/v2/status.json"

watching = dict()

def get_gh_status():
    # return None
    response_json = requests.get(STATUS_URL).json()
    # print(json.dumps(response_json, sort_keys=True, indent=4))
    if response_json["status"]["indicator"] != "none":
        print("something down")
        return get_gh_comp()
    else:
        return None


def set_watching():
    response_json = requests.get(COMPONENT_URL).json()
    for component in response_json["components"]:
        if component["status"] == "operational" and component["name"] not in to_ignore:
            watching[component["name"]] = component["status"]
            print("Adding - " + component["name"])



def get_gh_comp():
    # return None
    response_json = requests.get(COMPONENT_URL).json()
    return_str = ""
    for component in response_json["components"]:
        print("Checking - " + component["name"])
        if component["name"] not in watching and component["name"] not in to_ignore:
            watching[component["name"]] = ""
            print("Was missing - " + component["name"])

        if component["name"] in watching and component["status"] != watching[component["name"]]:
            watching[component["name"]] = component["status"]
            return_str += f'**{component["name"]}** - {component["status"].replace("_", " ")}\n'
        
    if return_str != "":
        return return_str + "For more information go to https://www.githubstatus.com"
    else:
        return None

class MainCog(commands.Cog):
    def __init__(self, client):
        load_dotenv()
        self.client = client
        set_watching()
        self.channelNum = int(os.getenv('GH_CHANNEL'))
        self.channel = None
        self.periodic.start()

        
        
        
    
    @commands.command(name='gh_status', help='Gets the status of Github')
    async def gh_status(self,ctx):
        status = get_gh_status()
        if status == None:
            await ctx.send("No reported issues")
        else:
            await ctx.send(status)

    @tasks.loop(minutes=1)
    async def periodic(self):
        await self.client.wait_until_ready()

        if (self.channel == None):
            self.channel = self.client.get_channel(self.channelNum)

        status = get_gh_status()
        if status != None:
            await self.channel.send(status)
            


def setup(client):
    client.add_cog(MainCog(client))