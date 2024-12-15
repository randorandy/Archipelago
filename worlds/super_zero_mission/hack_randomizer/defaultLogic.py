from typing import ClassVar

from .item import items_unpackable, Items
from .loadout import Loadout
from .logicInterface import LocationLogicType, LogicInterface
from .logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places.
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    GravitySuit, Varia, Wave, SpeedBooster, Spazer, Ice, Grapple,
    Plasma, Screw, Charge, SpaceJump, Energy, Reserve, Xray
) = items_unpackable

energy200 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Energy) + loadout.count(Items.Reserve) >= 2
))

energy300 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Energy) + loadout.count(Items.Reserve) >= 4
))

energy600 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Energy) + loadout.count(Items.Reserve) >= 10
))
energy900 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Energy) + loadout.count(Items.Reserve) >= 16
))

missile15 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Missile) * 5 >= 15
))
super10 = LogicShortcut(lambda loadout: (
    loadout.count(Items.Super) * 2 >= 10
))
powerBomb11 = LogicShortcut(lambda loadout: (
    loadout.count(Items.PowerBomb) * 2 >= 11
))
pinkDoor = LogicShortcut(lambda loadout: (
    (Missile in loadout) or
    (Super in loadout)
))
canUseBombs = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    ((Bombs in loadout) or (PowerBomb in loadout))
))
canUsePB = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (PowerBomb in loadout)
))
canIBJ = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (Bombs in loadout)
))
canBreakBlocks = LogicShortcut(lambda loadout: (
    #with bombs or screw attack, maybe without morph
    (canUseBombs in loadout) or
    (Screw in loadout)
))
fullBeams = LogicShortcut(lambda loadout: (
    (Ice in loadout) and
    (Wave in loadout) and
    (Plasma in loadout)
))
brinstar = LogicShortcut(lambda loadout: (
    #To go right past the robot
    (Morph in loadout) or
    (SpeedBooster in loadout)
    #or another way around?
))
outsideBombs = LogicShortcut(lambda loadout: (
    (brinstar in loadout) and
    (Morph in loadout) and
    (
        (canIBJ in loadout) or
        (pinkDoor in loadout) or
        (SpaceJump in loadout) or
        (SpeedBooster in loadout) or
        (Ice in loadout)
        ##Possibly more ways to get up far right Brin
        #From grapple would need Supers, ok
        #From moat would need Bombs, ok
        ##From ship, crazy, idk
        )
))
variaArea = LogicShortcut(lambda loadout: (
    (brinstar in loadout) and
    (
        #from left
        (
            (pinkDoor in loadout) and
            (
                (canIBJ in loadout) or
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (Ice in loadout)
                ) and
            (
                (canUseBombs in loadout) or
                (
                    (Varia in loadout) and
                    (energy300 in loadout)
                    ) or
                (GravitySuit in loadout) or
                (energy600 in loadout) or
                (
                    (canUsePB in loadout) and
                    (SpeedBooster in loadout)
                    )
                )
            ) or
        #from right
        (
            (
                (canBreakBlocks in loadout) or
                (SpeedBooster in loadout)
                ) and
            (
                (canIBJ in loadout) or
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (Ice in loadout) or
                (SpeedBooster in loadout)
                )
            )
        )
))
kraidEntry = LogicShortcut(lambda loadout: (
    (
        (pinkDoor in loadout) and
        (
            (canBreakBlocks in loadout) or
            (SpeedBooster in loadout)
            )
        )
))
kraidTrigger = LogicShortcut(lambda loadout: (
    #For entering spore spawn
    (kraidEntry in loadout) and
    (pinkDoor in loadout) and
    ((Bombs in loadout) or (Wave in loadout)) and
    (Morph in loadout)
))
kraidEagle = LogicShortcut(lambda loadout: (
    (   #Traditional
        (kraidEntry in loadout) and
        (kraidTrigger in loadout) and
        (Super in loadout)
        ) or
    (   #Mockball Gate
        (kraidEntry in loadout) and
        (Super in loadout) and
        (Morph in loadout)
        )
    #the lava dive entry, norfair tube, and tourian backdoor
    #are more expensive than these
))
kraidHub = LogicShortcut(lambda loadout: (
    (canUseBombs in loadout) and
    (
        (Super in loadout) or
        (
            (SpeedBooster in loadout) and
            (Wave in loadout)
            )
        )
))
beatTourian = LogicShortcut(lambda loadout: (
    (Varia in loadout) and #hellrun?
    (Super in loadout) and
    (SpeedBooster in loadout) and
    (canUseBombs in loadout) and
    (Charge in loadout)
))
lavaDive = LogicShortcut(lambda loadout: (
    (canUseBombs in loadout) and
    (Super in loadout) and
    (
        (energy900 in loadout) or
        (
            (Varia in loadout) and
            (energy600 in loadout)
            ) or
        (GravitySuit in loadout)
        )   
))
L1 = LogicShortcut(lambda loadout: (
    #traditional entry
    (
        (Super in loadout) and
        (canUseBombs in loadout) and
        (SpaceJump in loadout) and
        (
            (Missile in loadout) or
            (Charge in loadout)
            )
        ) or
    #lava dive entry
    (
        (lavaDive in loadout)
        )
))
norfairMapHub = LogicShortcut(lambda loadout: (
    (
        (energy300 in loadout) or
        (Varia in loadout)
        ) and
    (
        (SpeedBooster in loadout) or
        (
            (brinstar in loadout) and
            (Super in loadout) and
            (canUseBombs in loadout)
            ) or
        (
            (canUseBombs in loadout) and
            (pinkDoor in loadout) and
            (Grapple in loadout)
            )
        )
))
norfairEast = LogicShortcut(lambda loadout: (
    (norfairMapHub in loadout) and
    (canUseBombs in loadout) and
    (
        (energy300 in loadout) or
        (Varia in loadout)
        )
))


