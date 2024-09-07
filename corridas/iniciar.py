from core import Interaction
from .termos import acept_terms
from discord import Embed


async def iniciar_competicao(itc: Interaction):
    itc = await acept_terms(itc)
    if not itc:
        return
    embed = Embed(
        colour=0x2F3136,
        description="<:seta4:1173824193176031253> Criei o canal #corrida-1 para prosseguirmos com a criação da sua corrida."
    )
    if itc.data["custom_id"] == "acept_terms":
        await itc.response.edit_message(embed=embed)
    else:
        await itc.response.send_message(embed=embed, ephemeral=True)