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


from random import randint
from discord.ext import tasks, commands
import discord
import requests


class NetTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx, ip: str):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json").json()
            embed = discord.Embed(
                title="IP Address Info:", description=ip, colour=randint(1, 16777215)
            )
            embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author.name))
            try:
                embed.add_field(
                    name="Associated hostname:",
                    value=response["hostname"],
                    inline=False,
                )
            except:
                embed.add_field(
                    name="Associated hostname:",
                    value="This address has no hostname associated.",
                )
            embed.add_field(
                name="Location:",
                value=f"[{response['city']}, {response['region']}, {response['country']}](https://google.com/maps/search/{response['loc']})",
                inline=False,
            )
            embed.add_field(
                name="Organisation/ISP:", value=response["org"], inline=False
            )
            await ctx.send(content=None, embed=embed)
        except:
            await ctx.send("Address does not exist, or is invalid.")


def setup(bot):
    bot.add_cog(NetTools(bot))