norfairCavern = LogicShortcut(lambda loadout: (
    (
        (norfairEast in loadout) and
        (
            (energy600 in loadout) or
            (Varia in loadout)
            ) and
        (
            (Wave in loadout) or
            (SpeedBooster in loadout)
            )
        ) or
    (lavaDive in loadout)
))

frontShip = LogicShortcut(lambda loadout: (
    (outsideBombs in loadout) and
    (
        (
            (canUseBombs in loadout) and
            (SpeedBooster in loadout)
            ) or
        (
            (Screw in loadout) and
            (
                (HiJump in loadout) or
                (Springball in loadout) or
                (SpaceJump in loadout) or
                (canIBJ in loadout)
                )
            )
        )
))

lowerNorfair = LogicShortcut(lambda loadout: (
    (
        (norfairCavern in loadout) and
        (Super in loadout) and
        (canUseBombs in loadout) and
        (
            (Varia in loadout) or
            (energy600 in loadout) #guess
            )
        ) or
    (
        (frontShip in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout) and
        (Charge in loadout) and
        (Varia in loadout)
        ##match ship entry to L2 
        )
        
))
L2 = LogicShortcut(lambda loadout: (
    (
        (lowerNorfair in loadout) and
        (Charge in loadout)
        ) or
    (
        (frontShip in loadout) and
        (SpeedBooster in loadout) and
        (Super in loadout) and
        ##any% ship entry to L2
        ##also need to escape
        (energy600 in loadout)
        )
))
aboveShip = LogicShortcut(lambda loadout: (
    (
        (
            (frontShip in loadout) and
            (SpeedBooster in loadout)
            ) or
        (
            (L2 in loadout) and
            (canUseBombs in loadout) and #these 4 v copied from L4 logic
            (SpaceJump in loadout) and
            (Missile in loadout) and
            (SpeedBooster in loadout)
            )
        )
))
aboveShipStealth = LogicShortcut(lambda loadout: (
    (frontShip in loadout) and
    (
        (SpeedBooster in loadout) and
        (Super in loadout) and
        (canUseBombs in loadout) and #already have this prob
        (
            (Grapple in loadout) or
            (SpaceJump in loadout)
            )
        )
))

belowShip = LogicShortcut(lambda loadout: (
    (aboveShip in loadout) or
    (
        (L2 in loadout) and
        (energy600 in loadout)
        )
))

