import discord
from contextlib import suppress
from typing import Callable
from discord.ext.commands import Context


class Pagination(discord.ui.View):
    def __init__(self, ctx: Context, get_page: Callable):
        self.ctx = ctx
        self.get_page = get_page
        self.n_pages = None
        self.message = None
        self.index = 1
        super().__init__(timeout=100)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        else:
            emb = discord.Embed(
                description=f"Only the author of the command can perform this action.",
                color=16711680
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False

    async def navegate(self):
        emb, self.n_pages = await self.get_page(self.index)
        if self.n_pages == 1:
            await self.ctx.reply(embed=emb)
        elif self.n_pages > 1:
            self.update_buttons()
            self.message = await self.ctx.reply(embed=emb, view=self)

    async def edit_page(self, interaction: discord.Interaction):
        emb, self.n_pages = await self.get_page(self.index)
        self.update_buttons()
        await interaction.response.edit_message(embed=emb, view=self)

    def update_buttons(self):
        if self.index > self.n_pages // 2:
            self.children[2].emoji = "⏮️"
        else:
            self.children[2].emoji = "⏭️"
        self.children[0].disabled = self.index == 1
        self.children[1].disabled = self.index == self.n_pages

    @discord.ui.button(custom_id="anterior", emoji="◀️", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1
        await self.edit_page(interaction)

    @discord.ui.button(custom_id="proxima", emoji="▶️", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1
        await self.edit_page(interaction)

    @discord.ui.button(custom_id="end/home", emoji="⏭️", style=discord.ButtonStyle.blurple)
    async def end(self, interaction: discord.Interaction, button: discord.Button):
        if self.index <= self.n_pages//2:
            self.index = self.n_pages
        else:
            self.index = 1
        await self.edit_page(interaction)

    async def on_timeout(self):
        if self.message:
            with suppress(discord.NotFound):
                await self.message.edit(view=None)

    @staticmethod
    def total_pages(total_results: int, results_per_page: int) -> int:
        return ((total_results - 1) // results_per_page) + 1