import discord
from typing import Optional, List


class Participante:
    def __init__(self, member: discord.Member, jog_id: Optional[int] = None):
        self.member = member
        self.jog_id = jog_id
        self.clipe: Optional[str] = None
        self.posicao: Optional[int] = None


class Corrida:
    def __init__(self, corrida_id: int, criador: discord.Member, thread: discord.Thread):
        self.id = corrida_id
        self.cridador = criador
        self.canal = thread
        self.participantes: List[Participante] = []