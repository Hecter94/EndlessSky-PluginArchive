#import sys
import math
import os
import random
try:
	from PIL import Image, ImageDraw
except ModuleNotFoundError:
	pass

patt_overlay_path = "imgparts/000 shipoverlay/"

def remap(value, fromLow, fromHigh, toLow, toHigh): 
	return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

def avg_deviation(numlist):
	totalnum = 0
	for num in numlist:
		totalnum += num
	avg = totalnum/len(numlist)
	x = 0
	for num in numlist:
		x += (num-avg)**2
	return avg, math.sqrt(x/totalnum)

def img_additive(arr1, arr2): #Probably doesn't work
	arr3 = [list(a) for a in list(arr1.copy())]
	i = 0
	for y in arr1: #y
		ii = 0
		for x in y: #x
			arr3[i][ii] = arr2[i][ii] + arr1[i][ii]
			ii += 1
		i+=1
	return arr3

def img_multiply(arr1, arr2, fraction=0):
	arr3 = [list(a) for a in list(arr1.copy())]
	a = 127 #127
	w1 = 1. + fraction
	w2 = 2 - w1
	i = 0
	for y in arr1: #y
		ii = 0
		#arr3[i]
		for x in y: #x
			arr3[i][ii] = int(((arr2[i][ii]*w1) * (arr1[i][ii]*w2))/a)
			ii += 1
		i+=1
	return arr3

def img_overlay(arr1, arr2):
	arr3 = [list(a) for a in list(arr1.copy())]
	i = 0
	for y in arr1: #y
		ii = 0
		for x in y: #x
			if arr2[i][ii] < 128:
				arr3[i][ii] = int(((arr2[i][ii] * arr1[i][ii])/127))
			else:
				arr3[i][ii] = int(255-(((255-arr2[i][ii]) * (255-arr1[i][ii]))/127))
			ii += 1
		i+=1
	return arr3

def polar_to_cartesian(angle, amplitude):
	x = amplitude * math.cos(angle)
	y = amplitude * math.sin(angle)
	return x,y

def customOpenImage(file_name):
	file_name_copy = file_name
	file_name_copy = file_name_copy.removesuffix(".PNG")
	file_name_copy = file_name_copy.removesuffix(".png")
	file_name_alt = file_name_copy + ".PNG"
	try:
		return Image.open(file_name_copy + ".png")
	except FileNotFoundError:
		return Image.open(file_name_alt)

def get_overlay_pattern(faction,palette,pattern_complexity=3,style=0,color_style=0):
	w, h = 110, 220

	if style==0:
		style = random.randint(1,4)
	shape = []
	edge_offset = 10

	start_x = random.randrange(0+edge_offset,round((w/2)-edge_offset))
	start_y = random.randrange(0+edge_offset,h-edge_offset)
	end_x = random.randrange(round((w/2)+edge_offset),w-edge_offset)
	end_y = random.randrange(0+edge_offset,h-edge_offset)
	shape.append([(start_x, start_y), (end_x, end_y)])
	if style == 1: #array (probably should move to second step)
		shape.append([(start_x, start_y+20), (end_x, end_y+20)])
		shape.append([(start_x, start_y-20), (end_x, end_y-20)])
	elif style == 2: #Random connected lines
		for n in range(pattern_complexity):
			start_x = end_x
			start_y = end_y
			end_x = random.randrange(0+edge_offset,w-edge_offset)
			end_y = random.randrange(0+edge_offset,h-edge_offset)
			shape.append([(start_x, start_y), (end_x, end_y)])
	elif style == 3: #Random connected lines + angle limits
		max_angle = 15
		max_amplitude = 40
		prev_angle = random.uniform(0,359)
		for n in range(pattern_complexity):
			start_x = end_x
			start_y = end_y
			while True:
				new_angle = random.uniform(prev_angle-max_angle, prev_angle+max_angle)
				new_dist = random.uniform(1,max_amplitude)
				#print(f"na {new_angle}, nd {new_dist}")
				end_x,end_y =  polar_to_cartesian(new_angle,new_dist)
				end_x += round(start_x)
				end_y += round(start_y)
				#print(f"nX {end_x}, nY {end_y}")
				if end_x > edge_offset and end_y > edge_offset:
					break
			#print(f"nX {end_x}, nY {end_y}")
			shape.append([(start_x, start_y), (end_x, end_y)])
	elif style == 4: #Random lines
		for n in range(pattern_complexity):
			start_x = random.randrange(0+edge_offset,w-edge_offset)
			start_y = random.randrange(0+edge_offset,w-edge_offset)
			end_x = random.randrange(0+edge_offset,w-edge_offset)
			end_y = random.randrange(0+edge_offset,h-edge_offset)
			shape.append([(start_x, start_y), (end_x, end_y)])
	
	# creating new Image object
	img = Image.new("RGBA", (w, h))
	
	color_alt = random.choice(['blue','green','magenta'])
	color_fill_list = ['red','orange','yellow',color_alt]
	col_width = random.randint(3,8)
	
	if color_style == 1:
		color_style == random.randint(1,2)

	img1 = ImageDraw.Draw(img)
	if color_style == 1: #one color per line segment
		i = 0 
		for nn in range(round(pattern_complexity/palette)):
			for n in range(palette):
				img1.line(shape[min(len(shape)-1,i)], fill=color_fill_list[n], width = col_width)
				i+=1
	elif color_style == 2: #single color
		i = 0 
		color_sel = random.randint(0,len(color_fill_list)-1)
		for nn in range(round(pattern_complexity/palette)):
			for n in range(palette):
				img1.line(shape[min(len(shape)-1,i)], fill=color_fill_list[color_sel], width = col_width)
				i+=1
	#img.show()
	#img.putalpha(127)
	if faction != None:
		global patt_overlay_path
		try:
			img.save(f"{patt_overlay_path}{faction.name}.png")
		except FileNotFoundError:
			os.makedirs(patt_overlay_path)
			img.save(f"{patt_overlay_path}{faction.name}.png")
	pass

