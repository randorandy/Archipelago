from typing import Iterator, Tuple

#from .hack_randomizer.defaultLogic import phantoon, ridley, kraid, draygon #normally
from .hack_randomizer.defaultLogic import L1, L2, L3, L4, beatTourian
from .hack_randomizer.game import Game
from .hack_randomizer.loadout import Loadout
from .hack_randomizer.logic_shortcut import LogicShortcut

from BaseClasses import CollectionState

from .item import name_to_id as item_name_to_id, id_to_hack_item


can_win = LogicShortcut(lambda loadout: (
        #(phantoon in loadout) and (ridley in loadout) and (kraid in loadout) and (draygon in loadout) #Normally
        (L1 in loadout) and (L2 in loadout) and (L3 in loadout) and (L4 in loadout) and (beatTourian in loadout)
))

def item_counts(cs: CollectionState, p: int) -> Iterator[Tuple[str, int]]:
    """
    the items that player p has collected

    ((item_name, count), (item_name, count), ...)
    """
    return ((item_name, cs.count(item_name, p)) for item_name in item_name_to_id)


def cs_to_loadout(cr_game: Game, collection_state: CollectionState, player: int) -> Loadout:
    """ convert Archipelago CollectionState to hack_randomizer loadout state """
    loadout = Loadout(cr_game)
    for item_name, count in item_counts(collection_state, player):
        loadout.contents[id_to_hack_item[item_name_to_id[item_name]]] += count
    return loadout
