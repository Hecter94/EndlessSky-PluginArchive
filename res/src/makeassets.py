import os
import requests
import zipfile

def zipdir(path, ziph): # ziph is zipfile handle
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file), 
			os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

if os.getcwd() == "/storage/emulated/0/Download/mgit/test3/res/src": # check for local testing
	os.chdir("../../")

with open("res/config.txt") as f: # read paths and files
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

entries = os.listdir(pathtoplugins)
entries = sorted(entries)
fchecked = fmiss = 0
for entry in entries: # for all plugin folders
	fchecked += 1
	withdots = entry.replace(" ",".")
	try:
		response = requests.head(assetfullpath + withdots + ".zip") # check if asset zip is there
		response.raise_for_status()
	except requests.exceptions.HTTPError as err:
		fmiss += 1
		with zipfile.ZipFile(withdots + ".zip", "w", zipfile.ZIP_DEFLATED) as zipf:
			zipdir(pathtoplugins + entry, zipf)
		print("checked: ERROR: "+ str(response.status_code) + " | CREATED " + withdots + ".zip")
	else:
		print("checked: OK: " + withdots + ".zip")
print("\n" + str(fchecked) + " folders checked | " + str(fmiss) + " x error on asset file")