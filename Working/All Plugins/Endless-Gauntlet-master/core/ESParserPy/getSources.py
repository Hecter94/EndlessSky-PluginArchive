# getSources.py
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



from .dataFile import DataFile

import os
import sys



def GetSources(dataPath, pluginPath=""):
	dataPath = os.path.normpath(dataPath)
	files = []
	
	for tup in os.walk(dataPath):
		for file in tup[2]:
			files.append(DataFile(os.path.join(tup[0], file)))
			
	if pluginPath:
		pluginPath = os.path.normpath(pluginPath)
		for dir in os.listdir(pluginPath):
			subPath = os.path.join(pluginPath, dir)
			for subdir in os.listdir(subPath):
				if subdir == "data":
					for tup in os.walk(os.path.join(subPath, subdir)):
						for file in tup[2]:
							files.append(DataFile(os.path.join(tup[0], file)))
					
	return files
	
	
def GetImages(imagePath, pluginPath=""):
	imagePath = os.path.normpath(imagePath)
	files = []
	
	for tup in os.walk(imagePath):
		for file in tup[2]:
			path = os.path.join(tup[0], file)
			files.append((GetImageName(path), path))
			
	if pluginPath:
		pluginPath = os.path.normpath(pluginPath)
		for dir in os.listdir(pluginPath):
			subPath = os.path.join(pluginPath, dir)
			for subdir in os.listdir(subPath):
				if subdir == "images":
					for tup in os.walk(os.path.join(subPath, subdir)):
						for file in tup[2]:
							path = os.path.join(tup[0], file)
							files.append((GetImageName(path), path))
							
	return files
	
	
def GetImageName(path):
	path = path.replace("\\", "/")
	return path.rpartition("/images/")[2]
	
	
def GetConfigPath():
	curPlatform = sys.platform
	path = ""
	if curPlatform.startswith("linux"):
		path = os.path.expanduser("~/.local/share/endless-sky/")
	elif curPlatform == "darwin":
		path = os.path.expanduser("~/Library/Application Support/endless-sky/")
	elif curPlatform == "win32":
		path = os.path.expandvars("%appdata%\\endless-sky")
		
	return path
	
	
def GetGamePath():
	curPlatform = sys.platform
	path = ""
	if curPlatform.startswith("linux"):
		path = os.path.expanduser("~/.steam/steam/steamapps/common/Endless Sky/data")
	elif curPlatform == "darwin":
		path = os.path.expanduser("~/Library/Application Support/Steam/SteamApps/common/Endless Sky/data")
	elif curPlatform == "win32":
		path = os.path.expandvars("%programfiles(x86)%\\Steam\\steamapps\\common\\Endless Sky\\data")
		
	return path
	
