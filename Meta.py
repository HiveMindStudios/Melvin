
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


class Meta(commands.Cog, name="Meta Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {int(self.bot.latency*1000)}ms")

    @commands.command()
    async def time(self, ctx):
        await ctx.send(f"The current time is: {time.time()}s (from 1/1/1970)")

    @commands.command(name='dump', hidden=True)
    async def dump(self, ctx, target):
        await ctx.send(await self.bot.application_info())

    @commands.command()
    async def guilds(self, ctx):
        await ctx.send(len(self.bot.guilds))

    @commands.command()
    async def status(self, ctx, verbose_flag):
        await ctx.send(f"""```
        Bot latency: {int(self.bot.latency*1000)} ms \n
        Connected guilds: {len(self.bot.guilds) if verbose_flag != True else self.bot.guilds } \n
        
        """)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

def setup(bot):
    bot.add_cog(Meta(bot))
