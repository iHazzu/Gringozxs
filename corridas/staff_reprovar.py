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
    emb = itc.message.embeds[0]
    corrida_id = int(emb.title.split(" ")[-1])
    emb.add_field(
        name="Julgamento",
        value=f"Reprovada por {itc.user.mention}\n>>> {modal.motivo_field.value}"
    )
    emb.colour = 16711680
    await modal.response.edit_message(embed=emb, view=None)

    data = await bot.db.get("SELECT canal_id FROM corridas WHERE id=%s", corrida_id)
    thread = bot.get_channel(data[0][0])
    emb = Embeds.red(
        "### <:naogostei:1173824189682159689> Corrida Reprovada\n"
        f"A corrida de vocês foi reprovada pela staff. Motivo da reprovação:\n>>> {modal.motivo_field.value}"
    )
    await thread.send(content="@here", embed=emb)


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