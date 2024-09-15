from core import Bot, Corrida, Embeds, MOD_CHANNEL_ID
from discord import ui, ButtonStyle


async def salvar(bot: Bot, run: Corrida):
    for p in run.participantes:
        await bot.db.set('''
            INSERT INTO participantes(jogador_id, corrida_id, posicao, clipe)
            VALUES (%s, %s, %s, %s)
        ''', p.jog_id, run.id, p.posicao, p.clipe)
    emb = Embeds.invisible(
        f"## Competição {run.id}"
    )
    run.participantes = sorted(run.participantes, key=lambda x: x.posicao)
    v = "\n".join([f"{p.posicao}. {p.member.mention} [clipe]({p.clipe})" for p in run.participantes])
    emb.add_field(name="Canal", value=f"<:seta4:1173824193176031253> {run.canal.mention}", inline=False)
    emb.add_field(name="Resultado", value=f"<:seta4:1173824193176031253> {v}", inline=False)
    view = ui.View(timeout=None)
    view.add_item(ui.Button(
        emoji="<:gostei:1173824190885937182>", label="Aprovar",
        style=ButtonStyle.gray, custom_id="aprovar_corrida"
    ))
    view.add_item(ui.Button(
        emoji="<:naogostei:1173824189682159689>", label="Reprovar",
        style=ButtonStyle.gray, custom_id="reprovar_corrida"
    ))
    channel = bot.get_channel(MOD_CHANNEL_ID)
    await channel.send(embed=emb, view=view)

    emb = Embeds.invisible(
        "<:seta4:1173824193176031253> A nossa Moderação recebeu as informações da competição e ela esta em análise. "
        "Vocês serão notificados quando o resultado sair.\n\n"
        "<:seta4:1173824193176031253> Enquanto aguardam o resultado, deixem um feedback "
        "para os players da partidas clicando no botão abaixo."
    )
    emb.title = f"### <:sinoo:1173824189036245073> Corrida {run.id} Registrada"
    view2 = ui.View(timeout=None)
    view2.add_item(ui.Button(
        emoji="<:chat:1173824187845062707>", label="Feedback",
        style=ButtonStyle.gray, custom_id="feedback_corrida"
    ))
    await run.canal.send(embed=emb, view=view2)
