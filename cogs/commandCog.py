from discord.ext import commands

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
        self.client = client

    @commands.command(name='gh_status', help='Gets the status of Github')
    async def gh_status(self,ctx):
        status = get_gh_status()
        if status == None:
            print("No reported issues")
            # await ctx.send("No reported issues")
        else:
            print("status")
            # await ctx.send(status)


def setup(client):
    client.add_cog(MainCog(client))