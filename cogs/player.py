import discord
from discord.ext import commands

from main import LLarry
from utils import general
# end


class Player(commands.Cog):
    """CoC-Player related commands."""
    def __init__(self, client: LLarry):
        self.client = client

    # Command: player
    @commands.command()
    async def player(self, ctx, tag):
        """Returns information about a player in Clash of Clans."""

        p = await self.client.coc_client.get_player(tag)
        if p.town_hall_weapon in [1, None]:
            th_weapon = ""
        else:
            th_weapon = f"-{p.town_hall_weapon}"

        league_link = p.league.icon.url
        townhall_link = f"https://coc.guide/static/imgs/other/town-hall-{p.town_hall}{th_weapon}.png"

        embed_player = await general.embed_gen(
            ctx.channel,
            None,
            f"LOL",
            None,
            townhall_link,
            None,
            discord.Colour.blurple(),
            True
        )
        embed_player.set_author(name=f"{p.name} ({p.tag})", icon_url=league_link)
        await ctx.send(embed=embed_player)

def setup(client):
    client.add_cog(Player(client))