from core import Interaction, Embeds
from corridas import staff_aprovar


async def go(itc: Interaction, corrida_id: int):
    data = await itc.client.db.get("SELECT true FROM corridas WHERE id=%s", corrida_id)
    if not data:
        emb = Embeds.invisible(f"<:icons_discordmod:1279250675192172576> Corrida `{corrida_id}` não existe.")
        return await itc.response.send_message(embed=emb, ephemeral=True)
    await staff_aprovar.aprovar_corrida(itc, corrida_id)