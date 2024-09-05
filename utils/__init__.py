from discord.ext import commands
from core import Context, Bot, is_bot_admin
from . import Script


class UtilsCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @is_bot_admin()
    @commands.command(name="eval")
    async def script(self, ctx: Context, *, code: str):
        """Run a script in the bot

        Args:
            ctx: the context associated with the command
            code: the code to run
        """
        await Script.go(ctx=ctx, code=code)