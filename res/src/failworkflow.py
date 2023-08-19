import os
if os.path.isfile('res/errorlog.txt'):
	with open('res/errorlog.txt') as file1:
		content = file1.read()
	print('The following non-critical errors were found:\n')
	print(content)
	print('\nFailing workflow on purpose now!')
	fail_command
else:
	print("The scripts didn't generate errors.")
