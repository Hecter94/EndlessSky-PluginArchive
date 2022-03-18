# gameData.py
# Copyright (C) 2018 Frederick W. Goy IV
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



from .ship import Ship



class GameData(object):
	def __init__(self, params, files):
		self.ships = {}
		self.fighters = {}
		self.drones = {}
		self.ammo = []
		
		self.Load(params, files)
		
		
	def Load(self, params, files):
		variants = []
		for file in files:
			path = file.root.Token(1)
			if not file or params.rootPath in path or "deprecated" in path:
				continue
				
			for node in file.Begin():
				if node.Token(0) == "ship" and node.Size() >= 2:
					ship = Ship(node)
					if ship.variantName:
						variants.append(ship)
					else:
						self.ships[ship.modelName] = ship
				elif node.Token(0) == "outfit" and node.Size() >= 2:
					isAmmo = False
					hasAmmo = False
					for child in node.BeginFlat():
						if child.Token(0) == "category" and child.Size() >= 2:
							if child.Token(1) == "Ammunition":
								isAmmo = True
						elif child.Token(0) == "ammo":
							hasAmmo = True
					if isAmmo and not hasAmmo:
						self.ammo.append(node.Token(1))
							
		for variant in variants:
			variant.GetBase(self.ships[variant.modelName])
			self.ships[variant.variantName] = variant
			
		for key in list(self.ships):
			ship = self.ships[key]
			if not ship.category or key in params.excludeShips:
				self.ships.pop(key)
				continue
			ship.SetTier()
			
			weight = params.categoryWeights[ship.category]
			tWeight = params.tierWeights[ship.tier]
			if not weight or not tWeight:
				self.ships.pop(key)
				continue
			ship.cost = weight + tWeight
			
			if ship.category == "Fighter":
				self.fighters[key] = self.ships.pop(key)
			elif ship.category == "Drone":
				self.drones[key] = self.ships.pop(key)
				
				