L3 = LogicShortcut(lambda loadout: (
    (canUsePB in loadout) and
    (
        (Super in loadout) or
        (SpeedBooster in loadout)
        )
))
enterTourian = LogicShortcut(lambda loadout: (
    (
        (
            (L1 in loadout) and
            (L2 in loadout) and
            (lowerNorfair in loadout)
            ) or
        (canUsePB in loadout)
        #L3 is stricter than pb shortcut thru G2
        ) #more?
))
L4 = LogicShortcut(lambda loadout: (
    (
        (belowShip in loadout) or
        (L2 in loadout)
        ) and
    (canUseBombs in loadout) and
    (SpaceJump in loadout) and
    (Missile in loadout) and
    (SpeedBooster in loadout)
))
escape = LogicShortcut(lambda loadout: (
    #all major items
    (Missile in loadout) and
    (Super in loadout) and
    (canUsePB in loadout) and
    (Grapple in loadout) and
    (Xray in loadout) and
    (Charge in loadout) and
    (Ice in loadout) and
    (Wave in loadout) and
    (Plasma in loadout) and
    (Varia in loadout) and
    (GravitySuit in loadout) and
    (Bombs in loadout) and
    (SpeedBooster in loadout) and
    (SpaceJump in loadout) and
    (Screw in loadout)
))



