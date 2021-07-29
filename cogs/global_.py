from discord.ext import commands
# end imports


class Global(commands.Cog):
    """Global variables"""
    def __init__(self, client):
        self.client = client


    # Channel
    error_channel = 764227729653628949

    # Emojis
    e_reload = "🔄"
    e_arrow_up_right = "↗️"
    e_arrow_down_right = "↘️"
    e_white_checkmark = "✅"
    e_warstar = "<:warstar:869971390101585970>"
    e_trophy = "<:trophy:869971390055481425>"
    e_troops_donation = "<:troopsdonation:869971390466510878>"
    e_shield = "<:shield:869971389560549417>"
    e_royal_champion = "<:royalchampion:869971390151934032>"
    e_receive = "<:receive:869971389833158768>"
    e_level = "<:level:869971390034497576>"
    e_grand_warden = "<:grandwarden:869971389992534076>"
    e_gold = "<:gold:869971390009344140>"
    e_error = "<:error:869971390042877983>"
    e_elixir = "<:elixir:869971389703143506>"
    e_donate = "<:donate:869971389921239081>"
    e_dark_elixir = "<:darkelixir:869971389908656189>"
    e_battle_machine = "<:battlemachine:869971389933817917>"
    e_barbarian_king = "<:barbarianking:869971389883494400>"
    e_attack = "<:attack:869971389837369435>"
    e_archer_queen = "<:archerqueen:869971389896065064>"
    e_league = "<:league:869990439107854416>"
    e_ratio = f"<:ratio:870058820968251403>"
    e_clan_games = f"<:clangames:870017176436883477>"
    e_wall_wrecker = f"<:wallwrecker:870017176852123658>"
    e_spells_donation = f"<:spellsdonation:870017176617222154>"
    e_clan = "<:clan:870066665600221194>"
    e_checkmark = "<:checkmark:870277471092764672>"
    e_xmark = "<:xmark:870277471071776778>"

    e_label_veteran = "<:veteran:870037558099333190>"
    e_label_trophypushing = "<:trophypushing:870037557826682910>"
    e_label_teacher = "<:teacher:870037557461803120>"
    e_label_talkative = "<:talkative:870037558116110346>"
    e_label_newbie = "<:newbie:870037557851873330>"
    e_label_hungrylearner = "<:hungrylearner:870037558208397372>"
    e_label_friendlywars = "<:friendlywars:870037557604397077>"
    e_label_friendly = "<:friendly:870037557763768340>"
    e_label_farming = "<:farming:870037557948317766>"
    e_label_competitive = "<:competitive:870037557835071498>"
    e_label_clanwars = "<:clanwars:870037557939929199>"
    e_label_clanwarleague = "<:clanwarleague:870037558044811295>"
    e_label_clangames2 = "<:clangames2:870037557914771537>"
    e_label_builderbase = "<:builderbase:870037557839278180>"
    e_label_basedesigning = "<:basedesigning:870037557465976852>"
    e_label_amateurattacker = "<:amateurattacker:870037557520523324>"
    e_label_activedonator = "<:activedonator:870037555670818827>"
    e_label_activedaily = "<:activedaily:870037555985383474>"

    # Hex colors
    zap_color = 0x29b6ee

    error_red = 0xb90000
    success_green = 0x36cf21
    unsuccessful_red = 0xf51616

    # Other
    space_character = "　"


def setup(client):
    client.add_cog(Global(client))