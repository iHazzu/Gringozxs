# -*- coding: utf-8 -*-
from core import Context, Bot, handle_error, setup_logging
from utils import UtilsCog
from os import environ as env
import asyncio


# object initialization
bot = Bot()


# events
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"\033[92m|=====| BOT ONLINE |=====|\n\033[94m- Client: {bot.user}\033[00m")


@bot.event
async def on_command_error(ctx: Context, error: Exception):
    await handle_error(ctx=ctx, error=error)


# running
async def main():

    # logs settup to terminal and file
    setup_logging()

    try:
        # commands categories
        await bot.add_cog(UtilsCog(bot=bot))

        await bot.start(env["DISCORD_BOT_TOKEN"])   # conecting bot
    finally:
        await bot.close()


asyncio.run(main())