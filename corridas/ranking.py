import discord
from core import Bot
from datetime import datetime, UTC


rank_message = None


async def update_ranking(bot: Bot):
    start_date = datetime.now(UTC).date().replace(day=1)
    data = await bot.db.get('''
        SELECT j.discord_id, SUM(p.pontos) AS pts, COUNT(*) as corridas
        FROM jogadores j
        INNER JOIN participantes p ON p.jogador_id=j.id
        INNER JOIN corridas c ON c.id=p.corrida_id
        WHERE c.resultado='APROVADA' AND c.criado_em > %s
        GROUP BY j.discord_id
        ORDER BY pts DESC
        LIMIT 10
    ''', start_date)
    emb = discord.Embed(
        description="### <:icons_shine1:1279271814270550168> Melhores P1s do Mês\n",
        colour=16763904
    )
    for i, d in enumerate(data):
        emb.description += f"{i+1}. <@{d[0]}>: {d[1]} pts / {d[2]} runs\n"
    msg = await load_rank_message(bot)
    emb.set_footer(text="Ranking atualizado a cada 5 mins", icon_url=msg.guild.icon.url)
    await msg.edit(embed=emb)


async def load_rank_message(bot: Bot) -> discord.Message:
    global rank_message
    if rank_message is None:
        channel = bot.get_channel(1281236703587205120)
        rank_message = await channel.fetch_message(1285808462478966794)
    return rank_message