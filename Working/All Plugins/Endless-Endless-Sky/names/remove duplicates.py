#This small script alphabetizes and removes duplicates in the specified file
file_name = input('Name of file: ')

try:
	print('replacing...')
	lines = sorted(set(open(file_name + '.txt', 'r').readlines()))
	output = open('output.txt', 'w')
	for item in lines:
		output.write(item)
	print('Finished!')
	input()
except:
	print('Error: File not found.')
	input()
