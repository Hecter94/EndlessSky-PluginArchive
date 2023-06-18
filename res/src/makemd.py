import os
import requests
from datetime import datetime
import PIL
from PIL import Image

iconpng = assetfile = pluginname =  lastmodified = size = author = website = category = status = description = pluginnameurl = news = ""
allplugins = cheats = gameplay = graphics = outfits = overhauls = overwrites = patches = races = ships = story = weapons = uncategorized = 0
categories = ["Cheats", "Gameplay", "Graphics", "Outfits", "Overhauls", "Overwrites", "Patches", "Races", "Ships", "Story", "Weapons", "Uncategorized"]
plist = []

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
			
def replacevar(string): # replaces %variables% in header template with real values
	if cat == "AllPlugins":
		string = string.replace("%amount%", str(allplugins))
	elif cat == "Cheats":
		string = string.replace("%amount%", str(cheats))
	elif cat == "Gameplay":
		string = string.replace("%amount%", str(gameplay))
	elif cat == "Graphics":
		string = string.replace("%amount%", str(graphics))
	elif cat == "Outfits":
		string = string.replace("%amount%", str(outfits))
	elif cat == "Overhauls":
		string = string.replace("%amount%", str(overhauls))
	elif cat == "Overwrites":
		string = string.replace("%amount%", str(overwrites))
	elif cat == "Patches":
		string = string.replace("%amount%", str(patches))
	elif cat == "Races":
		string = string.replace("%amount%", str(races))
	elif cat == "Ships":
		string = string.replace("%amount%", str(ships))
	elif cat == "Story":
		string = string.replace("%amount%", str(story))
	elif cat == "Weapons":
		string = string.replace("%amount%", str(weapons))
	elif cat == "Uncategorized":
		string = string.replace("%amount%", str(uncategorized))
	string = string.replace("%allplugins%", str(allplugins))
	string = string.replace("%cheats%", str(cheats))
	string = string.replace("%gameplay%", str(gameplay))
	string = string.replace("%graphics%", str(graphics))
	string = string.replace("%outfits%", str(outfits))
	string = string.replace("%overhauls%", str(overhauls))
	string = string.replace("%overwrites%", str(overwrites))
	string = string.replace("%patches%", str(patches))
	string = string.replace("%races%", str(races))
	string = string.replace("%ships%", str(ships))
	string = string.replace("%story%", str(story))
	string = string.replace("%weapons%", str(weapons))
	string = string.replace("%uncategorized%", str(uncategorized))
	return string

def replacevarp(string):
	string = string.replace("%assetfullpath%", assetfullpath)
	string = string.replace("%assetfile%", assetfile)
	string = string.replace("%pluginname%", pluginname)
	string = string.replace("%assetfile%", assetfile)
	string = string.replace("%lastmodified%", lastmodified)
	string = string.replace("%size%", size)
	string = string.replace("%pluginurl%", pluginurl)
	string = string.replace("%author%", author)
	string = string.replace("%webroot%", webroot)
	string = string.replace("%indexfile%", indexfile)
	string = string.replace("%news%", news)
	
	if website == "N/A": # for prevent [N/A](N/A) links
		websitecheck = "N/A"
		websitelink = ""
	else:
		websitecheck = ""
		websitelink = website
	string = string.replace("%website%", websitelink)
	string = string.replace("%websitecheck%", websitecheck)
	string = string.replace("%category%", category)
	string = string.replace("%status%", status)
	string = string.replace("%iconpng%", str(iconpng))
	string = string.replace("%pluginnameurl%", pluginnameurl)	
	string = string.replace("%description%", description)
	return string
				
# counting categories of files in  pluginlistfolder
entries = os.listdir(pathtoplugins)
entries.sort(key=str.lower)
for entry in entries:
	allplugins += 1
	# if pluginlist file exists, read it
	if os.path.exists(listfolder + entry + ".txt") == True:
		with open(listfolder + entry + ".txt", "r") as file1:
			cat = file1.readline()
			cat = file1.readline()
			cat = file1.readline()
			cat = file1.readline().split("=")[1].replace("\n", "")
			if cat == "cheats":
				cheats += 1
			elif cat == "gameplay":
				gameplay += 1
			elif cat == "graphics":
				graphics += 1
			elif cat == "outfits":
				outfits += 1
			elif cat == "overhauls":
				overhauls += 1
			elif cat == "overwrites":
				overwrites += 1
			elif cat == "patches":
				patches += 1
			elif cat == "races":
				races += 1
			elif cat == "ships":
				ships += 1
			elif cat == "story":
				story += 1
			elif cat == "weapons":
				weapons += 1
			else:
				uncategorized += 1
	else:
		uncategorized += 1
		cat = "uncategorized"
		# if no pluginlist file exists, create an empty one	
		with open(listfolder + entry + ".txt" , "w") as file1:
			file1.writelines("author=N/A\nwebsite=N/A\ndirectlink=N/A\ncategory=N/A\nstatus=N/A\ndescription=N/A\n")
		print(entry + ".txt CREATED! because plugin was there, but no listfile!")
	with open(listfolder + entry + ".txt", "r") as file1:
		text = file1.read()
		plist.append(str(cat) + "\n" + entry + "\n" + text) # create a list of all listfiles

