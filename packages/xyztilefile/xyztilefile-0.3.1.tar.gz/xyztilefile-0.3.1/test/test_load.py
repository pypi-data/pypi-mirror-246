from xyztilefile import *
import pprint
from datetime import  datetime

pp = pprint.PrettyPrinter(indent=3)

pp.pprint(calc_xyz_from_lonlat(135.0,35.0,15))
x, y, z = calc_xyz_from_lonlat(135.0,35.0,15)

test= XYZTileFile("./test/{z}/{x}/{y}.png")
pp.pprint(test)

test_http = XYZTileFile("http://localhost:8080/tile/{z}/{x}/{y}.png")
pp.pprint(test_http)
try:
    pp.pprint(test_http.save())
except NotImplementedError as e:
    print(f"NotImplementedError is detected as expected: {e}")
#test_http.get(x,y,z)


test_sample = XYZTileFile("./tile/{z}/{x}/{y}.xyzsample")
pp.pprint(test_sample)
try:
    data = test_sample.get(x,y,z)
except OSError as e:
    print(f"OSError is detected as expected: {e}")

try:
    test_error = XYZTileFile(None)
except TypeError as e:
    print(f"TypeError is detected as expected: {e}")

try:
    test_error = XYZTileFile("http://google.com")
except ValueError as e:
    print(f"ValueError is detected as expected: {e}")


xyz = calc_xyz_from_lonlat

test_txt = XYZTileFile("./tile_sample/{z}/{x}/{y}.txt")
pp.pprint(test_txt)
txt = test_txt.get(*xyz(135.0,35.0,15))
pp.pprint(txt)
pp.pprint(test_txt.set(x,y,z,txt))#+"\nNew line is added"))
pp.pprint(test_txt.save(x,y,z))


test_json = XYZTileFile("./tile_sample/{z}/{x}/{y}.json")
pp.pprint(test_json)
data = test_json.get(*xyz(135.0,35.0,15))
pp.pprint(data)
data.append({"id":3, "txt":f"new line as {datetime.now()}"})
pp.pprint(test_json.set(x-1,y,z,data))
pp.pprint(test_json.save_all())


print()
print("Testing HTTP Text")
test_httptxt = XYZTileFile("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.txt")
pp.pprint(test_httptxt)
txt = test_httptxt.get(*xyz(135.0,35.0,15))
pp.pprint(txt)
print(txt)
pp.pprint(test_httptxt)

try:
    txt = test_httptxt.get(*xyz(0,0,15))
except OSError as e:
    print(f"OSError is detected as expected: {e}")

print()
print("Testing HTTP JSON")
test_httpjson = XYZTileFile("https://raw.githubusercontent.com/aDAVISk/xyztilefile/dev/tile_sample/{z}/{x}/{y}.json")
pp.pprint(test_json)
data = test_json.get(*xyz(135.0,35.0,15))
pp.pprint(data)
