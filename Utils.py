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
import re
import random


    # !health - Health and food level of bot

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #TODO Rewrite command to use better syntax
    @commands.command()
    async def roll(self, ctx, query = 'd20'):
        diceRolls = re.findall("[\d]*)d([\d]*)(kh|kl|r)?(?(3)([\d]*))(\+|-|\*|\/)?(?(5)([\d]*)")
        for rolls in diceRolls:
            if diceRolls.group(3):






def setup(bot):
    bot.add_cog(Utils(bot))