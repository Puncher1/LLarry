import discord
from discord.ext import commands
from discord import ui, ButtonStyle
import typing

from cogs.global_ import Global as g
# end imports


class SelectMenuHandler(ui.Select):
    """Adds a SelectMenu to a specific message and returns it's value on selecting an option."""

    def __init__(self,
                 options: list,
                 place_holder: str,
                 disabled: bool,
                 select_user: typing.Union[discord.Member, discord.User, None]
                 ):
        self.options_ = options
        self.select_user = select_user
        self.disabled_ = disabled
        self.placeholder_ = place_holder
        super().__init__(placeholder=self.placeholder_, options=self.options_, disabled=self.disabled_)

    async def callback(self, interaction: discord.Interaction):
        if self.select_user is None or interaction.user == self.select_user:
            self.view.value = interaction.data["values"][0]
            self.view.stop()


class ButtonHandler(ui.Button):
    """Adds a Button to a specific message and returns it's value on pressing it."""

    def __init__(self,
                 label: typing.Union[str, None],
                 custom_id: typing.Union[str, None],
                 style: ButtonStyle,
                 emoji: typing.Union[str, None],
                 url: typing.Union[str, None],
                 disabled: bool,
                 button_user: typing.Union[discord.Member, discord.User, None]
                 ):
        self.label_ = label
        self.custom_id_ = custom_id
        self.style_ = style
        self.emoji_ = emoji
        self.url_ = url
        self.disabled_ = disabled
        self.button_user = button_user
        super().__init__(label=self.label_, custom_id=self.custom_id_, style=self.style_, emoji=self.emoji_,
                         url=self.url_, disabled=self.disabled_)

    async def callback(self, interaction: discord.Interaction):
        if self.button_user is None or self.button_user == interaction.user:
            if self.custom_id_ is None:
                self.view.value = None
            else:
                self.view.value = interaction.data["custom_id"]

            self.view.stop()


