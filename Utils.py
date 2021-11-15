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

import os
from discord.ext import tasks, commands
import discord
import re
import random
import numpy as np
import urllib
import datetime
from json.decoder import JSONDecodeError
import requests
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qr(self, ctx, *, content):
        """Generates a QR code

        Args:
            content (string): Text to be converted to an QR code
        """
        try:
            embed = discord.Embed(
                title="Here's your QR code!",
                colour=random.randint(1, 16777215),
                url=f"http://api.qrserver.com/v1/create-qr-code/?data={urllib.parse.quote(str(content))}&size=1000x1000&ecc=Q&margin=8",
                timestamp=datetime.datetime.now(),
            )
            embed.set_image(
                url=f"http://api.qrserver.com/v1/create-qr-code/?data={urllib.parse.quote(str(content))}&size=256x256&ecc=Q&margin=8"
            )
            embed.set_footer(
                text="Melvin",
                icon_url="https://cdn.discordapp.com/avatars/763866497683554305/c104103646e159b7b5921be963d9d663.png?size=128",
            )
            await ctx.send(embed=embed)
        except:
            await ctx.send("Error")

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
            await ctx.send("Unknown roll function")


    @commands.command()
    async def metar(self, ctx, ICAO="ZKPY", verbosity="", measuringUnit="meters"):
        """Shows weather for ICAO code
        When passed with an ICAO airport code <https://airportcodes.io/>, returns current weather in METAR format and forecast in TAF format,
        When -v is passed as verbosity flag, shows latitude, longitude, elevation, city and country code"""
        embed = discord.Embed(
            title="Weather Info For: " + ICAO.upper(),
            colour=random.randint(1, 16777215),
        )
        try:
            response = requests.get(f"https://avwx.rest/api/metar/{ICAO.upper()}?options=info,summary&airport=true&reporting=true&format=json&onfail=cache", headers={"Authorization": os.getenv("ICAO_API_KEY")}).json()
            embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author.name))
            embed.add_field(name="Airport Name:", value=response["info"]["name"], inline=False)
            try:
                embed.add_field(
                    name="Current Weather:", value=response["sanitized"], inline=False
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
                embed.add_field(name="City:", value=response["info"]["city"], inline=False)
                embed.add_field(
                    name="Country Code:", value=response["info"]["country"], inline=False
                )
                embed.add_field(
                    name="State Code:", value=response["info"]["state"], inline=False
                )
                embed.add_field(
                    name="Latitude:",
                    value=str(response["info"]["latitude"]) + "°",
                    inline=False
                )
                embed.add_field(
                    name="Longitude:",
                    value=str(response["info"]["longitude"]) + "°",
                    inline=False
                )
                embed.add_field(
                    name="Elevation:",
                    value=str(response["info"]["elevation_ft"]) + "ft"
                    if measuringUnit.lower() == "feet" or measuringUnit.lower() == "ft"
                    else str(response["info"]["elevation_m"]) + "m",
                    inline=False
                )
            if verbosity == "-s":
                embed.add_field(name="Explanation:", value=response["summary"], inline=False)
        except JSONDecodeError:
            embed.add_field(name="Error encountered:", value="Enter a valid ICAO code")

        await ctx.send(content=None, embed=embed)


    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f"{random.randint(1,6)}!")

def setup(bot):
    bot.add_cog(Utils(bot))
