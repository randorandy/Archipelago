import json
from dataclasses import dataclass
from enum import IntEnum
from itertools import chain
from typing import Final, List, Set, Mapping, Tuple, Dict, Union, Optional
from pathlib import Path

from .hack_randomizer.romWriter import RomWriter

from BaseClasses import Location, ItemClassification
from .location import HackLocation
from .config import base_id, open_file_apworld_compatible
from .item import local_id_to_hack_item, HackItem

from .hack_randomizer.game import Game as CrGame
from .hack_randomizer.ips import patch as ips_patch


box_blue_tbl = {
    ### dupes below 
    "A": 0x2CE0,
    "B": 0x2CE1, #Confirmed CR
    "C": 0x2CE2, #Confirmed CR
    "D": 0x2CE3,
    "E": 0x2CE4, #Confirmed CR
    "F": 0x2CE5,
    "G": 0x2CE6, #Confirmed CR
    "H": 0x2CE7, #Confirmed CR
    "I": 0x2CE8, #Confirmed CR
    "J": 0x2CE9, #Confirmed CR
    "K": 0x2CEA, #Confirmed CR
    "L": 0x2CEB, #Confirmed CR
    "M": 0x2CEC, #Confirmed CR
    "N": 0x2CED, #Confirmed CR
    "O": 0x2CEE, #Confirmed CR
    "P": 0x2CEF, #Confirmed CR
    "Q": 0x2CF0, #Confirmed CR
    "R": 0x2CF1, #Confirmed CR
    "S": 0x2CF2, #Confirmed CR
    "T": 0x2CF3, #Confirmed CR
    "U": 0x2CF4, #Confirmed CR
    "V": 0x2CF5,
    "W": 0x2CF6,
    "X": 0x2CF7, 
    "Y": 0x2CF8, #Confirmed CR
    "Z": 0x2CF9,
    " ": 0x2C0F,
    "!": 0x2CDF,
    "?": 0x2CDE,
    "'": 0x2CDC,
    ",": 0xACDC,
    ".": 0x2CDA,
    "-": 0x2CFA, #was showing up as a Q  with 2cf0
    "_": 0x000E,  # character used for edges of screen during text box
    "1": 0x2C00, #confirmed CR
    "2": 0x2C01,
    "3": 0x2C02,
    "4": 0x2C03,
    "5": 0x2C04, #confirmed CR
    "6": 0x2C05, #confirmed CR
    "7": 0x2C06,
    "8": 0x2C07,
    "9": 0x2C08,
    "0": 0x2C09, #confirmed CR
    "%": 0x2C0A,
}
""" item names use this, player names are ascii """


