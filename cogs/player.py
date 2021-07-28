import discord
from discord.ext import commands
import coc
import typing

from main import LLarry
from utils import embeds, formatting
from cogs.global_ import Global as g
# end


class Player(commands.Cog):
    """CoC-Player related commands."""
    def __init__(self, client: LLarry):
        self.client = client

    # Command: player
    @commands.command()
    async def player(self, ctx, tag):
        """Returns information about a player in Clash of Clans."""

        p = await self.client.coc_client.get_player(player_tag=tag)

        # Player information
        gold_value = p.get_achievement("Gold Grab").value
        gold_formatted = formatting.num_formatting(gold_value)

        elixir_value = p.get_achievement("Elixir Escapade").value
        elixir_formatted = formatting.num_formatting(elixir_value)

        dark_elixir_value = p.get_achievement("Heroic Heist").value
        dark_elixir_formatted = formatting.num_formatting(dark_elixir_value)

        troops_donated = p.get_achievement("Friend in Need").value
        troops_donated_formatted = formatting.num_formatting(troops_donated)

        spells_donated = p.get_achievement("Sharing is caring").value
        spells_donated_formatted = formatting.num_formatting(spells_donated)

        clan_games = p.get_achievement("Games Champion").value
        total_attacks_won = p.get_achievement("Conqueror").value
        total_defenses_won = p.get_achievement("Unbreakable").value

        heroes_emojis = {
            "Barbarian King": g.e_barbarian_king,
            "Archer Queen": g.e_archer_queen,
            "Grand Warden": g.e_grand_warden,
            "Royal Champion": g.e_royal_champion,
            "Battle Machine": g.e_battle_machine
        }

        labels_emojis = {
            "Clan Wars": g.e_label_clanwars,
            "Clan War League": g.e_label_clanwarleague,
            "Trophy Pushing": g.e_label_trophypushing,
            "Friendly Wars": g.e_label_friendlywars,
            "Clan Games": g.e_label_clangames2,
            "Builder Base": g.e_label_builderbase,
            "Base Designing": g.e_label_basedesigning,
            "Farming": g.e_label_farming,
            "Active Donator": g.e_label_activedonator,
            "Active Daily": g.e_label_activedaily,
            "Hungry Learner": g.e_label_hungrylearner,
            "Friendly": g.e_label_friendly,
            "Talkative": g.e_label_talkative,
            "Teacher": g.e_label_teacher,
            "Competitive": g.e_label_competitive,
            "Veteran": g.e_label_veteran,
            "Newbie": g.e_label_newbie,
            "Amateur Attacker": g.e_label_amateurattacker
        }

        if p.town_hall_weapon in [1, None]:
            town_hall_weapon = ""
        else:
            town_hall_weapon = f"-{p.town_hall_weapon}"

        if p.league.icon.medium:
            league_icon_url = p.league.icon.medium
        else:
            league_icon_url = "https://lh3.googleusercontent.com/proxy/X-8nlk3Gx_-Sf7kGRunhBpy79VQDMkQ5evRZEK_4jJDin9NI08W7MP4jIynhex-8RtG__1fgAV2ZbOqd9CNVZgIafWkBwngQV3BNCwo36csmY20"
        town_hall_link = f"https://coc.guide/static/imgs/other/town-hall-{p.town_hall}{town_hall_weapon}.png"
        trophies = f"{g.e_trophy} `{p.trophies}`"
        level = f"{g.e_level} `{p.exp_level}`"
        league = f"{g.e_league} `{p.league}`"
        best_trophies = f"{g.e_trophy} `{p.best_trophies}`"
        war_stars = f"{g.e_warstar} `{p.war_stars}`"
        attacks_won = f"{g.e_attack} `{p.attack_wins}`"
        defenses_won = f"{g.e_shield} `{p.defense_wins}`"
        donated = f"{g.e_donate} `{p.donations}`"
        received = f"{g.e_receive} `{p.received}`"
        if p.donations == p.received:
            donation_ratio = f"{g.e_ratio} `1:1`"
        else:
            try:
                donation_ratio = f"{g.e_ratio} `1:{round(p.received / p.donations, 1)}`"
            except ZeroDivisionError:
                donation_ratio = f"{g.e_ratio} `1:{p.received}`"


        gold = f"{g.e_gold} `{gold_formatted}`"
        elixir = f"{g.e_elixir} `{elixir_formatted}`"
        dark_elixir = f"{g.e_dark_elixir} `{dark_elixir_formatted}`"

        troops_donated = f"{g.e_troops_donation} `{troops_donated_formatted}`"
        spells_donated = f"{g.e_spells_donation} `{spells_donated_formatted}`"
        total_attacks_won = f"{g.e_attack} `{total_attacks_won}`"
        total_defenses_won = f"{g.e_shield} `{total_defenses_won}`"
        clan_games_points = f"{g.e_clan_games} `{clan_games}`"

        hereos = ""
        for hereo in p.heroes:
            hereo_emoji = heroes_emojis[hereo.name]
            substring = f"{hereo_emoji} `{hereo.level}` "
            hereos += substring

        if hereos == "":
            hereos = "No heroes available."


        labels = []
        for label in p.labels:
            substring = f"{labels_emojis[label.name]} `{label.name}`"
            labels.append(substring)
        if labels:
            labels = "\n".join(labels)
        else:
            labels = "No labels selected."

        # Clan information
        if p.clan is None:
            clan_information = "Not in clan."
        else:
            clan = await p.get_detailed_clan()
            clan_information = f"> **Name:** `{clan.name}`" \
                               f"\n> **Tag:** `{clan.tag}`" \
                               f"\n> **Position:** `{p.role}`" \
                               f"\n> **Members:** `{clan.member_count}`"

        embed_player = await embeds.embed_gen(
            ctx.channel,
            None,
            None,
            None,
            town_hall_link,
            None,
            g.zap_color,
            True
        )
        embed_player.set_author(name=f"{p.name} ({p.tag})", icon_url=league_icon_url)

        embed_player.add_field(name=f"{g.e_clan} Clan Info", value=f"{clan_information}", inline=False)
        embed_player.add_field(name=f"Trophies", value=trophies)
        embed_player.add_field(name="Level", value=level)
        embed_player.add_field(name="League", value=league)
        embed_player.add_field(name="Best Trophies", value=best_trophies)
        embed_player.add_field(name="Attacks won", value=attacks_won)
        embed_player.add_field(name="Defenses won", value=defenses_won)
        embed_player.add_field(name="Donated", value=donated)
        embed_player.add_field(name="Received", value=received)
        embed_player.add_field(name="Donation Ratio", value=donation_ratio)
        embed_player.add_field(name="Gold Grab", value=gold)
        embed_player.add_field(name="Elixir Grab", value=elixir)
        embed_player.add_field(name="Dark Elixir Grab", value=dark_elixir)
        embed_player.add_field(name="Total Troops donated", value=troops_donated)
        embed_player.add_field(name=f"_ _", value=f"_ _")
        embed_player.add_field(name="Total Spells donated", value=spells_donated)
        embed_player.add_field(name="Total Attacks won", value=total_attacks_won)
        embed_player.add_field(name=f"_ _", value=f"_ _")
        embed_player.add_field(name="Total Defenses won", value=total_defenses_won)
        embed_player.add_field(name="War Stars", value=war_stars)
        embed_player.add_field(name=f"_ _", value=f"_ _")
        embed_player.add_field(name="Clan Games Points", value=clan_games_points)
        embed_player.add_field(name="Heroes", value=hereos)
        embed_player.add_field(name=f"_ _", value=f"_ _")
        embed_player.add_field(name="Labels", value=labels)


        await ctx.send(embed=embed_player)

def setup(client):
    client.add_cog(Player(client))