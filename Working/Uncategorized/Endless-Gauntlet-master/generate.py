# generate.py
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



from core.backup import Backup
from core.event import Event
from core.gameData import GameData
from core.map import Map
from core.mission import Mission
from core.params import Params
from core.sales import Sales

from core.ESParserPy.dataFile import DataFile
from core.ESParserPy.dataWriter import DataWriter
from core.ESParserPy.getSources import GetSources

import os
import random
import sys
import uuid



def OnFail(message):
	print(message)
	input("Press enter to abort.")
	sys.exit("Aborting...")
	
	
if __name__ == "__main__":
	if sys.version_info[0] < 3:
		message = ("This program requires version 3 of Python." +
			"\nVisit: https://www.python.org/downloads/")
		OnFail(message)
		
	thisDir = os.path.dirname(os.path.abspath(__file__))
	paramDir = os.path.join(thisDir, "params.txt")
	if not os.path.isfile(paramDir):
		OnFail("Cannot locate params.txt in " + paramDir)
		
	uID = uuid.uuid4().int
	paramsFile = DataFile(paramDir)
	params = Params(thisDir, uID, paramsFile.root)
	random.seed(params.uID)
	
	if not params.gamePath.endswith("data"):
		params.gamePath = os.path.join(params.gamePath, "data")
	if not os.path.isdir(params.gamePath):
		OnFail("Cannot locate game data files in " + params.gamePath)
		
	if params.usePlugins:
		if not params.pluginPath.endswith("plugins"):
			params.pluginPath = os.path.join(params.pluginPath, "plugins")
		if not os.path.isdir(params.pluginPath):
			print("Cannot find plugin directory in " + params.pluginPath)
			userIn = input("Continue with only vanilla ships? y/n: ")
			no = ("n", "no", "No", "NO")
			if userIn in no:
				sys.exit("Aborting...")
			else:
				params.pluginPath = ""
				print("Using only vanilla ships.")
	else:
		params.pluginPath = ""
	
	if params.doBackup:
		Backup(params)
	
	print("Initializing sources...")
	files = GetSources(params.gamePath, params.pluginPath)
	gameData = GameData(params, files)
	
	outFiles = []
	dataDir = os.path.join(thisDir, "data")
	outFiles.append([Mission(params, gameData), DataWriter(dataDir + "/mission.txt")])
	outFiles.append([Map(params), DataWriter(dataDir + "/map.txt")])
	outFiles.append([Sales(gameData.ammo), DataWriter(dataDir + "/sales.txt")])
	outFiles.append([Event(params.galaxySize), DataWriter(dataDir + "/events.txt")])

	print("Writing files...")
	for newFile in outFiles:
		for node in newFile[0].Begin():
			newFile[1].Write(node)
			newFile[1].WriteNewLine()
		newFile[1].Save()
	print("Done!")
	
	input("Press enter to close.")
	
	
