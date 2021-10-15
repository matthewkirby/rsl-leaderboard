from collections import namedtuple
import requests

Option = namedtuple('Option', ['name', 'percentage'])

def format_percentage(num):
    x = f"{num:.3}"
    if x == "1e+02":
        x = '100'
    elif x.split('.')[-1] == '0':
        x = x.split('.')[0]
    return x + '%'

class Setting:
    def __init__(self, name, weights):
        netweight = sum(weights.values())
        self.options = [Option(name, format_percentage(100*weight/netweight)) for name, weight in weights.items()]
        self.name = name
        try:
            self.alias = aliasdict[name]
        except:
            print(f"Fancy name not found for {name}")
            self.alias = name

        self.htmlblock = ''
        self.build_html()

    def build_html(self):
        self.htmlblock += '<div class="one-setting">'
        self.htmlblock += '<span class="setting-header" onclick="toggle_block_visibility(this, \'option-block\')">'
        self.htmlblock += f'<h4>{self.alias}</h4>'
        self.htmlblock += f'<span class="race-date">{self.name}</span>'
        self.htmlblock += '</span>'

        self.htmlblock += '<span class="option-block">'
        for opt in self.options:
            self.htmlblock += '<li class="option-row">'
            self.htmlblock += f'<div class="percentage">{opt.percentage}</div>'
            self.htmlblock += f'<div class="option-name">{opt.name}</div>'
            self.htmlblock += '</li>'
        self.htmlblock += '</span>'

        self.htmlblock += '</div>'


def download_weights():
    r = requests.get("https://raw.githubusercontent.com/matthewkirby/plando-random-settings/master/weights/rsl_season3.json")
    weightdict = r.json()['weights']

    settinglist = []
    for name, weights in weightdict.items():
        settinglist.append(Setting(name, weights))

    return settinglist

aliasdict = {
    "logic_rules": "Logic Rules",
    "open_forest": "Open Forest",
    "open_kakariko": "Kakariko Gate",
    "open_door_of_time": "Open Door of Time",
    "zora_fountain": "Zora Fountain",
    "gerudo_fortress": "Gerudo Fortress",
    "bridge": "Bridge Condition",
    "bridge_medallions": "Variable Bridge Medallions",
    "bridge_stones": "Variable Bridge Stones",
    "bridge_rewards": "Variable Bridge Dungeons",
    "triforce_hunt": "Triforce Hunt",
    "bombchus_in_logic": "Bombchus in Logic",
    "one_item_per_dungeon": "One Major Item Per Dungeon",
    "trials_random": "Random Number of Trials",
    "trials": "Number of Trials",
    "starting_age": "Randomize Starting Age",
    "shuffle_interior_entrances": "Interior Entrance Shuffle",
    "shuffle_grotto_entrances": "Grotto Entrance Shuffle",
    "shuffle_dungeon_entrances": "Dungeon Entrance Shuffle",
    "shuffle_overworld_entrances": "Overworld Entrance Shuffle",
    "mix_entrance_pools": "Mixed Entrance Pools",
    "decouple_entrances": "Decoupled Entrance Pools",
    "owl_drops": "Shuffle Owl Drops",
    "warp_songs": "Randomize Warp Song Destination",
    "spawn_positions": "Randomize Overworld Spawn",
    "mq_dungeons_random": "Random Number of Master Quest Dungeons",
    "mq_dungeons": "Number of Master Quest Dungeons",
    "shopsanity": "Randomize Left Side Shop Items",
    "tokensanity": "Randomize Gold Skulltula Tokens",
    "shuffle_scrubs": "Randomize Deku Salesmen",
    "shuffle_cows": "Randomize Cows",
    "shuffle_song_items": "Randomize Song Checks",
    "shuffle_kokiri_sword": "Shuffle Kokiri Sword",
    "shuffle_ocarinas": "Shuffle Ocarina",
    "shuffle_weird_egg": "Shuffle Weird Egg",
    "shuffle_gerudo_card": "Shuffle Gerudo Card",
    "shuffle_beans": "Shuffle Beans",
    "shuffle_medigoron_carpet_salesman": "Shuffle Medigoron and Carpet Salesman",
    "shuffle_mapcompass": "Shuffle Map and Compass",
    "shuffle_smallkeys": "Shuffle Small Keys",
    "shuffle_fortresskeys": "Shuffle Gerudo Fortress Keys",
    "shuffle_bosskeys": "Shuffle Boss Keys",
    "shuffle_ganon_bosskey": "Shuffle Ganon's Boss Key",
    "lacs_condition": "Light Arrow Cutscene Condition",
    "lacs_medallions": "Variable LACs Medallions",
    "lacs_stones": "Variable LACs Stones",
    "lacs_rewards": "Variable LACs Dungeons",
    "enhance_map_compass": "Maps and Compass Give Information",
    "reachable_locations": "All Locations Reachable",
    "logic_no_night_tokens_without_suns_song": "Night Tokens Require Sun's Song",
    "skip_child_zelda": "Skip Child Zelda",
    "no_escape_sequence": "Skip Collapse",
    "no_guard_stealth": "Skip Guard Stealth",
    "no_epona_race": "Free Epona",
    "skip_some_minigame_phases": "Skip First Minigame Phase",
    "useful_cutscenes": "Enable Useful Cutscenes",
    "fast_chests": "Remove Big Chest Animation",
    "free_scarecrow": "Free Scarecrow",
    "chicken_count_random": "Random Number of Cuccos",
    "complete_mask_quest": "Complete Mask Quest",
    "chicken_count": "Number of Cuccos",
    "big_poe_count_random": "Random Number of Big Poes",
    "big_poe_count": "Number of Big Poes",
    "ocarina_songs": "Shuffle Song Notes",
    "correct_chest_sizes": "Chest Size Matches Contents",
    "fast_bunny_hood": "Fast Bunny Hood",
    "clearer_hints": "Clear Hints",
    "hints": "Hints",
    "hint_dist": "Hint Distribution",
    "misc_hints": "Misc. Hints",
    "text_shuffle": "Text Shuffle",
    "damage_multiplier": "Damage Multiplier",
    "no_collectible_hearts": "No Collectible Heart Drops (Hero Mode)",
    "starting_tod": "Starting Time of Day",
    "item_pool_value": "Item Pool",
    "junk_ice_traps": "Number of Ice Traps",
    "ice_trap_appearance": "Freestand Ice Trap Appearence",
    "logic_earliest_adult_trade": "Earliest Adult Trade Item",
    "logic_latest_adult_trade": "Latest Adult Trade Item",
    "start_with_consumables": "Start with Deku Nuts and Sticks",
    "start_with_rupees": "Start with a Full Wallet",
    "starting_hearts": "Starting Hearts",
    "shuffle_hideoutkeys": "Shuffle Gerudo Fortress Keys",
    "ganon_bosskey_medallions": "Medallions Required for Ganon Boss Key",
    "ganon_bosskey_stones": "Stones Required for Ganon Boss Key",
    "ganon_bosskey_rewards": "Dungeon Rewards Required for Ganon Boss Key",
}