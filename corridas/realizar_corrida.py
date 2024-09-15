from core import Bot, Corrida, Interaction, Embeds
from discord import utils, ui, ButtonStyle, TextStyle
from datetime import timedelta
from typing import Optional
from asyncio import wait_for, TimeoutError
from .salvar_corrida import salvar


async def realizar(bot: Bot, run: Corrida):
    end_time = utils.utcnow() + timedelta(minutes=15, seconds=30)
    show_time = utils.format_dt(end_time, "R")
    emb = Embeds.blue(
        "A competição de vocês começou, então prepare o seu nitro, "
        "aqueça seu carro que a partida começooooooooooou! 🏁.\n\n"
    )
    for p in run.participantes:
        emb.description += f"<:icons_reminder:1279271795752435714> {p.member.mention}\n"
    emb.description += f"\n<:seta4:1173824193176031253> A corrida finaliza em {show_time}. Caso algum jogador não "
    emb.description += f"envie o clipe e o resultado através do botao abaixo, a competição será anulada."
    view = CorridaView(run)
    msg = await run.canal.send(embed=emb, view=view)
    anulada = False
    try:
        await wait_for(view.wait(), 13*60)
    except TimeoutError:
        emb = Embeds.invisible(
            "<:seta4:1173824193176031253> O tempo da partida esta quase acabando (restam 2 minutos). "
            "Utilizem o botão da mensagem anterior para enviar os clipes e resultados.\n\n"
            "Se os clipes/resultados de todos os participantes não forem enviados agora, a competição será anulada."
        )
        await run.canal.send(content="@here", embed=emb)
        try:
            await wait_for(view.wait(), 150)
        except TimeoutError:
            emb = Embeds.red("<:icons_ban:1279251062527889460> A partida foi anulada.")
            await run.canal.send(embed=emb)
            anulada = True
    view.children[0].disabled = True
    await msg.edit(view=view)
    if not anulada:
        await salvar(bot, run)


class CorridaView(ui.View):
    def __init__(self, run: Corrida):
        super().__init__(timeout=None)
        self.run = run

    async def interaction_check(self, itc: Interaction) -> bool:
        for participante in self.run.participantes:
            if participante.member == itc.user:
                return True
        emb = Embeds.invisible("<:icons_discordmod:1279250675192172576> Você não está participando desta competição.")
        await itc.response.send_message(embed=emb, ephemeral=True)
        return False

    @ui.button(emoji="<:Icon_Roles:1178321652497535026>", label="Enviar Informações", style=ButtonStyle.gray)
    async def informacoes(self, itc: Interaction, button: ui.Button):
        modal = InformacoesForm(len(self.run.participantes))
        await itc.response.send_modal(modal)
        await modal.wait()
        if not modal.itc:
            return
        try:
            posicao = int(modal.posicao_field.value)
        except ValueError:
            emb = Embeds.invisible(
                f"<:icons_discordmod:1279250675192172576> A posição `{modal.posicao_field.value}` inserida "
                f"não é um número."
            )
            return await modal.itc.response.send_message(embed=emb, ephemeral=True)
        if posicao > len(self.run.participantes):
            emb = Embeds.invisible(f"<:icons_discordmod:1279250675192172576> Posição `{posicao}` inexistente.")
            return await modal.itc.response.send_message(embed=emb, ephemeral=True)
        for p in self.run.participantes:
            if p.member != itc.user and p.posicao == posicao:
                emb = Embeds.invisible(
                    f"<:icons_discordmod:1279250675192172576> O jogador {p.member.mention} já alegou estar na "
                    f"posição `{posicao}`. Vocês devem entrar em um consenso."
                )
                return await modal.itc.response.send_message(embed=emb, ephemeral=True)
        participante = utils.get(self.run.participantes, member=itc.user)
        participante.posicao = posicao
        participante.clipe = modal.clipe_field.value
        emb = itc.message.embeds[0]
        parts = emb.description.split("\n\n")
        lines = []
        for p in self.run.participantes:
            if p.posicao:
                line = f"<:gostei:1173824190885937182> {p.member.mention} ({p.posicao}°)"
            else:
                line = f"<:icons_reminder:1279271795752435714> {p.member.mention}"
            lines.append(line)
        parts[1] = "\n".join(lines)
        emb.description = "\n\n".join(parts)
        await modal.itc.response.edit_message(embed=emb)
        if all(p.posicao for p in self.run.participantes):
            self.stop()


class InformacoesForm(ui.Modal):
    clipe_field = ui.TextInput(
        label="Insira o link para o seu clipe da partida:",
        style=TextStyle.short,
        placeholder="https://...",
        required=True
    )
    posicao_field = ui.TextInput(
        label="Qual foi a sua posição final?",
        style=TextStyle.short,
        max_length=2,
        required=True
    )

    def __init__(self, max_posicao: int):
        self.itc: Optional[Interaction] = None
        self.posicao_field.placeholder = f"De 1 a {max_posicao}..."
        super().__init__(title=f"DADOS DA COMPETIÇÃO", timeout=120)

    async def on_submit(self, itc: Interaction):
        self.itc = itc