import discord


MOD_CHANNEL_ID = 1281236880209219686


class Embeds:
    @classmethod
    def green(cls, description: str = "") -> discord.Embed:
        return discord.Embed(colour=3853362, description=description)

    @classmethod
    def yellow(cls, description: str = "") -> discord.Embed:
        return discord.Embed(colour=16627968, description=description)

    @classmethod
    def red(cls, description: str = "") -> discord.Embed:
        return discord.Embed(colour=16711680, description=description)

    @classmethod
    def blue(cls, description: str = "") -> discord.Embed:
        return discord.Embed(colour=2513645, description=description)

    @classmethod
    def invisible(cls, description: str = "") -> discord.Embed:
        return discord.Embed(colour=3092790, description=description)