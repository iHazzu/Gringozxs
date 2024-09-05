from discord.ext.commands import CommandError, Context, check
from .constants import Embeds
import logging
from discord.utils import _ColourFormatter

ADMIM_IDS = [535159866717896726, 628120853154103316]     # hazzu, Ve7s


class NotBotAdmin(CommandError):
    """Raised when someone not authorized try to use admin commands"""
    pass


def is_bot_admin():
    def predicate(ctx: Context) -> bool:
        if ctx.author.id in ADMIM_IDS:
            return True
        raise NotBotAdmin
    return check(predicate)


async def handle_error(ctx: Context, error: Exception):
    # get the original error
    error = getattr(error, 'original', error)   # hybrid layer
    error = getattr(error, 'original', error)   # command invoke layer
    if isinstance(error, NotBotAdmin):
        emb = Embeds.yellow("🔒 Only bot admins can run this command.")
        await ctx.reply(embed=emb)
    else:
        emb = Embeds.red(f"❌ An unexpected error occurred: `{error}`.")
        await ctx.reply(embed=emb)
        raise error


def setup_logging():
    """Configurar logging para exibir logs no terminal e também salvar em um arquivo"""
    terminal = logging.StreamHandler()
    terminal.setFormatter(_ColourFormatter())
    file = logging.FileHandler('logs.log', 'a')
    file.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s]: %(message)s"))
    logging.basicConfig(level=logging.WARNING, handlers=[terminal, file], force=True)