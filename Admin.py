

    @commands.command()
    @commands.has_any_role("Administracja")
    async def przypomnij(self, ctx, czas, *, wiadomość):
        await ctx.send(f"Przypomnę ci \"{wiadomość}\" za {czas}s")
        await asyncio.sleep(int(czas))
        await ctx.author.send(f"Przypominam o {wiadomość}")

    @commands.command()
    @commands.has_any_role("Administracja")
    async def dm(self, ctx, wiadomość, *, cel):
        serwer = bot.get_guild(id_serwera)
        await serwer.get_member(int(cel.strip("<@!>"))).send(wiadomość)
        await ctx.send(f"Wysłano wiadomość do {cel}")
        print(f"Wysłano wiadomość do {cel}")
