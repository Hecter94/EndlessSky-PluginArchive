import os
import requests
from datetime import datetime
import time

iconpng = assetfile = pluginname =  lastmodified = size = author = website = category = status = description = pluginnameurl = news = allnews = pluginissues = updatecheck = readme = repo_last_commit = ""
allplugins = cheats = gameplay = graphics = outfits = overhauls = overwrites = patches = races = ships = starts = story = weapons = uncategorized = 0
categories = ["Cheats", "Gameplay", "Graphics", "Outfits", "Overhauls", "Overwrites", "Patches", "Races", "Ships", "Starts", "Story", "Weapons", "Uncategorized"]
plist = []

# giving github enough Time for the zip uploads
time.sleep(600)

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

# read last commit pluginname and date to put it into 2 lists		
commit_p = []
commit_d = []
with open("res/last_commits.txt", "r") as file1:
	last_commits = file1.readlines()
for commit in last_commits:
	splitted = commit[:len(commit) -1].split("|")
	commit_p.append(splitted[0])
	commit_d.append(splitted[1])
	

			
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
	elif cat == "Starts":
		string = string.replace("%amount%", str(starts))
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
	string = string.replace("%starts%", str(starts))
	string = string.replace("%story%", str(story))
	string = string.replace("%weapons%", str(weapons))
	string = string.replace("%uncategorized%", str(uncategorized))
	return string

def replacevarp(string): # replaces %variables% in plugin and category template with real values
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
	string = string.replace("%newsamount%", newsamount)	
	string = string.replace("%pluginissues%", pluginissues)
	string = string.replace("%updatecheck%", updatecheck)
	string = string.replace("%readme%", readme)
	string = string.replace("%last_commit%", repo_last_commit)
	if website == "N/A" or website == "" or website == "NA": # for prevent [N/A](N/A) links
		websitecheck = "N/A"
		websitelink = ""
	else:
		websitecheck = ""
		websitelink = website
	string = string.replace("%website%", websitelink)
	string = string.replace("%websitecheck%", websitecheck)
	string = string.replace("%category%", category)
	string = string.replace("%lowercategory%", category.lower())
	string = string.replace("%status%", status)
	string = string.replace("%iconpng%", str(iconpng))
	string = string.replace("%pluginnameurl%", pluginnameurl)	
	string = string.replace("%description%", description)
	return string
				
# reading the plugin issues from plugin_issues.txt	
with open("res/plugin_issues.txt") as file1:
	pluginissues = file1.read()
				
				
# counting categories of files in  pluginlistfolder and create a list object with
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
			if cat.lower() == "cheats": # count plugins in category
				cheats += 1
			elif cat.lower() == "gameplay":
				gameplay += 1
			elif cat.lower() == "graphics":
				graphics += 1
			elif cat.lower() == "outfits":
				outfits += 1
			elif cat.lower() == "overhauls":
				overhauls += 1
			elif cat.lower() == "overwrites":
				overwrites += 1
			elif cat.lower() == "patches":
				patches += 1
			elif cat.lower() == "races":
				races += 1
			elif cat.lower() == "ships":
				ships += 1
			elif cat.lower() == "starts":
				starts += 1
			elif cat.lower() == "story":
				story += 1
			elif cat.lower() == "weapons":
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


# writing res/allnews.md and putting the amount  of news entries defined in the config.txt to the new variable
with open("res/news.txt", "r") as file1:
	newslist = file1.readlines()
# get all values for all news
for each in  newslist: 
	news_line = each.split(" | ") # 3 variables from the news file
	ndate = news_line[0]
	nname = news_line[1]
	nnew_or_update = news_line[2].split(" ")[0]
	if os.path.isfile(listfolder + nname + ".txt"):
		with open(listfolder + nname + ".txt", "r") as file1: # 2 valriables from the listfile
			nauthor = file1.readline().replace("author=", "").strip()
			ncat = file1.readline()
			ncat = file1.readline()
			ncat = file1.readline().replace("category=", "").strip()
		if ncat == "N/A" or ncat == "" or ncat == "NA":
			ncat = "uncategorized"
		# got variables now: ndate, nnew_or_updated, nname, nauthor, ncat, define how a news line should look
		nline = ndate + " | " +  nnew_or_update + " Plugin '" + nname + "' by " + nauthor + " | [" + ncat.lower() + "](" + webroot + 'res/mds/' + ncat.lower() + ".md#" + nname.lower().replace(' ', '-').replace('.', '') + ")<br>\n"
	else: # no listfile found, plugin must got deleted or renamed
		nline = ndate + " | " + nnew_or_update + " Plugin " + nname + " | Plugin got deleted or renamed <br>\n"
	allnews = allnews + nline
