# dataWriter.py
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



import io
import os



class DataWriter(object):
	__slots__ = ('indent', 'space', 'before', 'path', 'out')
	
	def __init__(self, path):
		self.indent = b""
		self.space = b" "
		self.before = self.indent
		self.path = os.path.normpath(path)
		self.out = io.BytesIO()
		
		
	def Save(self):
		try:
			with io.open(self.path, "wb") as saveFile:
				saveFile.write(self.out.getvalue())
			
		except (IOError, OSError) as error:
			message = error.strerror + " " + error.filename
			print(message)
			
			
	def Write(self, node):
		for it in range(node.Size()):
			self.WriteToken(node.Token(it))
		self.WriteNewLine()
		
		if node.HasChildren():
			self.BeginChild()
			for child in node.children:
				self.Write(child)
			self.EndChild()
			
			
	def WriteNewLine(self):
		self.out.write(b"\n")
		self.before = self.indent
		
		
	def BeginChild(self):
		self.indent += b"\t"
		self.before = self.indent
		
		
	def EndChild(self):
		self.indent = self.indent.rpartition(b"\t")[0]
		self.before = self.indent
		
		
	def WriteComment(self, string):
		self.out.write(self.indent + b"# " + string.encode() + b"\n")
		
		
	def WriteToken(self, string):
		hasSpace = False
		hasQuote = False
		
		for it in string:
			if it.isspace():
				hasSpace = True
			
			if it == '"':
				hasQuote = True
		
		self.out.write(self.before)
		if not string:
			self.out.write(b'""')
		elif hasSpace and hasQuote:
			self.out.write(b"`" + string.encode() + b"`")
		elif hasQuote:
			self.out.write(b"`" + string.encode() + b"`")
		elif hasSpace:
			self.out.write(b'"' + string.encode() + b'"')
		else:
			self.out.write(string.encode())
		
		self.before = self.space

