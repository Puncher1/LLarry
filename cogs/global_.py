from discord.ext import commands
# end imports


class Global(commands.Cog):
    """Global variables"""
    def __init__(self, client):
        self.client = client

    # Users
    owner = 305354423801217025


    # Channels
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
    e_gem = "<:gem:870407153217851462>"
    
    e_yeti = "<:yeti:871000221025447936>"
    e_wizzard = "<:wizzard:871000221545553991>"
    e_witch = "<:witch:871000221193211925>"
    e_wallbreaker = "<:wallbreaker:871000220887056435> "
    e_valkyre = "<:valkyre:871000221662994442>"
    e_pekka = "<:pekka:871000222036283412>"
    e_minion = "<:minion:871000220891230249>"
    e_miner = "<:miner:871000221189021717>"
    e_lavahound = "<:lavahound:871000221562318858>"
    e_icegolem = "<:icegolem:871000221021257758>"
    e_hogrider = "<:hogrider:871000221012873217>"
    e_healer = "<:healer:871000222011109400>"
    e_headhunter = "<:headhunter:871000221058998272>"
    e_golem = "<:golem:871000221860102144>"
    e_goblin = "<:goblin:871000221319065630>"
    e_giant = "<:giant:871000221885268038>"
    e_dragonrider = "<:dragonrider:871000221189017600>"
    e_dragon = "<:dragon:871000220824137770>"
    e_bowler = "<:bowler:871000221818175559>"
    e_barbarian = "<:barbarian:871000221310648350>"
    e_balloon = "<:balloon:871000221314871346>"
    e_babydragon = "<:babydragon:871000220765392927>"
    e_archer = "<:archer:871000220215959582>"
    e_electrodragon = "<:electrodragon:871095514425335888>"
    e_superpekka = "<:superpekka:871118174345633833>"
    e_sneakyarcher = "<:sneakyarcher:871118174203035689>"
    e_ragebarbarian = "<:ragedbarbarian:871118174123339818>"
    e_nightwitch = "<:nightwitch:871118174475657297>"
    e_hogglider = "<:hogglider:871118174274338916>"
    e_dropship = "<:dropship:871118174425350194>"
    e_cannoncart = "<:cannoncart:871118174274338919>"
    e_bomber = "<:bomber:871118174316269578>"
    e_betaminion = "<:betaminion:871118174345633832>"
    e_boxergiant = "<:boxergiant:871118174295318599>"

    e_lightning_spell = "<:lightningspell:871400553522020382>"
    e_healing_spell = "<:healingspell:871400553199063092>"
    e_rage_spell = "<:ragespell:871400552725102624>"
    e_jump_spell = "<:jumpspell:871400552821575710>"
    e_freeze_spell = "<:freezespell:871400552725102623>"
    e_clone_spell = "<:clonespell:871400552611840052>"
    e_invisibility_spell = "<:invisibilityspell:871400552519573585>"
    e_poison_spell = "<:poisonspell:871400552607649803>"
    e_earthquake_spell = "<:earthquakespell:871400552767045632>"
    e_haste_spell = "<:hastespell:871400553052242010>"
    e_skeleton_spell = "<:skeletonspell:871400552477650975>"
    e_bat_spell = "<:batspell:871400552339214336>"

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
    ignored_help_cogs = ["ErrorListeners", "Global"]


def setup(client):
    client.add_cog(Global(client))