from core import Interaction, Corrida
from .termos import fetch_jog_id
from .obter_participantes import obter_participantes


async def iniciar_competicao(itc: Interaction):
    itc, criador_id = await fetch_jog_id(itc)
    if not itc:
        return
    data = await itc.client.db.get("INSERT INTO corridas(criador_id) VALUES (%s) RETURNING id", criador_id)
    corrida_id = data[0][0]
    thread = await itc.channel.create_thread(name=f"Corrida {corrida_id}", invitable=True)
    corrida = Corrida(corrida_id, itc.user, thread)
    await obter_participantes(itc, corrida)