#TODO: Train AI for generating parts to be assembled. (Or maybe not, each checkpoint is massive)
def get_sprites(setselect="human"):
	#print(os.listdir(f"imgparts/{setselect}"))
	file_list = [f for f in os.listdir(f"imgparts/{setselect}") if f.endswith(".png") or f.endswith(".PNG")]
	part_directional = [] #unsorted directional part
	part_non_directional = [] #unsorted non-directional part

	#Create catalog, assembly required before use.
	for part in file_list:
		part = part.removesuffix(".png")
		part = part.removesuffix(".PNG")
		#print("cata:", part)
		if part.endswith("-l") or part.endswith("-r"):
			if part.endswith("-l"): #if -l exist -r also should, handle later if not.
				part = part.removesuffix("-l")
				part_directional.append(part)
				#print("dir:", part)
		else:
			part_non_directional.append(part)
			#print("uni:", part)
	part_dir_dict = {}
	part_dir_dict['engine'] = []
	part_dir_dict['gun'] = []
	part_dir_dict['turret'] = []
	part_dir_dict['perimeter'] = []
	part_dir_dict['cockpit'] = []
	part_dir_dict['body'] = []
	part_dir_dict['core'] = []
	part_dir_dict['greeble'] = []
	part_dir_dict['other'] = []
	#sort by catagory
	for part in part_directional:
		part = f"imgparts/{setselect}/"+part
		if part.endswith("engine"):
			part_dir_dict['engine'].append(part)
		elif part.endswith("gun"):
			part_dir_dict['gun'].append(part)
		elif part.endswith("turret"):
			part_dir_dict['turret'].append(part)
		elif part.endswith("perimeter"):
			part_dir_dict['perimeter'].append(part)
		elif part.endswith("cockpit"):
			part_dir_dict['cockpit'].append(part)
		elif part.endswith("body"):
			part_dir_dict['body'].append(part)
		elif part.endswith("core"):
			part_dir_dict['core'].append(part)
		elif part.endswith("greeble"):
			part_dir_dict['greeble'].append(part)
		else:
			part_dir_dict['other'].append(part)
	
	part_uni_dict = {}
	part_uni_dict['engine'] = []
	part_uni_dict['gun'] = []
	part_uni_dict['turret'] = []
	part_uni_dict['perimeter'] = []
	part_uni_dict['cockpit'] = []
	part_uni_dict['body'] = []
	part_uni_dict['core'] = []
	part_uni_dict['greeble'] = []
	part_uni_dict['other'] = []
	for part in part_non_directional:
		part = f"imgparts/{setselect}/"+part
		if part.endswith("engine"):
			part_uni_dict['engine'].append(part)
		elif part.endswith("gun"):
			part_uni_dict['gun'].append(part)
		elif part.endswith("turret"):
			part_uni_dict['turret'].append(part)
		elif part.endswith("perimeter"):
			part_uni_dict['perimeter'].append(part)
		elif part.endswith("cockpit"):
			part_uni_dict['cockpit'].append(part)
		elif part.endswith("body"):
			part_uni_dict['body'].append(part)
		elif part.endswith("core"):
			part_uni_dict['core'].append(part)
		elif part.endswith("greeble"):
			part_uni_dict['greeble'].append(part)
		else:
			part_uni_dict['other'].append(part)
	return part_dir_dict,part_uni_dict

def pick_part_dir (partDir): #TODO: check and choose appropriate sprite size for category.
	#random.shuffle(partlistdir)
	#print("Dir")
	#note parts already got directory attached.
	partDir = partDir.removesuffix(".PNG")
	partDir = partDir.removesuffix(".png")
	try:
		customOpenImage(partDir+"-r")
		Lexist = True
	except FileNotFoundError:
		Lexist = False
	try:
		customOpenImage(partDir+"-l")
		Rexist = True
	except FileNotFoundError:
		Rexist = False
	#print(Lexist,Rexist)
	if Lexist and Rexist:
		part_suffix_l = "-l"
		part_suffix_r = "-r"
		part = [customOpenImage(partDir+part_suffix_l),
				customOpenImage(partDir+part_suffix_r)]
	elif Lexist and not Rexist:
		part_suffix_l = "-l"
		part_suffix_r = "-l"
		part = [customOpenImage(partDir+part_suffix_l),
				customOpenImage(partDir+part_suffix_l)]
	elif Rexist and not Lexist:
		part_suffix_l = "-r"
		part_suffix_r = "-r"
		part = [customOpenImage(partDir+part_suffix_r),
				customOpenImage(partDir+part_suffix_r)]
	else:
		part = None
	return part

#Sort bounds by smallest
def sort_bounds(newboundmin,newboundmax,sortby='x'):
	if sortby.casefold() == 'x':
		mode_sel = 0
	else:
		mode_sel = 1
	for i in range(len(newboundmin)):
		for j in range(i+1,len(newboundmin)):
			if newboundmin[i][mode_sel] < newboundmin[j][mode_sel]:
				newboundmin[i][mode_sel],newboundmin[j][mode_sel] = newboundmin[j][mode_sel],newboundmin[i][mode_sel]
				newboundmax[i][mode_sel],newboundmax[j][mode_sel] = newboundmax[j][mode_sel],newboundmax[i][mode_sel]
	return newboundmin,newboundmax

