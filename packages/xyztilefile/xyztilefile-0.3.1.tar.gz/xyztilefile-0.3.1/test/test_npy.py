import pprint
import numpy as np
from xyztilefile import *

pp = pprint.PrettyPrinter(indent=3)

x, y, z = calc_xyz_from_lonlat(135.0,35.0,15)
xyz = calc_xyz_from_lonlat

ar = np.arange(12).reshape((4,3))
print("Initial")
test = XYZTileFile("./tile_sample/{z}/{x}/{y}.npy")
pp.pprint(test)

print()
print("Set array")
test.set(x,y,z,ar)
pp.pprint(test)

print()
print("Save & clear cache")
test.save(x,y,z)
test.clc()
pp.pprint(test)

print()
print("Load the saved array")
ar2 = test.get(*xyz(135.0,35.0,15))
pp.pprint(ar2)
pp.pprint(test)

print()
print("Testing HTTP npy")
test_http = XYZTileFile("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.npy")
ar3 = test_http.get(*xyz(135.0,35.0,15))
pp.pprint(ar3)
#ar3[0,0] = 100
pp.pprint(test_http)
