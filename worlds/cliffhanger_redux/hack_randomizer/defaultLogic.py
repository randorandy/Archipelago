from typing import ClassVar

from .item import items_unpackable
from .logicInterface import LocationLogicType, LogicInterface
from .logic_shortcut import LogicShortcut

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    GravitySuit, Varia, Wave, SpeedBooster, Spazer, Ice, Grapple,
    Plasma, Screw, Charge, SpaceJump, Energy, Reserve, Xray
) = items_unpackable

energy200 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 1
))

energy300 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 2
))
energy400 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 3
))
energy500 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 4
))
energy600 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 5
))
energy700 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 6
))
energy800 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 7
))
energy900 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 8
))
energy1000 = LogicShortcut(lambda loadout: (
    loadout.count(Energy) >= 9
))
energy1200 = LogicShortcut(lambda loadout: (
    loadout.count(Energy)  >= 11
))
energy1500 = LogicShortcut(lambda loadout: (
    loadout.count(Energy)  >= 14
))


hellrun1 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy200 in loadout)
))
hellrun2 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy300 in loadout)
))
hellrun3 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy400 in loadout)
))
hellrun4 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy500 in loadout)
))
hellrun5 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy600 in loadout)
))
hellrun6 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy700 in loadout)
))
hellrun8 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy900 in loadout)
))
hellrun9 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy1000 in loadout)
))
hellrun11 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy1200 in loadout)
))
hellrun14 = LogicShortcut(lambda loadout: (
    (Varia in loadout) or
    (energy1500 in loadout)
))