#Sort parts by smallest
def sort_parts(partlist,mode='x',minsize=0,maxsize=100):
	if mode.casefold() == 'x':
		mode_sel = 0
	else:
		mode_sel = 1
	#sortlist = [list(p.size) for p in partlist]
	for i in range(len(partlist)):
		for j in range(i+1,len(partlist)):
			if partlist[i].size[mode_sel] < partlist[j].size[mode_sel]:
				partlist[i],partlist[j] = partlist[j],partlist[i]
	npartlist = []
	for part in partlist:
		if part.size[mode_sel] > minsize and part.size[mode_sel] < maxsize:
			partcleanup = part.filename.removesuffix('.png')
			partcleanup = partcleanup.removesuffix('-l')
			partcleanup = partcleanup.removesuffix('-r')
			npartlist.append(partcleanup)
	return partlist,npartlist

#Get valid range of positions within specified bounds
def get_part_pos (partlist,newboundmin,newboundmax,mode,part,part_size,uniMode,stray=[[1,1],[1,1]],core_img=None,part_type='',placemode='symmetric'):
	if mode.casefold() == 'x':
		mode_sel = 0
	else:
		mode_sel = 1
	if part_type == 'center':
		newboundmin,newboundmax = sort_bounds(newboundmin,newboundmax,'x')
	elif part_type == 'gun':
		newboundmin,newboundmax = sort_bounds(newboundmin,newboundmax,'y')
	elif part_type == 'engine':
		newboundmin,newboundmax = sort_bounds(newboundmin,newboundmax,'y')
		newboundmin.reverse()
		newboundmax.reverse()
	valid_part = False
	h = 0
	while not valid_part:
		h += 1
		m = random.randrange(len(newboundmin))
		if part_type == 'gun':
			m = random.randrange(1,max(2,round(len(newboundmin)/2)))
		elif part_type == 'engine':
			m = random.randrange(1,max(2,round(len(newboundmin)/2)))
		elif part_type == 'center':
			m = random.randrange(1,max(2,round(len(newboundmin)/2)))
		#print(f"bminmax {mode}:",newboundmin[m][mode_sel],newboundmax[m][mode_sel])
		for n in partlist:
			if mode_sel == 0: # X pos
				rposmin = round(newboundmin[m][0]*stray[0][0])
				rposmax = round((newboundmax[m][0]*stray[0][1]))
				canvasmin = abs(part_size[0][mode_sel]/2)
				if placemode == 'asym':
					canvasmin = abs(part_size[0][mode_sel])
				canvasmax = (core_img.size[0])-part_size[0][mode_sel]*.5
				#print(f"TrueImg:    {core_img.size[0],core_img.size[1]}")
				#print(f"Compensated:{canvasmin,canvasmax}")
				#print(f"PrevBoundX: {rposmin,rposmax}")
				rposmin = max(rposmin,canvasmin)
				rposmax = min(rposmax,canvasmax)
				#print(f"NewBoundX:  {rposmin,rposmax}")
			else: # Y pos
				#rposmax = round(newboundmax[m][mode_sel]-abs(part_size[0][mode_sel]/2-core_img.size[0]))
				#rposmin = round(newboundmin[m][mode_sel]+abs(part_size[0][mode_sel]/2-core_img.size[0]))
				rposmin = round(newboundmin[m][mode_sel]*stray[1][0])
				rposmax = round(newboundmax[m][mode_sel]*stray[1][1]) 
				canvasmin = abs(part_size[0][mode_sel])
				canvasmax = (core_img.size[1])-part_size[0][mode_sel]*.5
				#print(f"TrueImg:    {core_img.size[0],core_img.size[1]}")
				#print(f"Compensated:{canvasmin,canvasmax}")
				#print(f"PrevBoundY: {rposmin,rposmax}")
				rposmin = max(rposmin,canvasmin)
				rposmax = min(rposmax,canvasmax)
				#print(f"NewBoundY:  {rposmin,rposmax}")
			#If it doesn't fit, pick a new part.
			if rposmin < rposmax: 
				valid_part = True
				break
			else:
				if not uniMode:
					part = pick_part_dir(n)
					part_size = [p.size for p in part]
				else:
					part = customOpenImage(n+"")
					part = [part, part]  
					part_size = [p.size for p in part]
		
		#If no part fits, rescale the part. Low Pri as some part might not work well resized.
		if not valid_part:
			nscale = .9
			for n in range(part_size[0][mode_sel]-1):
				#part[L/R][X/Y]
				new_size = [max(1,math.ceil(part[0].size[0] * nscale)),max(1,math.ceil(part[0].size[1] * nscale))]
				part = [p.resize(new_size) for p in part]
				part_size = [p.size for p in part]
				rposmin = round(newboundmin[m][mode_sel])
				rposmax = round(newboundmax[m][mode_sel])
				rposmin = max(rposmin,abs(part_size[0][mode_sel]/2))
				rposmax = min(rposmax,((core_img.size[mode_sel]/2)*1+mode_sel)-part_size[0][mode_sel]/2)
				canvasmin = abs((part_size[0][mode_sel]/2)*1+mode_sel)
				canvasmax = (core_img.size[mode_sel])-part_size[0][mode_sel]*.5
				rposmin = max(rposmin,canvasmin)
				rposmax = min(rposmax,canvasmax)
				if rposmin > rposmax:
					nscale -= .1
				else:
					valid_part = True
					break
		if valid_part:
			break
		#print(h)
		if h >= 50:
			part = [Image.new('RGBA',[1,1],'black') for i in range(2)]
			part_size = [p.size for p in part]
			if mode_sel == 0:
				rposmin = round(newboundmin[m][0]*stray[0][0])
				rposmax = round((newboundmax[m][0]*stray[0][1]))
				canvasmin = abs(part_size[0][mode_sel]/2)
				canvasmax = (core_img.size[0])-part_size[0][mode_sel]*.5
				rposmin = max(rposmin,canvasmin)
				rposmax = min(rposmax,canvasmax)   
			else:
				rposmin = round(newboundmin[m][mode_sel]*stray[1][0])
				rposmax = round(newboundmax[m][mode_sel]*stray[1][1]) 
				canvasmin = abs(part_size[0][mode_sel])
				canvasmax = (core_img.size[1])-part_size[0][mode_sel]*.5
				rposmin = max(rposmin,canvasmin)
				rposmax = min(rposmax,canvasmax)
			break
	#print(f"bminmax {mode}:",newboundmin[m][mode_sel],newboundmax[m][mode_sel])
	return part,part_size,rposmin,rposmax

