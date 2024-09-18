from discord.ext import commands
from core import Bot
from discord.ext import tasks
from . import msg_competicao
from .iniciar import iniciar_competicao
from .feedback import feedback_corrida
from .staff_reprovar import reprovar_corrida
from .staff_aprovar import aprovar_corrida
from .ranking import update_ranking


class CorridasCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.reenviar_msg_competicao.start()
        self.atualizar_ranking_loop.start()

    @tasks.loop(hours=15)
    async def reenviar_msg_competicao(self):
        if not self.reenviar_msg_competicao.current_loop:
            return
        await msg_competicao.reenviar(self.bot)

    @tasks.loop(minutes=5)
    async def atualizar_ranking_loop(self):
        await update_ranking(self.bot)

    @reenviar_msg_competicao.before_loop
    @atualizar_ranking_loop.before_loop
    async def wait_ready(self):
        await self.bot.wait_until_ready()