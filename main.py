import asyncio
import discord
from discord.ext import tasks, commands
import os

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True


def get_prefix(bot, message):
    """A callable Prefix for the bot."""
    prefixes = ["$", "melvin "]
    if not message.guild:
        return "$"
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
initial_extensions = ["Meta", "Fun", "Admin", "Utils", "Music", "Logger", "NetTools", "MemberManagement"]

bot = commands.Bot(
    command_prefix=get_prefix, description="A multipurpose bot", intents=intents
)

if __name__ == "__main__":
    pass

@bot.event
async def on_ready():
    for extension in initial_extensions:
        await bot.load_extension(extension)
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
