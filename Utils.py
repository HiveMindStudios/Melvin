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
from discord.ext import tasks, commands
import re
import random
import numpy as np
import whois

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, query="d20"):
        """Rolls the dice! Default - d20
        Syntax:
        [amount]d<sides>[kh<number>][kl<number>][r<number>][+|-<number>]
        kh{num} - Keep Highest <number> rolls ([amount] should be more than <num>+1)
        kl{num} - Keep Lowest <number> rolls ([amount] should be more than <num>+1)
        r{num} - Lowest roll will be <number>
        [+|-{num}] - add/subtract modifier <number>"""
        diceRolls = re.findall(r"(\+|-|\/|\*)?([\d]*)d([\d]*)(kh|kl|r)?([\d])*", query)
        toCalc = []
        k = 0
        modifiers = re.findall(r"(\+|-)+([\d]*)(?!d)", query)
        modSum = 0
        for mod in modifiers:
            if mod[1] == "":
                temp = list(mod)
                temp[1] = 0
                mod = tuple(temp)
            toCalc.append([mod[0], mod[1], "", ""])
            modSum += int(str(mod[0]) + str(mod[1]))
        g = 0
        diceRolls = np.array(diceRolls)
        for i in range(len(diceRolls)):
            if diceRolls[i][1] == "":
                diceRolls[i][1] = 1
            if diceRolls[i][0] == "":
                diceRolls[i][0] = "+"
        try:
            for rolls in diceRolls:
                #! Check if roll function exists
                if diceRolls[k][3] != "":
                    #! Roll dice and drop lowest (keep highest)
                    if diceRolls[k][3] == "kh":
                        rolledDice = []
                        droppedDice = []
                        for i in range(int(diceRolls[k][1])):
                            rolledDice.append(random.randint(1, int(diceRolls[k][2])))

                        for j in range(len(rolledDice) - int(diceRolls[k][4])):
                            droppedDice.append(
                                rolledDice.pop(rolledDice.index(min(rolledDice)))
                            )

                        toCalc.append(
                            [diceRolls[k][0], sum(rolledDice), rolledDice, droppedDice]
                        )
                    #! Roll dice and drop highest (keep lowest)
                    elif diceRolls[k][3] == "kl":
                        rolledDice = []
                        droppedDice = []
                        for i in range(int(diceRolls[k][1])):
                            rolledDice.append(random.randint(1, int(diceRolls[k][2])))

                        for j in range(len(rolledDice) - int(diceRolls[k][4])):
                            droppedDice.append(
                                rolledDice.pop(rolledDice.index(max(rolledDice)))
                            )

                        toCalc.append(
                            [diceRolls[k][0], sum(rolledDice), rolledDice, droppedDice]
                        )
                    #! Roll dice with a minimum roll
                    elif diceRolls[k][3] == "r":
                        toCalc.append(
                            random.randint(diceRolls[k][4], diceRolls[k][2], "", "")
                        )
                    #! Exit command when function is unknown (shouldn't happen)
                    else:
                        raise Exception("RollFuncErr")
                else:
                    rolledDice = []
                    for i in range(int(diceRolls[k][1])):
                        rolledDice.append(random.randint(1, int(diceRolls[k][2])))
                    toCalc.append([diceRolls[k][0], sum(rolledDice), rolledDice, ""])
                k += 1
            #! Start of the calculations and messages
            l = 0
            result = ""
            mess = f"Rolling {query}:"
            for calculations in toCalc:
                #! Calculatations
                if calculations[0] == "" and l != 0:
                    calculations[0] = "+"
                result += str(calculations[0]) + str(calculations[1])
                #! Message creation
                if calculations[2] != "":
                    mess += "{"
                    for i in range(len(calculations[2])):
                        mess += f"({calculations[2][i]}) + "
                    for i in range(len(calculations[3])):
                        mess += f"(~~{calculations[3][i]}~~) + "
                    mess += "} + "
                l += 1
            mess = re.sub(r"\) \+ \}", ")}", mess)
            await ctx.send(f"{mess}{modSum}: **{eval(result)}**")
            # *                 ^ call a spade a spade, eh?
            # *                                ~Peter
        except:
            print(f"{ctx.author} attempted to roll with invalid roll function")
            await ctx.send(f"Unknown roll function")
    @commands.command()
    async def whois(self, ctx, domain):
        if type(domain) != str:
            await ctx.send(f"{domain} is not a string")    
        else:
            domainData = whois.whois(domain)
            if domainData.domain_name == None:
                await ctx.send(f"Domain: {domain}, doesn't exist")
            else:
                embed = discord.Embed(
                    title=f"Domain info for {domain}",
                    colour=discord.Colour.random()
                )
                noData = embed.add_field(
                        name="Country",
                        value="Unable to find data"
                    )
                embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author.name))
                embed.add_field(
                    name="Domain Name:",
                    value=f"{domainData.domain_name} UTC",
                    inline=False
                )
                embed.add_field(
                    name="Updated:",
                    value=f"{domainData.updated_date if type(domainData.updated_date) == str else domainData.updated_date[0]} UTC",
                    inline=False
                )
                embed.add_field(
                    name="Created:",
                    value=f"{domainData.creation_date if type(domainData.creation_date) == str else domainData.creation_date[0]} UTC",
                    inline=False
                )
                embed.add_field(
                    name="Expires:",
                    value=f"{domainData.expiration_date if type(domainData.expiration_date) == str else domainData.expiration_date[0]} UTC",
                    inline=False
                )
                embed.add_field(
                    name="Name Servers:",
                    value=str(domainData.name_servers),
                    inline=False
                )
                embed.add_field(
                    name="Registrar:",
                    value=domainData.registrar,
                    inline=False
                )
                try:
                    embed.add_field(
                        name="Country:",
                        value=domainData.country,
                        inline=False
                    )
                except:
                    noData
                try:
                    embed.add_field(
                        name="City:",
                        value=domainData.city,
                        inline=False
                    )
                except:
                    noData
                try:
                    embed.add_field(
                        name="Adress:",
                        value=domainData.adress,
                        inline=False
                    )
                except:
                    noData
                try:
                    embed.add_field(
                        name="Org:",
                        value=domainData.org,
                        inline=False
                    )
                except:
                    noData
            await ctx.send(content=None, embed=embed)


def setup(bot):
    bot.add_cog(Utils(bot))
