from collections import defaultdict
from typing import Dict, Iterator

from BaseClasses import Item, ItemClassification as IC

from .config import base_id

from .zfactor_randomizer.item import Item as ZFInternalItem, Items
from .zfactor_randomizer.fillAssumed import FillAssumed

classifications: Dict[str, IC] = defaultdict(lambda: IC.progression)
classifications.update({
    Items.Reserve[0]: IC.useful,
    Items.PowerBomb[0]: IC.useful,
    Items.Energy[0]: IC.useful,  # 12 progression set by create_items
    Items.Super[0]: IC.useful,  # 5 progression set by create_items
    Items.Missile[0]: IC.useful  # 1 progression set by create_items
})


class ZFItem(Item):
    game = "Z Factor"
    __slots__ = ("zf_item",)
    zf_item: ZFInternalItem

    def __init__(self, name: str, player: int) -> None:
        classification = classifications[name]
        code = name_to_id[name]
        super().__init__(name, classification, code, player)
        self.zf_item = id_to_zf_item[code]


local_id_to_zf_item: Dict[int, ZFInternalItem] = {
    0x00: Items.Energy,
    0x01: Items.Missile,
    0x02: Items.Super,
    0x03: Items.PowerBomb,
    0x04: Items.Bombs,
    0x05: Items.Charge,
    0x06: Items.Ice,
    0x07: Items.HiJump,
    0x08: Items.SpeedBooster,
    0x09: Items.Wave,
    0x0a: Items.Spazer,
    0x0b: Items.Springball,
    0x0c: Items.Varia,
    0x0d: Items.GravitySuit,
    0x0e: Items.Xray,
    0x0f: Items.Plasma,
    0x10: Items.Grapple,
    0x11: Items.SpaceJump,
    0x12: Items.Screw,
    0x13: Items.Morph,
    0x14: Items.Reserve
}


id_to_zf_item = {
    id_ + base_id: item
    for id_, item in local_id_to_zf_item.items()
}

name_to_id = {
    item[0]: id_
    for id_, item in id_to_zf_item.items()
}


def names_for_item_pool() -> Iterator[str]:
    zf_fill = FillAssumed()
    for zf_item in zf_fill.prog_items:
        yield zf_item[0]
    for zf_item in zf_fill.extra_items:
        yield zf_item[0]
