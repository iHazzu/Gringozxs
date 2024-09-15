from core import Interaction
from typing import Optional, Tuple
from discord import ui, ButtonStyle, Embed
import json


with open("corridas/termos_embed.json") as file:
    termos_emb = Embed.from_dict(json.load(file))


async def fetch_jog_id(itc: Interaction) -> Tuple[Optional[Interaction], Optional[int]]:
    bot = itc.client
    data = await bot.db.get("SELECT id FROM jogadores WHERE discord_id=%s", itc.user.id)
    if data:
        return itc, data[0][0]
    view = TermsView()
    await itc.response.send_message(embed=termos_emb, view=view, ephemeral=True)
    await view.wait()
    return view.itc, view.jog_id


class TermsView(ui.View):
    def __init__(self):
        self.itc: Optional[Interaction] = None
        self.jog_id: Optional[int] = None
        super().__init__(timeout=600)

    @ui.button(emoji="<:gostei:1173824190885937182>", label="Li e aceito os termos", style=ButtonStyle.gray, custom_id="acept_terms")
    async def acept(self, itc: Interaction, button: ui.Button):
        self.itc = itc
        data = await itc.client.db.get("INSERT INTO jogadores(discord_id) VALUES(%s) RETURNING id", itc.user.id)
        self.jog_id = data[0][0]
        self.stop()

    @ui.button(emoji="<:naogostei:1173824189682159689>", label="Eu discordo", style=ButtonStyle.gray)
    async def reject(self, itc: Interaction, button: ui.Button):
        emb = Embed(
            colour=0x265aed,
            description="<:naogostei:1173824189682159689> O termo não foi aceito e você não poderá continuar com a sua ação."
        )
        await itc.response.edit_message(embed=emb, view=None)
        self.stop()