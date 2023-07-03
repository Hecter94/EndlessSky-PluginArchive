import os
import requests
from datetime import datetime
import glob
import shutil
from zipfile import ZipFile


# check for local testing
if os.getcwd() == "/storage/emulated/0/Download/mgit/test3/res/src":
	os.chdir("../../")

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
			
entries = os.listdir(listfolder) # for all listfiles
entries.sort(key=str.lower)
for entry in entries:
	with open(listfolder + entry, "r") as file1:
		x = file1.readline()
		x = file1.readline()
		x = file1.readline()
		directlink = x.replace("directlink=","")
		if directlink != "N/A\n": # when there is a direct link
			directlink = directlink.strip()
			pluginname = entry[:len(entry) -4]
			print("\ndirectlink found for: " + pluginname)
			withdots = pluginname.replace(" ", ".") 
			withdots = withdots.replace("'", ".")
			withdots = withdots.replace(",", ".") 
			withdots = withdots.replace("(", ".") 
			withdots = withdots.replace(")", ".") 
			withdots = withdots.replace("&", ".")  
			withdots = withdots.replace("...", ".")
			withdots = withdots.replace("..", ".")
			if withdots[len(withdots)-1] == ".":
				withdots = withdots[:len(withdots)-1]
			directzip = directlink.split(os.sep)
			directzip = str(directzip[len(directzip)-1])
						
			try: # check asset file
				response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True)
				response.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(err)
			else:
				response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True)
				response.raise_for_status()
				modif = response.headers['Last-Modified']
				datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
				assetlastmodified = datetime_object.date()
				try: # check directlink
					response = requests.head(directlink, allow_redirects=True)
					response.raise_for_status()
				except requests.exceptions.HTTPError as err:
					print(err)
				else:
					response = requests.head(directlink, allow_redirects=True)
					response.raise_for_status()
					try: # checking if last-modicied tag is there
						modif = response.headers['Last-Modified']
					except:
						if directlink[:18] == "https://github.com": # if github repo, get last commit
							print("no Last-Modified tag in header, but found github")
							urllist = directlink.split(os.sep)
							author = urllist[3]
							plug = urllist[4]
							params = {'page': '1', 'per_page': '1'}
							response = requests.get('https://api.github.com/repos/' + author +'/' + plug + '/commits', params=params)
							cont = str(response.content)
							dateandtime = cont.split(",")[4]
							commitdate = dateandtime[8:18] 
							committime = dateandtime[19:27]
							linklastmodified = datetime.strptime(commitdate, '%Y-%m-%d').date()
							datediff = linklastmodified - assetlastmodified # both lastmodified were successful, compare them
							if datediff.days < 1: 
								print("ABORTING: assetfile is newer | link: " + str(linklastmodified) + " asset: " + str(assetlastmodified) + " datediff: " + str(datediff.days))
							else:	
								print("SUCCESS: linkfile is newer")				
								assetsize = int(response.headers['Content-Length']) / 1024 # get size in kb
								if assetsize >= 102400:
									print(assetsize)
									print("ABORTING: directlink is bigger than 100 mb")
								else:
									print("SUCCESS: file is smaller than 100 mb")
									if os.path.isdir("temp") == False:
										os.mkdir("temp")
									with open("temp/" + pluginname + ".zip", "wb") as file2: # create zip file
										r = requests.get(directlink, allow_redirects=True)
										file2.write(r.content)
										print("SUCCESS: downloaded zip")
						else:
							print("ABORTING: no Last-Modified tag in header")
					else:
						modif = response.headers['Last-Modified']
						datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
						linklastmodified = datetime_object.date()
						datediff = linklastmodified - assetlastmodified # both lastmodified were successful, compare them
						if datediff.days < 1: 
							print("ABORTING: assetfile is newer | link: " + str(linklastmodified) + " asset: " + str(assetlastmodified) + " datediff: " + str(datediff.days))
						else:	
							print("SUCCESS: linkfile is newer")				
							assetsize = int(response.headers['Content-Length']) / 1024 # get size in kb
							if assetsize >= 102400:
								print(assetsize)
								print("ABORTING: directlink is bigger than 100 mb")
							else:
								print("SUCCESS: file is smaller than 100 mb")
								if os.path.isdir("temp") == False:
									os.mkdir("temp")
								with open("temp/" + pluginname + ".zip", "wb") as file2: # create zip file
									r = requests.get(directlink, allow_redirects=True)
									file2.write(r.content)
									print("SUCCESS: downloaded zip")						

# extracting zips
listing = glob.glob("temp/*.zip")
print("\nlast modified checks DONE, extracting zips now")
for entry in listing:
	# unzip all zips
	with ZipFile(entry, 'r') as zObject:
		zObject.extractall("temp/")
		firstfolder = zObject.namelist()[0] # first folder inside zip, should be pluginname
		firstfolder = firstfolder[:len(firstfolder) -1]
		ossep = entry.split(os.sep)
		stripped = ossep[1]
		stripped = stripped[:len(stripped)-4] # pluginname stripped from zip name
		print(entry + " | extacted to: temp/" + firstfolder)
		# check for same names of zip and first folder in zip
		if stripped != firstfolder:
			print("ERROR: mismatch between zipname and in-zip folder!")
			shutil.move("temp/" + firstfolder, "temp/" + stripped)
			print("temp/" + firstfolder + " | renamed to: temp/" + stripped)
		if os.path.isdir(pathtoplugins + stripped):
			shutil.rmtree(pathtoplugins + stripped) # delete old plugin
		shutil.move("temp/" + stripped, pathtoplugins + stripped)
	with open("res/news.txt", "r") as file1: 
		news = file1.readlines()
	with open("res/news.txt", "w") as file1: # write to news file, newest on top, keep old contents
		today = datetime.today().strftime('%Y-%m-%d')
		with open("res/pluginlist/" + stripped + ".txt") as file2:
			c = file2.readline()
			c = file2.readline()
			c = file2.readline()
			c = file2.readline()
			c = c.replace("category=", "")
			c = c.strip()
			if c == "N/A":
				c = "uncategorized"
			c = "[" + c + "](" + webroot + indexfile + "#" + c + ")\n" # anchor link to category
		news = [today + " '" + stripped + "' updated | category: " + c] + news
		file1.writelines(news)
	# renaming zips to asset convention
	withdots = stripped.replace(" ", ".") 
	withdots = withdots.replace("'", ".")
	withdots = withdots.replace(",", ".") 
	withdots = withdots.replace("(", ".") 
	withdots = withdots.replace(")", ".") 
	withdots = withdots.replace("&", ".") 
	withdots = withdots.replace("...", ".")
	withdots = withdots.replace("..", ".")
	if withdots[len(withdots)-1] == ".":
		withdots = withdots[:len(withdots)-1]
	shutil.move(entry, "temp/" + withdots + ".zip")
					