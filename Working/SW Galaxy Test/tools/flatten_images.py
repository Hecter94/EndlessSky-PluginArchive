import glob
from os import system
import re
	
def get_index(i):
	m = re.match(r"images/ui/sw_sectors_(?P<x>[0-9]+)_(?P<y>[0-9]+).png", i)
	return int(m.group("y")) * 1000 + int(m.group("x"))
		

l = glob.glob("images/ui/sw_sectors_*.png")

l.sort(key = lambda i:get_index(i))	

for i in l:
	m = re.match(r"images/ui/sw_sectors_(?P<id>[0-9_]+).png", i)
	print(m.group('id'))
	dest = f"{'images/ui/' + 'sw_full_' + m.group('id') + '.png'}"
	sector =  f"{'images/ui/' + 'sw_sectors_' + m.group('id') + '.png'}"
	hyperlanes =  f"{'images/ui/' + 'sw_hyperlanes_' + m.group('id') + '.png'}"
	system(f"convert -composite images/ui/bg.png {sector} {dest}")
	system(f"convert -composite {dest} {hyperlanes} {dest}")
