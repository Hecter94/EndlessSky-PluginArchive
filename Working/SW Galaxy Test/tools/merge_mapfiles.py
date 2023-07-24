import argparse
from endless_sky.datafile import DataFile
from re import sub

parser = argparse.ArgumentParser()

parser.add_argument("locations")
parser.add_argument("links")

args = parser.parse_args()

links = {}

for i in DataFile(args.links).root.filter_first("system"):
	links[i.tokens[1]] = []
	for j in i.filter_first("link"):
		links[i.tokens[1]].append(j.tokens[1])
	
from pprint import pprint

with open(args.locations) as f:
	contents = f.read()
	
contents = sub(r"\tlink .+\n", "", contents)

with open(args.locations + ".linkless.txt", "w") as f:
	f.write(contents)
	
systems = []	
	
for i in DataFile(args.links).root.filter_first("system"):
	systems.append(i.tokens[1])
	
for i in systems:
	if not links.get(i):
		continue
	for j in links[i]:
		contents = contents.replace(f'system "{i}"', f'system "{i}"\n\tlink "{j}"')
		contents = contents.replace(f'system {i}\n', f'system {i}\n\tlink "{j}"\n')
		
with open(args.locations + ".merged.txt", "w") as f:
	f.write(contents)
	
	