from typing import Union

from .zfactor_randomizer.defaultLogic import Default
from .zfactor_randomizer.game import Game

from .location import location_data #could be worlds.zfactor.location


def make_zf_game(seed: Union[int, None])-> Game:
    seed = seed or 0
    cr_game = Game(Default,location_data,seed)
    return cr_game
