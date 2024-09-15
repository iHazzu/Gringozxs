from discord.ext import commands
from core import Bot
from discord.ext import tasks
from . import msg_competicao
from .iniciar import iniciar_competicao
from .feedback import feedback_corrida


class CorridasCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.reenviar_msg_competicao.start()

    @tasks.loop(hours=15)
    async def reenviar_msg_competicao(self):
        await msg_competicao.reenviar(self.bot)