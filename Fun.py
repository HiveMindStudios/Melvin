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

import discord
from discord.ext import commands
import requests
import random
from json.decoder import JSONDecodeError


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def op(self, ctx, user):
        await ctx.send(f"{user} was given Administrator rights")

    @commands.command()
    async def bless(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} blessed {user}. What a good person.")

    @commands.command()
    async def askgod(self, ctx):
        await ctx.send(
            [
                "You probably don't want to know.",
                "Certainly, maybe?",
                "I can't predict it right now",
                "Why should I tell you?",
            ][random.randint(0, 3)]
        )

    @commands.command()
    async def kill(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} killed {user}")

    @commands.command()
    async def infect(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} infected {user} with Covid-19")

    @commands.command()
    async def yn(self, ctx):
        await ctx.send(["Yes.", "No."][random.randint(0, 1)])

    @commands.command()
    async def dox(self, ctx, user="<@763866497683554305>"):
        await ctx.send(
            f"{user}'s IP address is {random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        )

    @commands.command()
    async def give(self, ctx, user, item, amount=1):
        if user != None and item != None:
            await ctx.send(f"{ctx.author.mention} gave {amount} {item} to {user}")
        else:
            await ctx.send("Please specify user and item")

    @commands.command()
    async def kit(self, ctx, type="free"):
        await ctx.send(f"{ctx.author.mention} recevied a {type} kit!")

    @commands.command(hidden=True)
    async def uuid(self, ctx, user=""):
        if user != None:
            await ctx.send(f"{user}'s uuid: {ctx.mentions}")
        else:
            await ctx.send(f"Your uuid: {ctx.author.id}")


    @commands.command()
    async def tp(self, ctx, who, where):
        """Moves an user to a specified VC."""
        channel = ctx.get_channel(where)
        member = ctx.get_member(who)
        await member.move_to(channel)

    @commands.command()
    async def helloworld(self, ctx):
        """Hello world!"""
        h = random.randint(0, 100)
        if h == 69:
            await ctx.send("Shit Happens.")
        else:
            await ctx.send("Hello World!")

    @commands.command()
    async def randomtp(self, ctx, user=""):
        """Moves specified user to random VC in server.
        Defaults to command invoker"""
        voiceChannels = []
        for guild in ctx.bot.guilds:
            for channel in ctx.guild.voice_channels:
                voiceChannels.append(channel)
                randomchannel = random.randint(0, len(voiceChannels) - 1)
        if user == "":
            user = ctx.author.id
        else:
            user = int(user.strip("<@!>"))
        await self.bot.get_guild(ctx.guild.id).get_member(user).move_to(
            voiceChannels[randomchannel]
        )

    @commands.command()
    async def yeet(self, ctx, target=""):
        if target == "":
            user = ctx.author.id
        else:
            user = int(target.strip("<@!>"))
        await self.bot.get_guild(ctx.guild.id).get_member(user).move_to(None)

    @commands.command()
    async def metar(self, ctx, ICAO="ZKPY", verbosity="", measuringUnit="meters"):
        """Shows weather for ICAO code
        When passed with an ICAO airport code <https://airportcodes.io/>, returns current weather in METAR format and forecast in TAF format,
        When -v is passed as verbosity flag, shows latitude, longitude, altitude, city and country code"""
        embed = discord.Embed(
            title="Weather Info For: " + ICAO.upper(),
            colour=random.randint(1, 16777215),
        )
        try:
            response = requests.get(f"https://wx.void.fo/all/{ICAO.upper()}").json()
            embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author.name))
            embed.add_field(name="Airport Name:", value=response["name"], inline=False)
            try:
                embed.add_field(
                    name="Current Weather:", value=response["metar"], inline=False
                )
            except:
                embed.add_field(
                    name="Current Weather:", value="No METAR found!", inline=False
                )
            try:
                embed.add_field(
                    name="Weather Forecast:", value=response["taf"], inline=False
                )
            except:
                embed.add_field(
                    name="Weather Forecast:", value="No TAF found!", inline=False
                )
            if verbosity == "-v":
                embed.add_field(name="City:", value=response["city"], inline=False)
                embed.add_field(
                    name="Country Code:", value=response["country_code"], inline=False
                )
                embed.add_field(
                    name="Latitude:",
                    value=str(response["latitude"]) + "°",
                    inline=False,
                )
                embed.add_field(
                    name="Longitude:",
                    value=str(response["longitude"]) + "°",
                    inline=False,
                )
                embed.add_field(
                    name="Altitude:",
                    value=str(response["altitude_feet"]) + "ft"
                    if measuringUnit.lower() == "feet" or measuringUnit.lower() == "ft"
                    else str(response["altitude_meters"]) + "m",
                    inline=False,
                )
        except JSONDecodeError:
            embed.add_field(name="Error encountered:", value="Enter a valid ICAO code")

        await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
