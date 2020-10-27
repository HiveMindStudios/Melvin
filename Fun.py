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

from typing import no_type_check
from discord.ext import tasks, commands
import requests
import re
import random

yn = ["Yes.", "No."]
god = ["You probably don't want to know.", "Certainly, maybe?", "I can't predict it right now", "Why should I tell you?"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def op(self, ctx, user):
        await ctx.send(f"{user} was given Administrator rights")

    @commands.command()
    async def bless(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} blessed {user}. What a good person")

    @commands.command()
    async def askgod(self, ctx):
        await ctx.send(god[random.randint(0, len(god)-1)])

    @commands.command()
    async def kill(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} killed {user}")

    @commands.command()
    async def infect(self, ctx, user):
        await ctx.send(f"{ctx.author.mention} infected {user} with Covid-19")

    @commands.command()
    async def yes(self, ctx):
        await ctx.send(yes[random.randint(0, len(yes)-1)])

    @commands.command()
    async def no(self, ctx):
        await ctx.send(no[random.randint(0, len(no)-1)])

    @commands.command()
    async def yn(self, ctx):
        await ctx.send(yn[random.randint(0, 1)])

    @commands.command()
    async def dox(self, ctx, user=""):
        if not user == "":
            await ctx.send("Error")
        else:
            await ctx.send(f"{user}'s IP address is {random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}")



    #TODO $tp - teleport!
    #TODO $tpa - Request teleport to someone
    #TODO $tphere - Request someone to teleport to you
    #TODO $tpaccept - Accept a teleport request
    #TODO $tpdeny - Deny a teleport request
    #TODO $randomtp - Teleport to the random voice channel
    #TODO $locate - locate a user (only vc)
    #TODO $uuid - Find a minecraft player's uuid
    #TODO $online EXAMPLE "!online 2b2t.org" - Check how many players are online on a minecraft server.
    #* $ip - find location and isp of an ip or domain.
    #* $down - Check if a website is down
    #TODO $runtime - Uptime of bot (runtime has been disabled due to an exploit re-enabled.)
    #TODO $whois - Check who is the owner of the website server moderators for breaking the rules.
    #* $no - NO
    #* $yes - YES
    #TODO $give - give someone something
    #TODO $kill - kill someone
    #TODO $bless - bless someone. You are a good person.
    #TODO $dox - find someones ip
    #* $nwordcount - !nwordcount PLAYER - check how many nwords the player has said. Added for black history month.
    #* $quote - get a random message someone has said!
    #TODO $y/n - Yes or no
    #TODO $infect - infect someone with autisms.
    #TODO $askgod / !askallah / !askrusher - ask
    #TODO $kit - recieve a kit!
    #TODO $execute - start a vote to execute someone, use /kill yes or /kill no to vote.

    #TODO $urban or !ud - Get top urban dictionary definition
    #TODO $verse or !bible - Get a random bible verse!