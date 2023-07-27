import os
import requests
from datetime import datetime
import glob
import shutil
from zipfile import ZipFile


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

# creating temp directory			
if os.path.isdir("temp") == False: 
	os.mkdir("temp")						

# getting username and token for login to github api(to increase request limit from 60/hr to 5000/hr)
username = os.getenv("GITHUB_ACTOR")
token = os.getenv("github_token")

# reading listfiles and check for updates
entries = os.listdir(listfolder)
entries.sort(key=str.lower)		
for entry in entries:
	with open(listfolder + entry, "r") as file1:
		x = file1.readline()
		x = file1.readline()
		x = file1.readline()
		directlink = x.replace("directlink=","")
	if directlink == "N/A\n": # when there is no direct link go to next file
		continue
	else:
		directlink = directlink.strip()
		pluginname = entry[:len(entry) -4] # removes '.txt'
		 # getting asset file name
		withdots = pluginname.replace(" ", ".").replace("'", ".").replace(",", ".").replace("(", ".").replace(")", ".").replace("&", ".").replace("...", ".").replace("..", ".")
		if withdots[len(withdots)-1] == ".":
			withdots = withdots[:len(withdots)-1]
		directzip = directlink.split(os.sep)
		directzip = str(directzip[len(directzip)-1])
		
		try: # check if asset file is there, and get assetlastmodified
			response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True)
			response.raise_for_status()
		except requests.exceptions.HTTPError as err:
			print(err)
			assetlastmodified = "FALSE"
		else:
			modif = response.headers['Last-Modified']
			datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
			assetlastmodified = datetime_object.date()
		
		try: # check directlink
			response = requests.head(directlink, allow_redirects=True)
			response.raise_for_status()
		except requests.exceptions.HTTPError as err:
			print("ERROR: directlink not reachable: " + directlink)
			print(err)
			continue
		else: 
			try: # checking if last-modified/content-length tags are there
				modif = response.headers['Last-Modified']
				datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
				linklastmodified = datetime_object.date()
				linksize = int(response.headers['Content-Length']) / 1024 # get size in kb
			except:
				if directlink[:18] == "https://github.com": # check if github repo
					urllist = directlink.split(os.sep)
					author = urllist[3]
					plug = urllist[4]
					linksize = "FALSE"
					try: # check github api for last commit
						params = {'page': '1', 'per_page': '1'}
						response = requests.get('https://api.github.com/repos/' + author +'/' + plug + '/commits', params=params, auth=(username,token))
					except:
						print("ERROR: github api not reachable: " + plug)
						linklastmodified = "FALSE"
						continue
					else: # get last commit date and time
						cont = str(response.content)
						dateandtime = cont.split(",")[4]
						commitdate = dateandtime[8:18] 
						committime = dateandtime[19:27]
						linklastmodified = datetime.strptime(commitdate, '%Y-%m-%d').date()
		if linksize != "FALSE":
			if linksize >= 204800:
				print("ABORTING: directlink is bigger than 200 mb")
				continue
		if linklastmodified != "FALSE":
			if assetlastmodified != "FALSE":
				datediff = linklastmodified - assetlastmodified # both lastmodified were successful, compare them
				if datediff.days < 1: 
					print("", end="")
				else:	
					print("SUCCESS: linkfile is newer: " + pluginname + "\n")
					with open("temp/" + pluginname + ".zip", "wb") as file2: # create zip file
						r = requests.get(directlink, allow_redirects=True)
						file2.write(r.content)
			else:
				print("no assetfile, must be a new plugin: " + pluginname + "\n")
				with open("temp/new_plugin_" + pluginname + ".zip", "wb") as file2: # create zip file, naming it see if it a new one
					r = requests.get(directlink, allow_redirects=True)
					file2.write(r.content)
				
