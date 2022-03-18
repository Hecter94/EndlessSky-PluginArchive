# backup.py
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



import os
import shutil



def Backup(params):
	thisDir = os.path.join(params.rootPath, "core")
	saveDir = params.savesPath
	backDir = os.path.join(thisDir, "backup")
	
	if not os.path.isdir(saveDir):
		return
		
	if not os.path.isdir(backDir):
		os.mkdir(backDir)
		
	isFirst = False
	if not os.path.isdir(os.path.join(backDir, "first run")):
		isFirst = True
		os.mkdir(os.path.join(backDir, "first run"))
		
	if not os.path.isdir(os.path.join(backDir, "recent")):
		os.mkdir(os.path.join(backDir, "recent"))
		
	toPath = (os.path.join(backDir, "first run") if isFirst else os.path.join(backDir, "recent"))
	for file in os.listdir(saveDir):
		fileFrom = os.path.join(saveDir, file)
		fileTo = os.path.join(toPath, file)
		shutil.copy(fileFrom, fileTo)
		
