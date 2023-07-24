from endless_sky.datafile import DataFile

# 10362 9612 ->  197700  250500 (0)
# 10830 8829 ->  197985 249959 (23.31222308) 

from common import transform_latitude
import common

celestia_x1 = 10362
celestia_y1 = 9612
auto_x1 = 197700
auto_y1 = 250500

celestia_x2 = 10830
celestia_y2 = 8829
auto_x2 = 197985
auto_y2 = 249959

# How much we will need to multiply Celestia's coordinates by to get our coordinates
scale_x = (auto_x1 - auto_x2) / (celestia_x1 - celestia_x2)
scale_y = ((auto_y1 - auto_y2) / (celestia_y1 - celestia_y2)) * 1

# How much we'll have to add afterwards
offset_x = auto_x1 - scale_x * celestia_x1  
offset_y = auto_y1 - scale_x * celestia_y1- 800

print(scale_x, offset_x, scale_y, offset_y)

def adjust_latitude(y):
	return (y - common.offy) + common.offy

def transform_point(x, y):
	return x * scale_x + offset_x, adjust_latitude(y * scale_y + offset_y)

path = "old map files/celestia_map_subtracted.txt"

positions = []

for system in DataFile(path).root.filter_first("system"):
	for pos in system.filter_first("pos"):
		positions.append((pos.tokens[1], pos.tokens[2]))
	

with open(path, "r") as f:
	contents = f.read()
	
for x, y in positions:
	nx, ny = transform_point(float(x), float(y))
	contents = contents.replace(f'pos {x} {y}', f'pos {nx} {ny}')

with open(path + ".translated.txt", "w") as f:
	f.write(contents)
	
