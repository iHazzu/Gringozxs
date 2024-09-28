from core import Interaction, Embeds
from discord import ui, TextStyle
from typing import Optional


async def aprovar_corrida(itc: Interaction):
    bot = itc.client
    emb = itc.message.embeds[0]
    corrida_id = int(emb.description.split("\n")[0].split(" ")[-1])
    jogs_data = await bot.db.get('''
        SELECT j.id, j.discord_id
        FROM jogadores j
        INNER JOIN participantes p ON p.jogador_id=j.id 
        WHERE p.corrida_id=%s
        ORDER BY p.posicao''', corrida_id)
    jog_ids = [d[0] for d in jogs_data]
    modal = AprovarForm(len(jog_ids))
    await itc.response.send_modal(modal)
    await modal.wait()
    if not modal.itc:
        return
    points = modal.points_field.value.split(" ")
    if len(points) != len(jog_ids) or not all(p.isdigit() for p in points):
        emb = Embeds.invisible(
            f"<:icons_discordmod:1279250675192172576> Você inseriu a pontuação para cada jogador de forma incorreta. "
            f"Insira a pontuação dos jogadores separada por espaço e em ordem de posição. Por "
            f"exemplo, se uma corrida teve 3 participantes, insira `10 5 2` para adicionar 10 pontos ao 1° lugar, "
            f"5 pontos ao 2° lugar e 2 pontos ao 3° lugar."
        )
        return await modal.itc.response.send_message(embed=emb, ephemeral=True)
    query = ""
    for i, jog_id in enumerate(jog_ids):
        query += f"UPDATE participantes SET pontos={points[i]} WHERE jogador_id={jog_id};"
    query += f"UPDATE corridas SET resultado='Aprovada' WHERE id={corrida_id}"
    await bot.db.set(query)
    emb.add_field(
        name="Aprovada",
        value=f"Moderador: {itc.user.mention}\nPontuações: `{modal.points_field.value}`",
        inline=False
    )
    emb.colour = 3853362
    await modal.itc.response.edit_message(embed=emb, view=None)

    data = await bot.db.get("SELECT canal_id FROM corridas WHERE id=%s", corrida_id)
    thread = bot.get_channel(data[0][0])
    emb = Embeds.green(
        "### <:gostei:1173824190885937182> Corrida Aprovada\n"
        "A corrida de vocês foi aprovada pela staff. Confiram a pontuação que cada jogador recebeu:\n"
    )
    for i, d in enumerate(jogs_data):
        emb.description += f"{i+1}. <@{d[1]}>: {points[i]} pts\n"
    await thread.send(content="@everyone", embed=emb)


class AprovarForm(ui.Modal):
    points_field = ui.TextInput(
        label="Pontuação para cada um dos {} jogadores:",
        style=TextStyle.short,
        required=True
    )

    def __init__(self, n_participantes: int):
        self.itc: Optional[Interaction] = None
        self.points_field.label = self.points_field.label.format(n_participantes)
        super().__init__(title=f"APROVAR CORRIDA", timeout=300)

    async def on_submit(self, itc: Interaction):
        self.itc = itc