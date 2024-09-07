from core import Bot
from discord.ui import View


async def reenviar(bot: Bot):
    channel = bot.get_channel(1275907152963309699)
    async for msg in channel.history():
        if not msg.embeds:
            continue
        emb = msg.embeds[0]
        if not emb.author or "Sistema de Competição" not in emb.author.name:
            continue
        view = View.from_message(msg)
        emb.set_author(name=f"Sistema de Competição - {channel.guild.name}", icon_url=channel.guild.icon.url)
        await channel.send(embed=emb, view=view)
        await msg.delete()
        break