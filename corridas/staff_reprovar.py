from core import Interaction, Embeds
from discord import ui, TextStyle
from typing import Optional


async def reprovar_corrida(itc: Interaction):
    bot = itc.client
    modal = ReprovarForm()
    await itc.response.send_modal(modal)
    await modal.wait()
    if not modal.itc:
        return
    motivo = modal.motivo_field.value
    emb = itc.message.embeds[0]
    corrida_id = int(emb.description.split("\n")[0].split(" ")[-1])
    emb.add_field(
        name="Julgamento",
        value=f"Reprovada por {itc.user.mention}\n>>> {motivo}"
    )
    emb.colour = 16711680
    await modal.itc.response.edit_message(embed=emb, view=None)

    data = await bot.db.get('''
        UPDATE corridas
        SET resultado='REPROVADA'
        WHERE id=%s
        RETURNING canal_id
    ''', corrida_id)
    thread = bot.get_channel(data[0][0])
    emb = Embeds.red(
        "### <:naogostei:1173824189682159689> Corrida Reprovada\n"
        f"A corrida de vocês foi reprovada pela staff. Motivo da reprovação:\n>>> {motivo}"
    )
    await thread.send(content="@everyone", embed=emb)


class ReprovarForm(ui.Modal):
    motivo_field = ui.TextInput(
        label="Motivo pelo qual está reprovando:",
        style=TextStyle.paragraph,
        max_length=1000,
        required=True
    )

    def __init__(self):
        self.itc: Optional[Interaction] = None
        super().__init__(title=f"REPROVAR CORRIDA", timeout=300)

    async def on_submit(self, itc: Interaction):
        self.itc = itc