location_logic: LocationLogicType = {
    "Morph Ball": lambda loadout: (
        True
    ),
    "Retro Ceiling Energy Tank": lambda loadout: (
        True
    ),
    "White Wall Missile": lambda loadout: (
        (brinstar in loadout)
    ),
    "White Crag Chozo Energy Tank": lambda loadout: (
        (brinstar in loadout)
    ),
    "Alpha Missile": lambda loadout: (
        (brinstar in loadout)
    ),
    "Plasma Beam": lambda loadout: (
        (canUsePB in loadout) and
        (
            (SpeedBooster in loadout) or
            (Super in loadout) #Backdoor
            )
    ),
    "Retro White Climb Super": lambda loadout: (
        (SpeedBooster in loadout)
    ),
    "Charge Beam": lambda loadout: (
        (Morph in loadout) and
        (pinkDoor in loadout) and
        (Charge in loadout)
    ),
    "Retro White Climb Energy": lambda loadout: (
        (SpeedBooster in loadout)
    ),
    
    "Crater Missile": lambda loadout: (
        (SpeedBooster in loadout) or
        (
            (
                (canUseBombs in loadout) or
                (
                    (Screw in loadout) and
                    (Morph in loadout)
                    )
                ) and
            (SpaceJump in loadout) or
            (canIBJ in loadout)
            )
    ),
    "Early Super": lambda loadout: (
        (SpeedBooster in loadout) or
        (canIBJ in loadout)
    ),
    "Flooded Cavern Gate Super": lambda loadout: (
        (Super in loadout) and
        (
            (
                (brinstar in loadout) and
                (
                    (SpeedBooster in loadout) or
                    (canIBJ in loadout)
                    )
                ) or
            (canBreakBlocks in loadout)
            ) and
        (
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (HiJump in loadout) or
            (SpeedBooster in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "Early Super Energy": lambda loadout: (
        (SpeedBooster in loadout) or
        (canIBJ in loadout) or
        (
            (Morph in loadout) and
            (SpaceJump in loadout)
            ) or
        (
            (brinstar in loadout) and
            (pinkDoor in loadout) and
            (canUseBombs in loadout) and
            (Grapple in loadout)
            ) 
    ),
    "Gauntlet Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (SpeedBooster in loadout)
    ),
    "Bomb Torizo": lambda loadout: (
        (outsideBombs in loadout) and
        (canUseBombs in loadout)
    ),
    "Outside Bombs Missile": lambda loadout: (
        (outsideBombs in loadout) and
        (Morph in loadout) and #clip time
        (
            (SpeedBooster in loadout) or
            (canUseBombs in loadout)
            ) #must escape the area with bombs or speed
    ),
    "Varia Grapple Block Missile": lambda loadout: (
        (variaArea in loadout) and
        (Grapple in loadout) and
        (Morph in loadout)
    ),
    "White Lava Energy Tank": lambda loadout: (
        (brinstar in loadout) and
        (
            (
                (Varia in loadout) and
                (Energy in loadout)
                ) or
            (GravitySuit in loadout)
            )
    ),
    "Varia Suit": lambda loadout: (
        (variaArea in loadout) and
        (
            (SpaceJump in loadout) or
            (Grapple in loadout)
            )
    ),
    "Retro White Climb Missile": lambda loadout: (
        (pinkDoor in loadout) and
        (
            (canUsePB in loadout)
            ) ##or speed? other ways?
    ),
    "Brinstar Basement Energy Tank": lambda loadout: (
        (brinstar in loadout) and
        (
            (canUseBombs in loadout) or
            (
                (canBreakBlocks in loadout) and
                (pinkDoor in loadout)
                )
            )
    ),
    "Beetom Spark Top Missile": lambda loadout: (
        (SpeedBooster in loadout) or
        (
            (canUseBombs in loadout) and
            (
                (SpaceJump in loadout) or
                (canIBJ in loadout)
                )
            )
    ),
    "Beetom Spark Bottom Missile": lambda loadout: (
        (canUseBombs in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (Super in loadout) or
            (
                (Grapple in loadout) and
                (pinkDoor in loadout)
                )
            ) #chozo ruins logic
    ),
    "Retro Yellow Missile": lambda loadout: (
        (variaArea in loadout)
    ),
    "Etecoons": lambda loadout: (
        (canUsePB in loadout) and
        (pinkDoor in loadout)
    ),
    "Kraid Reserve Tank": lambda loadout: (
        (kraidEntry in loadout) and
        (Morph in loadout)
    ),
    "Kraid Reserve Super": lambda loadout: (
        (kraidEntry in loadout) and
        (Morph in loadout) and
        (SpeedBooster in loadout)
    ),
    "Spore Spawn Super": lambda loadout: (
        (kraidEntry in loadout) and
        (
            (canIBJ in loadout) or
            (SpaceJump in loadout) or
            (HiJump in loadout) or
            (Grapple in loadout) #need to get up to the orb
            ) and
        (
            (   #secret save entry
                (Super in loadout) and
                (canUseBombs in loadout)
                ) or
            #traditional entry
            (kraidTrigger in loadout) or
            #eagle entry
            (kraidEagle in loadout)
            )   
    ),
    "Kraid Eagle Missile": lambda loadout: (
        (kraidEagle in loadout)
    ),
    "Norfair Top Grapple Missile": lambda loadout: (
        (Grapple in loadout) and
        (
            (pinkDoor in loadout) or
            (canUseBombs in loadout)
            ) and
        (
            (SpeedBooster in loadout) or
            (canUseBombs in loadout) or
            (
                (Super in loadout) and
                (SpaceJump in loadout)
                )
            )
    ),
    "Mini Kraid Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (
            (Super in loadout) or
            (Plasma in loadout)
            ) and
        (
            (Super in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Grapple Beam": lambda loadout: (
        (Grapple in loadout) and
        (canUseBombs in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (
                (HiJump in loadout) and
                (Super in loadout)
                )
            ) 
    ),
    "Crater Power Bomb": lambda loadout: (
        (beatTourian in loadout)
    ),
    "Speed Super": lambda loadout: (
        (L1 in loadout)
    ),
    "Speed Booster": lambda loadout: (
        (L1 in loadout)
    ),
    "Back of Gauntlet Left Missile": lambda loadout: (
        (beatTourian in loadout)
    ),
    "Back of Gauntlet Right Missile": lambda loadout: (
        (beatTourian in loadout)
    ),
    "Kraid Lonely Missile": lambda loadout: (
        (kraidHub in loadout)
    ),
    "Kraid Inverted Chozo Missile": lambda loadout: (
        (kraidHub in loadout) and
        (SpeedBooster in loadout)
    ),
    "Kraid Lower Retro Pillar Missile": lambda loadout: (
        (kraidEntry in loadout)
    ),
    "Terminator": lambda loadout: (
        (beatTourian in loadout)
    ),
    "Kraid Green Hopper Super": lambda loadout: (
        (kraidHub in loadout)
    ),
    "Kraid Mockball Gate Energy Tank": lambda loadout: (
        (kraidHub in loadout)
    ),

    "All Bosses Missile": lambda loadout: (
        (escape in loadout)
    ),
    "Forget-Me-Not Missile": lambda loadout: (
        (canUsePB in loadout)
    ),
    "Kraid Spark Out Missile": lambda loadout: (
        (kraidHub in loadout) and
        (
            (SpeedBooster in loadout) or
            (
                (canUsePB in loadout) and
                (Super in loadout)
                )
            )
    ),
    "Kraid Upper Retro Pillar Missile": lambda loadout: (
        (kraidEntry in loadout)
    ),
    "White Lava Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (Varia in loadout) and
                (energy600 in loadout)
                )
            )
    ),
    "Kraid Right Shaft Energy Tank": lambda loadout: (
        (kraidEntry in loadout) and
        (
            (
                (SpeedBooster in loadout) and
                (canUsePB in loadout)
                ) or
            (
                (canUseBombs in loadout) and
                (Super in loadout)
                )
            )
    ),
    "Kraid Left Shaft Super": lambda loadout: (
        (Super in loadout) and
        (canUseBombs in loadout)
    ),
    "Kraid Pink Spark Wall Missile": lambda loadout: (
        (kraidEntry in loadout) and
        (canUseBombs in loadout) and
        (SpeedBooster in loadout)
    ),
    "Kraid Pillar Secret Super": lambda loadout: (
        (kraidHub in loadout)
    ),
    "Above Kraid Energy Tank": lambda loadout: (
        (Super in loadout) and
        (canUseBombs in loadout) and
        (SpaceJump in loadout)
    ),
    "LN Pink Multispark Super Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Pink Multispark Chozo Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Save Crumble Power Bomb": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Norfair Entrance Energy Tank": lambda loadout: (
        (canUseBombs in loadout) and
        (
            (
                (norfairMapHub in loadout) and
                (
                    (pinkDoor in loadout) or
                    (canUsePB in loadout) or
                    (SpeedBooster in loadout)
                    )
                ) or
            (
                (Super in loadout) and
                (
                    (energy200 in loadout) or
                    (Varia in loadout)
                    )
                )
            )
    ),
    "Crocomire Super": lambda loadout: (
        (SpeedBooster in loadout) or
        (
            (canUseBombs in loadout) and
            (Super in loadout)
            )
    ),
    "Norfair Lava Dive Missile": lambda loadout: (
        (lavaDive in loadout)
    ),
    "Norfair Top Power Bomb": lambda loadout: (
        (norfairMapHub in loadout) and
        (canUsePB in loadout)
    ),
    "Bubble Crumble Super": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "HiJump": lambda loadout: (
        (norfairEast in loadout) and
        (
            (SpeedBooster in loadout) or
            (Plasma in loadout)
            )
    ),
    "Norfair Big Cavern Super": lambda loadout: (
        (norfairCavern in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout)
            )
    ),
    "LN Pink Wall Speed Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Entry Spark Behind Super": lambda loadout: (
        (lowerNorfair in loadout) and
        (Wave in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Entry Spark Energy": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Norfair Above Lava Dive Missile": lambda loadout: (
        (
            (Grapple in loadout) and
            (
                (SpeedBooster in loadout) or
                ((SpaceJump in loadout) and (Super in loadout)) or
                ((HiJump in loadout) and (Super in loadout))
                )
            ) or
        (
            (norfairMapHub in loadout) and
            (canUseBombs in loadout)
            )
    ),
    "Norfair Lava Dive Power Bomb": lambda loadout: (
        (lavaDive in loadout)
    ),
    "Norfair Double Chozo Maze Super": lambda loadout: (
        (L1 in loadout) and
        (canUseBombs in loadout) and
        (norfairMapHub in loadout)
    ),
    "Norfair Background Maze Power Bomb": lambda loadout: (
        (norfairCavern in loadout) and
        (super10 in loadout) and
        (SpeedBooster in loadout)
    ),
    "Norfair Drapes Missile": lambda loadout: (
        (norfairCavern in loadout) and
        (Wave in loadout) and
        (Super in loadout)
    ),
    "Norfair Background Maze Missile": lambda loadout: (
        (norfairCavern in loadout) and
        (super10 in loadout) and
        (SpeedBooster in loadout)
    ),
    "Wave Beam": lambda loadout: (
        (norfairCavern in loadout) and
        (Wave in loadout) and
        (Super in loadout)
    ),
    "Kraid Speedball Super": lambda loadout: (
        (SpeedBooster in loadout) and
        (
            (L1 in loadout) or
            (lavaDive in loadout)
            )
    ),
    "Lava Dive Chozo Energy Tank": lambda loadout: (
        (lavaDive in loadout)
    ),
    "LN Entry Spark Pillar Missile": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Gold Torizo Power Bomb": lambda loadout: (
        (belowShip in loadout) and
        (SpaceJump in loadout) and
        (canUsePB in loadout) and
        (Charge in loadout)
    ),
    "LN Screw Spark Power Bomb": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout) and
        (canUsePB in loadout)
    ),
    "Donald Duck Maze Super": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Donald Duck Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Pink Chambers Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Green Multispark Energy Tank": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "LN Cage Super": lambda loadout: (
        (lowerNorfair in loadout) and
        (canUseBombs in loadout) #shot blocks?
    ),
    "LN Ten Spark Power Bomb": lambda loadout: (
        (lowerNorfair in loadout) and
        (canUsePB in loadout) and
        (SpeedBooster in loadout)
    ),

    "Retro Mockball Energy Tank": lambda loadout: (
        (variaArea in loadout) and
        (canUseBombs in loadout)
    ),
    "LN Circle Missile": lambda loadout: (
        (lowerNorfair in loadout) and
        (canUseBombs in loadout)
    ),
    "Screw Attack": lambda loadout: (
        (lowerNorfair in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout)
            )
    ),
    "Moat Chozo": lambda loadout: (
        (Morph in loadout) and
        (Super in loadout) and
        (
            (canUseBombs in loadout) or
            (SpeedBooster in loadout) or
            (SpaceJump in loadout)
            )
    ),
    "Tourian Upper Vent Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (SpeedBooster in loadout) and
        (Plasma in loadout)
    ),
    "Tourian Tiny Lava Power Bomb": lambda loadout: (
        (enterTourian in loadout) and
        (canUsePB in loadout) and
        (
            (energy300 in loadout) or
            (Varia in loadout)
            )
    ),
    "Tourian Backdoor X-Ray": lambda loadout: (
        (L3 in loadout) or
        (
            (enterTourian in loadout) and
            (canUsePB in loadout) and
            (
                (energy300 in loadout) or
                (Varia in loadout)
                )
            )
    ),
    "Tourian Backdoor Power Bomb": lambda loadout: (
        (L3 in loadout) or
        (
            (enterTourian in loadout) and
            (canUsePB in loadout) and
            (
                (energy300 in loadout) or
                (Varia in loadout)
                )
            )
    ),
    "Tourian Vent Energy Tank": lambda loadout: (
        (enterTourian in loadout) and
        (canUsePB in loadout) and
        (
            (energy300 in loadout) or
            (Varia in loadout)
            )
    ),
    "Tourian Vent Missile": lambda loadout: (
        (beatTourian in loadout) and
        (canUsePB in loadout) and
        (L3 in loadout)
    ),
    "Tourian Spark Super": lambda loadout: (
        (beatTourian in loadout) and
        (SpeedBooster in loadout)
    ),
    "Tourian Outside Spark Missile": lambda loadout: (
        (beatTourian in loadout)
    ),
    "Level 2 Energy Tank": lambda loadout: (
        (L2 in loadout)
    ),
    "Ship Hangar Power Bomb": lambda loadout: (
        (L2 in loadout) and
        (canUsePB in loadout)
    ),
    "Chozodia Extra Power Bomb": lambda loadout: (
        (L2 in loadout) and
        (canUsePB in loadout)
    ),
    "Outside Ship Lower Missile": lambda loadout: (
        (frontShip in loadout) and
        (SpeedBooster in loadout)
    ),
    "Ship Low Crumble Power Bomb": lambda loadout: (
        (belowShip in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Ship X-Ray Scope": lambda loadout: (
        (belowShip in loadout) and
        (
            (aboveShipStealth in loadout) or
            (Ice in loadout)
            ) and
        (L2 in loadout) and
        (SpeedBooster in loadout) and
        (canUsePB in loadout) and
        (pinkDoor in loadout) and
        (
            (Super in loadout) or
            (SpaceJump in loadout)
            ) #probably correct now
    ),
    "Ship Purple Low Super": lambda loadout: (
        (belowShip in loadout) and
        (
            (
                (L3 in loadout) and
                (canUseBombs in loadout)
                ) or
            (
                (canUseBombs in loadout) and
                (
                    (HiJump in loadout) or
                    (SpeedBooster in loadout) or
                    (SpaceJump in loadout) or
                    (Springball in loadout) or
                    (canIBJ in loadout)
                    ) and
                (
                    (Super in loadout) or
                    (SpeedBooster in loadout)
                    )
                )
            )
    ),
    "Dachora Escape Missile": lambda loadout: (
        (escape in loadout)
    ),
    "Outside Ship Hull Super": lambda loadout: (
        (aboveShip in loadout) and
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Outside Ship Middle Energy Tank": lambda loadout: (
        (aboveShip in loadout) and
        (SpeedBooster in loadout)
    ),
    "Outside Ship Vent Pirates Power Bomb": lambda loadout: (
        (aboveShip in loadout) and
        (canUsePB in loadout)
    ),
    "Ship Hello Supers Power Bomb": lambda loadout: (
        (aboveShip in loadout) and
        (SpeedBooster in loadout) and
        (super10 in loadout)
    ),
    "Ship Reserve Tank": lambda loadout: (
        (aboveShip in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout)
            ) and
        (canUsePB in loadout) and
        (
            (Wave in loadout) and
            (
                (Charge in loadout) or
                (Plasma in loadout)
                )
            )
    ),
    "Ship Reserve Super": lambda loadout: (
        (aboveShip in loadout) and
        (
            (SpeedBooster in loadout) or
            (SpaceJump in loadout)
            ) and
        (canUsePB in loadout)
    ),
    "Precious Power Bomb": lambda loadout: (
        (
            (L4 in loadout) or
            (
                (belowShip in loadout) and
                (canUsePB in loadout)
                ) or
            (
                (aboveShip in loadout) and
                (canUsePB in loadout)
                )
            ) and
        (SpeedBooster in loadout) and
        (SpaceJump in loadout) and
        (canBreakBlocks in loadout)
    ),
    "Ship Block Spark Energy Tank": lambda loadout: (
        (
            (L2 in loadout) or
            (
                (belowShip in loadout) and
                (canUsePB in loadout)
                )
            ) and
        (SpeedBooster in loadout) and
        (SpaceJump in loadout)
    ),
    "Chozodia Gate Pair Energy Tank": lambda loadout: (
        (belowShip in loadout) and
        (L2 in loadout) and #approx
        (SpeedBooster in loadout)
    ),
    "Chozodia Gate Pair Missile": lambda loadout: (
        (belowShip in loadout) and
        (L2 in loadout) and #approx
        (SpeedBooster in loadout) 
    ),
    "Botwoon Super": lambda loadout: (
        (belowShip in loadout) and
        (
            (
                (GravitySuit in loadout) and #need?
                (SpeedBooster in loadout)
                ) or
            (
                (Super in loadout) and
                (
                    (GravitySuit in loadout) or
                    (HiJump in loadout) #need?
                    )
                )
            )
    ),
    "Botwoon Power Bomb": lambda loadout: (
        (belowShip in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
            ) and
        (Charge in loadout)
    ),
    "Gravity Suit": lambda loadout: (
        (belowShip in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
            ) and
        (Charge in loadout) and
        (canUsePB in loadout) and
        (SpaceJump in loadout) and
        (Screw in loadout) and
        (Plasma in loadout)
    ),
    "Botwoon Energy Tank": lambda loadout: (
        (belowShip in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
            ) and
        (Charge in loadout)
    ),
    "Tourian Escape Energy Tank": lambda loadout: (
        (beatTourian in loadout)
    ),
    "LN Deep Spark Energy Tank": lambda loadout: (
        (lowerNorfair in loadout) and
        (SpeedBooster in loadout)
    ),
    "Tourian Challenge Missile": lambda loadout: (
        (L3 in loadout) and
        (missile15 in loadout) and
        (super10 in loadout) and
        (powerBomb11 in loadout) and
        (Xray in loadout) and
        (SpeedBooster in loadout) and
        (fullBeams in loadout)
    ),
    "Old Mother Brain Power Bomb": lambda loadout: (
        (beatTourian in loadout) and
        (SpeedBooster in loadout) and
        (canUsePB in loadout) #added just in case
        #possibly might not need PB too
    ),
    "Spikesuit Power Bomb": lambda loadout: (
        (norfairEast in loadout) and
        (Super in loadout) and
        (Varia in loadout) and
        (GravitySuit in loadout) and
        (energy300 in loadout) and
        (SpeedBooster in loadout)
    ),
    "Norfair Bubble Wrap Missile": lambda loadout: (
        (norfairEast in loadout)
    ),
    "Out of LN Energy Tank": lambda loadout: (
        (lowerNorfair in loadout) or
        (
            (norfairEast in loadout) and
            (Super in loadout) and
            (
                (Springball in loadout) or
                (
                    (SpeedBooster in loadout) and
                    (canUsePB in loadout)
                    )
                )
            )
    ),
    "Spring Ball Wall Power Bomb": lambda loadout: (
        (norfairCavern in loadout) and
        (canUsePB in loadout) and
        (SpeedBooster in loadout)
    ),
    "Spring Ball": lambda loadout: (
        (norfairCavern in loadout) and
        (
            (Wave in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Crateria Reserve Tank": lambda loadout: (
        (Morph in loadout) and
        (
            (canIBJ in loadout) or
            (SpaceJump in loadout) or
            (SpeedBooster in loadout) or
            (
                (HiJump in loadout) and
                (Super in loadout)
                ) or
            (
                (canUseBombs in loadout) and
                (Grapple in loadout)
                )
            )
    ),
    "Norfair Wood Chozo Energy Tank": lambda loadout: (
        (norfairEast in loadout)
    ),
    "Norfair Wood Chozo Super Missile": lambda loadout: (
        (norfairEast in loadout) and
        (Super in loadout)
    ),
    "Retro Basement Bomb Missile": lambda loadout: (
        (pinkDoor in loadout) and
        (canUseBombs in loadout)
    ),
    "Space Jump": lambda loadout: (
        (Super in loadout) and
        (
            (kraidHub in loadout) or
            (canUsePB in loadout)
            )
    ),
    "Flappy Bird Missile": lambda loadout: (
        (belowShip in loadout) and
        (L2 in loadout) and #approx
        (SpeedBooster in loadout) and
        (SpaceJump in loadout)
    ),
    "Spazer Right Missile": lambda loadout: (
        (kraidEagle in loadout) and
        (Super in loadout) and
        (canUseBombs in loadout)
    ),
    "Spazer Left Missile": lambda loadout: (
        (kraidEagle in loadout) and
        (Super in loadout) and
        (canUseBombs in loadout)
    ),
    "Spazer": lambda loadout: (
        (kraidEagle in loadout) and
        (Super in loadout) and
        (canUseBombs in loadout)
    ),
    "Ice Beam": lambda loadout: (
        (norfairEast in loadout)
    ),
    "Norfair Double Pillar Pink Missile": lambda loadout: (
        (norfairCavern in loadout) and
        (
            (Super in loadout) or
            (
                (SpeedBooster in loadout) and
                (GravitySuit in loadout) and
                (Wave in loadout)
                )
            ) #might be simpler than this
    ),
    "Chozodia Green Vent Energy Tank": lambda loadout: (
        (L2 in loadout) and
        (Super in loadout)
    ),
    "Outside Ship Tube Super": lambda loadout: (
        (belowShip in loadout) and
        (canUsePB in loadout)
    ),

    "Billy Mays Missile": lambda loadout: (
        (SpeedBooster in loadout)
    ),
    "Kraid Left Shaft Energy Tank": lambda loadout: (
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Ridley Energy Tank": lambda loadout: (
        (
            (lowerNorfair in loadout) and
            (Charge in loadout)
            ) or
        (L2 in loadout)
    ),
    "LN Chain Hang Missile": lambda loadout: (
        (lowerNorfair in loadout)
    ),
    "Speed Robots Power Bomb": lambda loadout: (
        (belowShip in loadout) and
        (GravitySuit in loadout) and
        (SpeedBooster in loadout) and
        (canUsePB in loadout) and
        (Plasma in loadout)
    ),
    "Security Missile": lambda loadout: (
        (L2 in loadout) and
        (L3 in loadout) and
        (L4 in loadout) and
        (SpeedBooster in loadout) #maybe this is right
    ),
    "Norfair Reserve": lambda loadout: (
        (norfairCavern in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout)
        #basically LN without varia requirement
    ),

}


class Default(LogicInterface):
    location_logic: ClassVar[LocationLogicType] = location_logic
