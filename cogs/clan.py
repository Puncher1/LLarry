import time

import discord
from discord.ext import commands
import coc.utils
import pycountry

from main import Zap
from cogs.global_ import Global as g
from utils.components import ButtonHandler
from utils import embeds
# end imports


class Clan(commands.Cog):
    """Clan commands"""
    def __init__(self, client: Zap):
        self.client = client
        self.name = f"{g.e_clan} {self.qualified_name}"


    async def sending_clan(self, ctx: commands.Context, tag):
        """Sending clan information."""

        await ctx.trigger_typing()

        c = await self.client.coc_client.get_clan(tag)
        leader = coc.utils.get(c.members, role=coc.Role.leader)

        shields_png = discord.File("./images/shields.png", filename="shields.png")

        clan_level = f"{g.e_clan_level} `{c.level}`"
        clan_members = f"{g.e_members} `{c.member_count}/50`"
        clan_warleague = f"{g.e_clan_trophy} `{c.war_league}`"
        clan_points = f"{g.e_trophy} `{c.points}`"

        if f"{c.location}" == "International":
            clan_location = f"🌍 `International`"
        else:
            location_alpha = pycountry.countries.get(name=f"{c.location}").alpha_2.lower()
            clan_emoji = f":flag_{location_alpha}:"

            clan_location = f"{clan_emoji} `{c.location}`"

        if f"{c.type}" == "inviteOnly":
            clan_type = f"{g.e_type} `Invite only`"
        elif f"{c.type}" == "closed":
            clan_type = f"{g.e_type} `Closed`"
        elif f"{c.type}" == "open":
            clan_type = f"{g.e_type} `Open`"

        clan_required_trophies = f"{g.e_trophy} `{c.required_trophies}`"
        clan_war_frequency = f"{g.e_clan} `{c.war_frequency.title()}`"
        clan_war_wins = f"{g.e_donate} `{c.war_wins}`"
        clan_war_loses = f"{g.e_receive} `{c.war_losses}`"

        if c.public_war_log:
            clan_war_log = f"{g.e_checkmark} `Public`"
        else:
            clan_war_log = f"{g.e_xmark} `Private`"


        embed_clan = await embeds.embed_gen(
            ctx.channel,
            None,
            f"{c.description}",
            f"Leader: {leader.name} ({leader.tag})",
            c.badge.large,
            None,
            g.zap_color,
            True
        )

        embed_clan.set_author(name=f"{c.name} ({c.tag})", icon_url="attachment://shields.png")

        embed_clan.add_field(name="Level", value=clan_level)
        embed_clan.add_field(name="Members", value=clan_members)
        embed_clan.add_field(name="War League", value=clan_warleague)
        embed_clan.add_field(name="Points", value=clan_points)
        embed_clan.add_field(name="Location", value=clan_location)
        embed_clan.add_field(name="Type", value=clan_type)
        embed_clan.add_field(name="Required Trophies", value=clan_required_trophies)
        embed_clan.add_field(name="War Frequency", value=clan_war_frequency)
        embed_clan.add_field(name="War Wins", value=clan_war_wins)
        embed_clan.add_field(name="War Loses", value=clan_war_loses)
        embed_clan.add_field(name="War Log", value=clan_war_log)
        embed_clan.add_field(name="Labels", value="!!!!Labels hier!!!!")


        embed_clan.set_footer(text=embed_clan.footer.text, icon_url=leader.league.icon.medium)

        view = discord.ui.View()
        view.add_item(ButtonHandler("Members", "Members", discord.ButtonStyle.green, None,
                                    None, False, ctx.author))
        view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=c.share_link, disabled=False,
                                    label="Open in-game", emoji=None, button_user=None, custom_id=None))

        timeout = False
        clan_msg = None

        current_embed = embed_clan
        current_view = view
        while not timeout:

            if not clan_msg:
                clan_msg = await ctx.send(embed=current_embed, view=current_view, file=shields_png)
            else:
                await clan_msg.edit(embed=current_embed, view=current_view)

            timeout = await current_view.wait()
            if not timeout:
                if current_view.value == "Members":
                    start = time.perf_counter()
                    print(c.members)

                    embed_members = await embeds.embed_gen(
                        ctx.channel,
                        None,
                        "Members",
                        None,
                        c.badge.large,
                        None,
                        g.zap_color,
                        True
                    )
                    embed_members.set_author(name=f"{c.name} ({c.tag})", icon_url=f"attachment://shields.png")

                    view = discord.ui.View()
                    view.add_item(ButtonHandler(style=discord.ButtonStyle.green, url=None, disabled=False,
                                                label="Statistics", emoji=None, button_user=ctx.author, custom_id="Statistics"))

                    view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=c.share_link, disabled=False,
                                                label="Open in-game", emoji=None, button_user=None, custom_id=None))
                    current_embed = embed_members
                    current_view = view
                    end = time.perf_counter()
                    duration = end - start
                    print(duration)

                elif current_view.value == "Statistics":
                    view = discord.ui.View()
                    view.add_item(ButtonHandler("Members", "Members", discord.ButtonStyle.green, None,
                                                None, False, ctx.author))
                    view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=c.share_link, disabled=False,
                                                label="Open in-game", emoji=None, button_user=None, custom_id=None))

                    current_view = view
                    current_embed = embed_clan



    # Command: clan
    @commands.command(description="Clan information")
    async def clan(self, ctx, tag):
        """Returns information about a clan of Clash of Clans using the clan's tag."""

        await self.sending_clan(ctx, tag)

def setup(client):
    client.add_cog(Clan(client))