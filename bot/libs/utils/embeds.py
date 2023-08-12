import discord


class Embed(discord.Embed):
    """Xelt's custom default embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 163, 253))
        super().__init__(**kwargs)


class SuccessActionEmbed(discord.Embed):
    """Xelt's custom success action embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(75, 181, 67))
        kwargs.setdefault("title", "Action successful")
        kwargs.setdefault("description", "The action requested was successful")
        super().__init__(**kwargs)


class ErrorEmbed(discord.Embed):
    """Xelt's custom error embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(214, 6, 6))
        kwargs.setdefault("title", "Oh no, an error has occurred!")
        kwargs.setdefault(
            "description",
            "Uh oh! It seems like the command ran into an issue! For support, please visit the Support Server to get help!",
        )
        super().__init__(**kwargs)


class ConfirmEmbed(discord.Embed):
    """Custom confirm embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 191, 0))
        kwargs.setdefault("title", "Are you sure?")
        super().__init__(**kwargs)