def get_word_array(w: int) -> Tuple[int, int]:
    """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
    return w & 0x00FF, (w & 0xFF00) >> 8


def make_item_name_for_rom(item_name: str) -> bytearray:
    """ 64 bytes (32 chars) centered, encoded with box_blue.tbl """
    data = bytearray()

    item_name = item_name.upper()[:26]
    item_name = item_name.strip()
    item_name = item_name.center(26, " ")
    item_name = "___" + item_name + "___"
    assert len(item_name) == 32, f"{len(item_name)=}"

    for char in item_name:
        w0, w1 = get_word_array(box_blue_tbl.get(char, 0x2C0F))
        data.append(w0)
        data.append(w1)
    assert len(data) == 64, f"{len(data)=}"
    return data


_symbols: Optional[Dict[str, str]] = None


def offset_from_symbol(symbol: str) -> int:
    global _symbols
    if _symbols is None:
        path = Path(__file__).parent.resolve()
        json_path = path.joinpath("data", "ap_hack_patch", "sm-basepatch-symbols.json")
        with open_file_apworld_compatible(json_path) as symbols_file:
            _symbols = json.load(symbols_file)
        assert _symbols

    snes_addr_str = _symbols[symbol]
    snes_addr_str = "".join(snes_addr_str.split(":"))
    snes_addr = int(snes_addr_str, 16)
    offset = RomWriter.snes_to_index_addr(snes_addr)
    return offset


_item_sprites = [
    {
        "fileName":          "off_world_prog_item.bin",
        "paletteSymbolName": "prog_item_eight_palette_indices",
        "dataSymbolName":    "offworld_graphics_data_progression_item"
    },
    {
        "fileName":          "off_world_item.bin",
        "paletteSymbolName": "nonprog_item_eight_palette_indices",
        "dataSymbolName":    "offworld_graphics_data_item"
    }
]


def patch_item_sprites(rom: Union[bytes, bytearray]) -> bytearray:
    """
    puts the 2 new off-world item sprites in the rom

    takes sprites from Super Metroid world directory
    """
    tr = bytearray(rom)

    path = Path(__file__).parent.resolve()

    for item_sprite in _item_sprites:
        palette_offset = offset_from_symbol(item_sprite["paletteSymbolName"])
        data_offset = offset_from_symbol(item_sprite["dataSymbolName"])
        with open_file_apworld_compatible(
            path.joinpath("data", "custom_sprite", item_sprite["fileName"]), 'rb'
        ) as file:
            offworld_data = file.read()
            tr[palette_offset:palette_offset + 8] = offworld_data[0:8]
            tr[data_offset:data_offset + 256] = offworld_data[8:264]
    return tr



class _DestinationType(IntEnum):
    Me = 0
    Other = 1
    LinkWithMe = 2


@dataclass
class _ItemTableEntry:
    destination: _DestinationType
    item_id: int
    player_index: int
    advancement: bool

    def to_bytes(self) -> bytes:
        return (self.destination.to_bytes(2, "little") +
                self.item_id.to_bytes(2, "little") +
                self.player_index.to_bytes(2, "little") +
                self.advancement.to_bytes(2, "little"))


NUM_ITEMS_WITH_ICONS = len(local_id_to_hack_item)

ItemNames_ItemTable_PlayerNames_PlayerIDs = Tuple[List[bytearray], Dict[int, _ItemTableEntry], bytearray, List[int]]

ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON = Tuple[List[List[int]], Dict[str, List[int]], List[int], List[int]]


class ItemRomData:
    player: Final[int]
    """ my AP id for this game """
    my_locations: List[HackLocation]
    """ locations in my world """
    player_ids: Set[int]
    """ all the players I interact with (including myself and 0 (the server player)) """
    player_id_to_name: Mapping[int, str]

    def __init__(self, my_player_id: int, player_id_to_name: Mapping[int, str]) -> None:
        self.player = my_player_id
        self.my_locations = []
        self.player_ids = {0, my_player_id}
        self.player_id_to_name = player_id_to_name

    def register(self, loc: Location) -> None:
        """ call this with every multiworld location """
        if loc.player == self.player:
            # my location
            assert isinstance(loc, HackLocation)
            if not loc.item:
                # This function should only be called after fill is complete.
                raise ValueError("got a location with no item")
            self.player_ids.add(loc.item.player)
            self.my_locations.append(loc)
        else:  # not my location
            if loc.item and loc.item.player == self.player:
                # my item in someone else's location
                self.player_ids.add(loc.player)

    def _make_tables(self) -> ItemNames_ItemTable_PlayerNames_PlayerIDs:
        """ after all locations are registered """
        item_table: Dict[int, _ItemTableEntry] = {}

        item_names_after_constants: List[bytearray] = []
        sorted_player_ids = sorted(self.player_ids)
        if len(sorted_player_ids) > 202:  # magic number from asm patch TODO change to 142
            # this should never happen
            sorted_player_ids = sorted_player_ids[:202]  # TODO change to 142
            if self.player > sorted_player_ids[-1]:
                sorted_player_ids[-1] = self.player

        # id in this game to index in rom tables
        player_id_to_index = {
            id_: i
            for i, id_ in enumerate(sorted_player_ids)
        }

        for loc in self.my_locations:
            cr_loc = loc.cr_loc
            cr_loc_ids = [cr_loc["index"]]
            assert loc.item
            progression = bool(loc.item.classification & ItemClassification.progression)
            player_index = player_id_to_index.get(loc.item.player, 0)  # 0 player is Archipelago
            if loc.item.player == self.player:
                # my item in my location
                assert loc.item.code
                table_entry = _ItemTableEntry(
                    _DestinationType.Me,
                    loc.item.code - base_id,
                    player_index,
                    progression
                )
            else:  # someone else's item in my location
                # TODO: check for item links that include me
                item_id = NUM_ITEMS_WITH_ICONS + len(item_names_after_constants)
                # items we can display from other games
                if isinstance(loc.item, HackItem):
                    # someone else's super junkoid item in my location
                    assert loc.item.code
                    item_id = loc.item.code - base_id
                if item_id == NUM_ITEMS_WITH_ICONS + len(item_names_after_constants):
                    # if we didn't find a super junkoid sprite for this item
                    item_names_after_constants.append(make_item_name_for_rom(loc.item.name))

                table_entry = _ItemTableEntry(
                    _DestinationType.Other,
                    item_id,
                    player_index,
                    not progression
                )
            for loc_id in cr_loc_ids:
                item_table[loc_id] = table_entry

        player_names = bytearray()
        player_names.extend(b"  Archipelago   ")
        for player_id in sorted_player_ids[1:]:
            this_name = self.player_id_to_name[player_id].upper().encode("ascii", "ignore")[:16].center(16)
            player_names.extend(this_name)

        return item_names_after_constants, item_table, player_names, sorted_player_ids

    def get_jsonable_data(self) -> ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON:
        """ data that can be encoded to json, and can be passed to `patch_from_json` """
        item_names_after_constants, item_table, player_names, sorted_player_ids = self._make_tables()

        return (
            [list(item_name) for item_name in item_names_after_constants],
            {str(loc_id): list(entry.to_bytes()) for loc_id, entry in item_table.items()},
            list(player_names),
            sorted_player_ids
        )

    @staticmethod
    def patch_from_json(
        rom: Union[bytes, bytearray],
        json_result: ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON
    ) -> bytearray:
        tr = bytearray(rom)
        item_names_after_constants, item_table, player_names, sorted_player_ids = json_result

        item_names_offset = offset_from_symbol("message_item_names") + 64 * NUM_ITEMS_WITH_ICONS
        concat_bytes = bytes(chain.from_iterable(item_names_after_constants))
        tr[item_names_offset:item_names_offset + len(concat_bytes)] = concat_bytes

        item_table_offset = offset_from_symbol("rando_item_table")
        for index, entry in item_table.items():
            data = bytes(entry)
            this_offset = item_table_offset + int(index) * len(data)
            tr[this_offset:this_offset + len(data)] = data

        player_name_offset = offset_from_symbol("rando_player_name_table")
        tr[player_name_offset:player_name_offset + len(player_names)] = player_names

        player_id_offset = offset_from_symbol("rando_player_id_table")
        for i, id_ in enumerate(sorted_player_ids):
            this_offset = player_id_offset + i * 2
            tr[this_offset:this_offset + 2] = id_.to_bytes(2, "little")

        return tr


def ips_patch_from_file(ips_file_name: Union[str, Path], input_bytes: Union[bytes, bytearray]) -> bytearray:
    with open_file_apworld_compatible(ips_file_name, "rb") as ips_file:
        ips_data = ips_file.read()
    return ips_patch(input_bytes, ips_data)

def get_multi_patch_path() -> Path:
    """ multiworld-basepatch.ips """
    path = Path(__file__).parent.resolve()
    return path.joinpath("data", "ap_hack_patch", "multiworld-basepatch.ips")

@dataclass
class GenData:
    item_rom_data: ItemNames_ItemTable_PlayerNames_PlayerIDs_JSON
    cr_game: CrGame
    player: int
    game_name_in_rom: Union[bytes, bytearray]


def make_gen_data(data: GenData) -> str:
    """ serialized data from generation needed to patch rom """
    jsonable = {
        "item_rom_data": data.item_rom_data,
        "cr_game": data.cr_game.to_jsonable(),
        "player": data.player,
        "game_name_in_rom": list(data.game_name_in_rom)
    }
    return json.dumps(jsonable)


def get_gen_data(gen_data_str: str) -> GenData:
    """ the reverse of `make_gen_data` """
    from_json = json.loads(gen_data_str)
    return GenData(
        from_json["item_rom_data"],
        CrGame.from_jsonable(from_json["cr_game"]),
        from_json["player"],
        bytes(from_json["game_name_in_rom"])
    )