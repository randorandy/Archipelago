import random
from typing import Optional

from .fillInterface import FillAlgorithm
from .item import Item, Items
from .loadout import Loadout
from .location import Location
from .solver import solve

_minor_items = {
    Items.Missile: 46,
    Items.Super: 18,
    Items.PowerBomb: 9,
    Items.Energy: 13,
    Items.Reserve: 3
}


class FillAssumed(FillAlgorithm):
    prog_items: list[Item]
    extra_items: list[Item]
    itemLists: list[list[Item]]

    def __init__(self) -> None:
        self.prog_items = [
            Items.Missile,
            Items.Morph,
            Items.Super,
            Items.Grapple,
            Items.PowerBomb,
            Items.Springball,
            Items.Bombs,
            Items.HiJump,
            Items.GravitySuit,
            Items.Varia,
            Items.Wave,
            Items.SpeedBooster,
            Items.Spazer,
            Items.Ice,
            Items.Plasma,
            Items.Screw,
            Items.SpaceJump,
            Items.Charge,
            Items.Energy,
            Items.Reserve,
            Items.Xray
        ]

        self.extra_items = []
        for it, n in _minor_items.items():
            self.extra_items.extend([it for _ in range(n)])

        self.itemLists = [self.prog_items, self.extra_items]

    def _get_accessible_locations(self, loadout: Loadout) -> list[Location]:
        _, _, locs = solve(loadout.game, loadout)
        return locs

    def _get_available_locations(self, loadout: Loadout) -> list[Location]:
        return [loc for loc in self._get_accessible_locations(loadout) if loc["item"] is None]

    def _get_empty_locations(self, all_locations: dict[str, Location]) -> list[Location]:
        return [loc for loc in all_locations.values() if loc["item"] is None]

    @staticmethod
    def _choose_location(locs: list[Location], item_to_place) -> Location:
        #return random.choice(locs)
        this_choice = random.choice(locs)

        #morph ball special case
        #if item_to_place == Items.Morph :
        #    for loc_sweep in locs :
        #        if loc_sweep["roomname"] == "Morph Ball" :
        #            this_choice = loc_sweep
        #            print(" Rusty placed the morph ball")
        #yeah?

        return this_choice

    def choose_placement(self, availableLocations: list[Location], loadout: Loadout) -> Optional[tuple[Location, Item]]:
        from_items = (
            self.prog_items if len(self.prog_items) else (
                self.extra_items
            )
        )

        assert len(from_items), "tried to place item when placement algorithm has 0 items left in item pool"

        item_to_place = random.choice(from_items)
        
        #special morph case
        #if from_items.contains(Items.Morph) :
        #    item_to_place = Items.Morph
        #    print(" Rusty found the morph ball")

        from_items.remove(item_to_place)

        if from_items is self.prog_items:
            loadout = Loadout(loadout.game)
            for item in from_items:
                loadout.append(item)
            available_locations = self._get_available_locations(loadout)
        else:  # extra
            available_locations = self._get_empty_locations(loadout.game.all_locations)
        if len(available_locations) == 0:
            return None

        return self._choose_location(available_locations,item_to_place), item_to_place

    def count_items_remaining(self) -> int:
        return sum(len(li) for li in self.itemLists)

    def remove_from_pool(self, item: Item) -> None:
        """ removes this item from the item pool """
        pass  # removed in placement function
