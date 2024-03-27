
#Imports
from copy import copy
import math
#from math import sqrt
import glob
import random
import os
import generate_sprite_ship_PIL
import generate_weapons
import generate_outfits
import namegenerator

from struct import unpack

global ship_sprite_is_default
ship_sprite_is_default = False

#TODO: Turn into a config.
global debugMessage
debugMessage = True

def init_sales(faction):
	outfitter_output_file = f"data/{faction.name}/dev sales.txt"
	outfitter_output = open(outfitter_output_file, "a")
	outfitter_output.write('\n')
	outfitter_output.write('shipyard "eesdev"\n')
	outfitter_output.close()

def is_png(data):
	#print("IsPNG Data: ",data[1:4])
	#print("IsPNG Data: ",data[12:16])
	return ((data[1:4] == b'PNG')and (data[12:16] == b'IHDR'))

def get_png_info(data):
	if is_png(data):
		w, h = unpack('>LL', data[16:24])
		width = int(w)
		height = int(h)
	else:
		#print("Not png")
		return 0, 0
	return width, height

def randomizeSprite(sprites, used_sprites, ship_type,faction):
	#print("Randomize sprite for:",ship_type)
	#print("List:",sprites)
	global ship_sprite_is_default
	if len(sprites) != 0:
		ship_sprite = random.choice(sprites)
		i = 0
		for s in used_sprites:
			i += 1
			if s == ship_sprite and (i <= len(sprites)):
				#print("Same sprite as previous ship, rechoosing..")
				ship_sprite = random.choice(sprites)
		used_sprites.append(ship_sprite)
		ship_sprite_path = "ship/"+ ship_sprite
		thumb_sprite_path = "thumbnail/"+ship_sprite
		ship_sprite_is_default = False
		
	else:
		print("No sprite within category, using default.")
		ship_sprite_is_default = True
		ship_sprite = 'sparrow'
		if ship_type == 'Interceptor':
			ship_sprite = 'sparrow'
		elif ship_type == 'Light Warship':
			ship_sprite = 'quicksilver'
		elif ship_type == 'Medium Warship':
			ship_sprite = 'mule'
		elif ship_type == 'Heavy Warship':
			ship_sprite = 'leviathan'
		elif ship_type == 'Light Freighter':
			ship_sprite = 'star barge'
		elif ship_type == 'Heavy Freighter':
			ship_sprite = 'bulk freighter'
		elif ship_type == 'Transport':
			ship_sprite = 'shuttle'
		elif ship_type == 'Fighter':
			ship_sprite = 'lance'
		elif ship_type == 'Drone':
			ship_sprite = 'combat drone'
		ship_sprite_path = "ship/"+ship_sprite
		thumb_sprite_path = "thumbnail/"+ship_sprite
	return ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path

def roundup1000(x):
	return int(math.ceil(x / 1000.0)) * 1000
def roundup100(x):
	return int(math.ceil(x / 100.0)) * 100
def roundup10(x):
	return int(math.ceil(x / 10.0)) * 10
def roundup5(x):
	return int(math.ceil(x / 5.0)) * 5

def remap(value, fromLow, fromHigh, toLow, toHigh): 
	return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


#Deletes Files
#filelist = glob.glob(os.path.join("output/", "*.txt"))
#for f in filelist:
#    os.remove(f)

class class_ship():
	def __init__(self,name,sprite,spritepath,thumb,thumbnailpath,category,cost,shields,hull,reqcrew,bunk,mass,drag,heat_diss,fuel,cargo_cap,outfit_cap,weapon_cap,engine_cap) -> None:
		self.name = name
		self.noun = None
		self.sprite = sprite
		self.spritepath = spritepath
		self.thumbnail = thumb
		self.thumbnailpath = thumbnailpath
		self.category = category
		self.cost = cost
		self.shields = shields
		self.hull = hull
		self.reqcrew = reqcrew
		self.bunk = bunk
		self.mass = mass
		self.drag = drag
		self.heat_diss = heat_diss
		self.fuel = fuel
		self.cargo_space = cargo_cap
		self.outfit_space = outfit_cap
		self.weapon_cap = weapon_cap
		self.engine_cap = engine_cap
		self.death_weapon = {}
		#self.outfits_dict = {}
		self.outfits_list = [] #Just count dup for multiple
		self.gun_ports = 0
		self.turret_mounts = 0
		self.installed_weapons = 0
		self.carried = {}
		self.isWarship = False

#Analyze stats of their outfits so ships can be made to accomodate them
def analyze_outfits(faction):
	#faction.agg
	smallest_power = 1000000
	smallest_shield = 1000000
	smallest_energy_store = 1000000
	smallest_engine = 1000000
	smallest_gun = 1000000
	smallest_turret = 1000000
	for outfit in faction.outfitlist:
		if outfit.category == 'Power' and outfit.outfit_space < smallest_power and outfit.energy_gen > 0:
			smallest_power = outfit.outfit_space
	for outfit in faction.weaponlist:
		if outfit.category == 'Guns' and outfit.outfit_space < smallest_gun:
			smallest_gun = outfit.outfit_space
		if outfit.category == 'Turrets' and outfit.outfit_space < smallest_turret:
			smallest_turret = outfit.outfit_space
	for outfit in faction.engineslist:
		if outfit.category == 'Engines' and outfit.outfit_space < smallest_engine:
			smallest_engine = outfit.outfit_space
	if smallest_power == 1000000:
		smallest_power = 50
	if smallest_engine == 1000000:
		smallest_engine = 50
	if smallest_gun == 1000000:
		smallest_gun = 80
	if smallest_turret == 1000000:
		smallest_turret = 80
	return smallest_gun,smallest_turret,smallest_power,smallest_engine

def outfit_type(outfit):
	weaponCategories = ['Guns','Turrets','Secondary']
	if(outfit.energy_gen > 0):
		return "power gen"
	elif(outfit.energy_gen <= 0) and (outfit.energy_cap > 0):
		return "battery"
	elif(outfit.shields_gen > 0):
		return "shield gen"
	elif(outfit.hull_repair > 0):
		return "hull repair"
	elif(outfit.cooling > 0) or (outfit.active_cooling > 0):
		return "cooling"
	elif(outfit.ramscoop > 0):
		return "ramscoop"
	elif(weaponCategories.count(outfit.category)):
		return "weapon"
	else:
		return "other"

def outfit_sort(outfitlist,sortby="outfit space"):
	if sortby=="outfit space":
		for i in range(len(outfitlist)):
			for j in range(i+1,len(outfitlist)):
				if outfitlist[i].outfit_space < outfitlist[j].outfit_space:
					outfitlist[i],outfitlist[j] = outfitlist[j],outfitlist[i]
	return outfitlist

def ship_update(faction,ship,shipstats,outfit,mode,weapon=False):
	if weapon:
		weapon = outfit.weapon_type
	if mode == 'install' or mode == "Install":
		shipstats['outfit sp'] -= outfit.outfit_space
		shipstats['engine sp'] -= outfit.engine_space
		shipstats['engine energy'] += outfit.thrust_ener + outfit.turn_ener
		shipstats['engine heat'] += outfit.thrust_heat + outfit.turn_heat
		shipstats['thrust'] += outfit.thrust
		shipstats['turn'] += outfit.turn
		if weapon:
			shipstats['weapon sp'] -= outfit.weapon_space
			shipstats['weapon heat'] += outfit.fire_heat
			shipstats['weapon energy'] += outfit.fire_ener
		if weapon == "turret" or weapon == "antimissile":
			shipstats['turret free'] -= 1
		elif weapon == "gun":
			shipstats['gun free'] -= 1
		if weapon == "antimissile":
			shipstats['am count'] += 1
			shipstats['am energy'] += outfit.fire_ener * 60/outfit.reload
		shipstats['mass'] += outfit.mass
		shipstats['idle heat'] -= outfit.cooling
		shipstats['idle heat'] -= outfit.active_cooling

		shipstats['cooling ener'] += outfit.cooling_ener
		shipstats['energy storage'] += outfit.energy_cap
		shipstats['energy gen'] += outfit.energy_gen + outfit.solar_ener
		shipstats['energy use'] += outfit.energy_use
		shipstats['idle heat'] += outfit.heat_gen

		shipstats['regen energy'] += outfit.shields_ener + outfit.hull_ener
		shipstats['regen heat'] += outfit.shields_heat + outfit.hull_heat
		ship.outfits_list.append(outfit)
	elif mode == 'uninstall' or mode == "Uninstall":
		shipstats['outfit sp'] += outfit.outfit_space
		shipstats['engine sp'] += outfit.engine_space
		shipstats['engine energy'] -= outfit.thrust_ener + outfit.turn_ener
		shipstats['engine heat'] -= outfit.thrust_heat + outfit.turn_heat
		shipstats['thrust'] -= outfit.thrust
		shipstats['turn'] -= outfit.turn
		if weapon:
			shipstats['weapon sp'] -= outfit.weapon_space
			shipstats['weapon heat'] += outfit.fire_heat
			shipstats['weapon energy'] += outfit.fire_ener
		if weapon == "Turret" or weapon == "Anti-Missile":
			shipstats['turret free'] += 1
		elif weapon == "Gun":
			shipstats['gun free'] += 1
		if weapon == "Anti-Missile":
			shipstats['am count'] -= 1
			shipstats['am energy'] -= outfit.fire_ener * 60/outfit.reload
		shipstats['mass'] -= outfit.mass
		shipstats['idle heat'] += outfit.cooling
		shipstats['idle heat'] += outfit.active_cooling

		shipstats['cooling ener'] -= outfit.cooling_ener
		shipstats['energy storage'] -= outfit.energy_cap
		shipstats['energy gen'] -= outfit.energy_gen + outfit.solar_ener
		shipstats['energy use'] -= outfit.energy_use
		shipstats['idle heat'] -= outfit.heat_gen

		shipstats['regen energy'] -= outfit.shields_ener + outfit.hull_ener
		shipstats['regen heat'] -= outfit.shields_heat + outfit.hull_heat
		ship.outfits_list.pop(ship.outfits_list.index(outfit))
	pass

def outfit_install_engine(ship,shipstats,outfit):
	if shipstats['outfit sp'] >= outfit.outfit_space and shipstats['engine sp'] >= outfit.engine_space:
		ship.outfits_list.append(outfit)
		shipstats['outfit sp'] -= outfit.outfit_space
		shipstats['engine sp'] -= outfit.engine_space
		shipstats['energy use'] += outfit.thrust_ener
		shipstats['engine heat'] += outfit.thrust_heat
		shipstats['thrust'] += outfit.thrust
		shipstats['turn'] += outfit.turn
		if debugMessage:
			print(f"SHIPGEN: Install Engine [{outfit.name}]")
			print(f"OutfitSpace:{shipstats['outfit sp']}")
			print(f"EngineSpace:{shipstats['engine sp']}")
			print(f"Energy Use:{shipstats['energy use']}")
			#print(f"Energy Gen:{shipstats['energy gen']}")
			#print(f"Idle Heat:{shipstats['idle heat']}")
		return True
	else:
		if debugMessage:
			print(f"SHIPGEN: Install Engine Failed [{outfit.name}]")
			print(f"OutfitSpace:{shipstats['outfit sp']}")
			print(f"EngineSpace:{shipstats['engine sp']}")
			print(f"Energy Use:{shipstats['energy use']}")
			#print(f"Energy Gen:{shipstats['energy gen']}")
			#print(f"Idle Heat:{shipstats['idle heat']}")

