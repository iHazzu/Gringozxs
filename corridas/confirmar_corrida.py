from discord import ui, ButtonStyle, Embed
from discord.utils import get
from core import Interaction, Bot, Corrida
from .termos import fetch_jog_id


async def confirmacao(bot: Bot, run: Corrida):
    emb = Embed(
        colour=0x2F3136,
        description=f"A corrida será iniciada quando todos os participantes clicarem no botão abaixo.\n\n"
    )
    for p in run.participantes:
        emb.description += f"<:icons_reminder:1279271795752435714> {p.member.mention}\n"
    emb.description += "\n<:seta4:1173824193176031253> Antes de confirmar a corrida, verifique se você esta em um "
    emb.description += "chat de voz e se você esta pronto para começar a gravar."
    view = ConfirmarCorrida(run)
    await run.canal.send(embed=emb, view=view)
    if await view.wait():
        return


class ConfirmarCorrida(ui.View):
    def __init__(self, run: Corrida):
        super().__init__(timeout=300)
        self.run = run
        self.a_confirmar = [p.member for p in run.participantes]

    async def interaction_check(self, itc: Interaction) -> bool:
        if itc.user not in self.a_confirmar:
            emb = Embed(
                colour=0x2F3136,
                description=f"<:icons_discordmod:1279250675192172576> Você já confirmou a corrida. Aguarde até que "
                            f"os demais participantes também confirmem."
            )
            await itc.response.send_message(embed=emb, ephemeral=True)
            return False
        return True

    @ui.button(emoji="<:icons_like:1279250706208919644>", label="Confirmar", style=ButtonStyle.gray)
    async def confirmar(self, itc: Interaction, button: ui.Button):
        itc2, jog_id = await fetch_jog_id(itc)
        participante = get(self.run.participantes, member=itc.user)
        participante.jog_id = jog_id
        self.a_confirmar.remove(itc.user)
        emb = itc.message.embeds[0]
        parts = emb.description.split("\n\n")
        lines = []
        for p in self.run.participantes:
            if p.member in self.a_confirmar:
                line = f"<:icons_reminder:1279271795752435714> {p.member.mention}"
            else:
                line = f"<:gostei:1173824190885937182> {p.member.mention}"
            lines.append(line)
        parts[1] = "\n".join(lines)
        emb.description = "\n\n".join(parts)
        if itc2.data["custom_id"] == "acept_terms":
            emb_terms = Embed(colour=0x265aed, description="<:gostei:1173824190885937182> Você confirmou a corrida.")
            await itc2.response.edit_message(embed=emb_terms)
            await itc.message.edit(embed=emb)
        else:
            await itc.response.edit_message(embed=emb)
        if not self.a_confirmar:
            self.stop()