import discord
from discord import emoji
import mysql.connector
from discord.ext import commands

from main import Zap
from utils import embeds, formatting, db_connector
from utils.components import ButtonHandler
from cogs.global_ import Global as g
# end


class Player(commands.Cog):
    """Player commands"""

    def __init__(self, client: Zap):
        self.client = client
        self.name = f"{g.e_shield} {self.qualified_name}"

    async def sending_player(self, ctx, tag):
        """Sending player information."""

        p = await self.client.coc_client.get_player(player_tag=tag)

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
        embed_player.set_author(name=f"{p.name} ({p.tag})", icon_url=league_icon_url, url=p.share_link)

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

        view = discord.ui.View()
        view.add_item(ButtonHandler(style=discord.ButtonStyle.green, url=None, disabled=False,
                                    label="Troops", emoji=None, button_user=ctx.author, custom_id="Troops"))

        view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=p.share_link, disabled=False,
                                    label="Open in-game", emoji=None, button_user=None, custom_id=None))

        timeout = False
        player_msg = None

        current_embed = embed_player
        current_view = view
        while not timeout:

            if not player_msg:
                player_msg = await ctx.send(embed=current_embed, view=current_view)
            else:
                await player_msg.edit(embed=current_embed, view=current_view)
            timeout = await current_view.wait()
            if not timeout:
                if current_view.value == "Troops":

                    home_troops_emojis = {
                        "Barbarian": g.e_barbarian,
                        "Archer": g.e_archer,
                        "Giant": g.e_giant,
                        "Goblin": g.e_goblin,
                        "Wall Breaker": g.e_wallbreaker,
                        "Balloon": g.e_balloon,
                        "Wizard": g.e_wizzard,
                        "Healer": g.e_healer,
                        "Dragon": g.e_dragon,
                        "P.E.K.K.A": g.e_pekka,
                        "Baby Dragon": g.e_babydragon,
                        "Miner": g.e_miner,
                        "Electro Dragon": g.e_electrodragon,
                        "Yeti": g.e_yeti,
                        "Dragon Rider": g.e_dragonrider,
                        "Minion": g.e_minion,
                        "Hog Rider": g.e_hogrider,
                        "Valkyrie": g.e_valkyre,
                        "Golem": g.e_golem,
                        "Witch": g.e_witch,
                        "Lava Hound": g.e_lavahound,
                        "Bowler": g.e_bowler,
                        "Ice Golem": g.e_icegolem,
                        "Headhunter": g.e_headhunter
                    }

                    builder_troops_emojis = {
                        "Raged Barbarian": g.e_ragebarbarian,
                        "Sneaky Archer": g.e_sneakyarcher,
                        "Boxer Giant": g.e_boxergiant,
                        "Beta Minion": g.e_betaminion,
                        "Bomber": g.e_bomber,
                        "Baby Dragon": g.e_babydragon,
                        "Cannon Cart": g.e_cannoncart,
                        "Night Witch": g.e_nightwitch,
                        "Drop Ship": g.e_dropship,
                        "Super P.E.K.K.A": g.e_superpekka,
                        "Hog Glider": g.e_hogglider
                    }

                    spells_emojis = {
                        "Lightning Spell": g.e_lightning_spell,
                        "Healing Spell": g.e_healing_spell,
                        "Rage Spell": g.e_rage_spell,
                        "Jump Spell": g.e_jump_spell,
                        "Freeze Spell": g.e_freeze_spell,
                        "Clone Spell": g.e_clone_spell,
                        "Invisibility Spell": g.e_invisibility_spell,
                        "Poison Spell": g.e_poison_spell,
                        "Earthquake Spell": g.e_earthquake_spell,
                        "Haste Spell": g.e_haste_spell,
                        "Skeleton Spell": g.e_skeleton_spell,
                        "Bat Spell": g.e_bat_spell
                    }

                    not_unlocked = []

                    in_player_troops = [troop.name for troop in p.troops]
                    in_player_spells = [spell.name for spell in p.spells]
                    in_player_heroes = [hero.name for hero in p.heroes]

                    # Home Village
                    home_troops = []
                    ht_index = 1
                    for home_troop_name in list(home_troops_emojis):
                        home_troop = p.get_troop(home_troop_name, is_home_troop=True)

                        if home_troop_name not in in_player_troops:
                            string = f"{home_troops_emojis[home_troop_name]} ` N/A `"

                            not_unlocked.append(string)
                            continue

                        else:
                            if home_troop.level >= 10:
                                current_lvl = f"{home_troop.level}"
                            else:
                                current_lvl = f" {home_troop.level}"

                            if home_troop.max_level >= 10:
                                max_lvl = f"{home_troop.max_level}"
                            else:
                                max_lvl = f"{home_troop.max_level} "

                            string = f"{home_troops_emojis[home_troop_name]} `{current_lvl}/{max_lvl}`"

                        if ht_index % 4 == 0:
                            string += "\n"
                        else:
                            string += f"{g.space_character}"

                        home_troops.append(string)
                        ht_index += 1

                    # Builder Base
                    builder_troops = []
                    bb_index = 1
                    for builder_troop_name in list(builder_troops_emojis):
                        builder_troop = p.get_troop(builder_troop_name, is_home_troop=False)

                        if builder_troop_name not in in_player_troops:
                            string = f"{builder_troops_emojis[builder_troop_name]}  ` N/A `"

                            not_unlocked.append(string)
                            continue

                        else:
                            if builder_troop.level >= 10:
                                current_lvl = f"{builder_troop.level}"
                            else:
                                current_lvl = f" {builder_troop.level}"

                            if builder_troop.max_level >= 10:
                                max_lvl = f"{builder_troop.max_level}"
                            else:
                                max_lvl = f"{builder_troop.max_level} "

                            string = f"{builder_troops_emojis[builder_troop_name]} `{current_lvl}/{max_lvl}`"

                        if bb_index % 4 == 0:
                            string += "\n"
                        else:
                            string += f"{g.space_character}"

                        builder_troops.append(string)
                        bb_index += 1

                    # Spells
                    spells = []
                    spell_index = 1
                    for spell_name in list(spells_emojis):
                        spell_obj = p.get_spell(spell_name)

                        if spell_name not in in_player_spells:
                            string = f"{spells_emojis[spell_name]} ` N/A `"

                            not_unlocked.append(string)
                            continue

                        else:
                            if spell_obj.level >= 10:
                                current_lvl = f"{spell_obj.level}"
                            else:
                                current_lvl = f" {spell_obj.level}"

                            if spell_obj.max_level >= 10:
                                max_lvl = f"{spell_obj.max_level}"
                            else:
                                max_lvl = f"{spell_obj.max_level} "

                            string = f"{spells_emojis[spell_name]} `{current_lvl}/{max_lvl}`"

                        if spell_index % 4 == 0:
                            string += "\n"
                        else:
                            string += f"{g.space_character}"

                        spells.append(string)
                        spell_index += 1

                    # Heroes
                    heroes = []
                    hero_index = 1
                    for hero_name in list(heroes_emojis):
                        hero = p.get_hero(hero_name)

                        if hero_name not in in_player_heroes:
                            string = f"{heroes_emojis[hero_name]}  ` N/A `"

                            not_unlocked.append(string)
                            continue

                        else:
                            if hero.level >= 10:
                                current_lvl = f"{hero.level}"
                            else:
                                current_lvl = f" {hero.level}"

                            if hero.max_level >= 10:
                                max_lvl = f"{hero.max_level}"
                            else:
                                max_lvl = f"{hero.max_level} "

                            string = f"{heroes_emojis[hero_name]} `{current_lvl}/{max_lvl}`"

                        if hero_index % 4 == 0:
                            string += "\n"
                        else:
                            string += f"{g.space_character}"

                        heroes.append(string)
                        hero_index += 1

                    # Not Unlocked
                    not_unlocked_index = 1
                    not_unlocked_final = []
                    for not_unlocked_obj in not_unlocked:
                        if not_unlocked_index % 4 == 0:
                            not_unlocked_obj += "\n"
                        else:
                            not_unlocked_obj += f"{g.space_character}"

                        not_unlocked_final.append(not_unlocked_obj)
                        not_unlocked_index += 1


                    home_troops_str = "".join(home_troops)
                    builder_troops_str = "".join(builder_troops)
                    spells_str = "".join(spells)
                    heroes_str = "".join(heroes)
                    not_unlocked_str = "".join(not_unlocked_final)

                    embed_troops = await embeds.embed_gen(
                        ctx.channel,
                        None,
                        None,
                        None,
                        town_hall_link,
                        None,
                        g.zap_color,
                        True
                    )
                    embed_troops.set_author(name=f"{p.name} ({p.tag})", icon_url=league_icon_url)
                    embed_troops.add_field(name="Home Village", value=home_troops_str, inline=False)
                    embed_troops.add_field(name="Builder Base", value=builder_troops_str, inline=False)
                    embed_troops.add_field(name="Spells", value=spells_str, inline=False)
                    embed_troops.add_field(name="Heroes", value=heroes_str, inline=False)
                    embed_troops.add_field(name="Not Unlocked", value=not_unlocked_str, inline=False)

                    view = discord.ui.View()
                    view.add_item(ButtonHandler(style=discord.ButtonStyle.green, url=None, disabled=False,
                                                label="Statistics", emoji=None, button_user=ctx.author, custom_id="Statistics"))

                    view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=p.share_link, disabled=False,
                                                label="Open in-game", emoji=None, button_user=None, custom_id=None))
                    current_embed = embed_troops
                    current_view = view

                elif current_view.value == "Statistics":

                    view = discord.ui.View()
                    view.add_item(ButtonHandler(style=discord.ButtonStyle.green, url=None, disabled=False,
                                                label="Troops", emoji=None, button_user=ctx.author,
                                                custom_id="Troops"))

                    view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=p.share_link, disabled=False,
                                                label="Open in-game", emoji=None, button_user=None, custom_id=None))
                    current_embed = embed_player
                    current_view = view

            else:
                current_label = current_view.children[0].to_component_dict()['label']

                view = discord.ui.View()
                view.add_item(ButtonHandler(style=discord.ButtonStyle.green, url=None, disabled=True,
                                            label=current_label, emoji=None, button_user=ctx.author, custom_id=current_label))
                view.add_item(ButtonHandler(style=discord.ButtonStyle.grey, url=p.share_link, disabled=False,
                                            label="Open in-game", emoji=None, button_user=None, custom_id=None))
                current_view = view

                await player_msg.edit(embed=current_embed, view=current_view)

    # Command: player
    @commands.command(description="Player information")
    async def player(self, ctx, tag):
        """Returns information about a player of Clash of Clans using the player's tag."""
        await ctx.trigger_typing()
        await self.sending_player(ctx, tag)


    # Command: linkplayer
    @commands.command(aliases=["playerlink", "player-link", "link-player", "p-link"], description="Linking a player with you")
    async def linkplayer(self, ctx: commands.Context, tag):
        """
        To link a player of Clash of Clans with your Discord account by using the player's tag.
        Use `profile` to display the information about the linked player.
        """

        await ctx.trigger_typing()
        p = await self.client.coc_client.get_player(tag)
        db = db_connector.db_connect()

        try:
            sql = f"INSERT INTO linked_players (UserID, Tag) VALUES (%s, %s)"
            val = (ctx.author.id, p.tag)
            db.mycursor.execute(sql, val)
            db.connection.commit()

        except mysql.connector.IntegrityError:
            sql = f"SELECT Tag FROM linked_players WHERE UserID = {ctx.author.id}"
            db.mycursor.execute(sql)
            result = db.mycursor.fetchall()
            selected_tag = result[0][0]
            if selected_tag == p.tag:
                await embeds.embed_gen(
                    ctx.channel,
                    "Link player",
                    f"{g.e_xmark} `{p.name} ({p.tag})` is already linked with you.",
                    None,
                    None,
                    None,
                    g.unsuccessful_red,
                    False
                )
                return

            else:
                sql = f"UPDATE linked_players SET Tag = '{p.tag}' WHERE UserID = '{ctx.author.id}'"
                db.mycursor.execute(sql)
                db.connection.commit()

        db.connection.close()

        await embeds.embed_gen(
            ctx.channel,
            "Link player",
            f"{g.e_checkmark} Successfully linked player `{p.name} ({p.tag})` with you.",
            None,
            None,
            None,
            g.success_green,
            False
        )


    @commands.command(aliases=["playerunlink", "player-unlink", "unlink-player", "p-unlink"], description="Unlinking the linked player from you")
    async def unlinkplayer(self, ctx: commands.Context):
        """
        To unlink the linked player of Clash of Clans from you by using the player's tag.
        """

        await ctx.trigger_typing()
        db = db_connector.db_connect()

        sql = f"SELECT Tag FROM linked_players WHERE UserID = {ctx.author.id}"
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()
        if not result:
            await embeds.embed_gen(
                ctx.channel,
                "Unlink player",
                f"{g.e_xmark} You're not linked with an account.",
                None,
                None,
                None,
                g.unsuccessful_red,
                False
            )

        else:
            p = await self.client.coc_client.get_player(result[0][0])

            sql = f"DELETE FROM linked_players WHERE UserID = '{ctx.author.id}'"
            db.mycursor.execute(sql)
            db.connection.commit()

            await embeds.embed_gen(
                ctx.channel,
                "Unlink player",
                f"{g.e_checkmark} Successfully unlinked player `{p.name} ({p.tag})` from you.",
                None,
                None,
                None,
                g.success_green,
                False
            )

        db.connection.close()


    @commands.command(aliases=["p"], description="Linked player information")
    async def profile(self, ctx):
        """
        To display the information about the player of Clash of Clans which is linked with your Discord account.
        """

        await ctx.trigger_typing()
        db = db_connector.db_connect()
        sql = f"SELECT Tag FROM linked_players WHERE UserID = {ctx.author.id}"
        db.mycursor.execute(sql)
        result = db.mycursor.fetchall()
        if not result:
            x_mark = discord.File("./images/xmark.png", filename="xmark.png")

            embed_not_linked = await embeds.embed_gen(
                ctx.channel,
                None,
                None,
                None,
                None,
                None,
                g.unsuccessful_red,
                True
            )
            embed_not_linked.set_author(name="You're not linked with a player.", icon_url="attachment://xmark.png")
            await ctx.send(embed=embed_not_linked, file=x_mark)

        else:
            selected_tag = result[0][0]
            p = await self.client.coc_client.get_player(selected_tag)

            await self.sending_player(ctx, p.tag)


    @commands.command(description="Current league of a player")
    async def league(self, ctx, tag):
        """
        To display a high resolution image of the current league of a player of Clash of Clans using the player's tag.
        """

        await ctx.trigger_typing()
        p = await self.client.coc_client.get_player(tag)
        league_icon_url = p.league.icon.medium

        league_embed = await embeds.embed_gen(
            ctx.channel,
            None,
            None,
            None,
            None,
            league_icon_url,
            g.zap_color,
            True
        )
        league_embed.set_author(name=f"{p.name} ({p.tag})")
        await ctx.send(embed=league_embed)

def setup(client):
    client.add_cog(Player(client))