import hashlib
import os
import zipfile
from typing import Any, Optional

from .hack_randomizer.romWriter import RomWriter

import Utils
from Utils import read_snes_rom
from worlds.Files import APDeltaPatch, APContainer
from .patch_utils import get_gen_data, ips_patch_from_file, get_multi_patch_path, patch_item_sprites, \
    ItemRomData, offset_from_symbol

from .hack_metadata import import_game, import_patch_file_ending
from .redo_messages import redo_message_table

SMJUHASH = '21f3e98df4780ee1c667b84e57d88675'

AP_ITEM = ("AP Item",
           b"\xc0\xfb",
           b"\xc4\xfb",
           b"\xc8\xfb",
           b"\x00") 


# SNIClient assumes that the patch it gets is an APDeltaPatch
# Otherwise, it might be better to inherit from APContainer instead of APDeltaPatch.
# So in some places, instead of calling `super()`, we jump over APDeltaPatch to APContainer
# because we don't have a bs4diff.

class HackDeltaPatch(APDeltaPatch):
    hash = SMJUHASH
    game = import_game
    patch_file_ending = import_patch_file_ending

    gen_data: str
    """ JSON encoded """

    def __init__(self, *args: Any, patched_path: str = "", gen_data: str = "", **kwargs: Any) -> None:
        super().__init__(*args, patched_path=patched_path, **kwargs)
        self.gen_data = gen_data

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        APContainer.write_contents(self, opened_zipfile)
        opened_zipfile.writestr("rom_data.json",
                                self.gen_data,
                                compress_type=zipfile.ZIP_DEFLATED)

    def read_contents(self, opened_zipfile: zipfile.ZipFile):
        APContainer.read_contents(self, opened_zipfile)
        self.gen_data = opened_zipfile.read("rom_data.json").decode()

    def patch(self, target: str) -> None:
        self.read()
        write_rom_from_gen_data(self.gen_data, target)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes: Optional[bytes] = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        """if SMJUHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for Japan+US release. '
                            'Get the correct game and version, then dump it')"""
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["sm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def write_rom_from_gen_data(gen_data_str: str, output_rom_file_name: str) -> None:
    """ take the output of `make_gen_data`, and create rom from it """
    gen_data = get_gen_data(gen_data_str)

    base_rom_path = get_base_rom_path()
    rom_writer = RomWriter.fromFilePath(base_rom_path)  # this patches SM to the hack

    multi_patch_path = get_multi_patch_path()
    rom_writer.rom_data = ips_patch_from_file(multi_patch_path, rom_writer.rom_data)

    rom_writer.rom_data = patch_item_sprites(rom_writer.rom_data)

    rom_writer.rom_data = ItemRomData.patch_from_json(rom_writer.rom_data, gen_data.item_rom_data)

    # change values for chozo ball hearts and lucky frog to match the open variant
    #rom_writer.writeBytes(0x026474, b"\x19")
    #rom_writer.writeBytes(0x026909, b"\x32")

    for loc in gen_data.hack_game.all_locations.values():
        if loc["hiddenness"] == "hidden":
            plmid = AP_ITEM[3]
        elif loc["hiddenness"] == "chozo":
            plmid = AP_ITEM[2]
        else:
            plmid = AP_ITEM[1]

        rom_writer.writeItem(loc["locationid"], plmid, AP_ITEM[4])
        if loc["altlocationids"][0] != 0:
            for address in loc["altlocationids"]:
                rom_writer.writeItem(address, plmid, AP_ITEM[4])

    # TODO: deathlink
    # self.multiworld.death_link[self.player].value
    offset_from_symbol("config_deathlink")

    remote_items_offset = offset_from_symbol("config_remote_items")
    remote_items_value = 0b101
    # TODO: if remote items: |= 0b10
    rom_writer.writeBytes(remote_items_offset, remote_items_value.to_bytes(1, "little"))

    player_id_offset = offset_from_symbol("config_player_id")
    rom_writer.writeBytes(player_id_offset, gen_data.player.to_bytes(2, "little"))

    rom_writer.writeBytes(0x7fc0, gen_data.game_name_in_rom)

    # Remove gravity suit heat protection
    rom_writer.writeBytes(0x6e37d, b"\x01")
    rom_writer.writeBytes(0x869dd, b"\x01")

    # Morph Ball Fix
    rom_writer.writeBytes(0x268ce, b"\x04")
    rom_writer.writeBytes(0x26e02, b"\x04")

    #restore gravity pickup behavior (no bonus items!)
    rom_writer.writeBytes(0x262ff, b"\x20\x00")

    #return backdoor xray to within the destroyed room so its accessible
    rom_writer.writeBytes(0x3118a0, b"\x38\x1c")

    rom_writer = redo_message_table(rom_writer)

    #patch the char table (SZM)
    rom_writer.writeBytes(0x2baf3, b"\x0f\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38\x0a\x38\x0a\x38\xdd\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38\xdb\x38\xbe\x38\xda\x38\x0f\x38")
    rom_writer.writeBytes(0x2bb13, b"\x00\x38\x01\x38\x02\x38\x03\x38\x04\x38\x05\x38\x06\x38\x07\x38\x08\x38\x09\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38\xde\x38")
    rom_writer.writeBytes(0x2bb33, b"\x0f\x38\xc0\x38\xc1\x38\xc2\x38\xc3\x38\xc4\x38\xc5\x38\xc6\x38\xc7\x38\xc8\x38\xc9\x38\xca\x38\xcb\x38\xcc\x38\xcd\x38\xce\x38")
    rom_writer.writeBytes(0x2bb53, b"\xcf\x38\xd0\x38\xd1\x38\xd2\x38\xd3\x38\xd4\x38\xd5\x38\xd6\x38\xd7\x38\xd8\x38\xd9\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38\x0f\x38")

    rom_writer.finalizeRom(output_rom_file_name)  # writes rom file