def place_parts(core_img,
			part_list,
			count,
			symmetric=True,
			center=False,
			part_type='random',
			boundmin=[0,0],
			boundmax=[0,0],
			dir_chance = .5,
			weightX = .3,
			scaleRange = [1,1],
			pattern=None,
			clustermode = False,
			bounddict={},
			inputdictonly=False):

	width,height = core_img.size
	centW = round(width/2)
	centH = round(height/2)
	weightXAsym = centW
	if boundmax == [0,0]:
		boundmax = core_img.size
	count = round(count)

	#print("DictIn:",bounddict)
	part_dir_dict = part_list[0]
	part_uni_dict = part_list[1]

	bound_constrainX = .75
	bound_constrainY = 1 #Don't go below engine_min_H
	bound_minX = .8
	bound_minY = .8
	engine_min_H = .7
	gun_max_H = .2 #def .5
	gun_max_W = .2
	straypercentX = 1
	straypercentY = 1
	#=============================PART SELECTION
	haveparts = False
	if part_type == 'random':
		while not haveparts:
			part_type = random.choice(list(part_dir_dict.keys()))
			partlistdir = part_dir_dict[part_type] #directional
			partlistuni = part_uni_dict[part_type] #non-directional
			haveparts = len(partlistdir) != 0 or len(partlistuni) != 0
	partlistdir = part_dir_dict[part_type] #directional
	partlistuni = part_uni_dict[part_type] #non-directional
	if center:
		dir_chance = 0
	Dirbool = random.random() <= dir_chance
	partlistobj = []
	partlistobj2 =[]
	for pfiles in part_dir_dict[part_type]:
		partlistobj.append(customOpenImage(pfiles+"-l"))
	for pfiles in part_uni_dict[part_type]:
		partlistobj2.append(customOpenImage(pfiles+""))
	partlistobj,partlistname = sort_parts(partlistobj,'y',0,core_img.size[0]*.65)
	partlistobj2,partlistname2 = sort_parts(partlistobj2,'y',0,core_img.size[0]*.65)
	if len(partlistname) > 0:
		partlistdir = partlistname
	if len(partlistname2) > 0:
		partlistuni = partlistname2
	if len(partlistdir) == 0 and len(partlistuni) == 0:
		print(f"WARN: Parts for {part_type} not found, skipping.")
		hardpoint = [0,0]
		return core_img,bounddict,hardpoint
	random.shuffle(partlistdir)
	random.shuffle(partlistuni)
	uniMode = False
	part = None
	# while (part == None and (len(partlistdir) != 0 or len(partlistuni) != 0)):
	if Dirbool:
		if(len(partlistdir) != 0):
			part = pick_part_dir(partlistdir[0])
		else:
			part = customOpenImage(partlistuni[0]+"")
			part = [part,
					part]
			uniMode = True
	else:
		if(len(partlistuni) == 0):
			part = pick_part_dir(partlistdir[0])
		else:
			part = customOpenImage(partlistuni[0]+"")
			part = [part,
					part]
			uniMode = True
	if (part == None):
		print(f"WARN: Error when loading image for {part_type}, skipping.")
		hardpoint = [0,0]
		return core_img,bounddict,hardpoint
	#==============================================PART SCALING
	scale_rand = random.uniform(scaleRange[0],scaleRange[1])
	if part_type == "greeble":
		scale_rand = random.uniform(scaleRange[0]/5,scaleRange[1]/2)
	Rescale = True
	while Rescale:
		new_size = [round(part[0].size[0] * scale_rand), round(part[0].size[1] * scale_rand)]
		# part[Left/Right][Width,height]
		part = [p.resize(new_size) for p in part]
		part_size = [p.size for p in part]
		for n in range(len(part_size)):
			if part_size[n][0] > centW*1:
				scale_rand -= .1
			elif part_size[n][1] > centH*1:
				scale_rand -= .1
			else:
				Rescale = False
	#Coord base on center of image for X, top for Y sry for weird coordinate  
	#Basically it always gets mirrored on X, for Y I'm too lazy to mess with negatives.
	if clustermode:
		default_bound_min = [centW*(1-bound_minX),centH*(1-bound_minY)] #to leave some empty pixels on the edge, hopefully.    
		default_bount_max = [(centW*bound_constrainX),(height*bound_constrainY)]
	else:
		default_bound_min = [centW*(1-bound_minX),centH*(1-bound_minY)] #to leave some empty pixels on the edge, hopefully.    
		default_bount_max = [(centW*bound_constrainX),(height*bound_constrainY)]
	
	#area for the part to be placed.
	if boundmax == [0,0] and not clustermode:
		if part_type == 'gun':
			boundmin = [default_bound_min[0],part_size[0][1]+5]
			boundmax = [width*gun_max_W,(height*gun_max_H)+part_size[0][1]]
		elif part_type == 'engine':
			boundmin = [part_size[0][0],(centH*engine_min_H)-part_size[0][1]]
			boundmax = default_bount_max
		elif part_type == 'turret':
			boundmin = [p*.7 for p in default_bound_min]
			boundmax = [p*.7 for p in default_bount_max]
		elif part_type == 'greeble':
			boundmin = [default_bound_min[0]*0,(centH*engine_min_H)-part_size[0][1]]
			boundmax = [default_bount_max[0]/2,default_bount_max[1]*.7]
			straypercentX = .1
			straypercentY = .7
		else:
			boundmin = [0+part_size[0][0],0+part_size[0][1]]
			boundmax = default_bount_max
	
	loop = 0
	if len(bounddict.keys()) > 0:
		newboundmin = bounddict['min']
		newboundmax = bounddict['max']
	else:
		newboundmin = []
		newboundmax = []
		

	hardpoint = {}
	#trimodefuncX = -math.sqrt(boundmax[0])
	#trimodefuncY = (boundmin[1]+boundmax[1])/2
	gaussmode = True
	staticcount = count
	tocorner = 0
	c = 0
	b = 0
	if uniMode:
		partlistany = partlistuni
	else:
		partlistany = partlistdir
	if symmetric and not center:
		#place in pairs
		i = 0
		while count > 1:
			#Randomized Pos
			#clustermode will place parts within area of previous part.
			if len(newboundmin) == 0 or not clustermode:
				rXmin = round(centW)
				#rXmin = max(centW,rXmin)
				if gaussmode:
					rXmax = round(boundmax[0]+1-part_size[0][0]/2)
					rXavg,rXdv = avg_deviation([rXmin,rXmax])
					randX = round(random.gauss(rXmin,rXdv*10))
					randX = min(randX,rXmax)
					randX = max(randX,rXmin)
					rYmin = round(boundmin[1])
					rYmax = round(boundmax[1]+1-part_size[0][1]/2)
					rYavg,rYdv = avg_deviation([rYmin,rYmax])
					randY = round(random.gauss(rYmax/2,rYdv*5))
					randY = min(randY,rYmax)
					randY = max(randY,rYmin)
				else:
					rXmax = round(boundmax[0]+1-part_size[0][0]/2)
					randX = round(random.triangular(rXmin,rXmax,rXmin))
					rYmin = round(boundmin[1])
					rYmax = round(boundmax[1]+1-part_size[0][1]/2)
					randY = round(random.randrange(rYmin,rYmax))
			else:
				
				#NOTE:y is overriding X, might cause problems.
				if inputdictonly: #dict from input
					part,part_size,rXmin,rXmax = get_part_pos(partlistany,bounddict['min'],bounddict['max'],'x',part,part_size,uniMode,core_img=core_img,part_type=part_type)
				else: #dict updated with recently placed
					part,part_size,rXmin,rXmax = get_part_pos(partlistany,newboundmin,newboundmax,'x',part,part_size,uniMode,core_img=core_img,part_type=part_type)
				rXmin = max(centW+part_size[0][0]/2,rXmin)
				randX = round(random.triangular(rXmin,rXmax))
				
				mu = 0
				kappa = 4
				#randN = random.vonmisesvariate(mu,kappa)
				#randX = remap(randN,0,6,rXmin,rXmax)
				cc = min(4,round(((width*.7)/(part_size[0][0]/2))/(staticcount/2)))
				if cc != 0:
					if tocorner % cc == 0:
						randX = rXmax
						c += 1 
				randX = min(randX,rXmax)
				randX = round(max(randX,rXmin))
				if inputdictonly:
					part,part_size,rYmin,rYmax = get_part_pos(partlistany,bounddict['min'],bounddict['max'],'y',part,part_size,uniMode,core_img=core_img)
				else:
					part,part_size,rYmin,rYmax = get_part_pos(partlistany,newboundmin,newboundmax,'y',part,part_size,uniMode,core_img=core_img)
				randY = round(random.triangular(rYmin,rYmax)) #.1 weight make more vertical
				cb = round(((height*1)/(part_size[0][1]/2))/(staticcount/4))
				#randN = random.vonmisesvariate(mu,kappa)
				#randY = remap(randN,0,6,rYmin,rYmax)
				if cb != 0:
					if tocorner % cb == 0:
						b += 1
						if b % 2 == 0:
							randY = rYmax
						else:
							randY = rYmin
				randY = min(randY,rYmax)
				randY = round(max(randY,rYmin))
				tocorner += 1
				#print(f"X:{rXmin,rXmax}")
				#print(f"Y:{rYmin,rYmax}")
			#print(f"Sel:{[randX,randY]}")
			#NOTE: Y is sometimes slightly less than it should for some reason.
			posX = randX - round(part_size[0][0]/2) #+ centW
			posY = randY - round(part_size[0][1]/2) #+ centH #note pre=off
			core_img.paste(part[1],(posX, posY),part[1])
			newboundmin.append([posX,posY])
			#print(f"Newmin:{[posX,posY]}")
			nposX = randX + round(part_size[0][0]/2) #+ centW
			nposY = randY + round(part_size[0][1]/2) #+ centH
			newboundmax.append([nposX,nposY])
			#print(f"Newmax:{[nposX,nposY]}")
			if part_type == 'n':
				print(f"{part_type}:{randX,randY}")
				print(f"{part_type}:{posX,posY}")
				print(f"{part_type}:{nposX,nposY}")
				debugpart = customOpenImage("imgparts/human/qs-perimeter-r"+"")
				core_img.paste(debugpart,(posX, posY),debugpart)
				debugpart2 = customOpenImage("imgparts/human/qs-perimeter-rd"+"")
				core_img.paste(debugpart2,(nposX, nposY),debugpart2)
			#symX = centW - round(part_size[1][0]/2) - randX
			symX = width- round(part_size[1][0]/2) - randX + 1#it was 1 px off for some reason.
			core_img.paste(part[0],(symX, posY),part[0])
			if part_type == 'gun' or part_type == 'turret':
				hardpoint[i] = [randX-centW,posY-centH]
				hardpoint[i+1] = [symX-centW,posY-centH]
			elif part_type == 'engine':
				hardpoint[i] = [randX-centW,nposY-centH]
				hardpoint[i+1] = [symX-centW,nposY-centH]
			count -= 2
			i += 2
			#core_img.save(f'generatedsprites/stp{count}.png')

		#place single in the middle
		if count == 1:
			randX = centW
			if len(newboundmin) == 0 or not clustermode:
				rYmin = round(boundmin[1])
				rYmax = round(boundmax[1]+1)
				#
				canvasmin = abs(part_size[0][1]/2)
				canvasmax = (core_img.size[0])-part_size[0][1]*.5
				rposmin = max(rYmin,canvasmin)
				rposmax = min(rYmax,canvasmax)
				randY = random.randrange(round(rYmin),round(rYmax))
			else:
				#partlistuni should've been shuffled already, so should still be random.
				npart_type = part_type
				if part_type == 'cockpit':
					npart_type = 'center'
				part,part_size,rYmin,rYmax = get_part_pos(partlistuni,newboundmin,newboundmax,'y',part,part_size,uniMode=True,core_img=core_img,part_type=npart_type)
				
			randY = round(random.randrange(round(rYmin),round(rYmax+1))) 
			posX = randX - round(part_size[0][0]/2) #+ centW
			posY = randY - round(part_size[0][1]/2)
			core_img.paste(part[0],(posX, posY),part[0])

			newboundmin.append([posX,posY])
			#print(f"Newmin:{[posX,posY]}")
			nposX = randX + round(part_size[0][0]/2) #+ centW
			nposY = randY + round(part_size[0][1]/2)
			newboundmax.append([nposX,nposY])

			#DEBUG
			if part_type == 'n':
				print(f"core:{randX,randY}")
				print(f"core:{posX,posY}")
				print(f"core:{nposX,nposY}")
				debugpart = customOpenImage("imgparts/human/qs-perimeter-r"+"")
				core_img.paste(debugpart,(posX, posY),debugpart)
				debugpart = customOpenImage("imgparts/human/qs-perimeter-rd"+"")
				core_img.paste(debugpart,(nposX, nposY),debugpart)
			
			#print(f"Newmax:{[nposX,nposY]}")
			if part_type == 'gun' or part_type == 'turret':
				hardpoint[staticcount-count] = [0,posY-centH]
			elif part_type == 'engine':
				hardpoint[staticcount-count] = [0,nposY-centH]
			count -= 1
			#core_img.save(f'generatedsprites/stp{count}.png')
	#===========================CENTER MODE
	elif center:
		while count > 0:
			if pattern != None:
				randX = 0
				if len(newboundmin) == 0 or not clustermode:
					randY = round(random.randrange(round(boundmin[1]),round(boundmax[1]+1)))
				else:
					m = random.randrange(len(newboundmin))
					randY = round(random.randrange(round(newboundmin[m][1]),round(min(boundmax[1],newboundmax[m][1]))))
				randX += pattern[loop][0]*part_size[0][0]
				randY += pattern[loop][1]*part_size[0][1]
			else:
				randX = 0
				if len(newboundmin) == 0 or not clustermode:
					rYmin = round(boundmin[1]+part_size[0][1]/2)
					rYmax = round(boundmax[1]+1-part_size[0][1]/2)
					randY = round(random.randrange(rYmin,rYmax))
				else:
					part,part_size,rYmin,rYmax = get_part_pos(partlistuni,newboundmin,newboundmax,'y',part,part_size,uniMode=True,core_img=core_img)
					randY = round(random.randrange(rYmin,rYmax))
			posX = randX - round(part_size[0][0]/2)
			posY = randY - round(part_size[0][1]/2) #+ centH
			core_img.paste(part[0],(posX + centW, posY),part[0])
			#symX = centW - round(part_size[0]/2) - randX 
			newboundmin.append([posX,posY])
			#print(f"Newmin:{[posX,posY]}")
			nposX = randX + round(part_size[0][0]/2) + centW
			nposY = randY + round(part_size[0][1]/2)
			newboundmax.append([nposX,nposY])
			#print(f"Newmax:{[nposX,nposY]}")
			#symY = posY
			count -= 1
			loop += 1
	#===============================ASYMMETRIC MODE
	else:
		while count > 0:
			if len(newboundmin) == 0 or not clustermode:
				rXmin = round(centW)
				#rXmin = max(centW,rXmin)
				if gaussmode:
					rXmax = round(boundmax[0]+1-part_size[0][0]/2)
					rXavg,rXdv = avg_deviation([rXmin,rXmax])
					randX = round(random.gauss(rXmin,rXdv*10))
					randX = min(randX,rXmax)
					randX = max(randX,rXmin)
					rYmin = round(boundmin[1])
					rYmax = round(boundmax[1]+1-part_size[0][1]/2)
					rYavg,rYdv = avg_deviation([rYmin,rYmax])
					randY = round(random.gauss(rYmax/2,rYdv*5))
					randY = min(randY,rYmax)
					randY = max(randY,rYmin)
				else:
					rXmax = round(boundmax[0]+1-part_size[0][0]/2)
					randX = round(random.triangular(rXmin,rXmax,rXmin))
					rYmin = round(boundmin[1])
					rYmax = round(boundmax[1]+1-part_size[0][1]/2)
					randY = round(random.randrange(rYmin,rYmax))
			else:
				if uniMode:
					partlistany = partlistuni
				else:
					partlistany = partlistdir
				part,part_size,rXmin,rXmax = get_part_pos(partlistany,newboundmin,newboundmax,'x',part,part_size,uniMode,core_img=core_img,part_type=part_type,placemode='asym')
				randX = round(random.triangular(rXmin,rXmax))
				part,part_size,rYmin,rYmax = get_part_pos(partlistany,newboundmin,newboundmax,'y',part,part_size,uniMode,core_img=core_img)
				randY = round(random.triangular(rYmin,rYmax))
			posX = randX - round(part_size[0][0]/2) #+ round(centW*.7)
			posY = randY - round(part_size[0][1]/2) #+ centH
			side_sel = 1
			if centW-posX > 0:
				side_sel = 0
			core_img.paste(part[side_sel],(posX, posY),part[0])
			newboundmin.append([posX,posY])
			#print(f"Newmin:{[posX,posY]}")
			nposX = randX + round(part_size[0][0]/2)
			nposY = randY + round(part_size[0][1]/2)
			newboundmax.append([nposX,nposY])
			#print(f"Newmax:{[nposX,nposY]}")
			if part_type == 'gun' or part_type == 'turret':
				hardpoint[staticcount-count] = [(randX/2)-centW,posY-centH]
				#hardpoint[i+1] = [symX-centW,posY]
			elif part_type == 'engine':
				hardpoint[staticcount-count] = [(randX/2)-centW,nposY-centH]
				#hardpoint[i+1] = [symX-centW,nposY]
			count -= 1
	bounddict = {}
	bounddict['min'] = newboundmin.copy()
	bounddict['max'] = newboundmax.copy()
	return core_img,bounddict,hardpoint

