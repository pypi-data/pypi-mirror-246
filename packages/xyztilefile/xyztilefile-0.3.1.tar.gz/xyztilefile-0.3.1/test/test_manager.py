from xyztilefile import *
import pprint
from datetime import  datetime

pp = pprint.PrettyPrinter(indent=3)

pp.pprint(calc_xyz_from_lonlat(135.0,35.0,15))
xyz = calc_xyz_from_lonlat

print()
print("Testing Tile Manager")
test_json = XYZTileManager("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.json", "./tile_sample2/{z}/{x}/{y}.json")
pp.pprint(test_json)
data = test_json.get(*xyz(135.0,35.0,15))
pp.pprint(data)
pp.pprint(test_json)
