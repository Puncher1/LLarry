import discord
from discord.ext import commands

from cogs.global_ import Global as g
# end imports

class HelpSelectMenu(discord.ui.Select):
    """A class that represents a function that adds a select menu to the help message"""

    def __init__(self, client: commands.Bot, options: list, user: discord.Member):
        self.client = client
        self.options_ = options
        self.user = user
        super().__init__(placeholder="Choose a category", options=self.options_)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user == self.user:
            self.view.value = interaction.data["values"][0]
            self.view.stop()