missile10 = LogicShortcut(lambda loadout: (
    loadout.count(Missile) * 5 >= 10
))
missile15 = LogicShortcut(lambda loadout: (
    loadout.count(Missile) * 5 >= 15
))
super10 = LogicShortcut(lambda loadout: (
    loadout.count(Super) * 5 >= 10
))
super30 = LogicShortcut(lambda loadout: (
    loadout.count(Super) * 5 >= 30
))
powerBomb10 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(PowerBomb) >= 2
))
powerBomb15 = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    loadout.count(PowerBomb) >= 3
))
canCF = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (loadout.count(PowerBomb) >= 3) and
    (super10 in loadout) and
    (missile10 in loadout)
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
pinkDoor = LogicShortcut(lambda loadout: (
    (Missile in loadout) or
    (Super in loadout)
))
redTower = LogicShortcut(lambda loadout: (
    (canUseBombs in loadout) and
    (pinkDoor in loadout)
    #consider: you always have an easy way out of red tower thru billy with
    # IBJ or PB doing the museum
    # plus, the museum is a PB farm
))
blueTower = LogicShortcut(lambda loadout: (
    (redTower in loadout) and
    (
        (Ice in loadout) or
        (SpaceJump in loadout) or
        (Springball in loadout) or
        (
            (
                (Super in loadout) or
                (canUsePB in loadout) or
                (Screw in loadout)
                ) and
            (canIBJ in loadout)
            ) or
        (   #reserve route
            (canUsePB in loadout) and
            (SpeedBooster in loadout) and
            (
                (Plasma in loadout) or
                (Screw in loadout)
                )
            )
        )
))
moat = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (
        (Grapple in loadout) or
        (GravitySuit in loadout) or
        (SpaceJump in loadout) #to get across
        ) and
    (
        (Wave in loadout) or
        (SpeedBooster in loadout) #gate
        ) and
    (
        (canUseBombs in loadout) or
        (SpeedBooster in loadout) #crater block
        )
))
wsEntry = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (SpeedBooster in loadout) and
    (Grapple in loadout) and
    (Missile in loadout) and
    (canUseBombs in loadout)
))
phantoon = LogicShortcut(lambda loadout: (
    (Super in loadout) and
    (Missile in loadout) and
    (
        (wsEntry in loadout) or
        (
            (wsBack in loadout) and
            (Xray in loadout)
            )
        )
))
brin = LogicShortcut(lambda loadout: (
    (SpeedBooster in loadout) and
    (
        (canIBJ in loadout) or
        (Springball in loadout) or
        (powerBomb10 in loadout)
        ) and
    (energy300 in loadout) and
    (
        (Grapple in loadout) or #zigzag escape
        (
            (   #plasma escape
                (Springball in loadout) or
                (GravitySuit in loadout)
                ) and
            (
                (Plasma in loadout) or
                (Screw in loadout)
                )
            )
        )
))
warehouse = LogicShortcut(lambda loadout: (
    (blueTower in loadout) and
    (SpeedBooster in loadout)
    #bombs included in redTower
))
upperNorfair = LogicShortcut(lambda loadout: (
    (blueTower in loadout) and
    (Super in loadout)
))
croc = LogicShortcut(lambda loadout: (
    (upperNorfair in loadout) and #this implies some bombs
    (
        (
            (castle in loadout) and
            (hellrun6 in loadout)
            ) or
        (canUsePB in loadout)
        )and
    (
        (SpaceJump in loadout) or
        (Grapple in loadout) or
        (canIBJ in loadout) or
        (HiJump in loadout)
        )
))
wsBack = LogicShortcut(lambda loadout: (
    (   #phantoon route
        (wsEntry in loadout) and
        (Super in loadout)
        #which includes speed
        ) or
    (   #gray warehouse route
        (redTower in loadout) and
        (Super in loadout) and
        (
            (Wave in loadout) or
            (Ice in loadout)
            ) and
        (SpeedBooster in loadout)
        ) #can always get up red tower thru billy mays+canbomb
))
castle = LogicShortcut(lambda loadout: (
    (upperNorfair in loadout) and
    (SpeedBooster in loadout) and
    (
        (canUsePB in loadout) or
        (Super in loadout)
        ) and
    (
        (canUsePB in loadout) or
        (Wave in loadout)
        ) and
    (hellrun3 in loadout)
))
botwoon = LogicShortcut(lambda loadout: (
    (redTower in loadout) and
    (Super in loadout) and #red tower green door
    (canUsePB in loadout) and #break the tube
    (
        (canIBJ in loadout) or
        (HiJump in loadout) or
        (SpaceJump in loadout) or
        (GravitySuit in loadout) #get up the gray warehouse
        ) and 
    (   #Get up to botwoon's door
        (Grapple in loadout) or
        (GravitySuit in loadout) or
        (
            (HiJump in loadout) and
            (Springball in loadout)
            )
        )
))
bull = LogicShortcut(lambda loadout: (
    (redTower in loadout) and
    (Super in loadout) and #red tower green door
    (canUsePB in loadout) and #break the tube
    (
        (canIBJ in loadout) or
        (HiJump in loadout) or
        (SpaceJump in loadout) or
        (GravitySuit in loadout) #get up the gray warehouse
        ) and
    (Wave in loadout) and
    (Grapple in loadout) and
    (
        (Springball in loadout) or
        (GravitySuit in loadout)
        )
))

gt = LogicShortcut(lambda loadout: (
    (wsBack in loadout) and
    (canUsePB in loadout) and
    (GravitySuit in loadout) and
    (Super in loadout) and
    (energy600 in loadout)
))
ln = LogicShortcut(lambda loadout: (
    (
        (wsBack in loadout) and
        (Springball in loadout)
        ) or
    (
        (castle in loadout) and
        (gt in loadout)
        ) #must add hellrun requirements per item
))
ridley = LogicShortcut(lambda loadout: (
    (ln in loadout) and
    (canUsePB in loadout) and
    (hellrun9 in loadout) and
    (energy400 in loadout) and
    (
        (
            (Varia in loadout) and
            (Charge in loadout)
            ) or
        (super30 in loadout)
        )
))
kraid = LogicShortcut(lambda loadout: (
    (warehouse in loadout) and
        (pinkDoor in loadout) and
        (
            (Wave in loadout) or
            (canIBJ in loadout) #blue gate morph tunnel
            ) and
        (
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (Ice in loadout) or
            (SpeedBooster in loadout)
            )
))
draygon = LogicShortcut(lambda loadout: (
    (bull in loadout) and
    (GravitySuit in loadout) and
    (energy400 in loadout) and
    (
        (Grapple in loadout) or
        (Charge in loadout)
    )
))


