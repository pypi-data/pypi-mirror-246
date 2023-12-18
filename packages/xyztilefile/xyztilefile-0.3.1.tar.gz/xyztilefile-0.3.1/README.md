# xyztilefile

### Samples
#### Basic usage sample.
```Python
from xyztilefile import *
xyz = calc_xyz_from_lonlat

x, y, z = calc_xyz_from_lonlat(135.0,35.0,15)

test_txt = XYZTileFile("./tile_sample/{z}/{x}/{y}.txt")
txt = test_txt.get(*xyz(135.0,35.0,15))
test_txt.set(x,y,z,txt+"\nNew line is added")
test_txt.save(x,y,z)
```

#### Usage sample of XYZTileManager
```Python
from xyztilefile import *
xyz = calc_xyz_from_lonlat

test_json = XYZTileManager("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.json", "./tile_sample2/{z}/{x}/{y}.json")
data = test_json.get(*xyz(135.0,35.0,15))
```
XYZTileManager first check the locally saved cache which is the second argument. If such local file is missing, then XYZTileManager will try to retrieve data from the online source which is the first argument.



please check './test/' for more sample codes

### currently supported file formats
- txt : encoding must be UTF-8 
- json : encoding must be UTF-8
- png : with skit-image (tested with `./test/test_png.py`)
- npy : with numpy (tested with `./test/test_npy.py`)

- (generic : this format is basic but your customization is needed.)
