# dataFile.py
# Copyright (c) 2014 Michael Zahniser
# Copyright (C) 2017 Frederick W. Goy IV
#
# This program is a derivative of the source code from the Endless Sky
# project, which is licensed under the GNU GPLv3.
#
# Endless Sky source: https://github.com/endless-sky/endless-sky
#
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



from .dataNode import DataNode

import os
import io



class DataFile(object):
	__slots__ = 'root'
	
	def __init__(self, path=""):
		self.root = DataNode()
		if not path or not path.endswith(".txt"):
			return None
			
		if not self.Load(path):
			return None
		
		
	def __nonzero__(self):
		return self.root.HasChildren()
		
		
	def Begin(self):
		return self.root.Begin()
		
		
	def End(self):
		return self.root.End()
		
		
	def Load(self, path):
		result = []
		try:
			path = os.path.normpath(path)
			
			with io.open(path, "rb") as newFile:
				for line in newFile:
					line = line.decode("utf-8")
					if not line[-1] == "\n":
						result.append(line + "\n")
					else:
						result.append(line)
						
		except (IOError, OSError) as error:
			message = error.strerror + " " + error.filename
			print(message)
		
		if not result:
			return False
			
		if not result[-1] == "\n":
			result.append("\n")
				
		self.root.tokens.append("file")
		self.root.tokens.append(path)
		
		self.Parse(result)
		
		return True
		
		
	def Parse(self, data):
		stack = [self.root]
		whiteStack = [-1]
		for line in data:
			it = 0
			white = 0
			while line[it].isspace() and line[it] != "\n":
				white += 1
				it += 1
			
			if line[it] == "#" or line[it] == "\n":
				continue
			
			while whiteStack[-1] >= white:
				whiteStack.pop()
				stack.pop()
			
			node = DataNode()
			stack[-1].Append(node)
			
			stack.append(node)
			whiteStack.append(white)
			
			while line[it] != "\n":
				endQuote = line[it]
				isQuoted = False
				if endQuote == '"' or endQuote == '`':
					isQuoted = True
					it += 1
				
				token = ""
				if isQuoted:
					while line[it] != "\n" and line[it] != endQuote:
						token += line[it]
						it += 1
					if line[it] != endQuote:
						node.PrintTrace("Closing quote is missing.")
					it += 1
				
				else:
					while not line[it].isspace():
						token += line[it]
						it += 1
				
				node.tokens.append(token)
				
				if line[it] != "\n":
					while line[it].isspace() and line[it] != "\n":
						it += 1
					
				if line[it] == "#":
					break
					
					
	def Append(self, node):
		self.root.Append(node)
		
		
	def Remove(self, node):
		self.root.Remove(node)

