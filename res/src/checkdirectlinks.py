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
	
# creating res/last_commits.txt
with open("res/last_commits.txt", "w") as file1:
	file1.write("")

# getting username and token for login to github api(to increase request limit from 60/hr to 5000/hr)
username = os.getenv("GITHUB_ACTOR")
token = os.getenv("github_token")

# reading listfiles and check for updates
entries = os.listdir(listfolder)
entries.sort(key=str.lower)		
for entry in entries:
	with open(listfolder + entry, "r") as file1:
		x = file1.readline()
		website = file1.readline().replace("website=", "")
		x = file1.readline()
		directlink = x.replace("directlink=","")
	if directlink == "N/A\n": # when there is no direct
		
		# check for website github to get last commit, then continue to next
		website = website.strip()
		if website[:18] == "https://github.com":
			urllist = website.split(os.sep)
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
				commitdate = dateandtime[8:18] + " " + dateandtime[19:27]
				linklastmodified = datetime.strptime(commitdate, '%Y-%m-%d %H:%M:%S')
				with open("res/last_commits.txt", "a") as commit:
					commit.writelines(entry[:len(entry) - 4] + "|" + str(linklastmodified.date()) + "\n")
				continue
		continue
		
	else: # has directlink
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
			assetlastmodified = datetime_object
		
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
				linklastmodified = datetime_object
				if directlink[:18] == "https://github.com": # check if github repo | must be multi-plugin repo with own asset links
					with open("res/last_commits.txt", "a") as commit:
						commit.writelines(pluginname + "|" + str(linklastmodified.date()) + "\n")
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
						commitdate = dateandtime[8:18] + " " + dateandtime[19:27]
						linklastmodified = datetime.strptime(commitdate, '%Y-%m-%d %H:%M:%S')
						with open("res/last_commits.txt", "a") as commit:
							commit.writelines(pluginname + "|" + str(linklastmodified.date()) + "\n")
		if linksize != "FALSE":
			if linksize >= 307200:
				print("ABORTING: directlink is bigger than 300 mb")
				continue
				
		if linklastmodified != "FALSE":
			if assetlastmodified != "FALSE":
				datediff = linklastmodified - assetlastmodified # both lastmodified were successful, compare them
				# positive update, negative no update
				if datediff.days == 0: # same day, go check seconds
					if datediff.seconds > 600: # linkfile is at least 10 min newer, do update
						modified = 1
					else:
						print("", end="")
						modified = 0
				elif datediff.days < 0: # negative days, asset is newer, no update
					print("", end="")
					modified = 0					
				else: # positive days, linkfile is newer, do update
					modified = 1	
					
				if modified == 1:
					print("SUCCESS: linkfile is newer: " + pluginname)
					print("datediff: " + str(datediff.days) + " " + str(datediff.seconds) + " | asset: " + str(assetlastmodified) + " | link: " + str(linklastmodified) + "\n")
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
	print(plugin_name)
	
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
		sub_folders = os.listdir("temp/" + plugin_name + "/" + plugin_name) 
		for sub_f in sub_folders:
			if sub_f.lower() == "data": 
				print("DATA FOLDER FOUND, structure is correct")
				break
			elif sub_f.lower() == plugin_name.lower():
				print("SUBFOLDER FOUND, clearing structure and moving plugin to correct folder")
				shutil.move("temp/" + plugin_name + "/" + plugin_name + "/" + sub_f + "/", "temp/" + plugin_name + "/" + plugin_name + "X/")
				shutil.rmtree("temp/" + plugin_name + "/" + plugin_name )
				shutil.move("temp/" + plugin_name + "/" + plugin_name + "X/", "temp/" + plugin_name + "/" + plugin_name + "/")
				break	
			
	# remove irrelevant files and folders
	# remove files: *.zip .gitignore .gitattributes | folder: .git/ .github/ __MACOSX/
	check_irr = os.listdir("temp/" + plugin_name + "/" + plugin_name + "/")
	for irr in check_irr:
		if irr == ".gitignore":
			os.remove("temp/" + plugin_name + "/" + plugin_name + "/" + irr)
			print(irr + " removed")
		elif irr == ".gitattributes":
			os.remove("temp/" + plugin_name + "/" + plugin_name + "/" + irr)
			print(irr + " removed")
		elif irr[len(irr) -4:] == ".zip":
			os.remove("temp/" + plugin_name + "/" + plugin_name + "/" + irr)
			print(irr + " removed")
		elif irr == ".git":
			shutil.rmtree("temp/" + plugin_name + "/" + plugin_name + "/" + irr + "/")
			print(irr + " removed")
		elif irr == ".github":
			shutil.rmtree("temp/" + plugin_name + "/" + plugin_name + "/" + irr + "/")
			print(irr + " removed")
		elif irr == "__MACOSX":
			shutil.rmtree("temp/" + plugin_name + "/" + plugin_name + "/" + irr + "/")
			print(irr + " removed")
			
	# create new zip with correct paths
	shutil.make_archive("temp/" + plugin_name, 'zip', "temp/" + plugin_name + "/")
	print("new clean zip created")
	
	# delete old plugin folder, and move plugin to plugin folder		
	if os.path.isdir(pathtoplugins + plugin_name): 
		shutil.rmtree(pathtoplugins + plugin_name) 
	shutil.move("temp/" + plugin_name + "/" + plugin_name, pathtoplugins + plugin_name)
	print("plugin moved to " + pathtoplugins)
	
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
