from core import Interaction, Embeds


async def go(itc: Interaction, corrida_id: int):
    bot = itc.client
    data = await bot.db.get("UPDATE corridas SET resultado='Anulada' WHERE id=%s RETURNING canal_id", corrida_id)
    if not data:
        emb = Embeds.invisible(f"<:icons_discordmod:1279250675192172576> Corrida `{corrida_id}` não existe.")
        return await itc.response.send_message(embed=emb, ephemeral=True)
    await bot.db.set("UPDATE participantes SET pontos=0 WHERE corrida_id=%s", corrida_id)
    emb = Embeds.green(f"<:icons_like:1279250706208919644> Corrida `{corrida_id}` anulada.")
    await itc.response.send_message(embed=emb)
    thread = bot.get_channel(data[0][0])
    emb = Embeds.red(
        "### <:naogostei:1173824189682159689> Corrida Anulada\n"
        f"A corrida de vocês foi anulada pela staff."
    )
    await thread.send(content="@everyone", embed=emb)