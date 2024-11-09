import functools
import os
from threading import Event
from typing import Optional, Union, Dict, Any

from BaseClasses import ItemClassification, Region, CollectionState, MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World

from .client import ZFSNIClient
from .location import name_to_id as _loc_name_to_id, ZFLocation
from .item import name_to_id as _item_name_to_id, ZFItem, names_for_item_pool
from .logic import cs_to_loadout, can_win
from .options import make_zf_game

from .zfactor_randomizer.game import Game as ZFGame
from .zfactor_randomizer.defaultLogic import location_logic
from .zfactor_randomizer.item import Items

from .patch_utils import ItemRomData, GenData, make_gen_data
from .rom import ZFDeltaPatch

_ = ZFSNIClient  # load the module to register the handler


class ZFWebWorld(WebWorld):
    theme = "ice"


class ZFWorld(World):
    """
    Z Factor by Metaquarius
    """
    game = "Z Factor"
    data_version = 0
    web = ZFWebWorld()

    options_dataclass = PerGameCommonOptions
    options: PerGameCommonOptions

    location_name_to_id = _loc_name_to_id
    item_name_to_id = _item_name_to_id

    rom_name: Union[bytes, bytearray]
    rom_name_available_event: Event

    zf_game: Optional[ZFGame] = None

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.rom_name = b""
        self.rom_name_available_event = Event()

    def create_item(self, name: str) -> ZFItem:
        return ZFItem(name, self.player)

    def generate_early(self) -> None:
        early_items = ["Morph", "Missile"]
        early_item = self.multiworld.random.choice(early_items)
        self.multiworld.local_early_items[self.player][early_item] = 1

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        zf_game = make_zf_game(self.multiworld.seed)
        self.zf_game = zf_game

        for loc_name in _loc_name_to_id:
            loc = ZFLocation(self.player, loc_name, menu)
            menu.locations.append(loc)

            def access_rule_wrapped(local_loc_name: str,
                                    local_zf_game: ZFGame,
                                    p: int,
                                    collection_state: CollectionState) -> bool:
                loadout = cs_to_loadout(local_zf_game, collection_state, p)
                return location_logic[local_loc_name](loadout)

            access_rule = functools.partial(access_rule_wrapped,
                                            loc_name, self.zf_game, self.player)
            loc.access_rule = access_rule

            # completion condition
            def completion_wrapped(local_zf_game: ZFGame,
                                   p: int,
                                   collection_state: CollectionState) -> bool:
                loadout = cs_to_loadout(local_zf_game, collection_state, p)
                return can_win in loadout

            completion = functools.partial(completion_wrapped, zf_game, self.player)
            self.multiworld.completion_condition[self.player] = completion

    def create_items(self) -> None:
        count_e = 0  # 12 Energy are progression , the rest are not
        count_m = 0 # 4 Missiles are progression, the rest are not
        count_s = 0  # 5 Supers are progression, the rest are not
        count_p = 0  # 5 PowerBombs are progression, the rest are not
        for name in names_for_item_pool():
            this_item = self.create_item(name)
            if name == Items.Energy[0]:
                if count_e <= 12:
                    this_item.classification = ItemClassification.progression
                count_e += 1
            elif name == Items.Missile[0]:
                if count_m <= 4:
                    this_item.classification = ItemClassification.progression
                count_m += 1
            elif name == Items.Super[0]:
                if count_s <= 5:
                    this_item.classification = ItemClassification.progression
                count_s += 1
            elif name == Items.PowerBomb[0]:
                if count_p <= 5:
                    this_item.classification = ItemClassification.progression
                count_p += 1
            self.multiworld.itempool.append(this_item)

    def get_filler_item_name(self) -> str:
        filler_items = ["Missile", "Super", "PowerBomb"]
        filler_item = self.multiworld.random.choice(filler_items)
        return filler_item

    def generate_output(self, output_directory: str) -> None:
        assert self.zf_game, "can't call generate_output without create_regions"

        item_rom_data = ItemRomData(self.player, self.multiworld.player_name)
        for loc in self.multiworld.get_locations():
            item_rom_data.register(loc)

        # set rom name
        from Utils import __version__
        rom_name = bytearray(
            f'CR{__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}',
            'utf8'
        )[:21]
        rom_name.extend(b" " * (21 - len(rom_name)))
        assert len(rom_name) == 21, f"{rom_name=}"
        self.rom_name = rom_name
        self.rom_name_available_event.set()

        gen_data = GenData(item_rom_data.get_jsonable_data(), self.zf_game, self.player, self.rom_name)

        out_file_base = self.multiworld.get_out_file_name_base(self.player)

        patch_file_name = os.path.join(output_directory, f"{out_file_base}{ZFDeltaPatch.patch_file_ending}")
        patch = ZFDeltaPatch(patch_file_name,
                                       player=self.player,
                                       player_name=self.multiworld.player_name[self.player],
                                       gen_data=make_gen_data(gen_data))

        patch.write()

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = self.rom_name
        assert len(rom_name) == 21, f"{rom_name=}"
        new_name = base64.b64encode(rom_name).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
