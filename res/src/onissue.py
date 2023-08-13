import os 

content = os.environ['ISSUE_INPUT'] 
	
# read paths and files
with open("res/config.txt") as f:
	for line in f:
		line = str((line.strip()))
		if line.find("indexfile") == 0:	# i.e. indexfile = README.md | can get changed to whatever file you want the script output go
			indexfile = line.split(" = ")[1]
		if line.find("template") == 0:	# i.e. template = res/template.txt | a template how the indexfile should look, can be edited
			template = line.split(" = ")[1]
		if line.find("listfolder") == 0:	# i.e. listfolder = res/pluginlist/ | folder to where the plugin descriptions files are
			listfolder = line.split(" = ")[1]
		if line.find("pathtoplugins") == 0:	# i.e. pathtoplugins = myplugins/ | folder where the plugin folder and files are
			pathtoplugins = line.split(" = ")[1]
		if line.find("webroot") == 0:	# i.e. webroot = https://github.com/zuckung/test3/blob/main/
			webroot = line.split(" = ")[1]	
		if line.find("pluginurl") == 0:	# i.e. pluginurl = https://github.com/zuckung/test3/tree/main/Working/All%20Plugins/
			pluginurl = line.split(" = ")[1]
		if line.find("assetfullpath") == 0:	# i.e. assetfullpath = https://github.com/zuckung/test3/releases/download/Latest/
			assetfullpath = line.split(" = ")[1]
		if line.find("newsamount") == 0:	# i.e. newsamount = 20
			newsamount = line.split(" = ")[1]

def format_content():
	splitted = content.split('\n')
	if splitted[0] == '### Name\r':
		print('SUCCESS: Newly created issue is a plugin addition.')
		pluginname = splitted[2].strip()
		author = 'author=' + splitted[6].replace('\r', '\n')
		website = 'website=' + splitted[10].replace('\r', '\n')
		if website == 'website=_No response_\n':
			website = 'website=N/A\n'
		directlink = 'directlink=' + splitted[14].replace('\r', '\n')
		if directlink == 'directlink=_No response_\n':
			directlink = 'directlink=N/A\n'
		category = 'category=' + splitted[18].replace('\r', '\n')
		status = 'status=' + splitted[22].replace('\r', '\n')
		description = 'description=' + splitted[26].replace('\r', '\n')
		with open(listfolder + pluginname + '.txt', 'w') as file1:
			file1.writelines(author)
			file1.writelines(website)
			file1.writelines(directlink)
			file1.writelines(category)
			file1.writelines(status)
			file1.writelines(description)
		print('added "' + pluginname + '.txt" to listfolder\n')
		print(author + website+directlink+category+status+description)
	else:
		print("ABORTING: Newly created issue isn't a plugin addition.")
	
	
format_content()
