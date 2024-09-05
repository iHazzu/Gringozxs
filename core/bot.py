import discord
from .database import DataBase
from discord.ext import commands
from os import environ as env


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            case_insensitive=True,
            intents=discord.Intents(messages=True, members=True, guilds=True),
            member_cache_flags=discord.MemberCacheFlags.none(),
            max_messages=None
        )
        self.db = DataBase(max_conections=10)

    async def setup_hook(self) -> None:
        await self.db.connect(env["DATABASE_URL"])

    async def terminate(self) -> None:
        self.db.close()
        await self.close()