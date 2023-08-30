#!/bin/env python3
import sys
import os, stat



local_dir = "./"



file_lines_cache = {}
def GetRelativeFileLines(file_name):
	if os.path.exists(local_dir + file_name):
		file_name = local_dir + file_name
	if file_name in file_lines_cache:
		return file_lines_cache[file_name]
	else:
		file_lines = [""]
		with open(file_name) as f:
			file_lines = list(f.read().splitlines())
		file_lines_cache[file_name] = file_lines
		return file_lines



file_data_cache = {}
def GetFileData(file_name):
	if file_name in file_data_cache:
		return file_data_cache[file_name]
	else:
		file_data = ""
		with open(file_name) as f:
			file_data = f.read().replace("\r\n", "\n")
		file_data_cache[file_name] = file_data
		return file_data



class CSVFile:

	def __init__(self, file_name = None, data = None):
		assert((file_name == None) != (data == None))
		self.lines = []
		if file_name != None:
			data = GetFileData(file_name)
		assert(data != None)
		self.lines = list(data.rstrip('\n').split("\n"))
		self.lines = [line.split(",") for line in self.lines]
		self.field_count = len(self.lines[0])
		for line in self.lines:
			assert len(line) == self.field_count, "CSV file lines does not all have the same field count"

	def __getitem__(self, index):
		return self.lines[index]



csv_file_cache = {}
def GetCSV(file_name):
	if os.path.exists(local_dir + file_name):
		file_name = local_dir + file_name
	if file_name in csv_file_cache:
		return csv_file_cache[file_name]
	else:
		csv_file = CSVFile(file_name)
		csv_file_cache[file_name] = csv_file
		return csv_file



source_file_lines = ""

mode = os.fstat(0).st_mode
if len(sys.argv) == 2:
	if stat.S_ISFIFO(mode):
		print("WARNING: Ignoring standard input, an argument was provided!", file=sys.stderr)
	local_dir = os.path.dirname(sys.argv[1]) + "/"
	with open(sys.argv[1]) as f:
		source_file_lines = list(f.read().splitlines())
else:
	assert(stat.S_ISFIFO(mode))
	source_file_lines = sys.stdin.read()



def PrintFile(file_name):
		with open(file_name) as f:
			print(f.read())



i_source_file_line = 0
while i_source_file_line < len(source_file_lines):
	source_file_line = source_file_lines[i_source_file_line]
	# Special cases
	if source_file_line.startswith("[[include "):
		assert(source_file_line.endswith("]]"))
		new_lines = GetRelativeFileLines(source_file_line[10:-2])
		source_file_lines[i_source_file_line:i_source_file_line + 1] = new_lines
		source_file_line = source_file_lines[i_source_file_line]
	if source_file_line.startswith("[[put "):
		assert(source_file_line.endswith("]]"))
		PrintFile(source_file_line[6:-2])
		i_source_file_line += 1
		continue
	# Template replacement
	if source_file_line.startswith("[["):
		# Get the list to insert in the template
		list_name = source_file_line[2:]
		csv_file = GetCSV(list_name)
		# get the template
		template = ""
		i_source_file_line += 1
		while True:
			if i_source_file_line > len(source_file_lines):
				raise Exception("unterminated template")
			source_file_line = source_file_lines[i_source_file_line]
			if source_file_line == "]]":
				break
			else:
				if template != "":
					template += "\n"
				template += source_file_line
			i_source_file_line += 1
		# proceed
		for replacement_fields in csv_file:
			to_print = template
			for i in range(0, csv_file.field_count):
				to_print = to_print.replace('\\' + str(i + 1), replacement_fields[i])
			print(to_print)
	elif source_file_line.endswith("]]"):
		raise Exception("closed non-opened template")
	else:
		print(source_file_line)
	i_source_file_line += 1
