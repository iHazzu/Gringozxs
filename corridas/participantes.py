from core import Interaction, Bot
import discord


async def obter_participantes(itc: Interaction, corrida_id: int, thread: discord.Thread):
    bot = itc.client
    emb = discord.Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Envie uma mensagem mencionando o(s) outro(s) participante(s) "
                    f"desta competição:"
    )
    emb.set_author(name="Participantes da Competicão", icon_url=itc.guild.icon.url)
    await thread.send(content=itc.user.mention,  embed=emb)
    emb = discord.Embed(
        colour=0x2F3136,
        description=f"<:seta4:1173824193176031253> Criei o canal {thread.mention} "
                    f"para prosseguirmos com a criação da sua corrida."
    )
    if itc.data["custom_id"] == "acept_terms":
        await itc.response.edit_message(embed=emb, view=None)
    else:
        await itc.response.send_message(embed=emb, ephemeral=True)

    while True:
        msg = await resposta(thread, itc.user, bot)
        participantes = msg.mentions
        if itc.user in participantes:
            participantes.remove(itc.user)
        participantes.insert(0, itc.user)
        if len(participantes) > 1:
            break
        else:
            emb = discord.Embed(
                colour=0x2F3136,
                description=f"<:icons_discordmod:1279250675192172576> Mencione pelo menos um adversário para a competição."
            )
            await msg.reply(embed=emb)


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