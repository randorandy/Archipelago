import csv
import logging
import pathlib
import pkgutil
from typing import Optional, TypedDict, cast

from .item import Item


class Location(TypedDict):
    index: int
    roomname: str
    region: str
    vanillaitemname: str
    roomid: int
    locationid: int
    hiddenness: str
    altlocationids: list[int]
    item: Optional[Item]
    inlogic: bool


def pullCSV() -> dict[str, Location]:
    csvdict: dict[str, Location] = {}

    def comment_filter(line: str) -> bool:
        return (line[0] != '#')

    path = pathlib.Path(__file__).parent.resolve() ##OLD
    # with open(path.joinpath("cliff.csv"), 'r') as csvfile: ##OLD
    #  csvfile = pkgutil.get_data("hack_randomizer", "cliff.csv") TEMP
    csv_bytes = pkgutil.get_data(__package__, "cliff.csv") #
    if csv_bytes is None:
        logging.warning("`pkgutil.get_data` unable to read location data")
        # if pkgutil is unable to find it, try reading from file system
        path = pathlib.Path(__file__).parent.resolve()
        
        # rusty removed this option since it's open()
        #with open(path.joinpath('cliff.csv'), 'r') as file:
        #    csv_lines = file.readlines()
        csv_lines = "0,0,0,0,0,0,0,0" #hopefully this never happens
    else:
        csv_lines = csv_bytes.decode().splitlines()

    reader = csv.DictReader(filter(comment_filter, csv_lines))
    # reader = csv.DictReader(filter(commentfilter, csvfile)) TEMP
    for row in reader:
        row['altlocationids'] = row['altlocationids'].split(',')
        row["index"] = int(row['index'])
        row["roomid"] = int(row["roomid"], 16)
        row["locationid"] = int(row["locationid"], 16)
        row['altlocationids'] = [
            int(locstr, 16) for locstr in row['altlocationids'] if locstr != '']
        row['item'] = None
        row['inlogic'] = False
        csvdict[row["roomname"]] = cast(Location, row)
    return csvdict

