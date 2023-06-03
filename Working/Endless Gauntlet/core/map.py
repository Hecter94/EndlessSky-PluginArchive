# map.py
# Copyright (C) 2017 Frederick W. Goy IV
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



from .ESParserPy.dataNode import DataNode

import math
import random


asteroidNames = ['small metal', 'small rock', 'medium metal', 'medium rock', 
		'large metal', 'large rock']
		
stars = ['a0', 'a5', 'b5', 'f0', 'f5', 'g0', 'g5', 'k0', 'k5', 'm0', 'm4', 'm8']
		
def Map(params):
	print("Building map...")
	offsets = GetOffsets(params.galaxySize)
	points = GetCheckpoints(params)
	root = DataNode()
	for i in range(params.galaxySize):
		system = DataNode(tokens=["system", "VR System {}".format(i)])
		
		x = 20000 - offsets[i][0]
		y = 14000 - offsets[i][1]
		system.Append(DataNode(tokens=["pos", str(int(x)), str(int(y))]))
		system.Append(DataNode(tokens=["government", "Bounty"]))
		
		if i == 0:
			system.Append(DataNode(tokens=["link", "VR System 1"]))
		elif i == (params.galaxySize - 1):
			system.Append(DataNode(tokens=["link", "VR System {}".format(i - 1)]))
		else:
			system.Append(DataNode(tokens=["link", "VR System {}".format(i - 1)]))
			system.Append(DataNode(tokens=["link", "VR System {}".format(i + 1)]))
			
		asteroids = random.randint(0, 6)
		if asteroids:
			for j in random.sample(asteroidNames, asteroids):
				tokens = ["asteroids", str(j)]
				tokens.append(str(int(abs(random.gauss(1, 30)) + 1)))
				tokens.append("{:.4f}".format(random.uniform(1, 10)))
				system.Append(DataNode(tokens=tokens))
				
		system.Append(DataNode(tokens=["fleet", "healthpacks", str(params.frequency)]))
		
		star = "star/" + random.choice(stars)
		object = DataNode(tokens=["object"])
		system.Append(object)
		object.Append(DataNode(tokens=["sprite", star]))
		object.Append(DataNode(tokens=["period", "10"]))
		if i in points:
				name = "Checkpoint {}".format(points.index(i))
				checkpoint = DataNode(tokens=["object", name])
				system.Append(checkpoint)
				checkpoint.Append(DataNode(tokens=["sprite", "planet/digitalplanet"]))
				checkpoint.Append(DataNode(tokens=["distance", "960"]))
				checkpoint.Append(DataNode(tokens=["period", "450"]))
		if i == 0:
			wormhole = DataNode(tokens=["object", "The Gauntlet"])
			system.Append(wormhole)
			wormhole.Append(DataNode(tokens=["sprite", "planet/wormhole"]))
			wormhole.Append(DataNode(tokens=["distance", "540"]))
			wormhole.Append(DataNode(tokens=["period", "206"]))
			
		root.Append(system)
		
	if points:
		for i in range(len(points)):
			remaining = len(points) - (i + 1)
			planet = DataNode(tokens=["planet", "Checkpoint {}".format(i)])
			root.Append(planet)
			planet.Append(DataNode(tokens=["attributes", "gauntlet"]))
			planet.Append(DataNode(tokens=["landscape", "land/gauntlet"]))
			
			description = ("You have reached checkpoint {}. ".format(i + 1) +
				"There are {} checkpoints remaining.".format(remaining))
			planet.Append(DataNode(tokens=["description", description]))
			
			spaceport = "The spaceport here is empty."
			planet.Append(DataNode(tokens=["spaceport", spaceport]))
			planet.Append(DataNode(tokens=["outfitter", "Gauntlet Ammo"]))
			
	return root
	
	
def GetOffsets(galaxySize):
	offsets = []
	for i in range(galaxySize):
		angle = 0.25 * i
		x = (220 * angle) * math.cos(angle)
		y = (220 * angle) * math.sin(angle)
		
		offsets.append([x, y])
		
	return offsets
	
	
def GetCheckpoints(params):
	maxRange = min(10, params.maxPoint)
	minRange = min((maxRange - 1), max(1, params.minPoint))
	total = min(params.checkpoints, (maxRange - minRange))
	end = params.galaxySize - (params.galaxySize % 10)
	points = []
	if total:
		for i in range(0, end, 10):
			valid = range(minRange + i, maxRange + i)
			points += random.sample(valid, total)
			
	return sorted(points)
	
	
