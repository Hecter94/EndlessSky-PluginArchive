from endless_sky.datafile import DataFile
from endless_sky.datanode import DataNode
from pathlib import Path
from os import environ

p = Path(__file__).parent.parent / Path("data/")
p.mkdir(mode=0o775, parents=True, exist_ok=True)

systems = {}
systemCategories = {}

SYSTEMF = """
system \"{name}\"
	pos {x} {y}

""".lstrip('\n')

root = DataFile((Path(environ["ENDLESS_SKY_PATH"]) / Path("data/map.txt")).expanduser()).root

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
	if set(attr) & {"deep"}:
		systemCategories[i.tokens[1]] = "deep"

with open(p / Path("shifted systems.txt"), "w") as f:
	for k, (x, y) in systems.items():
		if systemCategories.get(k) == "deep":
			x -= 50
			f.write(SYSTEMF.format(name=k, x=x, y=y))
		
