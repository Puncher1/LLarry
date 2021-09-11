import discord
from discord.ext import commands
from discord import ui, ButtonStyle, SelectOption
import typing


class SelectMenuHandler(ui.Select):
    """Adds a SelectMenu to a specific message and returns it's value when option selected."""

    def __init__(self,
                 options: typing.List[SelectOption],
                 custom_id: typing.Union[str, None] = None,
                 place_holder: typing.Union[str, None] = None,
                 max_values: int = 1,
                 min_values: int = 1,
                 disabled: bool = False,
                 select_user: typing.Union[discord.Member, discord.User, None] = None,
                 interaction_message: typing.Union[str, None] = None,
                 ephemeral: bool = True
                 ):
        """
        Parameters:
            options (typing.List[SelectOption]): List of discord.SelectOption
            custom_id (typing.Union[str, None], optional): Custom ID of the view. Default to None.
            place_holder (typing.Union[str, None], optional): Place Holder string for the view. Default to None.
            max_values (int, optional): Maximum values that are selectable. Default to 1.
            min_values (int, optional): Minimum values that are selectable. Default to 1.
            disabled (bool): Whenever the button is disabled or not. Default to False.
            select_user (typing.Union[discord.Member, discord.User, None], optional): The user that can perform this action, leave blank for everyone. Defaults to None.
            interaction_message (typing.Union[str, None], optional): The response message when pressing on a selection. Default to None.
            ephemeral (bool): Whenever the response message should only be visible for the 'select_user' or not. Default to True.
        """

        self.options_ = options
        self.custom_id_ = custom_id
        self.select_user = select_user
        self.disabled_ = disabled
        self.placeholder_ = place_holder
        self.max_values_ = max_values
        self.min_values_ = min_values
        self.interaction_message_ = interaction_message
        self.ephemeral_ = ephemeral

        if self.custom_id_:
            super().__init__(options=self.options_, placeholder=self.placeholder_, custom_id=self.custom_id_,
                             disabled=self.disabled_, max_values=self.max_values_, min_values=self.min_values_)
        else:
            super().__init__(options=self.options_, placeholder=self.placeholder_,
                             disabled=self.disabled_, max_values=self.max_values_, min_values=self.min_values_)

    async def callback(self, interaction: discord.Interaction):
        if self.select_user is None or interaction.user == self.select_user:
            if self.interaction_message_:
                await interaction.response.send_message(content=self.interaction_message_, ephemeral=self.ephemeral_)

            self.view.value = self.values[0]
            self.view.stop()


class ButtonHandler(ui.Button):
    """Adds a Button to a specific message and returns it's value when pressed."""

    def __init__(self,
                 style: ButtonStyle,
                 label: str,
                 custom_id: typing.Union[str, None] = None,
                 emoji: typing.Union[str, None] = None,
                 url: typing.Union[str, None] = None,
                 disabled: bool = False,
                 button_user: typing.Union[discord.Member, discord.User, None] = None,
                 interaction_message: typing.Union[str, None] = None,
                 ephemeral: bool = True
                 ):
        """
        Parameters:
            style (ButtonStyle): Label for the button
            label (typing.Union[str, None], optional): Custom ID that represents this button. Default to None.
            custom_id (typing.Union[str, None], optional): Style for this button. Default to None.
            emoji (typing.Union[str, None], optional): An emoji for this button. Default to None.
            url (typing.Union[str, None], optional): A URL for this button. Default to None.
            disabled (bool, optional): Whenever the button should be disabled or not. Default to False.
            button_user (typing.Union[discord.Member, discord.User, None], optional): The user that can perform this action, leave blank for everyone. Defaults to None.
        """
        self.style_ = style
        self.label_ = label
        self.custom_id_ = custom_id
        self.emoji_ = emoji
        self.url_ = url
        self.disabled_ = disabled
        self.button_user = button_user
        self.interaction_message_ = interaction_message
        self.ephemeral_ = ephemeral

        if self.custom_id_:
            super().__init__(style=self.style_, label=self.label_, custom_id=self.custom_id_, emoji=self.emoji_,
                             url=self.url_, disabled=self.disabled_)
        else:
            super().__init__(style=self.style_, label=self.label_, emoji=self.emoji_,
                             url=self.url_, disabled=self.disabled_)

    async def callback(self, interaction: discord.Interaction):
        if self.button_user is None or self.button_user == interaction.user:
            if self.custom_id_ is None:
                self.view.value = None
            else:
                self.view.value = self.custom_id

            if self.interaction_message_:
                interaction.response.send_message(content=self.interaction_message_, ephermal=self.ephemeral_)

            self.view.stop()