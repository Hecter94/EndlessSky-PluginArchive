from endless_sky.datafile import DataFile

f = DataFile("data/map.txt")

for i in f.root.filter_first("system"):
	print("visited", "\"" + i.tokens[1] + "\"" )
for i in f.root.filter_first("planets"):
	print("visited planet", "\"" + i.tokens[1] + "\"" )