# Needs inkscape in PATH to work properly
import re
import subprocess
import common
import math
import xml.etree.ElementTree as ET

INKSCAPE_QUERYALL_REGEXP = r"(?P<name>[^,]*),(?P<x>[^,]*),(?P<y>[^,]*),(?P<w>[^,]*),(?P<h>[^,]*)\n"

S = subprocess.check_output(['inkscape', '-S', 'dev_images/galaxy_dev.svg']).decode('utf-8')

HEIGHT = None
WIDTH = None

GALAXYF = '''galaxy "{name}"
	pos {x} {y}
	sprite "{sprite}"
'''

tree = ET.parse('dev_images/galaxy_dev.svg')

for name, x, y, width, height in re.findall(INKSCAPE_QUERYALL_REGEXP, S):
	x, y, width, height = float(x), float(y), float(width), float(height)
	if name.startswith("svg"):
		WIDTH, HEIGHT = width, height
		
	if name.startswith("text"):
		innerText = None
		id = name[4:]
		for i in tree.getroot().iter():
			if i.attrib.get("id") == name:
				innerText = "".join(i.itertext())
		
		imw = (common.size_x / WIDTH) * width
		imh = (common.size_y / HEIGHT) * height
				
		nx = (x / WIDTH) * common.size_x + common.top_left_x + imw / 2
		ny = (y / HEIGHT) * common.size_y + common.top_left_y + imh / 2
		
		path = f'images/galaxy images/{innerText} {id}.png'
		subprocess.check_output(["inkscape", "dev_images/galaxy_dev.svg", 
			f"-i={name}",
			f"-j",
			f"--export-png={path}",
			f"--export-width={imw}"
			f"--export-height={imh}"])
		
		print(GALAXYF.format(
			name = f"{innerText} {id}",
			x = nx, 
			y = ny,
			sprite=path[len("images/"):-len(".png")]))
	



