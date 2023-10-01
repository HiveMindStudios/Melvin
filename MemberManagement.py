import discord
from discord.ext import commands


class MembersCog(commands.Cog, name="Member Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f"{member.display_name} joined on {member.joined_at}")

    @commands.command(name="top_role", aliases=["toprole"])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(
            f"The top role for {member.display_name} is {member.top_role.name}"
        )

    @commands.command(name="perms", aliases=["perms_for", "permissions"])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member = None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""
        if not member:
            member = ctx.author

        perms = "\n".join(perm for perm, value in member.guild_permissions if value)

        # * Embed creation
        embed = discord.Embed(
            title="Permissions for:", description=ctx.guild.name, colour=member.colour
        )
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        embed.add_field(name="\uFEFF", value=perms)

        await ctx.send(content=None, embed=embed)


async def setup(bot):
    await bot.add_cog(MembersCog(bot))
