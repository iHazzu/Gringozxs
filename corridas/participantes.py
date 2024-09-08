from core import Interaction, Bot
import discord
from typing import Union


async def obter_participantes(itc: Interaction, corrida_id: int, thread: discord.Thread):
    bot = itc.client
    emb = discord.Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Envie uma mensagem mencionando o(s) outro(s) participante(s)"
                    f"desta competição:"
    )
    emb.set_author(name="Participantes da Competicão", icon_url=itc.guild.icon.url)
    await thread.send(content=itc.user.mention,  embed=emb)
    msg = await resposta(thread, itc.user, bot)


async def resposta(
        channel: discord.TextChannel | discord.Thread,
        user: discord.abc.Snowflake,
        bot: Bot
) -> discord.Message:
    def check(m):
        if m.author == user and m.channel.id == channel.id:
            if not (m.content.startswith('!') and bot.get_command(m.content[1:]) is not None):
                return True
        return False
    msg = await bot.wait_for('message', check=check, timeout=600)
    await msg.add_reaction("<:icons_like:1279250706208919644>")
    return msg