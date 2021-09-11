import discord
from discord.ext import commands
from discord import ui, ButtonStyle, SelectOption
import typing


class SelectMenuHandler(ui.Select):
    """Adds a SelectMenu to a specific message and returns it's value when option selected.
        Args:
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
        self.options_ = options
        self.custom_id_ = custom_id
        self.select_user = select_user
        self.disabled_ = disabled
        self.placeholder_ = place_holder
        self.max_values_ = max_values
        self.min_values_ = min_values
        self.interaction_message_ = interaction_message
        self.ephemeral_ = ephemeral
        super().__init__(placeholder=self.placeholder_, options=self.options_, disabled=self.disabled_,
                         max_values=self.max_values_, min_values=self.min_values_)
        if self.custom_id_:
            super().__init__(custom_id=self.custom_id_)

    async def callback(self, interaction: discord.Interaction):
        if self.select_user is None or interaction.user == self.select_user:
            if self.interaction_message_:
                await interaction.response.send_message(content=self.interaction_message_, ephemeral=self.ephemeral_)

            self.view.value = self.values[0]
            self.view.stop()


class ButtonHandler(ui.Button):
    """Adds a Button to a specific message and returns it's value when pressed.
        Args:
            style (ButtonStyle): Label for the button
            label (typing.Union[str, None], optional): Custom ID that represents this button. Defaults to None.
            custom_id (typing.Union[str, None], optional): Style for this button. Defaults to None.
            emoji (typing.Union[str, None], optional): An emoji for this button. Defaults to None.
            url (typing.Union[str, None], optional): A URL for this button. Defaults to None.
            disabled (bool, optional): If this button should be disabled. Defaults to False.
            button_user (typing.Union[discord.Member, discord.User, None], optional): The user that can perform this action, leave blank for everyone. Defaults to None.
        """

    def __init__(self,
                 style: ButtonStyle,
                 label: typing.Union[str, None] = None,
                 custom_id: typing.Union[str, None] = None,
                 emoji: typing.Union[str, None] = None,
                 url: typing.Union[str, None] = None,
                 disabled: bool = False,
                 button_user: typing.Union[discord.Member, discord.User, None] = None,
                 interaction_message: typing.Union[str, None] = None,
                 ephemeral: bool = True
                 ):
        self.label_ = label
        self.custom_id_ = custom_id
        self.style_ = style
        self.emoji_ = emoji
        self.url_ = url
        self.disabled_ = disabled
        self.button_user = button_user
        self.interaction_message_ = interaction_message
        self.ephemeral_ = ephemeral
        super().__init__(label=self.label_, custom_id=self.custom_id_, style=self.style_, emoji=self.emoji_,
                         url=self.url_, disabled=self.disabled_)
        if self.custom_id_:
            super().__init__(custom_id=self.custom_id_)

    async def callback(self, interaction: discord.Interaction):
        if self.button_user is None or self.button_user == interaction.user:
            if self.custom_id_ is None:
                self.view.value = None
            else:
                self.view.value = self.custom_id

            if self.interaction_message_:
                interaction.response.send_message(content=self.interaction_message_, ephermal=self.ephemeral_)

            self.view.stop()