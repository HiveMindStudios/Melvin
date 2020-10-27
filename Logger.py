import discord
import re
from discord.ext import tasks, commands
import datetime

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == bot.user:
            return
        else:
            print(
                f"[{datetime.datetime.now()}]  {ctx.author} napisał {ctx.content} na {ctx.channel}")


def setup(bot):
    bot.add_cog(Logger(bot))
