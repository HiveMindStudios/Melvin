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

import asyncio
import discord
import yt_dlp
from discord.ext import tasks, commands

yt_dlp.utils.bug_reports_message = lambda: ""

ytdl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_opts = {"options": "-vn"}

ytdl = yt_dlp.YoutubeDL(ytdl_opts)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins the VC"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Plays from URL"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player, after=lambda e: print("Player error: %s" % e) if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def stream(self, ctx, *, url):
        """Plays an URL live"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print("Player error: %s" % e) if e else None
            )

        await ctx.send(f"Now playing: {player.title}")

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes volume of the player"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to any VC.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You're not connected to any VC.")
                raise commands.CommandError(
                    "Author not connected to any VC."
                )  # leave as is
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(bot):
    await bot.add_cog(Music(bot))
