import discord
from discord.ext import commands
from discord import ui

from cogs.global_ import Global as g
# end imports


class HelpSelectMenu(ui.Select):
    """A class that represents a function that adds a select menu to the help message"""

    def __init__(self, client: commands.Bot, options: list, user: discord.Member, place_holder: str, disabled: bool):
        self.client = client
        self.options_ = options
        self.user = user
        self.disabled_bool = disabled
        self.placeholder_str = place_holder
        super().__init__(placeholder=self.placeholder_str, options=self.options_, disabled=self.disabled_bool)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user == self.user:
            self.view.value = interaction.data["values"][0]
            self.view.stop()



