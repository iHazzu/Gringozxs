from core import Interaction, Embeds
from discord import Embed, utils


async def info(itc: Interaction, corrida_id: int):
    bot = itc.client
    data = await bot.db.get('''
        SELECT criado_em, canal_id, resultado,
        (SELECT discord_id FROM jogadores WHERE id=corridas.criador_id)
        FROM corridas
        WHERE id=%s
    ''', corrida_id)
    if not data:
        emb = Embeds.invisible(f"<:icons_discordmod:1279250675192172576> Corrida `{corrida_id}` não existe.")
        return await itc.response.send_message(embed=emb, ephemeral=True)
    d = data[0]
    emb = Embed(
        description=f"### Competição {corrida_id}\nConfira os detalhes da competição:",
        colour=0xffd700
    )
    emb.add_field(name="Criada em", value=utils.format_dt(d[0], 'd'), inline=True)
    criador = f"<@{d[3]}>" if d[3] else "Deletado"
    emb.add_field(name="Criada por", value=criador, inline=True)
    emb.add_field(name="Canal", value=f"<#{d[1]}>", inline=True)
    pdata = await bot.db.get('''
        SELECT p.posicao, j.discord_id, p.pontos, p.clipe
        FROM participantes p
        INNER JOIN jogadores j ON j.id=p.jogador_id
        WHERE p.corrida_id=%s
        ORDER BY p.posicao
    ''', corrida_id)
    v = ""
    for i, j in enumerate(pdata):
        v += f"{i+1}. <@{j[1]}>: {j[2]} pts [clipe]({j[3]})\n"
    emb.add_field(name="Jogadores/ranking", value=v, inline=False)
    v = d[2] if d[2] else "Não avaliada"
    emb.add_field(name="Avaliação", value=v, inline=False)
    await itc.response.send_message(embed=emb)