from typing import Union

from .hack_randomizer.defaultLogic import Default
from .hack_randomizer.game import Game

from .location import location_data #could be worlds.hack.location


def make_hack_game(seed: Union[int, None])-> Game:
    seed = seed or 0
    hack_game = Game(Default,location_data,seed)
    return hack_game
