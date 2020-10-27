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
import youtube_dl
from discord.ext import tasks, commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_opts = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)


class Muzyka(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['dołącz'])
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Dołącza do kanału głosowego"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command(aliases=['graj', 'odtwórz'])
    async def play(self, ctx, *, url):
        """Odtwarza utwór z URLa"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                'Błąd odtwarzacza: %s' % e) if e else None)

        await ctx.send('Teraz leci: {}'.format(player.title))

    @commands.command(aliases=['transmituj'])
    async def stream(self, ctx, *, url):
        """Odtwarza na żywo z URLa"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(
                'Błąd odtwarzacza: %s' % e) if e else None)

        await ctx.send('Teraz leci: {}'.format(player.title))

    @commands.command(aliases=['głośność'])
    async def volume(self, ctx, volume: int):
        """Zmienia głośność odtwarzania"""

        if ctx.voice_client is None:
            return await ctx.send("Nie podłączono do żadnego kanału.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Zmieniono głośność na {}%".format(volume))

    @commands.command(aliases=['zatrzymaj'])
    async def stop(self, ctx):
        """Zatrzymuje bota i rozłącza go"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                # blad_dolaczania
                await ctx.send("Nie jesteś podłączony do żadnego kanału głosowego.")
                raise commands.CommandError(
                    "Autor wiadomości nie jest podpięty do serwera.")  # leave as is
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