with open("res/allnews.md", "w") as file1: # writing allnews.md
	file1.writelines(allnews)
split_str = "\n" # setting variable news to right format and amount, to put into template
splitted_news = allnews.split(split_str)
part_news = splitted_news[:int(newsamount)]
news = split_str.join(part_news)
		


# writing the md files
with open(indexfile, "w") as file1:
	temphead = replacevar(temphead)
	temphead = replacevarp(temphead)
	file1.writelines(temphead) # writer header template
	if not os.path.isdir('res/mds/'):
		os.mkdir('res/mds/')
for cat in categories: # for each category
	with open('res/mds/' + cat.lower() + ".md", "w") as file1:
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
			if catcomp == "N/A" or catcomp == "" or catcomp == "NA":
				catcomp = "Uncategorized"
			if catcomp.capitalize() == cat:
				# get variables out of the list item p
				description = p.split("\n")
				if description[0] == "N/A" or description == "" or description == "NA":
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
					iconpath = pathtoplugins + pluginname
					iconpath = iconpath.replace("&", "%26")
					iconpath = iconpath.replace("'", "%27")
					iconpath = iconpath.replace("(", "%28")
					iconpath = iconpath.replace(")", "%29")
					iconpath = iconpath.replace(",", "%2C")
					iconpng = "<img src='../../"+ iconpath + "/icon.png' height='100'></img><br>\n"
				else:
					iconpng = ""
				# get last modified date and size from the assetfiles
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
					response = requests.head(assetfullpath + withdots + ".zip", allow_redirects=True) # get header of the release asset zips
					response.raise_for_status()
				except requests.exceptions.HTTPError as err:
					with open('res/errorlog.txt', 'a') as errorfile:
						errorfile.writelines("check release zip for plugin: " + pluginname + "\n")
					print(err)
					lastmodified = "N/A"
					size = "N/A" 
				else:
					modif = response.headers['Last-Modified'] # get last modified date
					datetime_object = datetime.strptime(modif, '%a, %d %b %Y %H:%M:%S %Z')
					lastmodified = str(datetime_object.date())
					assetsize = int(response.headers['Content-Length']) / 1024 # get file size of the assetfiles in kb or mb
					form = " kb"
					if assetsize > 1024:
						assetsize = assetsize / 1024
						form = " mb"
					size = str(round(assetsize, 2)) + form
					if directlink != "N/A": # check if plugin has direct updating and insert png
						updatecheck = "<img src='../img/check.png' width='15' ></img>"
					else:
						updatecheck = "<img src='../img/cross.png' width='15' ></img>"
				assetfile =  withdots + ".zip"
				
				# get last commit from the plugin repo
				for each in commit_p:
					if pluginname == each:
						index = commit_p.index(each)
						repo_last_commit = "(last commit " + commit_d[index] + ")"
						break
					else:
						repo_last_commit = ""
				
				
				# check for readme.md readme Readme.md readme.txt
				readme = ""
				check_readme = os.listdir(pathtoplugins + pluginname + "/")
				for each in check_readme:		
					if each.lower().find("readme") != -1:
						with open(pathtoplugins + pluginname + "/" + each) as readmefile:
							readme = "<details>\n<summary>:blue_book: Plugin readme</summary>\n<blockquote>" + readmefile.read() + "\n</blockquote>\n</details>"
							readme = readme.replace('~', '')
					
				file1.writelines(replacevarp(tempplug)) # write plugin template entry, exchanging %variables%
		file1.writelines(tempcatdownt) # write lower category template
