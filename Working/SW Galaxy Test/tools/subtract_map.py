import argparse
from endless_sky.datafile import DataFile
from re import sub

parser = argparse.ArgumentParser()

parser.add_argument("base")
parser.add_argument("subtract")

args = parser.parse_args()

subtract = []

with open(args.base, "r") as f:
	contents = f.read()

for i in DataFile(args.subtract).root.filter_first("system"):
	subtract.append(i.tokens[1])
	
for i in subtract:
	contents = sub(fr'system "{i}"\n(\t.+\n)+', "", contents)
	contents = sub(fr'system {i}\n(\t.+\n)+', "", contents)
	
with open(args.base + ".subtracted.txt", "w") as f:
	f.write(contents)