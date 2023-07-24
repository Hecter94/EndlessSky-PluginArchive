import json
import math
from urllib.request import urlopen
from math import radians, copysign
from sys import stderr
from common import mercator_y_transform
import common
from common import transform_latitude

url_sys = "http://1.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/4/{z}/{x}/{y}.grid.json"

url_hyp = "http://2.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/3/{z}/{x}/{y}.grid.json"


systems = {}
hyper = {}


try:
	with open("systems.json") as f:
		systems = json.load(f)
	
	with open("hyper.json") as f:
		hyper = json.load(f)
		
except FileNotFoundError:
	# Reload cache
	for z in range(5,6):
		stderr.write(f"Z: {z}\n")
		for x in range(z ** 2 + 5):
			for y in range(z ** 2 * 2):
				for k in (
					(systems, url_sys),
				):
					d, urlf = k
					for f in (
						urlf.format(z=z, x=x, y=y),
						#"""
						#urlf.format(x=x, y=1, z=y),
						#urlf.format(x=y, y=1, z=x),
						#urlf.format(x=x, z=1, y=y),
						#urlf.format(x=y, z=1, y=x),
						#"""
					):
						data = {}
						try:
							data = json.load(urlopen(f))
						except:
							pass
							
							
						if data.get("data") is None:
							stderr.write(str(data))
						else:
							for k, v in data["data"].items():
								d[v["cartodb_id"]] = v
					stderr.write(f"{x} {y}\n")
					stderr.flush()

with open("systems.json", "w") as f:
	json.dump(systems, f)
	
with open("hyper.json", "w") as f:
	json.dump(hyper, f)
print(len(systems))		
			
from pprint import pprint

FORMATSTRING = '''
system "{name}"
	government "Uninhabited"
	habitable 600
	belt 1500
	pos {x} {y}
	object "{name}"
		sprite planet/cloud6
		distance 500
		period 180

planet "{name}"
	government "Uninhabited"
	description "{name}_DESC"
	spaceport "{name}_SPACEPORT"
'''



for i in systems.values():
	if i.get("long") is None:
		stderr.write(str(i) + "\n")
		continue
	print(FORMATSTRING.format(
		x = i["long"] * common.scale_x + common.offx,
		y = transform_latitude(i["lat"]),
		name = i["name"],
		
	))
