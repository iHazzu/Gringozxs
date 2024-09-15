from core import Interaction, Embeds
from discord import ui, TextStyle
from typing import Optional


async def feedback_corrida(itc: Interaction):
    bot = itc.client
    modal = FeedbackForm()
    await itc.response.send_modal(modal)
    await modal.wait()
    if not modal.itc:
        return
    emb = itc.message.embeds[0]
    corrida_id = int(emb.title.split(" ")[-2])
    member_ids = await bot.db.get('''
        SELECT j.discord_id
        FROM jogadores
        INNER JOIN participantes p ON p.jogador_id=j.id
        WHERE p.corrida_id=%s AND j.discord_id != %s
    ''', corrida_id, itc.user.id)
    emb = Embeds.invisible(
        f"### Novo Feedback\n"
        f"O usuário {itc.user.mention} deixou um feedback para os jogadores que participaram da corrida com ele.\n\n"
        f">>> {modal.feedback_field.value}"
    )
    mentions = "-" + "\n-".join([f" <@{m_id}>" for m_id in member_ids])
    emb.add_field(name="Feedback para:", value=mentions, inline=False)
    channel = bot.get_channel(1281236640085442602)
    await channel.send(embed=emb)
    emb = Embeds.invisible(f"<:chat:1173824187845062707> {itc.user.mention}, feedback enviado!")
    await modal.itc.response.send_message(embed=emb)


class FeedbackForm(ui.Modal):
    feedback_field = ui.TextInput(
        label="Seu feedback para os demais jogadores:",
        style=TextStyle.paragraph,
        max_length=1000,
        required=True
    )

    def __init__(self):
        self.itc: Optional[Interaction] = None
        super().__init__(title=f"FEEDBACK", timeout=1000)

    async def on_submit(self, itc: Interaction):
        self.itc = itc