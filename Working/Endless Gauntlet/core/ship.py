# ship.py
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



class Ship(object):
	tierLookup = {
		"Heavy Warship": (45000, 180000, 540000, 1080000),
		"Medium Warship": (15000, 75000, 300000, 900000),
		"Light Warship": (8500, 45000, 170000, 510000),
		"Interceptor": (4500, 18000, 45000, 90000),
		"Fighter": (1500, 4500, 14000, 42000),
		"Drone": (1500, 4500, 14000, 42000),
		"Heavy Freighter": (12000, 75000, 300000, 600000),
		"Light Freighter": (4200, 18000, 28000, 84000),
		"Transport": (7500, 23000, 57000, 140000)}
		
		
	def __init__(self, dataNode):
		self.modelName = dataNode.Token(1)
		
		self.variantName = ""
		if dataNode.Size() > 2:
			self.variantName = dataNode.Token(2)
			
		self.hp = 0
		self.fighters = 0
		self.drones = 0
		self.category = ""
		self.tier = 0
		self.cost = 0.
		for node in dataNode.BeginFlat():
			key = node.Token(0)
			size = node.Size()
			if key == "category" and size >= 2:
				self.category = node.Token(1)
			elif key == "shields" and size >= 2:
				self.hp += node.Value(1)
			elif key == "hull" and size >= 2:
				self.hp += node.Value(1)
			elif key == "fighter":
				self.fighters += 1
			elif key == "drone":
				self.drones += 1
				
				
	def SetTier(self):
		if self.hp <= Ship.tierLookup[self.category][0]:
			self.tier = 1
		elif self.hp <= Ship.tierLookup[self.category][1]:
			self.tier = 2
		elif self.hp <= Ship.tierLookup[self.category][2]:
			self.tier = 3
		elif self.hp <= Ship.tierLookup[self.category][3]:
			self.tier = 4
		else:
			self.tier = 5
			
			
	def GetBase(self, baseShip):
		if not self.hp:
			self.hp = baseShip.hp
		if not self.fighters:
			self.fighters = baseShip.fighters
		if not self.drones:
			self.drones = baseShip.drones
		if not self.category:
			self.category = baseShip.category
			
			
