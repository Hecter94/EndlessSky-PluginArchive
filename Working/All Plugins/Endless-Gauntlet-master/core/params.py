# params.py
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



from .ESParserPy.getSources import GetConfigPath, GetGamePath

import os



class Params(object):
	def __init__(self, rootPath, uID, dataNode):
		self.rootPath = rootPath
		self.uID = uID
		defaultGamePath = GetGamePath()
		self.gamePath = defaultGamePath
		
		
		defaultPath = GetConfigPath()
		self.usePlugins = False
		self.pluginPath = (os.path.join(defaultPath, "plugins") if defaultPath else "")
		self.doBackup = False
		self.savesPath = (os.path.join(defaultPath, "saves") if defaultPath else "")
		
		self.galaxySize = 0
		self.checkpoints = 0
		self.minPoint = 0
		self.maxPoint = 0
		
		self.frequency = 0
		
		self.fleetSize = 0
		self.sizeVariance = 0
		
		self.categoryWeights = {}
		self.tierWeights = {}
		
		self.excludeShips = []
		
		self.Load(dataNode)
		
		
	def Load(self, dataNode):
		for node in dataNode.Begin():
			key = node.Token(0)
			if key == "paths":
				for child in node.Begin():
					childKey = child.Token(0)
					childSize = child.Size()
					if childKey == "game path":
						if childSize >= 2 and child.Token(1):
							self.gamePath = os.path.normpath(child.Token(1))
					elif childKey == "use plugins" and childSize >= 2:
						self.usePlugins = (True if child.Value(1) else False)
						if self.usePlugins:
							for grand in child.Begin():
								if grand.Token(0) == "plugin path":
									if grand.Size() >= 2 and grand.Token(1):
										self.pluginPath = os.path.normpath(grand.Token(1))
					elif childKey == "make backup" and childSize >= 2:
						self.doBackup = (True if child.Value(1) else False)
						if self.doBackup:
							for grand in child.Begin():
								if grand.Token(0) == "saves path":
									if grand.Size() >= 2 and grand.Token(1):
										self.savesPath = os.path.normpath(grand.Token(1))
			elif key == "galaxy":
				for child in node.Begin():
					childKey = child.Token(0)
					childSize = child.Size()
					if childKey == "size" and childSize >= 2:
						self.galaxySize = child.Value(1)
					elif childKey == "checkpoints" and childSize >= 2:
						self.checkpoints = child.Value(1)
					elif childKey == "min" and childSize >= 2:
						self.minPoint = child.Value(1)
					elif childKey == "max" and childSize >= 2:
						self.maxPoint = child.Value(1)
					elif childKey == "healthpack frequency" and childSize >= 2:
						self.frequency = child.Value(1)
			elif key == "fleets":
				for child in node.Begin():
					childKey = child.Token(0)
					childSize = child.Size()
					if childKey == "size" and childSize >= 2:
						self.fleetSize = child.Value(1)
					elif childKey == "variance" and childSize >= 2:
						self.sizeVariance = child.Value(1)
			elif key == "weights":
				for child in node.Begin():
					if child.Token(0) == "category":
						for grand in child.Begin():
							if grand.Size() >= 2:
								self.categoryWeights[grand.Token(0)] = grand.Value(1)
					elif child.Token(0) == "tier":
						for grand in child.Begin():
							if grand.Size() >= 2:
								self.tierWeights[grand.Value(0)] = grand.Value(1)
			elif key == "ships":
				for child in node.Begin():
					if child.Token(0) == "exclude":
						for grand in child.Begin():
							self.excludeShips.append(grand.Token(0))
			elif key == "seed":
				if node.Size() >= 2 and node.Token(1):
					self.uID = node.Value(1)
			else:
				node.PrintTrace("Skipping unrecognized parameter: ")
				
