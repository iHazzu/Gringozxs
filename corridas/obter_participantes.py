from core import Interaction, Bot, Corrida, Participante
import discord
from .confirmar_corrida import confirmacao


async def obter_participantes(itc: Interaction, run: Corrida):
    bot = itc.client
    emb = discord.Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Envie uma mensagem mencionando o(s) outro(s) participante(s) "
                    f"desta competição:"
    )
    emb.set_author(name="Participantes da Competicão", icon_url=itc.guild.icon.url)
    await run.canal.send(content=itc.user.mention,  embed=emb)
    emb = discord.Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Criei o canal {run.canal.mention} "
                    f"para prosseguirmos com a criação da sua corrida."
    )
    if itc.data["custom_id"] == "acept_terms":
        await itc.response.edit_message(embed=emb, view=None)
    else:
        await itc.response.send_message(embed=emb, ephemeral=True)

    while True:
        msg = await resposta(run.canal, itc.user, bot)
        participantes = msg.mentions
        if itc.user in participantes:
            participantes.remove(itc.user)
        participantes.insert(0, itc.user)
        if len(participantes) > 1:
            break
        else:
            emb = discord.Embed(
                colour=0x2F3136,
                description=f"<:icons_discordmod:1279250675192172576> Mencione pelo menos um adversário para a competição:"
            )
            await msg.reply(embed=emb)
    for member in participantes:
        run.participantes.append(Participante(member))
    await confirmacao(bot, run)


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
    return msg