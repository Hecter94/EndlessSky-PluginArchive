from endless_sky.datafile import DataFile

systems = []
links = []

for system in DataFile("data/map.txt").root.filter_first("system"):
	systems.append(system.tokens[1])
	links += [i.tokens[1] for i in system.filter_first("link")]

sl = list(set(links) - set(systems))

with open("data/map.txt") as f:
	contents = f.read()
	
for i in sl:
	contents = contents.replace(f"\tlink {i}\n", "")
	contents = contents.replace(f"\tlink \"{i}\"\n", "")

with open("data/map.txt", "w") as f:
	f.write(contents)