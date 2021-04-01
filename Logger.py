import discord
from discord.ext import commands
import datetime

#TODO: Rewrite as task
class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        else:
            print(
                f"[{datetime.datetime.now()}]  {ctx.author} sent {ctx.content} on {ctx.channel}")


def setup(bot):
    bot.add_cog(Logger(bot))
