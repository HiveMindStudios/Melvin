import discord
from discord.ext import commands
import asyncio

# TODO: ye olde switcharoo (Admin <=> Meta)
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindme(self, ctx, time, *, msg):
        """Bot will send a private message after given time (in seconds)"""
        await ctx.send(f'I\'ll remind you of "{msg}" in {time} seconds')
        await asyncio.sleep(int(time))
        await ctx.author.send(f"Hi! Popping in to remind you about {msg}. Cheers!")

    @commands.command()
    async def dm(self, ctx, target, *, message):
        """Sends a DM to an user"""
        await self.bot.get_guild(ctx.guild.id).get_member(
            int(target.strip("<@!>"))
        ).send(message)
        await ctx.send(f"DM'd {target}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
