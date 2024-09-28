from discord.ext import commands, tasks
from core import Bot, Interaction
from discord import app_commands, Permissions
from . import msg_competicao, Corrida
from .iniciar import iniciar_competicao
from .feedback import feedback_corrida
from .staff_reprovar import reprovar_corrida
from .staff_aprovar import aprovar_corrida
from .ranking import update_ranking


class CorridasCog(commands.Cog):
    corrida_group = app_commands.Group(
        name='corrida',
        description='gerenciamento de corridas',
        guild_ids=[1151642725142237249],
        default_permissions=Permissions(administrator=True)
    )

    def __init__(self, bot: Bot):
        self.bot = bot
        self.reenviar_msg_competicao.start()
        self.atualizar_ranking_loop.start()
        bot.tree.add_command(self.corrida_group)

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

    @corrida_group.command(name="info")
    async def corrida_info(self, itc: Interaction, corrida_id: int):
        """Obter as informações de uma corrida

        Args:
            itc: a interação associado ao comando
            corrida_id: o id da corrida (ex: 43)
        """
        await Corrida.info(itc, corrida_id)