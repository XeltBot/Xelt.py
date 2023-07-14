import inspect
from typing import Any, List, Optional, Union

import discord
from discord.ext import commands, menus
from libs.utils.pages import XeltPages

from .ui import HelpMenu


class GroupHelpPageSource(menus.ListPageSource):
    def __init__(
        self,
        group: Union[commands.Group, commands.Cog],
        entries: List[commands.Command],
        *,
        prefix: str,
    ):
        super().__init__(entries=entries, per_page=6)
        self.group: Union[commands.Group, commands.Cog] = group
        self.prefix: str = prefix
        self.title: str = f"{self.group.qualified_name} Commands"
        self.description: str = self.group.description

    async def format_page(self, menu: XeltPages, commands: List[commands.Command]):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            colour=discord.Colour.from_rgb(197, 184, 255),
        )

        for command in commands:
            signature = f"{command.qualified_name} {command.signature}"
            embed.add_field(
                name=signature,
                value=command.short_doc or "No help given...",
                inline=False,
            )

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(
                name=f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} commands)"
            )

        embed.set_footer(
            text=f'Use "{self.prefix}help command" for more info on a command.'
        )
        return embed


class FrontPageSource(menus.PageSource):
    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    def format_page(self, menu: HelpMenu, page: Any):
        embed = discord.Embed(
            title="Bot Help", colour=discord.Colour.from_rgb(255, 161, 231)
        )
        # embed.description = "help"
        embed.description = inspect.cleandoc(
            f"""
            Hello! Welcome to the help page.

            Use "{menu.ctx.clean_prefix}help command" for more info on a command.
            Use "{menu.ctx.clean_prefix}help category" for more info on a category.
            Use the dropdown menu below to select a category.
        """
        )

        embed.add_field(
            name="Support Server",
            value="For more help, consider joining the official server over at https://discord.gg/sYP7z2sUda",
            inline=False,
        )

        # created_at = time.format_dt(menu.ctx.bot.user.created_at, 'F')
        if self.index == 0:
            embed.add_field(
                name="About Kumiko",
                value=(
                    "Xelt is an multipurpose bot with a wide variety of commands and features. You may be wondering, "
                    "what an multipurpose bot is. Xelt offers features such as the famous typeracer game, custom prefix, and many more. You can get more "
                    "information on the commands offered by using the dropdown below.\n\n"
                    "Xelt is also open source. You can see the code on [GitHub](https://github.com/XeltBot/Xelt.py)"
                ),
                inline=False,
            )
        elif self.index == 1:
            entries = (
                ("<argument>", "This means the argument is __**required**__."),
                ("[argument]", "This means the argument is __**optional**__."),
                ("[A|B]", "This means that it can be __**either A or B**__."),
                (
                    "[argument...]",
                    "This means you can have multiple arguments.\n"
                    "Now that you know the basics, it should be noted that...\n"
                    "__**You do not type in the brackets!**__",
                ),
            )

            embed.add_field(
                name="How do I use this bot?",
                value="Reading the bot signature is pretty simple.",
            )

            for name, value in entries:
                embed.add_field(name=name, value=value, inline=False)

        return embed
