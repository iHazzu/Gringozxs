from discord.ext import commands
from core import Context, Bot, is_bot_admin
from discord.ext import tasks
from . import msg_competicao
from .iniciar import iniciar_competicao


class CorridasCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @tasks.loop(hours=15)
    async def reenviar_msg_competicao(self):
        await msg_competicao.reenviar(self.bot)