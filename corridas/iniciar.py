from core import Interaction
from .termos import fetch_jog_id
from discord import Embed
from participantes import obter_participantes


async def iniciar_competicao(itc: Interaction):
    itc, criador_id = await fetch_jog_id(itc)
    if not itc:
        return
    data = await itc.client.db.get("INSERT INTO corridas(criador_id) VALUES (%s) RETURNING id")
    corrida_id = data[0][0]
    thread = await itc.channel.create_thread(name=f"Corrida {corrida_id}", invitable=True)
    embed = Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Criei o canal {thread.mention} "
                    f"para prosseguirmos com a criação da sua corrida."
    )
    if itc.data["custom_id"] == "acept_terms":
        await itc.response.edit_message(embed=embed, view=None)
    else:
        await itc.response.send_message(embed=embed, ephemeral=True)
    await obter_participantes(itc, corrida_id, thread)