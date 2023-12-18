import pprint
import matplotlib.pyplot as plt
import numpy as np
from xyztilefile import *

pp = pprint.PrettyPrinter(indent=3)

x, y, z = calc_xyz_from_lonlat(135.0,35.0,15)
xyz = calc_xyz_from_lonlat

print("Initial")
test = XYZTileFile("./tile_sample/{z}/{x}/{y}.png")
pp.pprint(test)

print()
print("Load the saved image")
img = test.get(*xyz(135.0,35.0,15))
pp.pprint(img)
pp.pprint(test)
print(np.shape(img))
fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("loaded image")
plt.show()

print()
print("Set array")
img[0:100,-101:-1,:] = [np.random.randint(255), np.random.randint(255), np.random.randint(255), 255]
test.set(x,y,z,img)
pp.pprint(test)

fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("set image")
plt.show()

print()
print("Save & clear cache")
test.save(x,y,z)
test.clc()
pp.pprint(test)

print()
print("Load the saved image")
img = test.get(*xyz(135.0,35.0,15))
pp.pprint(img)
pp.pprint(test)

fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("saved & reloaded image")
plt.show()

print()
print("Testing HTTP PNG")
test_http = XYZTileFile("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.png")
img = test_http.get(*xyz(135.0,35.0,15))
pp.pprint(img)
pp.pprint(test_http)

fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("reloaded online image")
plt.show()
