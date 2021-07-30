import discord
from discord.ext import commands

from utils import embeds, components
from utils.components import SelectMenuHandler
from cogs.global_ import Global as g
# end imports


class Help(commands.HelpCommand):
    """A class that represents ``commands.HelpCommand``."""

    def get_command_signature(self, command):
        # creating own signature (<prefix><command> <arguments>)
        return f"`{self.context.clean_prefix}{command.qualified_name} {command.signature}` *{command.description}*"

    def get_cog_signature(self, cog):

        if not cog:
            pass
        else:
            return f"{cog.description}"

    async def send_bot_help(self, mapping):
        """Sending bot help message."""

        channel = self.get_destination()
        client = self.context.bot
        owner = client.get_user(g.owner)
        help_embed = await embeds.embed_gen(
            channel,
            "Help",
            f"**Zap!** is a Clash of Clans bot which is aimed to display information about players, clans, and more."
            f"\n```diff"
            f"\n<> required"
            f"\n[] optional"
            f"\n\n-help [command] for additional help on a command."
            f"\n```",
            f"Requested by {self.context.author}",
            client.user.avatar.url,
            None,
            g.zap_color,
            True
        )
        help_embed.set_author(name=f"By {owner}", icon_url=owner.avatar.url)

        cogs_list = []
        # iterate through every cog
        for cog_iter, cmds in mapping.items():
            cogs_list.append(cog_iter)

        for cog in cogs_list:
            if not cog or cog.qualified_name in g.ignored_help_cogs:
                continue

            filtered_cmds = await self.filter_commands(cog.get_commands(), sort=True)

            if not any(command in filtered_cmds for command in cog.get_commands()):
                continue

            # get cog's name, default: 'No Category'
            cog_signature = self.get_cog_signature(cog)
            cog_name = getattr(cog, "name", "No Category")
            help_embed.add_field(
                name=cog_name,
                value=cog_signature,
                inline=False
            )

        select_list = []
        cogs = client.cogs
        for cog_name in list(cogs):
            cog = cogs[cog_name]
            filtered_cmds = await self.filter_commands(cog.get_commands(), sort=True)

            if cog_name in g.ignored_help_cogs or not any(command in filtered_cmds for command in cog.get_commands()):
                continue
            select_element = discord.SelectOption(label=cog_name, description=cog.description)
            select_list.append(select_element)

        timeout = False
        help_msg = None

        current_embed = help_embed
        while not timeout:
            view = discord.ui.View()
            view.add_item(SelectMenuHandler(select_list, "Choose a category", False, self.context.author))

            if not help_msg:
                help_msg = await channel.send(embed=current_embed, view=view)
            else:
                await help_msg.edit(embed=current_embed, view=view)

            timeout = await view.wait()
            if not timeout:
                selection_str = view.value
                cog_for_help = client.get_cog(selection_str)
                if not cog_for_help:
                    raise discord.NotFound(f"Cog with name 'selection_str' doesn't exist.", f"Cog with name 'selection_str' doesn't exist.")
                else:

                    cog_embed = await embeds.embed_gen(
                        channel,
                        "Help",
                        f"**Zap!** is a Clash of Clans bot which is aimed to display information about players, clans, and more."
                        f"\n```diff"
                        f"\n<> required"
                        f"\n[] optional"
                        f"\n\n-help [command] for additional info about a command."
                        f"\n```",
                        f"Requested by {self.context.author}",
                        client.user.avatar.url,
                        None,
                        g.zap_color,
                        True
                    )
                    cog_embed.set_author(name=f"By {owner}", icon_url=owner.avatar.url)

                    # get signature (our own signature)
                    command_signatures = [self.get_command_signature(c) for c in cog_for_help.get_commands()]

                    new_desc = f"\n".join(command_signatures)
                    cog_embed.add_field(name=f"{cog_for_help.name}", value=f"{new_desc}")

                    current_embed = cog_embed

            else:
                view = discord.ui.View()
                view.add_item(SelectMenuHandler(select_list, "Disabled due to timeout", True, self.context.author))
                await help_msg.edit(embed=current_embed, view=view)

class General(commands.Cog):
    """General commands."""
    def __init__(self, client):
        self.client = client
        self.name = f"{g.e_attack} {self.qualified_name}"

        # Cog assignment for help command
        attributes = {
            'description': 'Shows this message or additional information on a command.',
            'cooldown': commands.CooldownMapping.from_cooldown(1, 5.0, commands.BucketType.user)
        }

        help_command = Help(command_attrs=attributes)
        help_command.cog = self
        client.help_command = help_command



def setup(client):
    client.add_cog(General(client))
