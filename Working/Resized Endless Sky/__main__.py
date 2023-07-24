from endless_sky.datafile import DataFile
from endless_sky.datanode import DataNode
from pathlib import Path
import math
from typing import Tuple
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

point = Point(0.5, 0.5)

p = Path("~/.local/share/endless-sky/plugins/resized-endless-sky/data/").expanduser()
p.mkdir(mode=0o775, parents=True, exist_ok=True)

def pol2cart(phi: float, radius: float) -> Tuple[float, float]:
	return math.cos(phi) * radius, math.sin(phi) * radius
	
def cart2pol(x: float, y: float) -> Tuple[float, float]:
	return math.atan2(y, x), math.sqrt(x ** 2 + y ** 2)
	

systems = {}
systemCategories = {}

def is_inside_polygon(system_polygon, point: Point):
	return Polygon([systems[i] for i in system_polygon]).covers(point)

def rotate_around(system1, system2, phi):
	phi2, radius = cart2pol(systems[system1][0] - systems[system2][0], systems[system1][1] - systems[system2][1])
	phi2 += phi
	x, y = pol2cart(phi2, radius)
	x += systems[system2][0]
	y += systems[system2][1]
	systems[system1] = x, y

SYSTEMF = """
system \"{name}\"
	pos {x} {y}

""".lstrip('\n')

root = DataFile(Path("~/misc/endless-sky-dev/data/map.txt").expanduser()).root

for i in root.filter_first("system"):
	pos = list(float(j) for j in next(i.filter_first("pos")).tokens[1:])
	systems[i.tokens[1]] = pos
	gov = list(i.filter_first("government"))
	attr = list(i.filter_first("attributes"))
	if attr:
		attr = attr[0].tokens[1:]
	else:
		attr = []
	if gov:
		gov = gov[0].tokens[1]
	else:
		gov = ""
	
	if set(attr) & {"kimek", "saryd", "arachi", "ringworld"} or i.tokens[1] in ("Last Word", "Companion"):
		systemCategories[i.tokens[1]] = "coalition"
	if gov == "Hai" or i.tokens[1] == "Hevru Hai":
		systemCategories[i.tokens[1]] = "hai"
	if gov == "Hai (Unfettered)":
		systemCategories[i.tokens[1]] = "unfettered"
	if gov == "Wanderer" or gov == "Pug (Wanderer)":
		systemCategories[i.tokens[1]] = "wanderer"
	if gov == "Korath":
		print("aa")
		systemCategories[i.tokens[1]] = "exile"
	if gov == "Kor Sestor" or i.tokens[1] in ("Host", "Persitar"):
		systemCategories[i.tokens[1]] = "sestor"
		
for i in root.filter_first("system"):
	pos = systems[i.tokens[1]]
	if (not systemCategories.get(i.tokens[1])) and is_inside_polygon(["Celeborim", "Solifar", "Chikatip", "Sevrelect", "Hesselpost", "Kasikfar", "Fasitopfar", "Sayaiban", "Faronektu", "Host"],
		Point(*pos)):
		systemCategories[i.tokens[1]] = "korath"
	if i.tokens[1] == "Dokdobaru":
		systemCategories[i.tokens[1]] = "korath"
		
	if is_inside_polygon(["Terminus", "Limen", "Orbona"],
		Point(*pos)):
		systemCategories[i.tokens[1]] = "terminus-area"
	if is_inside_polygon(["Umbral", "Tarazed", "Sadr", "Nunki", "Han", "Antares", "Graffias", "Kappa Centauri", "Men", "Yed Prior", "Aldhibain", "Wei", "Ascella", "Peacock", "Enif", "Sadalmelik", "Sadalsuud"],
		Point(*pos)):
		systemCategories[i.tokens[1]] = "south"
	if is_inside_polygon(["Algol", "Schedar", "Almach", "Polaris", "Hamal"],
		Point(*pos)):
		systemCategories[i.tokens[1]] = "syndicate-core"
		
for name, pos in systems.items():
	if systemCategories.get(name) == "south":
		rotate_around(name, "Rastaban", 0.5)
	if systemCategories.get(name) == "coalition":
		rotate_around(name, "Quaru", 0.3)
	if systemCategories.get(name) == "terminus-area":
		rotate_around(name, "Limen", math.pi * 1.5)
	if systemCategories.get(name) == "sestor":
		rotate_around(name, "Salipastart", math.pi / 2 + 0.1)

	

systems["Sagittarius A*"][1] -= 0

minv = 100
maxv = -100

with open(p / Path("map.txt"), "w") as f:
	f.write('''
galaxy "mw"
	sprite milkyway_dark4
	pos 5000 5000
''')
	for k, v in systems.items():
		phi, radius = cart2pol(v[0] - systems["Sagittarius A*"][0], v[1] - systems["Sagittarius A*"][1])
		phi += math.pi * 2
		phi = phi % (math.pi * 2)
		pphi = phi
		phi = phi / 2
		#print(pphi, phi)
		radius /= 200
		radius = radius ** 0.7
		radius *= 500
		if systemCategories.get(k) == "coalition":
			radius -= 200
			phi += 0.4
		if systemCategories.get(k) == "south":
			radius += 100
			phi -= 0.05
		if systemCategories.get(k) == "terminus-area":
			radius += 50
			phi -= 0.05
		if systemCategories.get(k) == "wanderer":
			radius += 300
			phi += 0.05
		if systemCategories.get(k) == "exile":
			radius -= 200
			radius *= 2
		if systemCategories.get(k) == "syndicate-core":
			radius -= 50
		if k == "Wah Ti":
			pass
		if k == "Achernar":
			radius += 50
		if k == "Hintar":
			phi -= 0.1
		if k == "Boral":
			phi -= 0.02
			radius -= 50
		if k == "Kor Nor'peli":
			radius -= 50
			phi -= 0.05
			
		maxv = max(phi, maxv)
		minv = min(phi, minv)
		phi = -phi
		phi -= math.pi / 4
		x, y = pol2cart(phi, radius)
		x += 5000
		y += 5000
		f.write(SYSTEMF.format(name=k, x=x, y=y))
	
	f.write('''
system Ankaa
	remove link Ruchbah
	link Alpheratz
system Ruchbah
	remove link Ankaa
system Mirach
	remove link Schedar
system Schedar
	remove link Mirach
system Achernar
	link "Alpha Hydri"
system Algol
	link Menkar
system Boral
	link Alphecca
	link "Kaus Borealis"
	link "Cebalrai"
	link "Hintar"
system Hintar
	link Boral
	link Ascella
	link "Zeta Aquilae"
	link Rasalhague
system Ascella
	remove link "Zeta Aquilae"
	remove link Rasalhague
system "Zeta Aquilae"
	remove link Ascella
system Rasalhague
	remove link "Ascella"
system "Cebalrai"
	remove link "Kaus Borealis"
system "Kaus Borealis"
	remove link "Cebalrai"
''')
	
print(maxv, minv)

	