# reading template file and splitting it to the 3 templates
with open(template, "r") as file1:
	temp = file1.read()
pos = temp.find("%%% template for category below this point %%%")
temphead = temp[:pos] # set header string
foot = temp[pos + 47:]	
pos = foot.find("%%% template for plugin entry below this point %%%")
temptempcat = foot[:pos] # set category string
tempplug = foot[pos + 50:] # set plugin string
pos = temptempcat.find("%pluginhere%")
tempcatup = temptempcat[:pos] # upper half of template category
tempcatdown = temptempcat[pos +12:] # lower half of template string


with open("res/news.txt", "r") as file1: # reading and formating lines
	newslist = file1.readlines()
for i in range(15):
	if i <= len(newslist)-1:
		news = news + newslist[i] + "\n"

# writing the md file
filerr = open("res/errorlog.txt", "w")
filerr.writelines("header request error log:\n")
filerr.close
with open(indexfile, "w") as file1:
	temphead = replacevar(temphead)
	temphead = replacevarp(temphead)
	file1.writelines(temphead) # writer header template
	for cat in categories: # for each category
		tempcatupt = tempcatup.replace("%category%", cat)
		tempcatupt = replacevar(tempcatupt)
		tempcatupt = replacevarp(tempcatupt)
		tempcatdownt = tempcatdown.replace("%category%", cat)
		tempcatdownt = replacevarp(tempcatdownt)
		tempcatdownt = replacevar(tempcatdownt)
		file1.writelines(tempcatupt) # write upper category template
		for p in plist: # listfiles list element, created in counting block... 'array' of all plugins
			pos = p.find("\n")
			catcomp = p[:pos]
			catcomp = catcomp.strip() # get category for comparing with actual category
			if catcomp == "N/A":
				catcomp = "Uncategorized"
			if catcomp.capitalize() == cat:
				# get variables out of the list item p
				description = p.split("\n")
				if description[0] == "N/A":
					category = description[0]
				else:
					category = description[0].capitalize() 
				pluginname = description[1]
				pluginnameurl = pluginname.replace(" ", "%20")
				author = description[2][7:] 
				website = description[3][8:] 
				directlink = description[4][11:]
				status = description[6][7:]
				for x in range(0, 7):
					description.pop(0)
				description[0] = description[0].replace("description=", "")
				alllines = ""
				for lines in description:
					alllines = alllines + ">" + lines + "\n"
				description = alllines
				
				if os.path.exists(pathtoplugins + pluginname + "/icon.png") == True: # check for icon.png, resize it, or hide it
					im = Image.open(pathtoplugins + pluginname + "/icon.png")
					w, h = im.size
					iconpath = pathtoplugins + pluginname
					iconpath = iconpath.replace("&", "%26")
					iconpath = iconpath.replace("'", "%27")
					iconpath = iconpath.replace("(", "%28")
					iconpath = iconpath.replace(")", "%29")
					iconpath = iconpath.replace(",", "%2C")
					if h > w:
						iconpng = "<img src='"+ iconpath + "/icon.png' height='100'></img><br>\n"
					else:
						iconpng = "<img src='"+ iconpath + "/icon.png' width='100'></img><br>\n"
				else:
					iconpng = ""
				
				# get last modified date from the assetfiles
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
				try:
					response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True)
					response.raise_for_status()
				except requests.exceptions.HTTPError as err:
					print(err)
					lastmodified = "N/A"
					size = "N/A" 
					filerr = open("res/errorlog.txt", "a")
					filerr.writelines(str(err) + " \n")
					filerr.close
				else:
					response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True)
					response.raise_for_status()
					modif = response.headers['Last-Modified']
					datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
					lastmodified = str(datetime_object.date())
					# get file size of the assetfiles in kb or mb
					assetsize = int(response.headers['Content-Length']) / 1024
					form = " kb"
					if assetsize > 1024:
						assetsize = assetsize / 1024
						form = " mb"
					size = str(round(assetsize, 2)) + form
				assetfile =  withdots + ".zip"
				file1.writelines(replacevarp(tempplug))
		file1.writelines(tempcatdownt) # write lower category template
