from endless_sky.datafile import DataFile
import common

f = DataFile("data/map.txt")

system_pname, system_names, system_pos, system_queue = dict(), dict(), dict(), dict()

for i in f.root.filter_first("system"):
	if len(i.tokens) <= 1:
		break
	name = i.tokens[1]
	pos = [float(j) for j in list(i.filter_first("pos"))[-1].tokens[1:]]
	system_names[tuple(pos)] = name
	system_pos[name] = tuple(pos)
	system_pname[name] = " ".join(list(i.filter_first("pos"))[-1].tokens)
	system_queue[name] = list()
	
def distance(p1, p2):
	return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

with open("data/map.txt") as f:
	s = f.read()

from json import load	

	
for pos, name in system_names.items():
	links = [system_names[i] for i in sorted(
		system_pos.values()
	, key=lambda i: distance(pos, i))[:4]]
	links = list(filter(lambda i: name != i and i.strip(), links))
	s = s.replace(f"pos {pos[0]} {pos[1]}", 
		f"pos {pos[0]} {pos[1]}\n\t" 
			+ '\n\t'.join([
				f"link \"{i}\"" for i in links
			])
		)
	for i in links:
		s = s.replace(f"{system_pname[i]}", 
			f"{system_pname[i]}\n\tlink \"{name}\""
			)

s = (s
	.replace('\n\tlink\n', '\n')
	.replace('\n\tlink \n', '\n')
	.replace('\n\tlink ""\n', '\n'))

with open("data/map.txt", "w") as f:
	f.write(s)