#########################################################################################################################
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#                                                                                                                       #
#########################################################################################################################


from discord.ext import tasks, commands
import requests
import time
import main
import bs4
import asciichartpy

bot = main.bot


class Nettools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            await ctx.send(f"```{ip} \n Associated hostname: {response.json['hostname']}\n Location: {response.json['city']}, {response.json['region']}, {response.json['country']}\n ISP: {response.json['org']}```")
        except:
            await ctx.send("Address does not exist, or is invalid.")

    @commands.command()
    async def downgraph(self, ctx, *service):
        bs4.BeautifulSoup
    #/html/body/div[3]/div[2]/div[1]/div[2]/div/div[2]/script
    #https://downdetector.com/status/discord/



#Isdown
    # ^ this pings a host