def generate_sprite(faction,category="Heavy Warship",width=0,height=0,part_list=[],gun=0,turret=0,enginesp=0):
	stacktype = 2
	symmode = True
	if faction != None:
		symmode = faction.shipsymmode
		
	#TODO consider ship data
	if width == 0 or height == 0:
		if category == "Drone" or category == "Fighter":
			width = random.randrange(80,100,2)
			height = random.randrange(80,100,2)
		elif category == "Interceptor":
			width = random.randrange(100,120,2)
			height = random.randrange(100,120,2)
		elif category == "Light Warship" or category == "Light Freighter":
			width = random.randrange(120,200,2)
			height = random.randrange(120,200,2)
		elif category == "Medium Warship":
			width = random.randrange(170,260,2)
			height = random.randrange(170,260,2)
		elif category == "Heavy Warship" or category == "Heavy Freighter":
			width = random.randrange(200,420,2)
			height = random.randrange(260,420,2)
		elif category == "Transport":
			width = random.randrange(120,260,2)
			height = random.randrange(120,260,2)

	width = int(math.ceil((width*faction.lenwid) / 2) * 2)
	height = int(math.ceil((height*1-faction.lenwid) / 2) * 2)
	if category == "Drone" or category == "Fighter":
		stacktype = 3
	elif category == "Interceptor":
		stacktype = 3
	elif category == "Light Warship" or category == "Light Freighter":
		stacktype = 3
	engine = max(1,round(enginesp/100)) #TODO: factor in overall outfitspace or mass?

	print(f"Generating ship {category} with size {width,height}")
	part_dir_dict = part_list[0]
	part_uni_dict = part_list[1]
	centW = round(width/2)
	centH = round(height/2)
	gpoints = {}
	tpoints = {}

	pcs = (width*height)/(260*260) #ratio of pieces to place to HWdefault

	new_img = Image.new('RGBA', (width,height))

	#patternformat = [[OriginXY],[TranslationXY],...] in sprite size ratio. TODO: Turn into a function.
	#pattern_Hline = [[0,0],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1],[0,1]]
	# 
	
	#TODO: Pack all setting variables into one.
	if stacktype == 1: #Decent without clustermode.
		new_img,bounddict = place_parts(new_img,part_list,count=4,part_type='engine')
		new_img,bounddict = place_parts(new_img,part_list,count=1,part_type='core',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=4,part_type='gun',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='perimeter',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=32,part_type='body',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='body',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=8,part_type='body',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='greeble',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=16,part_type='greeble',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=1,part_type='turret',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=6,part_type='turret',bounddict=bounddict)
		new_img,bounddict = place_parts(new_img,part_list,count=1,part_type="cockpit",bounddict=bounddict)
	elif stacktype == 2:
		new_img,bounddictc,a = place_parts(new_img,part_list,count=1,part_type='core',boundmin=[0,centH],boundmax=[0,centH])
		#new_img,bounddictc = place_parts(new_img,part_list,count=4,part_type='body',bounddict=bounddictc)
		new_img,bounddictb,a = place_parts(new_img,part_list,count=64*pcs,part_type='body',bounddict=bounddictc,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='body',bounddict=bounddictc,
																					clustermode=True,symmetric=symmode)
		new_img,bdg,gpoints = place_parts(new_img,part_list,count=gun,part_type='gun',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bde,epoints = place_parts(new_img,part_list,count=engine,part_type='engine',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='perimeter',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=8*pcs,part_type='body',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=0,part_type='greeble',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,tpoints = place_parts(new_img,part_list,count=turret,part_type='turret',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=1,part_type='cockpit',bounddict=bounddict,
																					clustermode=True,symmetric=symmode)
	elif stacktype == 3: #LW or less
		new_img,bounddictc,a = place_parts(new_img,part_list,count=1,part_type='core',boundmin=[0,centH],boundmax=[0,centH])
		#new_img,bounddictc = place_parts(new_img,part_list,count=4,part_type='body',bounddict=bounddictc)
		new_img,bounddictb,a = place_parts(new_img,part_list,count=4,part_type='body',bounddict=bounddictc,
																					clustermode=True,symmetric=symmode)
		new_img,bdg,gpoints = place_parts(new_img,part_list,count=gun,part_type='gun',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bde,epoints = place_parts(new_img,part_list,count=engine,part_type='engine',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=2,part_type='perimeter',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=4,part_type='body',bounddict=bounddictb,
																					clustermode=True)
		new_img,bounddict,tpoints = place_parts(new_img,part_list,count=turret,part_type='turret',bounddict=bounddictb,
																					clustermode=True,symmetric=symmode)
		new_img,bounddict,a = place_parts(new_img,part_list,count=1,part_type='cockpit',bounddict=bounddict,
																					clustermode=True,symmetric=symmode)
	elif stacktype == 99:
		new_img,bounddictc,a = place_parts(new_img,part_list,count=1,part_type='core')
		new_img,bounddictb,a = place_parts(new_img,part_list,count=2,part_type='body',bounddict=bounddictc,
																					clustermode=True)
	if faction != None:
		global patt_overlay_path
		patt_overlay = customOpenImage(f"{patt_overlay_path}{faction.name}")
		pto_x = random.randrange(0,width/2)
		pto_y = random.randrange(10,round(height*.5))
		col_img = Image.new('RGBA', (width,height), faction.shipcoloring) 
		pto_img = Image.new('RGBA', (width,height), "grey")
		#pto_img2 = Image.new('RGBA', (width,height))
		pto_img.paste(patt_overlay,(pto_x,pto_y),patt_overlay)
		if(symmode):
			pto_img = pto_img.transpose(Image.FLIP_LEFT_RIGHT)
			pto_img.paste(patt_overlay,(pto_x,pto_y),patt_overlay)
		pto_img = Image.blend(pto_img,new_img,.5)
		img_arr = list(new_img.getdata())
		img_oly = list(col_img.getdata())
		img_arr = img_multiply(img_arr,img_oly)
		img_arr2 = list(pto_img.getdata())
		img_arr3 = img_overlay(img_arr,img_arr2)
		nn_img = Image.new('RGBA', (width,height))
		img_arr3 = [tuple(a) for a in tuple(img_arr3)]
		nn_img.putdata(img_arr3)
		#nn_img.show()
		new_img = nn_img
		#new_img = Image.alpha_composite(new_img,pto_img)

	gradient = Image.linear_gradient('L')
	gradient = gradient.rotate(90)
	gradient = gradient.resize((width,height), resample=Image.BICUBIC)
	gradient = gradient.convert('RGBA')
	gradient.paste(new_img,(0,0),gradient)

	new_img = Image.blend(new_img,gradient,.5)

	#Make sure there's an empty pixel around the image.
	boarderimg = Image.new('RGBA', (width+2,height+2))
	boarderimg.paste(new_img,(1, 1),new_img)

	return boarderimg,gpoints,tpoints,epoints
	#new_img.save('test.png')
	#new_img.show()

StandaloneMode = False
TestMode = False
TestPattMode = False
if StandaloneMode:
	part_sel = input("Choose part type(default:human): ")
	if part_sel == "":
		part_sel = "human"
	cat = input("Choose category(default:Heavy Warship): ")
	if cat == "":
		cat = "Heavy Warship"
	try:
		num = int(input("Number to generate(default:5): "))
	except ValueError:
		num = 5
elif TestMode:
	part_sel = "indus a"
	cat = "Heavy Warship"
	num = 100
	#part_list=get_sprites(setselect="human") 
	part_list=get_sprites(setselect=part_sel) 
	for n in range(num):
		sprite,gpoints,tpoints,epoints = generate_sprite(None,category=cat,part_list=part_list)
		try:
			sprite.save(f'generatedsprites/{n}.png')
		except FileNotFoundError:
			os.makedirs('generatedsprites')
elif TestPattMode:
	get_overlay_pattern(None,3,8)

def call_generate_sprite(faction,category,name,gun,turret,width=0,height=0,enginesp=0):
	if faction.devmode:
		random.seed(faction.devmodeseed)
	gunlistx = []
	gunlisty = []
	turlistx = []
	turlisty = []
	engilistx = []
	engilisty = []
	part_list=get_sprites(setselect=faction.partset) 
	sprite,gpoints,tpoints,epoints = generate_sprite(faction,category,gun=gun,turret=turret,part_list=part_list,width=width,height=height,enginesp=enginesp)
	try:
		os.makedirs(f'images/ship/{faction.name}')
	except FileExistsError:
		pass
	sprite.save(f'images/ship/{faction.name}/{name}.png')
	if True:
		for i,gunxy in gpoints.items():
			#print(gunxy)
			gunlistx.append(gunxy[0])
			gunlisty.append(gunxy[1])
		for i,turxy in tpoints.items():
			turlistx.append(turxy[0])
			turlisty.append(turxy[1])
		for i,engixy in epoints.items():
			engilistx.append(engixy[0])
			engilisty.append(engixy[1])

	return gunlistx,gunlisty,turlistx,turlisty,engilistx,engilisty