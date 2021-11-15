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
import random



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

def setup(bot):
    bot.add_cog(Fun(bot))
