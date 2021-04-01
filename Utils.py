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
import re
import random
import numpy as np


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


def setup(bot):
    bot.add_cog(Utils(bot))
