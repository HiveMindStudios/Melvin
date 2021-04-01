import asyncio
import discord
from discord.ext import tasks, commands
import os

intents = discord.Intents.default()
intents.members = True


def get_prefix(bot, message):
    """A callable Prefix for the bot."""
    prefixes = ["$", "melvin "]
    if not message.guild:
        return "$"
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
initial_extensions = ["Meta", "Fun", "Admin", "Utils", "NetTools", "MemberManagement"]

bot = commands.Bot(
    command_prefix=get_prefix, description="A multipurpose bot", intents=intents
)

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n-----------------------------------------------\n"
    )
    await bot.change_presence(
        activity=discord.Streaming(
            name="$help for commands!", url="https://github.com/VectorKappa/Melvin"
        )
    )
    print(
        f"Successfully logged in and booted...!\n-----------------------------------------------\n"
    )


bot.run(os.getenv("MELVIN_KEY"))