def install_engine(faction,ship,shipstats,steeringlist,thrusterlist,enginelist):
	facengines = faction.engineslist
	facengines.reverse()
	for outfit in facengines: #I'll expect these to come in pairs 
		if outfit.turn > 0 and outfit.thrust > 0:
			enginelist.append(outfit) #append the object, more useful and can pull the name out later.
		else:
			if outfit.turn > 0:
				steeringlist.append(outfit)
			if outfit.thrust > 0:
				thrusterlist.append(outfit)
	enginelist = outfit_sort(enginelist)
	steeringlist = outfit_sort(steeringlist)
	thrusterlist = outfit_sort(thrusterlist)
	engine_pair_num = None
	thruster_pair_num = None
	engine_installed = False
	i = -1
	for outfit in enginelist:
		i += 1
		if(outfit.engine_space <= shipstats['engine sp']): #For Thruster+steering combo
			outfit_install_engine(ship,shipstats,outfit)
			engine_pair_num = i
			engine_installed = True
			if (faction.designpriority != "engines") or (outfit.engine_space <= shipstats['outfit sp']*.30):
				break
			#print(f"SHIPGEN: {outfit.name} equipped, {outfit.engine_space} used from {shipstats['engine sp']}")
	ii = -1
	for n in range(len(thrusterlist)):
		ii += 1
		if(shipstats['engine sp'] >= thrusterlist[n].engine_space+steeringlist[n].engine_space):
			if debugMessage:
				print(f"Engine Sp Ava:{shipstats['engine sp']}")
				print(f"Engine Sp toUse:{thrusterlist[n].engine_space+steeringlist[n].engine_space}")
			outfit_install_engine(ship,shipstats,thrusterlist[n])
			outfit_install_engine(ship,shipstats,steeringlist[n])
			thruster_pair_num = n
			engine_installed = True
			if debugMessage:
				print(f"Outfit sp left:{shipstats['outfit sp'] }")
			if (faction.designpriority != "engines"):
				break

	#If no engine fit, expand the ship.
	#TODO: Alternatively generate new, smaller engine.
	if not engine_installed:
		ship.engine_cap += (thrusterlist[ii].engine_space+steeringlist[ii].engine_space) - ship.engine_cap
		ship.outfit_space += (thrusterlist[ii].outfit_space+steeringlist[ii].outfit_space) - ship.outfit_space
		ship.outfits_list.append(thrusterlist[ii])
		ship.outfits_list.append(steeringlist[ii])

	return ship,shipstats,i,ii,engine_pair_num,thruster_pair_num

def install_antimissile(ship,shipstats,weapon):
	print(f"Installed AntiMissile {weapon.name}")
	ship.outfits_list.append(weapon)
	shipstats['weapon sp'] -= weapon.weapon_space
	shipstats['outfit sp'] -= weapon.outfit_space
	shipstats['weapon heat'] += weapon.fire_heat
	shipstats['am energy'] += weapon.fire_ener * 60/weapon.reload
	shipstats['turret free'] -= 1
	shipstats['am count'] += 1
	return ship,shipstats

def install_turret(ship,shipstats,weapon):
	print(f"Installed turret {weapon.name}")
	ship.outfits_list.append(weapon)
	shipstats['weapon sp'] -= weapon.weapon_space
	shipstats['outfit sp'] -= weapon.outfit_space
	shipstats['weapon energy'] += weapon.fire_ener * 60/weapon.reload
	shipstats['turret free'] -= 1
	ship.installed_weapons += 1
	return ship,shipstats
def install_gun(ship,shipstats,weapon):
	print(f"Installed gun {weapon.name}")
	ship.outfits_list.append(weapon)
	shipstats['weapon sp'] -= weapon.weapon_space
	shipstats['outfit sp'] -= weapon.outfit_space
	shipstats['weapon energy'] += weapon.fire_ener * 60/weapon.reload
	shipstats['weapon heat'] += weapon.fire_heat
	shipstats['gun free'] -= 1
	ship.installed_weapons += 1
	return ship,shipstats
def install_missile(ship,shipstats,weapon,faction):
	print(f"Installed Missile {weapon.name}")
	ship.outfits_list.append(weapon)
	shipstats['weapon sp'] -= weapon.weapon_space
	shipstats['outfit sp'] -= weapon.outfit_space
	shipstats['weapon energy'] += weapon.fire_ener * 60/weapon.reload
	shipstats['weapon heat'] += weapon.fire_heat
	shipstats['gun free'] -= 1
	ship.installed_weapons += 1
	launchername = weapon.name
	launchername = launchername.split()[0]
	ammo_cap = weapon.ammo_cap
	for ammo in faction.weaponlist:
		if ammo.weapon_type == 'missileammo':
			ammoname = ammo.name
			if ammoname.split()[0] == launchername.split()[0]:
				for n in range(ammo_cap):
					ship.outfits_list.append(ammo)
				break
	return ship,shipstats

def wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
	gunSpaceAva = shipstats['weapon sp'] > smallestWeapon[0] and shipstats['outfit sp'] > smallestWeapon[0]
	turretSpaceAva = shipstats['weapon sp'] > smallestWeapon[1] and shipstats['outfit sp'] > smallestWeapon[1]
	gunAvaliable = (shipstats['gun free'] >= 1 * gunExist) and gunSpaceAva
	turretAvaliable = shipstats['turret free'] >= 1 * turretExist and turretSpaceAva
	#spaceAvaliable = ((shipstats['weapon sp'] > smallestWeapon) and (shipstats['outfit sp'] > smallestWeapon))
	return (gunAvaliable or turretAvaliable)

