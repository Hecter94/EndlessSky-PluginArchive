#!/bin/env python3
import sys
import os, stat



local_dir = "./"



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



file_lines_cache = {}
def GetFileLines(file_name):
	if os.path.exists(local_dir + file_name):
		file_name = local_dir + file_name
	if file_name in file_lines_cache:
		return file_lines_cache[file_name]
	else:
		file_lines = ""
		with open(file_name) as f:
			file_lines = list(f.read().splitlines())
		file_lines_cache[file_name] = file_lines
		return file_lines



def PrintFile(file_name):
		with open(file_name) as f:
			print(f.read())



i_source_file_line = 0
while i_source_file_line < len(source_file_lines):
	source_file_line = source_file_lines[i_source_file_line]
	# Special cases
	if source_file_line.startswith("[[include "):
		assert(source_file_line.endswith("]]"))
		new_lines = GetFileLines(source_file_line[10:-2])
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
		replacement_lines = GetFileLines(list_name)
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
		for replacement_line in replacement_lines:
			print(template.replace('\\1', replacement_line))
	elif source_file_line.endswith("]]"):
		raise Exception("closed non-opened template")
	else:
		print(source_file_line)
	i_source_file_line += 1