location_logic: LocationLogicType = {
    "Alpha Missile": lambda loadout: (
        (Morph in loadout)
    ),
    "Baby Kraid Missile": lambda loadout: (
        (brin in loadout)
    ),
    "Back Lab Super Missile": lambda loadout: (
        (wsBack in loadout) and
        (Springball in loadout) and
        (
            (HiJump in loadout) or
            (SpaceJump in loadout) or
            (GravitySuit in loadout) or
            (canIBJ in loadout)
            ) #not sure about IBJ
    ),
    "Beyond Bull Prize Energy Tank": lambda loadout: (
        (bull in loadout) and
        (Plasma in loadout)
    ),
    "Big Pink Energy Tank": lambda loadout: (
        (brin in loadout)
    ),
    "Billy Mays Missile": lambda loadout: (
        (Morph in loadout) and
        (pinkDoor in loadout)
    ),
    "Billy Maze Super Energy Tank": lambda loadout: (
        (Morph in loadout) and
        (Super in loadout)
    ),
    "Blue Heads Power Bomb": lambda loadout: (
        (redTower in loadout) and
        (canUsePB in loadout)
    ),
    "Blue Tower Power Bomb": lambda loadout: (
        (warehouse in loadout) and
        (canUsePB in loadout) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Bombs": lambda loadout: (
        (Morph in loadout)
    ),
    "Botwoon Hallway Mid Missile": lambda loadout: (
        (bull in loadout) 
    ),
    "Botwoon Hallway Right Missile": lambda loadout: (
        (bull in loadout)
    ),
    "Botwoon Hallway Top Missile": lambda loadout: (
        (redTower in loadout) and
        (Super in loadout) and #red tower green door
        (canUsePB in loadout) and #break the tube
        (
            (canIBJ in loadout) or
            (HiJump in loadout) or
            (SpaceJump in loadout) or
            (GravitySuit in loadout) #get up the gray warehouse
            )
    ),
    "Bowling Energy Tank": lambda loadout: (
        (phantoon in loadout) or
        (
            (wsBack in loadout) and
            (Xray in loadout)
            ) or
        (
            (warehouse in loadout) and
            (canUsePB in loadout)
            ) #alt location left of Dray
    ),
    "Bowling Missile": lambda loadout: (
        (wsBack in loadout)
    ),
    "Brin Map Super Missile": lambda loadout: (
        (brin in loadout) and
        (Super in loadout)
    ),
    "Brin Northeast Speed Super Missile": lambda loadout: (
        (redTower in loadout) and
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (
            (canIBJ in loadout) or
            (HiJump in loadout) or
            (SpaceJump in loadout)
            )
    ),
    "Brinstar Entry Missile": lambda loadout: (
        (brin in loadout)
    ),
    "Brinstar Reserve Redux Super": lambda loadout: (
        (redTower in loadout) and
        (SpeedBooster in loadout) and
        (
            (canIBJ in loadout) or
            (HiJump in loadout) or
            (SpaceJump in loadout)
            )
    ),
    "Bull Arena Missile": lambda loadout: (
        (bull in loadout)
    ),
    "Bull Hidden Missile": lambda loadout: (
        (botwoon in loadout) and
        (Wave in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            ) #hopefully right?
    ),    
    "Castle Store Missile 1": lambda loadout: (
        (castle in loadout) and
        (SpeedBooster in loadout)
    ),
    "Castle Store Missile 3": lambda loadout: (
        (castle in loadout) and
        (SpeedBooster in loadout)
    ),
    "Castle Store Missile 4": lambda loadout: (
        (castle in loadout) and
        (SpeedBooster in loadout)
    ),
    "Castle Store Missile 2": lambda loadout: (
        (castle in loadout) and
        (SpeedBooster in loadout)
    ),
    "Cathedral Kago Missile": lambda loadout: (
        (blueTower in loadout) and
        (hellrun3 in loadout)
    ),
    "Charge Beam": lambda loadout: (
        (redTower in loadout)
    ),
    "Climb Experiments Power Bomb": lambda loadout: (
        (canUsePB in loadout) and
        (GravitySuit in loadout)
    ),
    "Climb Missile": lambda loadout: (
        (Morph in loadout) and
        (
            (canBreakBlocks in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Construction Zone Missile": lambda loadout: (
        (SpeedBooster in loadout)
    ),
    "Conveyor Super Missile": lambda loadout: (
        (wsBack in loadout) and
        (Springball in loadout)
    ),
    "Covern Ceiling Missile": lambda loadout: (
        (
            (wsBack in loadout) and
            (Springball in loadout)
            ) or
        (
            (castle in loadout) and
            (hellrun9 in loadout) and
            (
                (GravitySuit in loadout) or
                (canUseBombs in loadout) or
                (Springball in loadout)
                ) and
            (
                (Springball in loadout) or
                (canIBJ in loadout) or
                (SpaceJump in loadout) or
                (HiJump in loadout)
                )
            ) #route from below
    ),
    "Crat-Red Elevator Missile": lambda loadout: (
        (canUsePB in loadout) and
        (pinkDoor in loadout)
    ),
    "Crater Missile": lambda loadout: (
        (Super in loadout) and
        (SpeedBooster in loadout)
    ),
    "Crater Xray": lambda loadout: (
        (Super in loadout) and
        (SpeedBooster in loadout) and
        (Morph in loadout) and
        (
            (Wave in loadout) or
            (Ice in loadout)
            ) and
        (Springball in loadout)
    ),
    "Crateria Kihunters Missile": lambda loadout: (
        (canUsePB in loadout)
    ),
    "Croc Power Bomb": lambda loadout: (
        (croc in loadout) and
        (SpeedBooster in loadout)
    ),
    "Crumble Ocean Super Missile": lambda loadout: (
        (wsBack in loadout) and
        (Springball in loadout)
    ),
    "Dragon Bones Energy Tank": lambda loadout: (
        (ln in loadout) and
        (canUsePB in loadout) and
        (hellrun9 in loadout)
    ),
    "Dragon Pipes Super Missile": lambda loadout: (
        (castle in loadout) and
        (hellrun9 in loadout)
    ),
    "Early Hedron Power Bomb": lambda loadout: (
        (brin in loadout) and
        (canUsePB in loadout)
    ),
    "Evir Exit Power Bomb": lambda loadout: (
        (phantoon in loadout) and
        (Super in loadout) and
        (canUsePB in loadout)
    ),
    "G4 Missile": lambda loadout: (
        (moat in loadout) and
        (canBreakBlocks in loadout) and
        (SpeedBooster in loadout)
    ),
    "Gauntlet Power Bomb": lambda loadout: (
        (canUseBombs in loadout) and
        (Wave in loadout) and
        (SpeedBooster in loadout)
    ),
    "Grapple Beam": lambda loadout: (
        (
            (brin in loadout) and
            (Grapple in loadout) #front door
            ) or
        (
            (redTower in loadout) and
            (canUsePB in loadout) and
            (
                (Springball in loadout) or
                (GravitySuit in loadout)
                ) #back door
            )
    ),
    "Grapple Gladiator Energy Tank": lambda loadout: (
        (castle in loadout) and
        (hellrun11 in loadout) and
        (
            (GravitySuit in loadout) or
            (canUseBombs in loadout) or
            (Springball in loadout)
            ) #match covern missile
        
    ),
    "Gravity Suit": lambda loadout: (
        (gt in loadout)
    ),
    "Green Brin Sky Missile": lambda loadout: (
        (brin in loadout) and
        (
            (SpaceJump in loadout) or
            (Grapple in loadout)
            )
    ),
    "GT Power Bomb": lambda loadout: (
        (gt in loadout)
    ),
    "Hangman Robot Missile": lambda loadout: (
        (wsBack in loadout) and
        (Springball in loadout) and
        (SpeedBooster in loadout) and
        (pinkDoor in loadout)
    ),
    "HiJump": lambda loadout: (
        (bull in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "HiJump Missile": lambda loadout: (
        (bull in loadout) and
        (
            (HiJump in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "Ice Beam": lambda loadout: (
        (warehouse in loadout) and
        (pinkDoor in loadout) and
        (
            (Wave in loadout) or
            (canIBJ in loadout) #blue gate morph tunnel
            ) and
        (
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (Ice in loadout) or
            (SpeedBooster in loadout)
            )
    ),
    "Jabba Missile": lambda loadout: (
        (bull in loadout)
    ),
    "King Smurf Missile": lambda loadout: (
        (brin in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            ) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            ) #matches Plasma logic
    ),
    "Kraid Energy Tank": lambda loadout: (
        (blueTower in loadout) and
        (SpeedBooster in loadout)
    ),
    "Lava Monster Energy Tank": lambda loadout: (
        (croc in loadout) and
        (SpeedBooster in loadout) and
        (
            (Grapple in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (
                (HiJump in loadout) and
                (Springball in loadout)
                )
            ) 
    ),
    "Leaf Bypass Missile": lambda loadout: (
        (redTower in loadout) and
        (canUsePB in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "LN Elevator Missile": lambda loadout: (
        (ln in loadout) and
        (hellrun3 in loadout)
    ),
    "Mama Turtle Energy Tank": lambda loadout: (
        (wsBack in loadout) and
        (canUsePB in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout)
            )
    ),
    "Mama Turtle Missile": lambda loadout: (
        (wsBack in loadout) and
        (canUsePB in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout)
            )
    ),
    "Moat Missile": lambda loadout: (
        (Morph in loadout) and
        (
            (SpeedBooster in loadout) or
            (Wave in loadout)
            ) and
        (
            (canUseBombs in loadout) or
            (SpeedBooster in loadout)
            ) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (Grapple in loadout) or
            (SpaceJump in loadout)
            )
    ),
    "Mohawk Energy Tank": lambda loadout: (
        (redTower in loadout) and
        (Super in loadout) and #red tower to blue heads green door
        (canUsePB in loadout) and #break the tube
        (
            (canIBJ in loadout) or
            (HiJump in loadout) or
            (SpaceJump in loadout) or
            (GravitySuit in loadout) #get up the gray warehouse
            )
    ),
    "Morph Ball": lambda loadout: (
        True
    ),
    "Morph Ball Redux": lambda loadout: (
        (Morph in loadout)
    ),
    "Museum Energy Tank": lambda loadout: (
        (redTower in loadout) and
        (canUsePB in loadout) and
        (Super in loadout)
    ),
    "Museum Super Ceiling Missile": lambda loadout: (
        (redTower in loadout) and
        (Super in loadout)
    ),
    "Ninja Power Bomb": lambda loadout: (
        (wsBack in loadout) and
        (canUsePB in loadout) and
        (
            (GravitySuit in loadout) or
            (HiJump in loadout) or
            (Springball in loadout)
            )
    ),
    "Orb Fall Missile": lambda loadout: (
        (croc in loadout) and
        (
            (Grapple in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (
                (HiJump in loadout) and
                (Springball in loadout)
                )
            ) and
        (
            (Ice in loadout) or
            (SpaceJump in loadout) or
            (canIBJ in loadout) or
            (
                (HiJump in loadout) and
                (Springball in loadout)
                )
            )
    ),
    "Parlor Low Missile": lambda loadout: (
        (canUseBombs in loadout)
    ),    
    "Phantoon Super Missile": lambda loadout: (
        (phantoon in loadout)
    ),
    "Pink Pillar Missile": lambda loadout: (
        (brin in loadout)
    ),
    "Plasma Beam": lambda loadout: (
        (brin in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            ) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Post Gladiator Missile": lambda loadout: (
        (ln in loadout) and
        (hellrun4 in loadout)
    ),
    "Red Pool Energy Tank": lambda loadout: (
        (blueTower in loadout)
    ),
    "Reserve Tank 4": lambda loadout: (
        (warehouse in loadout) and
        (canUsePB in loadout) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Reserve Tank 2": lambda loadout: (
        (warehouse in loadout) and
        (canUsePB in loadout) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Reserve Tank 1": lambda loadout: (
        (warehouse in loadout) and
        (canUsePB in loadout) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Reserve Tank 3": lambda loadout: (
        (warehouse in loadout) and
        (canUsePB in loadout) and
        (
            (Plasma in loadout) or
            (Screw in loadout)
            )
    ),
    "Screw Attack": lambda loadout: (
        (blueTower in loadout) and
        (canUsePB in loadout) and
        (super10 in loadout) and
        (
            (GravitySuit in loadout) or
            (
                (HiJump in loadout) and
                (Springball in loadout)
                )
            )
    ),
    "Space Jump": lambda loadout: (
        (Morph in loadout) and
        (pinkDoor in loadout) and
        (Wave in loadout) and
        (Grapple in loadout) and
        (SpeedBooster in loadout) and
        (canUseBombs in loadout)
    ),
    "Spazer": lambda loadout: (
        (moat in loadout) and
        (pinkDoor in loadout)
    ),    
    "Spazer Eye Missile": lambda loadout: (
        (moat in loadout) and
        (pinkDoor in loadout) and
        (SpeedBooster in loadout) and
        (HiJump in loadout)
    ),
    "Speed Booster": lambda loadout: (
        (blueTower in loadout) and
        (hellrun2 in loadout) and
        (SpeedBooster in loadout)
    ),
    "Speed Missile": lambda loadout: (
        (blueTower in loadout) and
        (hellrun2 in loadout) and
        (canUsePB in loadout)
    ),
    "Speedkeep Flower Missile": lambda loadout: (
        (brin in loadout)
    ),
    "Springball": lambda loadout: (
        (botwoon in loadout) and
        (Charge in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "Springball Missile": lambda loadout: (
        (botwoon in loadout) and
        (Charge in loadout) and
        (
            (Springball in loadout) or
            (GravitySuit in loadout)
            )
    ),
    "Steam Super Missile": lambda loadout: (
        (castle in loadout) and
        (hellrun6 in loadout)
    ),
    "Sub Cathedral Energy Tank": lambda loadout: (
        (ridley in loadout) and
        (
            (Reserve in loadout) or
            (Springball in loadout)
            )
    ),
    "Tripper Missile": lambda loadout: (
        (upperNorfair in loadout) and
        (hellrun2 in loadout)
    ),
    "Under Lava Missile": lambda loadout: (
        (ln in loadout) and
        (GravitySuit in loadout) and
        (hellrun8 in loadout) #could tweak?
    ),
    "Under Lava Power Bomb": lambda loadout: (
        (ln in loadout) and
        (GravitySuit in loadout) and
        (hellrun8 in loadout) #could tweak? match above
    ),
    "Varia Missile": lambda loadout: (
        (phantoon in loadout) and
        (wsBack in loadout)
    ),
    "Varia Suit": lambda loadout: (
        (wsBack in loadout)
    ),
    "Wave Beam": lambda loadout: (
        (ridley in loadout)
    ),
    "WS Entry Energy Tank": lambda loadout: (
        (phantoon in loadout) and
        (
            (Springball in loadout) or
            (
                (Ice in loadout) and
                (Xray in loadout)
                ) #possible to ice clip upwards to collect
            )
    ),
    "WS Fish Tank Missile": lambda loadout: (
        (
            (wsEntry in loadout) and
            (Super in loadout)
            ) or
        (
            (redTower in loadout) and
            (Super in loadout) and
            (
                (Wave in loadout) or
                (Ice in loadout) #gate glitch
                ) and
            (
                (canIBJ in loadout) or
                (HiJump in loadout) or
                (SpaceJump in loadout) or
                (GravitySuit in loadout) #get up the gray warehouse
                ) and
            (
                (HiJump in loadout) or
                (GravitySuit in loadout) or
                (SpeedBooster in loadout) or
                (Ice in loadout) #get up fish tank wall
                )
            ) 
    ),
    "WS Kaizo Pillar Missile": lambda loadout: (
        (wsBack in loadout)
    ),
    "Zigzag Super Missile": lambda loadout: (
        (brin in loadout) and
        (Grapple in loadout)
    ),

}


class Default(LogicInterface):
    location_logic: ClassVar[LocationLogicType] = location_logic