def install_weapons(faction,ship,shipstats,weaponlist):
	c = 0  
	while (shipstats['turret free']+shipstats['gun free'] > 0) and (c < len(faction.weaponlist)):
		#print("Ship WepAdd CondChk 1: ", (shipstats['turret free']+shipstats['gun free'] > 0) )
		#print("Ship WepAdd CondChk 2: ", (c < len(faction.weaponlist) ))
		#'defense offense balance hitrun kite'
		gunExist = 0
		turretExist = 0
		nonAMTurretExist = False
		smallestGun = 9999999999
		smallestTurret = 9999999999
		for weapon in weaponlist:
			if weapon.weapon_type == "gun" or weapon.weapon_type == "missile":
				gunExist = 1
				if weapon.outfit_space < smallestGun:
					smallestGun = weapon.outfit_space
			if weapon.weapon_type == "turret" or weapon.weapon_type == "antimissile":
				turretExist = 1
				nonAMTurretExist = weapon.weapon_type == "turret"
				if weapon.outfit_space < smallestTurret:
					smallestTurret = weapon.outfit_space
		smallestWeapon = [smallestGun,smallestTurret]
		i = 0
		#TODO:Figure out better way to do this
		if faction.fleet_tactic == 'kite':
			while (wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)):
				for weapon in weaponlist:
					turretFree = bool(shipstats['turret free'] > 0)
					gunFree = bool(shipstats['gun free'] > 0)
					if (shipstats['turret free']==0) and (shipstats['gun free']==0):
						break
					if gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'missile':
						ship,shipstats = install_missile(ship,shipstats,weapon,faction)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'antimissile' and (shipstats['am count'] < 1 or not nonAMTurretExist):
						ship,shipstats = install_antimissile(ship,shipstats,weapon)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'turret':
						ship,shipstats = install_turret(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'gun':
						ship,shipstats = install_gun(ship,shipstats,weapon)
					i += 1
				if not wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
					break
		elif faction.fleet_tactic == 'hitrun':
			while (wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)):
				for weapon in weaponlist:
					turretFree = bool(shipstats['turret free'] > 0)
					gunFree = bool(shipstats['gun free'] > 0)
					if (shipstats['turret free']==0) and (shipstats['gun free']==0):
						break
					if turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'turret':
						ship,shipstats = install_turret(ship,shipstats,weapon)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'antimissile' and (shipstats['am count'] < 1 or not nonAMTurretExist):
						ship,shipstats = install_antimissile(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'gun':
						ship,shipstats = install_gun(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'missile':
						ship,shipstats = install_missile(ship,shipstats,weapon,faction)
					i += 1
				if not wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
					break
		elif faction.fleet_tactic == 'defense':
			while (wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)):
				for weapon in weaponlist:
					turretFree = bool(shipstats['turret free'] > 0)
					gunFree = bool(shipstats['gun free'] > 0)
					if (shipstats['turret free']==0) and (shipstats['gun free']==0):
						break
					if turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'antimissile' and (shipstats['am count'] < 1 or not nonAMTurretExist):
						ship,shipstats = install_antimissile(ship,shipstats,weapon)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'turret':
						ship,shipstats = install_turret(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'gun':
						ship,shipstats = install_gun(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'missile':
						ship,shipstats = install_missile(ship,shipstats,weapon,faction)
					i += 1
				if not wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
					break
		elif faction.fleet_tactic == 'offense':
			while (wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)):
				for weapon in weaponlist:
					turretFree = bool(shipstats['turret free'] > 0)
					gunFree = bool(shipstats['gun free'] > 0)
					if (shipstats['turret free']==0) and (shipstats['gun free']==0):
						break
					if gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'missile':
						ship,shipstats = install_missile(ship,shipstats,weapon,faction)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'turret':
						ship,shipstats = install_turret(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'gun':
						ship,shipstats = install_gun(ship,shipstats,weapon)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'antimissile' and (shipstats['am count'] < 1 or not nonAMTurretExist):
						ship,shipstats = install_antimissile(ship,shipstats,weapon)
					i += 1
				if not wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
					break
		else:
			while (wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)):
				res = wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist)
				for weapon in weaponlist:
					turretFree = bool(shipstats['turret free'] > 0)
					gunFree = bool(shipstats['gun free'] > 0)
					if (shipstats['turret free']==0) and (shipstats['gun free']==0):
						break
					if turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'antimissile' and (shipstats['am count'] < 1 or not nonAMTurretExist):
						ship,shipstats = install_antimissile(ship,shipstats,weapon)
					elif turretFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'turret':
						ship,shipstats = install_turret(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'gun':
						ship,shipstats = install_gun(ship,shipstats,weapon)
					elif gunFree and (weapon.weapon_space <= shipstats['weapon sp']) and weapon.weapon_type == 'missile':
						ship,shipstats = install_missile(ship,shipstats,weapon,faction)
				if not wep_install_loop_calc(shipstats,smallestWeapon,gunExist,turretExist):
					break
		c += 1
	return ship,shipstats

def get_outfit_space(outfit):
	return outfit.outfit_space

def pick_generator(faction,ship,shipstats,powergenlist,generator_percent=.5):
	chosen_generators = []

	#If no power generator exist somehow, make new one.
	if not len(powergenlist) and shipstats['outfit sp'] > 2:
		generate_outfits.create_power(faction,power_type_amount=1,min_outfit_space=2,max_outfit_space=shipstats['outfit sp'])
		for outfit in faction.outfitlist:
			if outfit_type(outfit) == "power gen":
				powergenlist.append(outfit)

	#Find Generator that fits just right.
	for outfit in powergenlist:
		if outfit.energy_gen >= shipstats['energy use'] and outfit.outfit_space <= shipstats['outfit sp']:
			chosen_generators.append(outfit)
	
	#Else make a combination of generators that works.
	if len(chosen_generators) == 0:
		maxPowerGen = 0
		n = 0
		maxGenIndex = 0
		tempPow = copy(shipstats['energy use'])
		outfit_sort(powergenlist)
		for outfit in powergenlist:
			fittableGenerators = math.floor(shipstats['outfit sp']/outfit.outfit_space)
			loopiteration = 0
			while tempPow > 0 and loopiteration < fittableGenerators:
				chosen_generators.append(outfit)
				tempPow -= outfit.energy_gen
				loopiteration += 1
			if False:
				if outfit.energy_gen > maxPowerGen:
					#tempPowList.append(outfit)
					maxGenIndex = copy(n)
					maxPowerGen = outfit.energy_gen
				n += 1
		#fittableGenerators = math.floor(shipstats['outfit sp']/powergenlist[maxGenIndex].outfit_space)
		#requiredGenerators = math.ceil(shipstats['energy use']/maxPowerGen)
		#if fittableGenerators <= requiredGenerators:
		#for n in range(requiredGenerators):
		#    chosen_generators.append(powergenlist[maxGenIndex])
			
	#Install another generator if it can fit and if faction prioritize it.
	if chosen_generators and faction.designpriority[0] == 'power':
		for outfit in powergenlist:
			if outfit.energy_gen >= chosen_generators[0].energy_gen and outfit.outfit_space >= shipstats['outfit sp']:
				chosen_generators.append(outfit)
	if len(chosen_generators):
		for generator in chosen_generators:
			just_install_generator(ship,shipstats,generator)
	else:
		if debugMessage:
			print("SHIPGEN: Install Generators Failed, no generator selected.")
			print(f"OutfitSpace:{shipstats['outfit sp']}")
			print(f"Energy Use:{shipstats['energy use']}")
			print(f"Energy Gen:{shipstats['energy gen']}")
			print(f"Idle Heat:{shipstats['idle heat']}")
	return ship,shipstats,powergenlist

def just_install_generator(ship,shipstats,outfit):
	if shipstats['outfit sp'] >= outfit.outfit_space:
		ship.outfits_list.append(outfit)
		shipstats['outfit sp'] -= outfit.outfit_space
		shipstats['energy use'] -= outfit.energy_gen
		shipstats['energy gen'] += outfit.energy_gen
		shipstats['energy storage'] += outfit.energy_cap
		shipstats['idle heat'] += outfit.heat_gen
		if debugMessage:
			print(f"SHIPGEN: Install Generator [{outfit.name}]")
			print(f"OutfitSpace/Req:{shipstats['outfit sp']}/{outfit.outfit_space}")
			print(f"Energy Use:{shipstats['energy use']}")
			print(f"Energy Gen:{shipstats['energy gen']}")
			print(f"Idle Heat:{shipstats['idle heat']}")
		return True
	else:
		if debugMessage:
			print(f"SHIPGEN: Install Generator Failed [{outfit.name}]")
			print(f"OutfitSpace/Req:{shipstats['outfit sp']}/{outfit.outfit_space}")
			print(f"Energy Use:{shipstats['energy use']}")
			print(f"Energy Gen:{shipstats['energy gen']}")
			print(f"Idle Heat:{shipstats['idle heat']}")
	return False


def install_generator(faction,ship,shipstats,powergenlist,generator_percent=.5):
	if faction.designpriority[0] == 'power':
		generator_percent += .1
	gen_loop_check = 0
	while shipstats['energy gen'] <= 0:
		for outfit in powergenlist:
			if (shipstats['energy use'] >= 0) and (outfit.outfit_space <= (shipstats['outfit sp']*generator_percent)):
				#print(f"installed {outfit.name}, space{outfit.outfit_space}/{shipstats['outfit sp']}")
				ship.outfits_list.append(outfit)
				shipstats['outfit sp'] -= outfit.outfit_space
				shipstats['energy use'] -= outfit.energy_gen
				shipstats['energy gen'] += outfit.energy_gen
				shipstats['energy storage'] += outfit.energy_cap
				shipstats['idle heat'] += outfit.heat_gen
				#Install another copy if still required.
				if (shipstats['energy use'] >= 0) and (outfit.outfit_space <= (shipstats['outfit sp']*generator_percent)):
					ship.outfits_list.append(outfit)
					shipstats['outfit sp'] -= outfit.outfit_space
					shipstats['energy use'] -= outfit.energy_gen
					shipstats['energy gen'] += outfit.energy_gen
					shipstats['energy storage'] += outfit.energy_cap
					shipstats['idle heat'] += outfit.heat_gen
				break
		if shipstats['energy use'] <= 0:
			break
		generator_percent = min(1,generator_percent + .1)
		if(shipstats['outfit sp'] == shipstats['outfit sp']*generator_percent):
			#print(f"No generator fits, {shipstats['outfit sp']}")
			if shipstats['outfit sp'] > 0:
				#print("Make new generator")
				generate_outfits.create_power(faction,power_type_amount=1,min_outfit_space=1,max_outfit_space=shipstats['outfit sp'])
				powergenlist.clear()
				for outfit in faction.outfitlist:
					if outfit_type(outfit) == "power gen" and outfit.outfit_space <= shipstats['outfit sp']:
						powergenlist.append(outfit)
						shipstats['outfit sp'] -= outfit.outfit_space
						shipstats['energy use'] -= outfit.energy_gen
						shipstats['energy gen'] += outfit.energy_gen
						shipstats['energy storage'] += outfit.energy_cap
						shipstats['idle heat'] += outfit.heat_gen
						if (shipstats['energy use'] >= 0) and (outfit.outfit_space <= (shipstats['outfit sp']*generator_percent)):
							ship.outfits_list.append(outfit)
							shipstats['outfit sp'] -= outfit.outfit_space
							shipstats['energy use'] -= outfit.energy_gen
							shipstats['energy gen'] += outfit.energy_gen
							shipstats['energy storage'] += outfit.energy_cap
							shipstats['idle heat'] += outfit.heat_gen
						if (shipstats['energy use'] <= 0):
							break
			else:
				#print("Expand ship")
				ship.outfit_space += outfit.outfit_space
				shipstats['outfit sp'] += outfit.outfit_space
		gen_loop_check += 1
		if gen_loop_check == 101:
			print("SHIPGEN[WARN]: No suitable generator.")
	return ship,shipstats,powergenlist

def install_regen(faction,ship,shipstats,shieldgenlist,hullgenlist):
	shieldgenpercent = min(1,random.gauss(.75,.1))
	if len(hullgenlist) != 0:
			shieldgenpercent = random.gauss(.5,.1)
	for outfit in shieldgenlist:
		if (outfit.outfit_space <= max(shipstats['outfit sp'],shipstats['outfit sp']*shieldgenpercent)):
			#print(f"installed {outfit.name}, space{outfit.outfit_space}/{shipstats['outfit sp']}")
			ship.outfits_list.append(outfit)
			shipstats['outfit sp'] -= outfit.outfit_space
			shipstats['regen energy'] += outfit.shields_ener
			shipstats['regen heat'] += outfit.shields_heat
			break
	for outfit in hullgenlist:
		if (outfit.outfit_space <= shipstats['outfit sp']):
			#print(f"installed {outfit.name}, space{outfit.outfit_space}/{shipstats['outfit sp']}")
			ship.outfits_list.append(outfit)
			shipstats['outfit sp'] -= outfit.outfit_space
			shipstats['regen energy'] += outfit.hull_ener
			shipstats['regen heat'] += outfit.hull_heat
			break
	return ship,shipstats

def install_battery(faction,ship,shipstats,batterylist,battthreshold=50):
	batteryInstalled = False
	for outfit in batterylist:
		if (outfit.outfit_space <= shipstats['outfit sp']) and (shipstats['energy storage'] <= battthreshold): #Just one storage
			#print(f"installed {outfit.name}, space{outfit.outfit_space}/{shipstats['outfit sp']}")
			ship.outfits_list.append(outfit)
			shipstats['outfit sp'] -= outfit.outfit_space
			shipstats['energy use'] -= outfit.energy_gen
			shipstats['energy use'] += outfit.energy_use
			shipstats['energy storage'] += outfit.energy_cap
			shipstats['idle heat'] += outfit.heat_gen
			batteryInstalled = True
			break
	if len(batterylist) and batteryInstalled:
		if debugMessage:
			print(f"SHIPGEN: Install Battery [{outfit.name}]")
			print(f"OutfitSpace/Req:{shipstats['outfit sp']}/{outfit.outfit_space}")
			print(f"Energy Cap:{shipstats['energy storage']}")
			print(f"Energy Gen:{shipstats['energy gen']}")
			print(f"Idle Heat:{shipstats['idle heat']}")
	elif len(batterylist) and not batteryInstalled:
		if debugMessage:
			print(f"SHIPGEN: Install Battery Failed")
			print(f"OutfitSpace/Req:{shipstats['outfit sp']}/{outfit.outfit_space}")
			print(f"Energy Cap:{shipstats['energy storage']}")
			print(f"Energy Gen:{shipstats['energy gen']}")
			print(f"Idle Heat:{shipstats['idle heat']}")
	elif not len(batterylist):
		if debugMessage:
			print(f"SHIPGEN: Install Battery Failed, No Battery Avaliable")

	return ship,shipstats
#Add outfits to the ship TODO*** Universal install function.
def outfit_ship(faction,ship): #TODO: Space calc is wrong, sometimes too much sometimes too few
	
	#Engines: Pair the thrust/steer then find pair that fits, so no oversized thruster and weak steer
	#shipstats['outfit sp'] = ship.outfit_space
	#shipstats['weapon sp'] = ship.weapon_cap
	#shipstats['engine sp'] = ship.engine_cap
	#shipstats['gun free'] = ship.gun_ports
	#shipstats['turret free'] = ship.turret_mounts
	print(f"SHIPGEN: {ship.name} Starting Stats")
	print(f"Outfit Space{ship.outfit_space}")
	print(f"Weapon Space{ship.weapon_cap}")
	print(f"Engine Space{ship.engine_cap}")
	shipstats = {
				"mass": 0,
				"outfit sp": ship.outfit_space,
				"weapon sp": ship.weapon_cap,
				"engine sp": ship.engine_cap,
				"gun free": ship.gun_ports,
				"turret free": ship.turret_mounts,
				"energy use": 0,
				"energy gen": 0,
				"engine energy": 0,
				"weapon energy": 0,
				"am energy": 0,
				"energy storage": 0,
				"regen energy": 0,
				"am count": 0,

				"cooling ener": 0,
				
				"idle heat": 0,
				"engine heat": 0,
				"weapon heat": 0,
				"regen heat": 0,

				"thrust": 0,
				"turn": 0,
				}

	thrusterlist = []
	steeringlist = []
	enginelist = []
	engine_pair_num = 0
	thruster_pair_num = 0

	powergenlist = []
	batterylist = []
	shieldgenlist = []
	hullgenlist = []
	h2hsmall_list = []
	h2hlarge_list = []
	
	#==============If have fuel, reserve 20 space for FTL
	if ship.fuel > 0:
		shipstats['outfit sp'] -= 20
	#==============Sort Outfits
	faction_outfitlist = faction.outfitlist
	#steeringlist,thrusterlist
	#faction_outfitlist=faction_outfitlist.reverse()
	for outfit in faction_outfitlist:
		if outfit_type(outfit) == "power gen":
			powergenlist.append(outfit)
		elif outfit_type(outfit) == "battery":
			batterylist.append(outfit)
		elif outfit_type(outfit) == "shield gen":
			shieldgenlist.append(outfit)
		elif outfit_type(outfit) == "hull repair":
			hullgenlist.append(outfit)
		elif outfit_type(outfit) == "other":
			if outfit.category == "Hand to Hand":
				if outfit.outfit_space == 0:
					h2hsmall_list.append(outfit)
				else:
					h2hlarge_list.append(outfit)
	powergenlist = outfit_sort(powergenlist)
	shieldgenlist = outfit_sort(shieldgenlist)
	hullgenlist = outfit_sort(hullgenlist)
	weaponlist = outfit_sort(faction.weaponlist)
	#==============Get pairs of Thruster/Steering
	facengines = faction.engineslist
	facengines.reverse()
	for outfit in facengines: #I'll expect these to come in pairs 
		if outfit.turn > 0 and outfit.thrust > 0:
			enginelist.append(outfit) #append the object, more useful and can pull the name out later.
		else:
			if outfit.turn > 0:
				steeringlist.append(outfit)
			if outfit.thrust > 0:
				thrusterlist.append(outfit)
	enginelist = outfit_sort(enginelist)
	steeringlist = outfit_sort(steeringlist)
	thrusterlist = outfit_sort(thrusterlist)
	ship_max_heat = (0.001 * ship.heat_diss) * ((ship.mass+(ship.outfit_space-shipstats['outfit sp'])) * 100)

	#=====================Install outfits base on faction design priority
	if False:
		for pri in faction.designpriority:
			if pri == 'engine':
				ship,shipstats,engindex,thrturindex,engine_pair_num,thruster_pair_num = install_engine(faction,ship,shipstats,steeringlist,thrusterlist,enginelist)
				print(f"SHIPGEN: Engine, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
					#print(f"SHIPGEN: {thrusterlist[n].name} equipped, {thrusterlist[n].engine_space+steeringlist[n].engine_space} used from {shipstats['engine sp']}")
			elif pri == 'weapon':
				ship,shipstats = install_weapons(faction,ship,shipstats,weaponlist)
				print(f"SHIPGEN: Weapon, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
			elif pri == 'power':
				#generator_percent = .5
				#ship,shipstats,powergenlist = install_generator(faction,ship,shipstats,powergenlist)
				ship,shipstats,powergenlist = pick_generator(faction,ship,shipstats,powergenlist)
				ship,shipstats = install_battery(faction,ship,shipstats,batterylist)
				print(f"SHIPGEN: Power, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
			elif pri == 'defense':
				ship,shipstats = install_regen(faction,ship,shipstats,shieldgenlist,hullgenlist)
				print(f"SHIPGEN: Defense, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#New Outfitting Method, install power-using things first by order of importance to functionality.

	#Install Engine
	ship,shipstats,engindex,thrturindex,engine_pair_num,thruster_pair_num = install_engine(faction,ship,shipstats,steeringlist,thrusterlist,enginelist)
	if debugMessage:
		print(f"SHIPGEN: Engine, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
		print(f"SHIPGEN: {thrusterlist[thrturindex].name} equipped, {thrusterlist[thrturindex].engine_space+steeringlist[thrturindex].engine_space} used")

	
	#Warship will install weapon first, non-warship install defense first.
	if ship.isWarship:
		#Install Weapons
		ship,shipstats = install_weapons(faction,ship,shipstats,weaponlist)
		print(f"SHIPGEN: Weapon, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")

		#Install Defense
		ship,shipstats = install_regen(faction,ship,shipstats,shieldgenlist,hullgenlist)
		print(f"SHIPGEN: Defense, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	else:
		#Install Defense
		ship,shipstats = install_regen(faction,ship,shipstats,shieldgenlist,hullgenlist)
		print(f"SHIPGEN: Defense, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")

		#Install Weapons
		ship,shipstats = install_weapons(faction,ship,shipstats,weaponlist)
		print(f"SHIPGEN: Weapon, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
		
	ship,shipstats,powergenlist = pick_generator(faction,ship,shipstats,powergenlist)
	ship,shipstats = install_battery(faction,ship,shipstats,batterylist)
	print(f"SHIPGEN: Power, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")

	#print(f"Postinit spaceleft: {shipstats['outfit sp']}")
	#Check if it have enough energy gen/store
	print(f"SHIPGEN: PreEStore, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']}")
	#IF not enough energy gen is installed, it probably can't because something is too big.
	#Find a suitable energy gen and space required for that outfit then try to make space
	# for it by downgrading other non-essentials like shield gen and hull repairs.
	#TODO:Allow picking engines or weapons to downgrade based on faction priority.
	#Not considering batteries because it was installed after the powergen.
	if (shipstats['energy use'] > 0):
		outfitspaceRequired = 0
		selectedPowGen = None
		reversedPowgenList = reversed(powergenlist)
		for outfit in reversedPowgenList:
			if outfit.energy_gen >= shipstats['energy use'] and shipstats['outfit sp'] < outfit.outfit_space:
				outfitspaceRequired = outfit.outfit_space - shipstats['outfit sp']
				selectedPowGen = outfit
				break
		for outfit in ship.outfits_list:
			if outfit_type(outfit) == "shield gen" :
				if debugMessage:
					print("Downgrading Shield Gen")
				enoughOutfitSpace = outfit.outfit_space > outfitspaceRequired
				#Figure out if there's smaller outfit that can fit and still have space avaliable.
				outfitOK = False
				if enoughOutfitSpace:
					currentIndex = shieldgenlist.index(outfit)
					while(currentIndex > 0):
						newOutfit = shieldgenlist[currentIndex-1]
						currentIndex -= 1
						if outfit.outfit_space - newOutfit.outfit_space >= outfitspaceRequired:
							outfitOK = True
							break
				if outfitOK:
					if debugMessage:
						print("Downgraded Shield Gen")
					ship_update(faction,ship,shipstats,outfit,"uninstall",weapon=False)
					ship_update(faction,ship,shipstats,newOutfit,"Install",weapon=False)
			elif outfit_type(outfit) == "hull repair" :
				if debugMessage:
					print("Downgrading Hull Repair")
				enoughOutfitSpace = outfit.outfit_space > outfitspaceRequired
				#Figure out if there's smaller outfit that can fit and still have space avaliable.
				outfitOK = False
				if enoughOutfitSpace:
					currentIndex = hullgenlist.index(outfit)
					while(currentIndex > 0):
						newOutfit = hullgenlist[currentIndex-1]
						currentIndex -= 1
						if outfit.outfit_space - newOutfit.outfit_space >= outfitspaceRequired:
							outfitOK = True
							break
				if outfitOK:
					if debugMessage:
						print("Downgraded Hull Repair")
					ship_update(faction,ship,shipstats,outfit,"uninstall",weapon=False)
					ship_update(faction,ship,shipstats,newOutfit,"Install",weapon=False)
			elif outfit_type(outfit) == "weapon":
				if debugMessage:
					print("Downsizing Weapon")
				enoughOutfitSpace = outfit.outfit_space > outfitspaceRequired
				#Figure out if there's smaller outfit that can fit and still have space avaliable.
				outfitOK = False
				if enoughOutfitSpace:
					currentIndex = weaponlist.index(outfit)
					while(currentIndex > 0):
						newOutfit = weaponlist[currentIndex-1]
						currentIndex -= 1
						weaponSameType = outfit.weapon_type == newOutfit.weapon_type
						if outfit.outfit_space - newOutfit.outfit_space >= outfitspaceRequired and weaponSameType:
							outfitOK = True
							break
				#Uninstall weapon first, if warship just make new weapon to fit.
				ship_update(faction,ship,shipstats,outfit,"uninstall",weapon=True)
				if outfitOK:
					if debugMessage:
						print("Downsized Weapon")
					ship_update(faction,ship,shipstats,newOutfit,"Install",weapon=True)
				if not outfitOK and ship.isWarship:
					weaponSpaceAva = shipstats['outfit sp'] - outfitspaceRequired
					if weaponSpaceAva <= 0:
						shipstats['outfit sp'] += abs(weaponSpaceAva) + 5
						shipstats['weapon sp'] += abs(weaponSpaceAva) + 5
						ship.outfit_space += abs(weaponSpaceAva) + 5
						ship.weapon_cap += abs(weaponSpaceAva) + 5
						weaponSpaceAva += abs(weaponSpaceAva) + 5
					generate_weapons.create_weapon(faction,weapon_amount = 1,weapon_min_outfit = 2, weapon_max_outfit = weaponSpaceAva)
					#Refresh weaponlist
					weaponlist = outfit_sort(faction.weaponlist)
					ship,shipstats = install_weapons(faction,ship,shipstats,weaponlist)
					print(f"Installed Smaller Weapon, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
		if selectedPowGen:
			ship_update(faction,ship,shipstats,selectedPowGen,"Install",weapon=False)
		
	#====================post outfitting check.
	if debugMessage:
		print(f"SHIPGEN: PO, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#=====================HEAT CHECK
	cl = 0
	cl_chk = 0 #Prevent infinite loop
	wep_heatf = .5
	eng_heatf = .8
	regen_heatf = .5
	totalheat = shipstats['idle heat']+(shipstats['regen heat']*regen_heatf)+(shipstats['engine heat']*eng_heatf)+(shipstats['weapon heat']*wep_heatf)
	#Check if ship is potentially overheating. Try to install existing cooling first.
	#Else generate new cooling. Else remove heat-generating outfit or downgrade reactor.
	while(totalheat > ship_max_heat*0.8) and cl_chk < 100:
		#print(f"SHIPGEN: Ship is overheating {totalheat:.1f}/{ship_max_heat*0.8:.1f}")
		#print("Checking existing cooling")
		#print(f"spaceleft: {shipstats['outfit sp']}")
		for iii in range(len(faction.outfitlist)):
			#Largest Cooling that fits
			largest_cooling = 0
			for outfit in faction.outfitlist:
				if (outfit_type(outfit) == "cooling") and (outfit.outfit_space <= shipstats['outfit sp']):
					if largest_cooling == 0:
						largest_cooling = outfit
					elif outfit.outfit_space >= largest_cooling.outfit_space and shipstats['outfit sp'] >= largest_cooling.outfit_space:
						largest_cooling = outfit
			if largest_cooling != 0:
				while(totalheat > ship_max_heat*0.8 and shipstats['outfit sp'] >= largest_cooling.outfit_space):
					#print(f"Installing {outfit.name}")
					ship.outfits_list.append(outfit)
					shipstats['outfit sp'] -= outfit.outfit_space
					shipstats['idle heat'] -= outfit.cooling
					shipstats['idle heat'] -= outfit.active_cooling
					shipstats['energy use'] += outfit.cooling_ener/2
					totalheat -= outfit.cooling
					totalheat -= outfit.active_cooling
		if (totalheat > ship_max_heat*0.8) and (shipstats['outfit sp'] > 0) and not largest_cooling:
			print("Generating new cooling")
			heatdiff = totalheat-ship_max_heat*0.8
			generate_outfits.create_cooling(faction,max_outfit_count=1,max_outfit_space=shipstats['outfit sp'],coolingmin=heatdiff)
			for outfit in faction.outfitlist:
				if (outfit_type(outfit) == "cooling") and (outfit.outfit_space <= shipstats['outfit sp']):
					if largest_cooling == 0:
						largest_cooling = outfit
					elif outfit.outfit_space >= largest_cooling.outfit_space and shipstats['outfit sp'] >= largest_cooling.outfit_space:
						largest_cooling = outfit
			if largest_cooling != 0:
				while(totalheat > ship_max_heat*0.8 and shipstats['outfit sp'] >= largest_cooling.outfit_space):
					#print(f"Installing {outfit.name}")
					ship.outfits_list.append(outfit)
					shipstats['outfit sp'] -= outfit.outfit_space
					shipstats['idle heat'] -= outfit.cooling
					shipstats['idle heat'] -= outfit.active_cooling
					shipstats['energy use'] += outfit.cooling_ener/2
					totalheat -= outfit.cooling
					totalheat -= outfit.active_cooling
		else:
			#print(f"SHIPGEN: preremv update {totalheat:.1f}/{ship_max_heat*0.8:.1f}")
			if(totalheat < ship_max_heat*0.8):
				break
			#print(f"spaceleft: {shipstats['outfit sp']}")
			if cl >= len(faction.outfitlist):
				#print("Uninstalling excess outfit")
				#exf = 0
				max_heat_gen = 0
				hot_outfit = None
				#============Check and remove non-critial stuff with the most heat gen
				for outfit1 in ship.outfits_list:
					if outfit1.energy_gen <= 0 and outfit1.thrust <=0 and outfit1.turn <= 0 and outfit1.heat_gen > max_heat_gen:
						max_heat_gen = outfit1.heat_gen
						hot_outfit = outfit1
					#exf += 1
				if hot_outfit != None:
					#=========Find the hottest and remove it.(Can't do it in above loop because it skips energy outfits.)
					for htnum in range(len(ship.outfits_list)):
						if ship.outfits_list[htnum].name == hot_outfit.name:
							#print("Hot outfit:", ship.outfits_list[htnum-1].name)
							ship.outfits_list.pop(htnum)
							shipstats['outfit sp'] += ship.outfits_list[htnum-1].outfit_space
							shipstats['idle heat'] -= ship.outfits_list[htnum-1].heat_gen
							totalheat -= ship.outfits_list[htnum-1].heat_gen
							break
				else:
					#print("Can't find one, downgrading generator")
					for outfit1 in ship.outfits_list:
						if outfit1.energy_gen > 0 and outfit1.heat_gen > max_heat_gen:
							max_heat_gen = outfit1.heat_gen
							hot_outfit = outfit1
					if hot_outfit != None:
						for htnum in range(len(ship.outfits_list)):
							try:
								if ship.outfits_list[htnum].name == hot_outfit.name:
									#print("Hot generator:", ship.outfits_list[htnum-1].name)
									ship.outfits_list.pop(htnum)
									shipstats['outfit sp'] += ship.outfits_list[htnum-1].outfit_space
									shipstats['energy use'] += ship.outfits_list[htnum-1].energy_gen
									shipstats['energy gen'] -= ship.outfits_list[htnum-1].energy_gen
									shipstats['energy storage'] -= ship.outfits_list[htnum-1].energy_cap
									shipstats['idle heat'] -= ship.outfits_list[htnum-1].heat_gen
									totalheat -= ship.outfits_list[htnum].heat_gen
									if shipstats['energy use'] > 0:
										for outfit3 in powergenlist:
											if (shipstats['energy use'] >= 0) and (outfit3.outfit_space <= (ship.outfits_list[htnum-1].outfit_space)):
												#print(f"installed {outfit3.name}, space{outfit3.outfit_space}/{shipstats['outfit sp']}")
												ship.outfits_list.append(outfit3)
												shipstats['outfit sp'] -= outfit3.outfit_space
												shipstats['energy use'] -= outfit3.energy_gen
												shipstats['energy gen'] += outfit3.energy_gen
												shipstats['energy storage'] += outfit3.energy_cap
												shipstats['idle heat'] += outfit3.heat_gen
												totalheat += outfit3.heat_gen
												#print(f"spaceleft: {shipstats['outfit sp']}")
												break
									#print(f"SHIPGEN: update {totalheat:.1f}/{ship_max_heat*0.8:.1f}")
										break
							except IndexError:
								pass
					else:
						#print("No generator found?")
						#print("Expand ship")
						ship.outfit_space += outfit1.outfit_space
						shipstats['outfit sp'] += outfit1.outfit_space
						
		cl_chk += 1
		if cl_chk == 100:
			print("Heat Balance Failed")
	if debugMessage:
		print(f"SHIPGEN: AftHeat, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#==================TURN CHECK
	turn = (shipstats['turn']*60)/(ship.mass+(ship.outfit_space-shipstats['outfit sp'])+ship.cargo_space)
	insaneturnthreshold = 320
	#TODO : chance to infinite loop, need proper fix.
	while (turn > insaneturnthreshold):
		newoutfitlist = ship.outfits_list
		print("Turn too high, refitting..")
		for outfit in ship.outfits_list:
			if (outfit.category != 'Engines'):
				continue
			#if turn > insaneturnthreshold:
			#Find engine outfit and install smaller pair or just smaller steering.
			if outfit.turn > 0 and outfit.thrust > 0:
				nosmaller = False
				oldenginenum = enginelist.index(outfit.name)
				try:
					newengine = enginelist[oldenginenum+1] #engines sorted from large to small
				except IndexError:
					nosmaller = True
				if not nosmaller:
					ship_update(faction,ship,shipstats,outfit,"uninstall",weapon=False)
					ship_update(faction,ship,shipstats,newOutfit,"Install",weapon=False)
					if False:
						target = ship.outfits_list.index(outfit)
						newoutfitlist.pop(target)
						shipstats['energy use'] -= outfit.thrust_ener - newengine.thrust_ener
						shipstats['energy use'] -= outfit.turn_ener - newengine.turn_ener
						shipstats['engine heat'] -= outfit.thrust_heat - newengine.thrust_heat
						shipstats['engine heat'] -= outfit.turn_heat - newengine.turn_heat
						shipstats['turn'] -= outfit.turn - newengine.turn
						shipstats['thrust'] -= outfit.thrust - newengine.thrust
						shipstats['outfit sp'] += outfit.outfit_space - newengine.outfit_space
						turn = (shipstats['turn']*60)/(ship.mass+(ship.outfit_space-shipstats['outfit sp'])+ship.cargo_space)
						newoutfitlist.append(newengine)
			elif outfit.turn > 0 and not outfit.thrust > 0:
				nosmaller = False
				oldenginenum = steeringlist.index(outfit)
				try:
					newengine = enginelist[oldenginenum+1] #engines sorted from large to small
				except IndexError:
					nosmaller = True
				if not nosmaller:
					ship_update(faction,ship,shipstats,outfit,"uninstall",weapon=False)
					ship_update(faction,ship,shipstats,newOutfit,"Install",weapon=False)
					if False:
						target = ship.outfits_list.index(outfit.name)
						newoutfitlist.pop(target)
						shipstats['energy use'] -= outfit.turn_ener - newengine.turn_ener
						shipstats['engine heat'] -= outfit.turn_heat - newengine.turn_heat
						shipstats['turn'] -= outfit.turn - newengine.turn
						shipstats['thrust'] -= outfit.thrust - newengine.thrust
						shipstats['outfit sp'] += outfit.outfit_space - newengine.outfit_space
						turn = (shipstats['turn']*60)/(ship.mass+(ship.outfit_space-shipstats['outfit sp'])+ship.cargo_space)
						newoutfitlist.append(newengine)
			#shipstats['outfit sp'] += outfit.outfit_space
		turn = (shipstats['turn']*60)/(ship.mass+(ship.outfit_space-shipstats['outfit sp'])+ship.cargo_space)
		ship.outfits_list = newoutfitlist
	if debugMessage:
		print(f"SHIPGEN: AftTurn, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#====================BATTERY CHECK
	if shipstats['energy storage'] < shipstats['weapon energy'] and shipstats['outfit sp'] > 0:
		ship,shipstats = install_battery(faction,ship,shipstats,batterylist,battthreshold=50000)
	if debugMessage:
		print(f"SHIPGEN: AftBatt, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#====================POWER CHECK
	if shipstats['energy use'] >= 0 and shipstats['outfit sp'] > 0:
		ship,shipstats,powergenlist = pick_generator(faction,ship,shipstats,powergenlist)
	elif shipstats['energy use'] >= 0 and shipstats['outfit sp'] <= 0:
		smallestpowgen = 0
		for powgen in powergenlist: #Look for smallest powergenerator sufficient for 70% power
			if smallestpowgen == 0:
				smallestpowgen = powgen
			if powgen.energy_gen >= shipstats['energy use'] * .7 and powgen.outfit_space <= smallestpowgen.outfit_space:
				smallestpowgen = powgen
		ship.outfit_space += smallestpowgen.outfit_space
		shipstats['outfit sp'] += smallestpowgen.outfit_space
		just_install_generator(ship,shipstats,smallestpowgen)
	if debugMessage:
		print(f"SHIPGEN: AftPow, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	#====================HEAT ReCHECK
	#Recalculate heat
	ship_max_heat = (0.001 * ship.heat_diss) * ((ship.mass+(ship.outfit_space-shipstats['outfit sp'])) * 100)
	if ship_max_heat <= shipstats['idle heat']:
		for outfit in faction.outfitlist:
			smallestcooling = 0
			#Install cooling if it can fit
			if (outfit_type(outfit) == "cooling") and (outfit.outfit_space <= shipstats['outfit sp']):
				#print(f"Installing {outfit.name}")
				ship.outfits_list.append(outfit)
				shipstats['outfit sp'] -= outfit.outfit_space
				shipstats['idle heat'] -= outfit.cooling
				shipstats['idle heat'] -= outfit.active_cooling
				if shipstats['idle heat'] < ship_max_heat:
					break
				#install another if it's required.
				elif (outfit.outfit_space <= shipstats['outfit sp']):
					ship.outfits_list.append(outfit)
					shipstats['outfit sp'] -= outfit.outfit_space
					shipstats['idle heat'] -= outfit.cooling
					shipstats['idle heat'] -= outfit.active_cooling
					if shipstats['idle heat'] < ship_max_heat:
						break
			#Else try to find smallest cooling that will work.
			elif (outfit_type(outfit) == "cooling"):
				if smallestcooling == 0:
					smallestcooling = outfit
				else:
					if smallestcooling.outfit < outfit.outfit and smallestcooling.cooling+smallestcooling.active_cooling<=outfit.cooling+outfit.active_cooling:
						smallestcooling = outfit
		if smallestcooling != 0:
			while shipstats['idle heat'] >= ship_max_heat:
				ship.outfits_list.append(smallestcooling)
				ship.outfit_space += smallestcooling.outfit_space
				ship_max_heat += smallestcooling.outfit_space
				shipstats['outfit sp'] += smallestcooling.outfit_space
				shipstats['idle heat'] -= smallestcooling.cooling
				shipstats['idle heat'] -= smallestcooling.active_cooling
	if debugMessage:
		print(f"SHIPGEN: AftHeat2, spaceleft:{shipstats['outfit sp']}, idleheat/max{round(shipstats['idle heat'],1)*60}/{ship_max_heat*60}, eneruse/store{shipstats['energy use']*60}/{shipstats['energy storage']*60}")
	if len(h2hsmall_list) != 0:
		h2h_to_use = random.choice(h2hsmall_list)
		h2h_using_percent = random.random()
		if ship.category.endswith("Warship"): #Todo use outfit space using h2h
			h2h_using_percent = random.uniform(.5,1)
		for n in range(round(ship.bunk*h2h_using_percent)):
			ship.outfits_list.append(h2h_to_use)
		if shipstats['outfit sp'] > 0:
			pass
	# No Cooler; idleHeat Ok, maxHeat close. 
	print(f"SHIPGEN: Done, spaceleft:{shipstats['outfit sp']:.3f}, idleheat/max{round(shipstats['idle heat'],1)*60:.3f}/{ship_max_heat*60:.3f}, eneruse/store{shipstats['energy use']*60:.3f}/{shipstats['energy storage']*60:.3f}")
	return ship

def identify_category(sprite):
	sprite_image = open("ship/"+sprite+".png", 'rb')
	guessed_category = []
	w,h = get_png_info(sprite_image)
	sprite_image.close()
	if w == 0 and h == 0:
		return ['unknown']
	if w <= 80 and h <= 80:
		guessed_category.append('Drone')
		guessed_category.append('Fighter')
	if w <= 120 and h <= 120:
		guessed_category.append('Interceptor')
	if( w > 120 or h > 120) and( w <= 170 or h <= 200):
		guessed_category.append('Light Warship')
		guessed_category.append('Transport')
	if( w > 170 or h > 170) and( w <= 260 or h <= 260):
		guessed_category.append('Medium Warship')
		guessed_category.append('Transport')
		guessed_category.append('Light Freighter')
	if( w > 260 or h > 260):
		guessed_category.append('Heavy Warship')
		guessed_category.append('Heavy Freighter')
	return guessed_category
#Ships
def create_ship(faction): #Todo, option for without faction?
	namegen = namegenerator.Namegenerator(faction)
	call_generate_sprite = False
	#Load images.
	interceptor_sprites = []
	light_warship_sprites = []
	medium_warship_sprites = []
	heavy_warship_sprites = []
	light_freighter_sprites = []
	heavy_freighter_sprites = []
	transport_sprites = []
	fighter_sprites = []
	drone_sprites = []
	if faction.spriteset == 'default': #TODO: Generate ship first and use data to generate sprite.
		pass
	elif faction.partset != '':
		call_generate_sprite = True
		#generate_sprite_ship_PIL.call_generate_sprite(faction)
	else: #[category_list.copy(),gun_pos.copy(),turret_pos.copy(),engine_pos.copy()]
		keylist = faction.spriteset.keys()
		#print(keylist)
		if len(keylist) > 0:
			for k in keylist:
				#print(faction.spriteset[k])
				spritelist = faction.spriteset[k]
				a = 0
				for sprite in spritelist[0]:
					#print("Sorting Sprites:", sprite)
					if len(sprite) == 0:
						sprite.append(identify_category(k))
					if (sprite == 'Interceptor') :
						interceptor_sprites.append(k)
					if (sprite == 'Light Warship') :
						light_warship_sprites.append(k)
					if (sprite =='Medium Warship'):
						medium_warship_sprites.append(k)
					if (sprite =='Heavy Warship'):
						heavy_warship_sprites.append(k)
					if (sprite =='Light Freighter'):
						light_freighter_sprites.append(k)
					if (sprite =='Heavy Freighter'):
						heavy_freighter_sprites.append(k)
					if (sprite =='Transport'):
						transport_sprites.append(k)
					if (sprite =='Fighter'):
						fighter_sprites.append(k)
					if (sprite =='Drone'):
						drone_sprites.append(k)
					a += 1
			

	generate_ships_config = open(ship_config_file, "r")
	ship_output = open(f"data/{faction.name}/" + faction.name +" ships"+".txt", "w")
	#Searches config file for values and creates variables

	#=========Default values
	shipLWMass = [100,300]
	shipMWMass = [250,500]
	shipHWMass = [500,2500]
	shipInMass = [40,110]
	shipFtMass = [35,80]
	shipDrMass = [35,80]
	shipTpMass = [50,300]
	shipLFMass = [150,350]
	shipHFMass = [450,2500]
	ship_amount = 3
	shipmax = 12
	use_seed = False
	for line in generate_ships_config: #Creates vars from txt file
		if "use_seed" in line:
			use_seed_check = next(generate_ships_config)
			if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
				use_seed = True
				
		if "ship_seed" in line and use_seed == True:
			ship_seed = next(generate_ships_config).removesuffix("\n")
			random.seed(int(ship_seed))

		if "ship_per_faction_max" in line:
			shipmax = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_per_faction_min" in line:
			shipmin = int(next(generate_ships_config).removesuffix("\n"))

		if "ship_LW_min_mass" in line:
			shipLWMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_LW_max_mass" in line:
			shipLWMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_MW_min_mass" in line:
			shipMWMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_MW_max_mass" in line:
			shipMWMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_HW_min_mass" in line:
			shipHWMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_HW_max_mass" in line:
			shipHWMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_In_min_mass" in line:
			shipInMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_In_max_mass" in line:
			shipInMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Ft_min_mass" in line:
			shipFtMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Ft_max_mass" in line:
			shipFtMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Dr_min_mass" in line:
			shipDrMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Dr_max_mass" in line:
			shipDrMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Tp_min_mass" in line:
			shipTpMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_Tp_max_mass" in line:
			shipTpMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_LF_min_mass" in line:
			shipLFMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_LF_max_mass" in line:
			shipLFMass[1] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_HF_min_mass" in line:
			shipHFMass[0] = int(next(generate_ships_config).removesuffix("\n"))
		if "ship_HF_max_mass" in line:
			shipHFMass[1] = int(next(generate_ships_config).removesuffix("\n"))
			
	ship_amount = random.randrange(shipmin,shipmax)

	if faction.devmode:
		random.seed(99)
	ship_amount = round(faction.shipcount)
	fleet_tactic = faction.fleet_tactic
	#'defense offense balance hitrun kite'

	ship_category_list = []
	count_civships = 0
	count_carrier = 0
	count_drone = 0
	count_fighter = 0
	categories_carried = ['Fighter', 'Drone']
	categories_warship = ['Interceptor', 'Light Warship', 'Medium Warship', 'Heavy Warship']
	categories_civilian = ['Transport', 'Light Freighter', 'Heavy Freighter']
	ship_wsnciv = []
	ship_wsnciv.extend(categories_civilian)
	ship_wsnciv.extend(categories_warship)
	#===============Randomly pick a few categories
	#fleet_tactic = random.choice('defense offense balance hitrun kite'.split())
	for n in range(ship_amount):
		count_fighter = ship_category_list.count('Fighter')
		count_drone = ship_category_list.count('Drone')
		if(n < 1 and (faction.agg <= 0 or faction.military > .4)): #Aggressive faction will have at least 1 warships, pick it first.
			warship = random.choice(categories_warship)
			ship_category_list.append(warship)
			if warship == 'Medium Warship' or warship == 'Heavy Warship':
				if random.randrange(3) > 1:
					count_carrier += 1
		elif(faction.agg >= 0 and count_civships < 1): #Passive faction should have at least 1 civiliain ship
			ship_category_list.append(random.choice(categories_civilian))
			count_civships += 1
		elif(faction.fleet_tactic == 'defense') and (ship_category_list.count('Heavy Warship') < 1):
			ship_category_list.append('Heavy Warship')
			if random.randrange(3) > 1:
					count_carrier += 1
		elif(faction.fleet_tactic == 'hitrun') and (ship_category_list.count('Light Warship') < 1):
			ship_category_list.append('Light Warship')
		else:
			ship_selected = random.choice(ship_wsnciv)
			ship_category_list.append(ship_selected)
			if ship_selected == 'Medium Warship' or ship_selected == 'Heavy Warship':
				if random.randrange(3) > 1:
					count_carrier += 1

	#If there's a carrier and no fighter, make one. Outside loop to prevent carrier being picked last.
	if(count_carrier >= 1 and count_fighter+count_drone < 1): 
		ship_category_list.append(random.choice(categories_carried))
		count_fighter = ship_category_list.count('Fighter')
		count_drone = ship_category_list.count('Drone')

#        if "" in line:
#             = next(generate_ships_config)
	shiplist = []
	smallest_gun,smallest_turret,smallest_power,smallest_engine = analyze_outfits(faction)
	warship = False
	ship_types_generated_count = 1
	#Generate Ship
	for ship in ship_category_list:
		imgW,imgH = 100,100
		used_sprites = []
		transport = 0
		freighter = 0
		shiptypenum = 0.
		if(ship == 'Light Warship'):
			shiptypenum = 0.1
			ship_mass = round(random.uniform(shipLWMass[0],shipLWMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(light_warship_sprites, used_sprites,ship, faction)
			warship = True
		elif(ship == 'Medium Warship'):
			shiptypenum = 0.5
			ship_mass = round(random.uniform(shipMWMass[0],shipMWMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(medium_warship_sprites, used_sprites,ship, faction)
			warship = True
		elif(ship == 'Heavy Warship'):
			shiptypenum = 1.
			ship_mass = round(random.uniform(shipHWMass[0],shipHWMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(heavy_warship_sprites, used_sprites,ship, faction)
			warship = True
		elif(ship == 'Interceptor'):
			shiptypenum = -0.9
			ship_mass = round(random.uniform(shipInMass[0],shipInMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(interceptor_sprites, used_sprites,ship, faction)
			warship = True
		elif(ship == 'Fighter'):
			shiptypenum = -0.9
			ship_mass = round(random.uniform(shipFtMass[0],shipFtMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(fighter_sprites, used_sprites,ship, faction)
		elif(ship == 'Drone'):
			shiptypenum = -0.9
			ship_mass = round(random.uniform(shipDrMass[0],shipDrMass[1]))
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(drone_sprites, used_sprites,ship, faction)
		elif(ship == 'Transport'):
			shiptypenum = random.gauss(-0.04, 0.1)
			ship_mass = round(random.uniform(shipTpMass[0],shipTpMass[1]))
			if shiptypenum == 0:
				shiptypenum = 0.1
			transport = 3
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(transport_sprites, used_sprites,ship, faction)
		elif(ship == 'Light Freighter'):
			shiptypenum = -0.6
			ship_mass = round(random.uniform(shipLFMass[0],shipLFMass[1]))
			freighter = 2.5
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(light_freighter_sprites, used_sprites,ship, faction)
		elif(ship == 'Heavy Freighter'):
			shiptypenum = random.gauss(0.5, 0.1)
			ship_mass = round(random.uniform(shipHFMass[0],shipHFMass[1]))
			freighter = 4
			ship_sprite, used_sprites, ship_sprite_path, thumb_sprite_path = randomizeSprite(heavy_freighter_sprites, used_sprites,ship, faction)

		try:
			image = open("images/ship/"+ship_sprite+".png", 'rb')
			imgdata = image.read()
			imgW, imgH = get_png_info(imgdata)
			imgA = (imgW*imgH)/2 #Ships don't take up entire area, /2 might be a bit much but will do for now.
			image.close()
		except FileNotFoundError:
			imgW,imgH = 100,100
			imgA = (imgW*imgH)/2 #Ships don't take up entire area, /2 might be a bit much but will do for now.   
		
		ship_hp = 1795.1869*2.718**(1.407*(faction.tier+shiptypenum)) #formula by ESCelestia
		ship_hp = abs(random.gauss(ship_hp, ship_hp/random.gauss(4,1)))

		ship_shields = roundup100(ship_hp*(1-faction.shieldhullFactor))
		ship_hull = roundup100(ship_hp*faction.shieldhullFactor)

		

		ship_cost = abs(roundup1000(random.gauss((ship_hp*163*faction.tier)/4, (ship_hp*163*faction.tier)/8))) #todo, proper formula

		#==Flawed math, don't use.
		#ship_hp_per_mass = (33.5101555)*2.718**((0.377)*(faction.tier**shiptypenum**2))
		#altshipnum = remap(shiptypenum,-0.9,1,1,2)
		#ship_hp_per_mass = (33.51*altshipnum)*2.718**((altshipnum*.85)*(faction.tier))
		#altshipnum = remap(shiptypenum,-0.9,1,1,10)
		#ship_mass=33.75 * (altshipnum*50)

		#ship_mass = round(ship_hp/(ship_hp_per_mass))
		ship_mass *= .8
		ship_mass += round((ship_mass*faction.shieldhullFactor)/random.uniform(2,3))

		bunkmid = round((ship_mass*0.1)*max(transport,1))

		ship_required_crew_percent = round((random.uniform(float(0.2), float(0.8))), 1) #todo factor in faction 
		ship_bunks = round(max(random.gauss(int(bunkmid), int(bunkmid/3)),1))
		ship_required_crew = round(max((ship_bunks * ship_required_crew_percent/max(1,transport)),1))

		ship_required_crew = max(1,round(ship_required_crew * (1 - faction.automation)))
		ship_automaton = random.random() < faction.dronechance
		
		#ship_mass = roundup10(random.randint(int(ship_min_mass), int(ship_max_mass)))
		ship_drag = abs(round(ship_mass*random.gauss(0.02,0.001), 2))

		ship_heat_dissipation = round(random.uniform(float(0.5), float(0.9)), 2)
		if ship == 'Interceptor' or ship_mass <= 100:
			ship_heat_dissipation += round(random.gauss(0.2,0.1),2)
		if (ship != 'Drone' and ship != 'Fighter'):
			ship_fuel_capacity = roundup100(random.randint(int(300), int(max(400,800*faction.tier))))
		elif (random.uniform(0,20) > 18):
			ship_fuel_capacity = roundup100(random.randint(int(100), max(200,int(200*(faction.tier/2)))))
		ship_cargo_space = roundup5((0.06*max(freighter*2,2))*ship_mass)
		ship_outfit_space = roundup10(random.randint(int(1*ship_mass), int(2*ship_mass)))
		ship_weapon_capacity = roundup10(random.randint(abs(int(ship_outfit_space/3.5+shiptypenum)), abs(int(ship_outfit_space/2.5+shiptypenum))))
		ship_engine_capacity = roundup10(random.randint(int(ship_outfit_space/4+shiptypenum), int(ship_outfit_space/3+shiptypenum)))

		ship_guns = round(random.randint(max(0,int(abs(-2*shiptypenum))), max(0,int(abs(-6*shiptypenum)))))
		ship_turrets = round(random.randint(max(0,int((2*shiptypenum))), max(1,round((8*shiptypenum)))))

		if faction.fleet_tactic == 'defense':
			ship_hp += round(ship_hp*.1)
		elif faction.fleet_tactic == 'offense':
			ship_weapon_capacity += round(ship_weapon_capacity*.1)
			ship_outfit_space += round(ship_outfit_space*.05)
			ship_guns += 2
		elif faction.fleet_tactic == 'kite':
			ship_hp -= round(ship_hp*.1)
			ship_engine_capacity += round(ship_engine_capacity*.05)
			ship_outfit_space += round(ship_outfit_space*.05)
		elif faction.fleet_tactic == 'hitrun':
			ship_hp -= round(ship_hp*.1)
			ship_engine_capacity += round(ship_engine_capacity*.1)
			ship_outfit_space += round(ship_outfit_space*.1)
			ship_mass *= .9
			
		if(warship == True) and ((ship_guns+ship_turrets) == 0):
			if(random.randint(0,1) >= 1):
				ship_guns += 1
			else:
				ship_turrets += 1

		ship_gun_pos_x = []
		ship_gun_pos_y = []
		ship_turret_pos_x = []
		ship_turret_pos_y = []
		ship_engine_pos_x = []
		ship_engine_pos_y = []

		#print("Sprite default:",ship_sprite_is_default)

		#If use loaded sprites, try getting pre-made hardpoints.
		if ship_sprite_is_default != True:
			if len(faction.spriteset[ship_sprite][1]) >= 1:
				gun_keys = faction.spriteset[ship_sprite][1].keys()
				for n in list(gun_keys):
					n = n.removeprefix('[')
					n = n.removesuffix(']')
					n = n.split(', ')
					ship_gun_pos_x.append(n[0])
					ship_gun_pos_y.append(n[1])
			if len(faction.spriteset[ship_sprite][2]) >= 1:
				turret_keys = faction.spriteset[ship_sprite][2].keys()
				for n in turret_keys:
					n = n.removeprefix('[')
					n = n.removesuffix(']')
					n = n.split(', ')
					ship_turret_pos_x.append(n[0])
					ship_turret_pos_y.append(n[1])
			if len(faction.spriteset[ship_sprite][3]) >= 1:
				engine_keys = faction.spriteset[ship_sprite][3].keys()
				for n in engine_keys:
					n = n.removeprefix('[')
					n = n.removesuffix(']')
					n = n.split(', ')
					ship_engine_pos_x.append(n[0])
					ship_engine_pos_y.append(n[1])

		random_hardpoint = True

		#Generate random hardpoint.
		if (random_hardpoint == True) and (imgH != 0 and imgW !=0): 
			print("Randomizing hardpoints")
			temp_gun = 1
			temp_turret = 1
			while len(ship_gun_pos_x) < ship_guns:
				#print("Random Gun port..")
				if (temp_gun%2 == 0) and (gun_pos_x_rnd != 0): #mirror the gun port
					gun_pos_x_rnd *= -1 
				else:
					gun_pos_y_rnd = round((imgH/2)*random.uniform(.75,.99),1) * -1 #y is flipped
					gun_pos_x_rnd = round((imgW/4)*random.uniform(0,.2),1)
				ship_gun_pos_x.append(gun_pos_x_rnd)
				ship_gun_pos_y.append(gun_pos_y_rnd)
				temp_gun += 1
			while len(ship_turret_pos_x) < ship_turrets:
				#print("Random Turret mount..")
				if (temp_turret%2 == 0) and (turret_pos_x_rnd != 0): #mirror the turret mount
					turret_pos_x_rnd *= -1 
				else:
					turret_pos_y_rnd = round((imgH/2)*random.uniform(.1,.9),1) * -1 #y is flipped
					turret_pos_x_rnd = round((imgW/4)*random.uniform(0,.2),1)
				ship_turret_pos_x.append(turret_pos_x_rnd)
				ship_turret_pos_y.append(turret_pos_y_rnd)
				temp_turret += 1
			if len(ship_engine_pos_y) == 0:
				ship_engine_pos_x.append(0)
				ship_engine_pos_y.append(round((imgH/2)*random.uniform(.8,.9),1))

		if count_carrier >= 1 and (ship == 'Heavy Warship' or ship == 'Medium Warship'):
			ship_fighters = round(random.randint(int((2*(1+shiptypenum))*count_fighter), int((6*(1+shiptypenum))*count_fighter)))
			ship_drones = round(random.randint(int((2*(1+shiptypenum))*count_drone), int((6*(1+shiptypenum))*count_drone)))
			count_carrier -= 1
		else:
			ship_fighters = 0
			ship_drones = 0
		
		#Make sure at least smallest outfits fits.
		#Engine *2 to account for steering.
		if smallest_engine*2 > ship_engine_capacity:
			ship_engine_capacity = smallest_engine*2
		if (smallest_gun > ship_weapon_capacity and ship_guns > 0) and warship == True:
			if ship == 'Interceptor' and faction.agg < 0 and ship_weapon_capacity > 0:
				generate_weapons.create_weapon(faction,weapon_amount=1,weapon_min_outfit=ship_weapon_capacity/2,weapon_max_outfit=ship_weapon_capacity)
			else:
				ship_weapon_capacity = smallest_gun
		if smallest_power > ship_outfit_space-(smallest_engine*2 + smallest_gun*ship_guns):
			ship_outfit_space += abs(ship_outfit_space-(smallest_engine*2 + smallest_gun*ship_guns))


		ship_blast_radius =round((ship_shields + ship_hull) * .01 / faction.tier)
		ship_shield_damage = roundup10((ship_shields + ship_hull) * .10 / faction.tier)
		ship_hull_damage = roundup10((ship_shields + ship_hull) * .05 / faction.tier)
		ship_hit_force =  roundup10((ship_shields + ship_hull) * .07 / faction.tier)
		
		ship_leak_leak = abs(roundup10(random.randrange(int(max(0,60*shiptypenum)),int(max(0,60*shiptypenum)+5))))
		ship_leak_flame = abs(roundup10(random.randrange(int(max(0,20*shiptypenum)),int(max(0,20*shiptypenum))+5)))
		ship_leak_big_leak = abs(roundup10(random.randrange(int(max(0,20*shiptypenum)),int(max(0,20*shiptypenum))+5)))

		try:
			ship_explode_tiny = abs(roundup10(random.randrange(int(max(0,60*shiptypenum)),int(max(20,60*shiptypenum)))))
			ship_explode_small = abs(roundup10(random.randrange(int(max(0,60*shiptypenum)),int(max(20,60*shiptypenum)))))
			ship_explode_medium = abs(roundup10(random.randrange(int(max(0,60*shiptypenum)),int(max(20,60*shiptypenum)))))
			ship_explode_large = abs(roundup10(random.randrange(int(max(0,60*shiptypenum)),int(max(5,60*shiptypenum)))))
		except ValueError:
			ship_explode_tiny = 20
			ship_explode_small = 60
			ship_explode_medium = 60
			ship_explode_large = 30


		#ship Name
		name_length_min = 6
		name_length_max = 10
		ship_name = namegen.generateNameFromRules(name_length_min,
													name_length_max,
													wordlen=faction.lang_wordlen,
													spacechance=faction.lang_spacechance,
													lang_charweight=faction.lang_charweight,
													seed=faction.devmodeseed+ship_types_generated_count)
		#doesn't work yet
		massperpix = 0.0001 #random.triangular(0.0009,0.00015)
		areapx = ship_mass/massperpix
		widthpx,lengthpx = round(areapx*(1-faction.lenwid)),round((areapx*faction.lenwid))
		widthpx,lengthpx = 0,0
		if call_generate_sprite:
			ship_gun_pos_x,ship_gun_pos_y,ship_turret_pos_x,ship_turret_pos_y,ship_engine_pos_x,ship_engine_pos_y = generate_sprite_ship_PIL.call_generate_sprite(faction,
																				ship,
																				ship_name,
																				ship_guns,
																				ship_turrets,
																				width=widthpx,height=lengthpx,enginesp=ship_engine_capacity)
			ship_sprite_path = f"ship/{faction.name}/{ship_name}"
		#ship_name_int = str(random.choice(numbers)) + str(random.choice(numbers)) + str(random.choice(numbers))
		#ship_name = str(ship_name) + "-" + str(ship_name_int)
		shipdeathweapon = {"blast radius": ship_blast_radius,"shield damage":ship_shield_damage,"hull damage": ship_hull_damage, "hit force": ship_hit_force}
		ship_data = class_ship(ship_name,ship_sprite,ship_sprite_path,ship_sprite,thumb_sprite_path,ship,ship_cost,ship_shields,
								ship_hull,ship_required_crew,ship_bunks,ship_mass,ship_drag,ship_heat_dissipation,ship_fuel_capacity,
								ship_cargo_space,ship_outfit_space,ship_weapon_capacity,ship_engine_capacity)
		ship_data.death_weapon = shipdeathweapon
		ship_data.gun_ports = ship_guns
		ship_data.turret_mounts = ship_turrets
		ship_data.carried['Fighter'] = ship_fighters
		ship_data.carried['Drone'] = ship_drones
		ship_data.isWarship = warship
		ship_data = outfit_ship(faction,ship_data)
		faction.shiplist.append(ship_data)

		print("Created ship " + ship_name)

		#Writes ES code to file, use \n for line break
		ship_output.write('ship "' + ship_name + '"\n')

		ship_output.write('\tsprite "' + str(ship_sprite_path) + '"\n')
		if not call_generate_sprite:
			ship_output.write('\tthumbnail "' + str(thumb_sprite_path) + '"\n')
		
		ship_output.write('\tattributes \n')
		ship_output.write('\t\tcategory "' + ship + '"\n')
		ship_output.write('\t\t"cost" ' + str(ship_cost) + "\n")
		ship_output.write('\t\t"shields" ' + str(ship_shields) + "\n")
		ship_output.write('\t\t"hull" ' + str(ship_hull) + "\n")
		ship_output.write('\t\t"required crew" ' + str(ship_required_crew) + "\n")
		if ship_automaton:
			ship_output.write('\t\t"automaton" 1'+ "\n")
		ship_output.write('\t\t"bunks" ' + str(ship_bunks) + "\n")
		ship_output.write('\t\t"mass" ' + str(round(ship_mass,1)) + "\n")
		ship_output.write('\t\t"drag" ' + str(ship_drag) + "\n")
		ship_output.write('\t\t"heat dissipation" ' + str(ship_heat_dissipation) + "\n")
		ship_output.write('\t\t"fuel capacity" ' + str(ship_fuel_capacity) + "\n")
		ship_output.write('\t\t"cargo space" ' + str(ship_cargo_space) + "\n")
		ship_output.write('\t\t"outfit space" ' + str(ship_outfit_space) + "\n")
		ship_output.write('\t\t"weapon capacity" ' + str(ship_weapon_capacity) + "\n")
		ship_output.write('\t\t"engine capacity" ' + str(ship_engine_capacity) + "\n")
		for key,val in faction.ship_protection.items():
			if val != 0:
				ship_output.write(f'\t\t"{key} protection" {val:.3f}' + "\n")
		ship_output.write('\t\tweapon ' + "\n")
		ship_output.write('\t\t\t"blast radius" ' + str(ship_blast_radius) + "\n")
		ship_output.write('\t\t\t"shield damage" ' + str(ship_shield_damage) + "\n")
		ship_output.write('\t\t\t"hull damage" ' + str(ship_hull_damage) + "\n")
		ship_output.write('\t\t\t"hit force" ' + str(ship_hit_force) + "\n")
		ship_output.write('\toutfits ' + "\n")
		outfit_dict = {'':0}

		#print("Ship outfits: ")
		#for shipoutfits in ship_data.outfits_list:
		#    print(shipoutfits.name)
		for item_num in range(len(ship_data.outfits_list)): 
			item = ship_data.outfits_list[item_num]
			keys = [a for a in outfit_dict.keys()]
			for n in keys:
				#print("Outfit n", n)
				#print("Outfit dt", item.name)
				if n != item.name:
					try:
						if outfit_dict[item.name] < 1:
							outfit_dict[item.name] = 1
					except KeyError:
						outfit_dict[item.name] = 1
				else:
					outfit_dict[item.name] += 1  
		for outfit in outfit_dict.keys():
			if outfit_dict[outfit] != 0:
				ship_output.write(f'\t\t"{outfit}" {outfit_dict[outfit]}\n')
		if (ship !='Drone' or (random.uniform(0,100) > 90*(faction.tier*0.1))) and (ship != 'Fighter' or (random.uniform(0,100) > 80*(faction.tier*0.1))):
			ship_output.write(f'\t\t"{faction.ftl}"' + '\n')
			#if(faction.tier >= 3) and (random.uniform(1,6) <= faction.tier*1.45):
			#    ship_output.write(f'\t\t"Jump Drive"' + '\n')
			#else:
			#    ship_output.write(f'\t\t"Hyperdrive"' + '\n')
		#ship_output.write('          ' + str() + " " + str() + "\n")
		#ship_output.write("\n")
		for n in range(len(ship_engine_pos_y)):
			ship_output.write(f'\tengine {ship_engine_pos_x[n]} {ship_engine_pos_y[n]}' + "\n")

		for n in range(ship_guns): #TODO: Fix whatever mess this is.
			if len(ship_gun_pos_x) != 0: #Both should have the same length so check just one
				gunX = ship_gun_pos_x[n-1]
				gunY = ship_gun_pos_y[n-1]
			else:
				gunX = 0+round(math.sin(1+n*3)) #So it don't overlap.
				gunY = 0
			ship_output.write(f'\tgun {gunX} {gunY}' + "\n")

		for n in range(ship_turrets):
			if len(ship_turret_pos_x) != 0: #Both should have the same length so check just one
				turretX = ship_turret_pos_x[n-1]
				turretY = ship_turret_pos_y[n-1]
			else:
				turretX = 0
				turretY = 0-n*2 #At least so it doesn't overlap
			ship_output.write(f'\tturret {turretX} {turretY}' + "\n")

		i = 0
		while i < ship_fighters:
			ship_output.write('\tbay "Fighter" 0 0' + "\n")
			i += 1
		i = 0
		while i < ship_drones:
			ship_output.write('\tbay "Drone" 0 0' + "\n")
			i += 1
		#####
		ship_output.write('\tleak "leak" ' + str(ship_leak_leak)+'\n')
		ship_output.write('\tleak "flame" ' + str(ship_leak_flame)+'\n')
		ship_output.write('\tleak "big leak" ' + str(ship_leak_big_leak)+'\n')

		ship_output.write('\texplode "tiny explosion" ' + str(ship_explode_tiny)+'\n')
		ship_output.write('\texplode "small explosion" ' + str(ship_explode_small)+'\n')
		ship_output.write('\texplode "medium explosion" ' + str(ship_explode_medium)+'\n')
		ship_output.write('\texplode "large explosion" ' + str(ship_explode_large)+'\n')
		#ship_output.write('\texplode "huge explosion" ' + str(ship_explode_huge))
		#ship_output.write('\t"final explode" "' + str(ship_final_explode) + '"' + "\n")

		ship_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} ship"\n')

		ship_output.write('\n')

		shiplist.append(ship_name)
		ship_types_generated_count += 1
	init_sales(faction)
	outfitter_output_file = f"data/{faction.name}/dev sales.txt"
	outfitter_output = open(outfitter_output_file, "a")
	#outfitter_output.write('\n')
	for shipn in shiplist:
		outfitter_output.write(f'\t"{shipn}"\n')
	outfitter_output.close()
	generate_ships_config.close()
	ship_output.close()

def load_ship_configs(faction):

	ship_configs_list = glob.glob("config/ship config/*.txt") #Imports files in directory
	ship_configs_amount = len(ship_configs_list) #Gets amount of items in list
	ship_configs_iterations = 0
	
	

	while ship_configs_iterations < ship_configs_amount: #Creates ships for each config files
		global ship_config_file #Config File
		ship_config_file = str(ship_configs_list[ship_configs_iterations]).replace("\\", "/")
		global ship_output_file #Output file
		ship_output_file = str(ship_configs_list[ship_configs_iterations]).replace("\\", "/").replace("config/ship config/", "")


		create_ship(faction)


		print("\n")
		ship_configs_iterations += 1



#load_ship_configs()

#input()