# extracting zips
listing = glob.glob("temp/*.zip")
print("\nlast modified checks DONE, extracting zips now")
for entry in listing:
	# check for different news generating, new or updated plugin
	if entry[:16] == "temp/new_plugin_":
		new_or_updated = "new"
		shutil.move(entry, "temp/" + entry[16:]) # cut off the 'new_plugin_'
		entry = "temp/" + entry[16:]
		print("\nnew plugin:", end=" " )
	else:
		new_or_updated = "updated"
		print("\nupdated plugin:", end=" ")
	# get names
	zip_name = entry.split(os.sep)[1]
	plugin_name = zip_name[:len(zip_name) -4]
	withdots = zip_name.replace(" ", ".").replace("'", ".").replace(",", ".").replace("(", ".").replace(")", ".").replace("&", ".").replace("...", ".").replace("..", ".")
	if withdots[len(withdots)-1] == ".":
		withdots = withdots[:len(withdots)-1]
	print(plugin_name +  " " + zip_name + " " + withdots)
	# extract zip now
	os.mkdir("temp/" + plugin_name)
	with ZipFile(entry, 'r') as zObject:
		zObject.extractall("temp/" + plugin_name + "/")
		firstfolder = zObject.namelist()[0] # first folder inside zip, should be pluginname
	firstfolder = firstfolder[:len(firstfolder) -1]
	print(entry + " | extracted to: temp/" + plugin_name)
	# replaces chars in file and folder names, which are allowed in linux, but not in windows	
	chars = ['\\', ':', '*', '?', '"', '<', '>', '|']
	for root, dirs, files in os.walk("temp/" + plugin_name + "/"):
		for name in files:
			for char in chars:
				if char in name:
					print(name + " has invalid char: " + char + " !renaming it!")		
					os.rename(os.path.join(root, name), os.path.join(root, name).replace(char, ''))
					name = name.replace(char,'')
		for name in dirs:
			for char in chars:
				if char in name:
					print(name + " has invalid char: " + char + " !renaming it!")		
					os.rename(os.path.join(root, name), os.path.join(root, name).replace(char, ''))
					name = name.replace(char,'')
	# check for correct folder structure and correct it
	if plugin_name != firstfolder:
		print("ERROR: mismatch between zipname and in-zip folder!")
		shutil.move("temp/"+ plugin_name + "/" + firstfolder, "temp/" + plugin_name + "/" + plugin_name)
		print(firstfolder + " | renamed to: " + plugin_name)
		sub_folder = os.listdir("temp/" + plugin_name + "/" + plugin_name) 
	for each in sub_folder:
		if each.lower() == "data": 
			print("DATA FOLDER FOUND, moving plugin to plugin folder")
			break
		elif each.lower() == plugin_name.lower():
			print("SUBFOLDER FOUND, clearing structure and moving plugin to plugin folder")
			shutil.move("temp/" + plugin_name + "/" + plugin_name + "/" + each + "/", "temp/" + plugin_name + "/" + plugin_name + "X/")
			shutil.rmtree("temp/" + plugin_name + "/" + plugin_name )
			shutil.move("temp/" + plugin_name + "/" + plugin_name + "X/", "temp/" + plugin_name + "/" + plugin_name + "/")
			break		
	# create new zip with correct paths
	shutil.make_archive("temp/" + plugin_name, 'zip', "temp/" + plugin_name + "/")
	# delete old plugin folder, and move plugin to plugin folder		
	if os.path.isdir(pathtoplugins + plugin_name): 
		shutil.rmtree(pathtoplugins + plugin_name) 
	shutil.move("temp/" + plugin_name + "/" + plugin_name, pathtoplugins + plugin_name)		
	# renaming zips to asset convention
	shutil.move("temp/" + zip_name, "temp/" + withdots)
	#generating news
	with open("res/news.txt", "r") as file1: # reading old news
		news = file1.readlines()
	with open("res/news.txt", "w") as file1: # write to news file, newest on top, keep old contents
		today = datetime.today().strftime('%Y-%m-%d')
		# writing date, stripped(pluginname) and new_or_update to news 
		news = [today + " | " + plugin_name + " | " + new_or_updated + " <br>\n"] + news
		file1.writelines(news)
