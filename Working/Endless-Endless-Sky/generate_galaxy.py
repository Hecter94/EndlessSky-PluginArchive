# Copyright (c) 2020 by Nucleartaxi

#Imports
import math
import glob
import random

import namegenerator #Custom Name generator

def roundup100(x):
    return int(math.ceil(x / 100.0)) * 100

def avg_deviation(numlist):
    if len(numlist) == 0:
        return 0,0
    totalnum = 0
    for num in numlist:
        totalnum += num
    avg = totalnum/len(numlist)
    x = 0
    for num in numlist:
        x += (num-avg)**2
    return avg, math.sqrt(x/totalnum)

#log_file = open('galaxy generator log.txt','w')
def myprint(text):
    print(text)
    #log_file.write(str(text) + '\n')   #will change to logging module
    
class system():
    def __init__(self, name, pos, links, galaxy_name, system_layer, planet_list, level, government=None):
        self.name = name
        self.pos = pos
        self.links = links
        self.galaxy_name = galaxy_name
        self.system_layer = system_layer
        self.planet_list = []
        self.level = level
        self.habitable = 300
        self.attributes = []
        self.asteroids = {}
        self.mineables = {} #name: [count, energy]
        self.hazard = []
        self.haze = ''
        self.cloud = '' #Image to paste behind system location

        self.government = government #reference to gov class
        self.fleets = []
        self.fleetdicts = {} #new mode
        self.capital = ''
        self.distgov = []
        self.allhypot = []
        self.contestants = {} #list of other government attempting to own the system but failed along with hypot

        self.hyptdifflist = []

class galaxy():
    def __init__(self, name, min_x, max_x, min_y, max_y, layer, is_circle, desc_files, planet_config, government,galaxy_center_x,galaxy_center_y):
        self.name = name
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.layer = layer
        self.is_circle = is_circle
        self.desc_files = desc_files
        self.planet_config = planet_config
        self.government = government
        self.center_x = galaxy_center_x
        self.center_y = galaxy_center_y
        self.radius_x = abs(max_x-galaxy_center_x)
        self.radius_y = abs(max_y-galaxy_center_y)

#Create a sector for the government along with assigning fleets
def government_region(center_x,center_y,radius_x,radius_y,system_list,government):
    prehypot = 0
    curcap = 0
    allhypot = [] 
    for s in range(len(system_list)):
        hypot = int(math.hypot(center_x - system_list[s].pos[0], center_y - system_list[s].pos[1]))
        if hypot < radius_x:
            if system_list[s].government != None:
                if duel_over_system(system_list[s],government,hypot):
                    system_list[s].government = government
                    #system_list[s].fleets.append(government.patrolfleets)
                    #system_list[s].fleets.append(government.civilianfleets)
                    system_list[s].distgov.append([government.name,hypot])
                    allhypot.append(hypot)
                    if hypot > prehypot:
                        system_list[curcap].capital = ''
                        system_list[s].capital = government
                        curcap = s
                    government.systemlist.append(system_list[s])
                else:
                    system_list[s].contestants[government] = hypot
            else:
                system_list[s].government = government
                #system_list[s].fleets.append(government.patrolfleets)
                #system_list[s].fleets.append(government.civilianfleets)
                system_list[s].distgov.append([government.name,hypot])
                allhypot.append(hypot)
                if hypot > prehypot:
                    system_list[curcap].capital = ''
                    system_list[s].capital = government
                    curcap = s
                government.systemlist.append(system_list[s])
            #myprint(f"{system.name} government: {government.name}")
    government.allhypot = allhypot

#Find center and make it the government centre, maybe, maybe not.
def gov_region_center(center_x,center_y,radius_x,radius_y,system_list,government):
    prevhypot = 999999999999
    center_system = None
    for s in range(len(system_list)):
        hypot = int(math.hypot(center_x - system_list[s].pos[0], center_y - system_list[s].pos[1]))
        if hypot < radius_x:
            if hypot < prevhypot:
                prevhypot = hypot
                center_system = system_list[s]
    pass

def duel_over_system(system,government,hypot):
    prevhypot = 0
    
    for h in system.distgov:
        if h[0] == system.government.name:
            prevhypot = h[1]
    govlinks = 0
    ngovlinks = 0
    for link in system.links:
        for ngsys in government.systemlist:
            if link == ngsys.name:
                ngovlinks += 1
        for gsys in system.government.systemlist:
            if link == gsys.name:
                govlinks += 1
    prevgovpow = govlinks*system.government.military + system.government.tier
    newgovpow = ngovlinks*government.military + system.government.tier 
    prevgovroll = (random.random() + .3)*.1
    newgovroll = (random.random() + .3)*.1
    win = (newgovroll*25)+(hypot*newgovpow) > (prevgovroll*25)+(prevhypot*prevgovpow)
    system.hyptdifflist.append(hypot - prevhypot)
    return win

def avghyptdiff(systemlist,bleedratio=.1):
    total = 0
    count = 0
    for system in systemlist:
        for hypt in system.hyptdifflist:
            total += abs(hypt)
            count += 1
    avg = total/count
    bleedrad = avg*bleedratio #Find base radius for fleets bleeding into another system
    return avg,bleedrad

def place_fleets(government,bleedrad):
    avghypot,dvhypot = avg_deviation(government.allhypot)
    distriRadius = (avghypot/2) #TODO: factor in faction stuffs.
    for sys in government.systemlist: 
        addiflet = 0
        for planet in sys.planet_list:
            if planet.is_habitable: #Make population affect fleet weight
                addiflet += 100 * planet.planet_properties.population/5
        for distlist in sys.distgov: #Make distance from gov center affect spawnrate
            if distlist[0] == government.name:
                thissysdist = distlist[1]
                fleetfreq = roundup100(min(4000,max(600,800*(distlist[1]/distriRadius))))
        for minable in sys.mineables.keys(): #If there's enough minables spawn miners.
            if sys.mineables[minable][0] > 20:
                for fleet in government.miningfleets:
                    sys.fleetdicts[str(fleet)] = round(fleetfreq*2)
        fleetfreqmilit = fleetfreq*(1.5-government.military)
        fleetfreqmilit = max(400,fleetfreqmilit-addiflet)
        fleetfreq = max(400,fleetfreq-addiflet)
        if len(sys.hazard) != 0: #Double fleet rarity if system have hazard TODO: Consider if gov ship's resistance.
            fleetfreq *= 2
            fleetfreqmilit *= 2
        for fleet in government.patrolfleets:
            sys.fleetdicts[str(fleet)] = round(fleetfreqmilit)
        for fleet in government.civilianfleets:
            sys.fleetdicts[str(fleet)] = round(fleetfreq)
        #If other government is contesting for the system, add their fleet if below threshold.
        for altgov in sys.contestants.keys(): #TODO: Probably should consider from the nearest system that can be used as base?
            if government.relations[altgov.name] >= 0:
                if thissysdist - sys.contestants[altgov] > bleedrad*(1+government.relations[altgov.name]):
                    altfleetfreq = roundup100(min(10000,max(600,800*(sys.contestants[altgov]/distriRadius))))
                    altfleetfreq *= (1+government.relations[altgov.name])
                    if len(sys.hazard) != 0:
                        altfleetfreq *= 2
                    for fleet in altgov.civilianfleets:
                        sys.fleetdicts[str(fleet)] = round(altfleetfreq)
            else:
                if thissysdist - sys.contestants[altgov] > bleedrad + (1-government.military):
                    altfleetfreq = roundup100(min(20000,max(600,800*(sys.contestants[altgov]/distriRadius))))
                    altgovmilitfreq = altfleetfreq*(1.5-government.military)
                    if len(sys.hazard) != 0:
                        altgovmilitfreq *= 2
                    for fleet in altgov.patrolfleets:
                        sys.fleetdicts[str(fleet)] = round(altgovmilitfreq)

def assign_haze(systemlist,radiusfull,radiusblackbody):
    global galaxy_center_x
    global galaxy_center_y
    haze_full = "_menu/haze-full"
    haze_blackbody = "_menu/haze-blackbody"
    for s in range(len(systemlist)):
        hypot = int(math.hypot(galaxy_center_x - system_list[s].pos[0], galaxy_center_y - system_list[s].pos[1]))
        if hypot < radiusfull:
            system_list[s].haze = haze_full
        elif hypot < radiusblackbody:
            system_list[s].haze = haze_blackbody
    return

def add_hazards(systemlist,hazardlist):
    systemperhazard_min = 1
    systemperhazard_max = 12
    for hazard in hazardlist:
        if hazard.cluster[0] <= 1:
            for n in range(systemperhazard_min,systemperhazard_max):
                syssel = random.randrange(len(systemlist))
                systemlist[syssel].hazard.append(hazard)
                systemlist[syssel].cloud = hazard.cloud
                systemlist[syssel].haze = hazard.haze
                systemlist[syssel].attributes.append(hazard.name)
        else:
            for n in range(systemperhazard_min,systemperhazard_max):
                syssel = random.randrange(len(systemlist))
                systemlist[syssel].hazard.append(hazard)
                systemlist[syssel].cloud = hazard.cloud
                systemlist[syssel].haze = hazard.haze
                systemlist[syssel].attributes.append(hazard.name)
                if False: #disabled, too lazy to make rn. TODO: save syslink as object so it's easier to refer to.
                    for sys2 in systemlist[syssel].links:
                        systemlist[syssel].hazard.append(hazard)
                        systemlist[syssel].cloud = hazard.cloud
                        if hazard.haze != '':
                            systemlist[syssel].haze = hazard.haze
    return hazardlist

class hazard_class():
    def __init__(self,name) -> None:
        self.name = name
        self.conststr = False
        self.period = 1
        self.duration = []
        self.strength = []
        self.range = []
        self.enveffect = []

        #For generation.
        self.cloud = ''
        self.haze = ''
        self.cluster = [] #size,count

def generate_hazards(faction,galaxy):
    namegen = namegenerator.Namegenerator(faction)
    hazard_type_min = 3
    hazard_type_max = 12
    hazard_type_mean = 6

    fileout = f'data/{galaxy.name} hazards.txt'

    generate_galaxy_config = open(galaxy_config_file, "r")
    for line in generate_galaxy_config: #reads lines in galaxy config and assigns variables
        if "use_seed" in line:
            use_seed_check = next(generate_galaxy_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if "hazard_seed" in line: #TODO: Make config for these
            hazard_seed = int(next(generate_galaxy_config))
        if "hazard_type_min" in line:
            hazard_type_min = int(next(generate_galaxy_config))
        if "hazard_type_max" in line:
            hazard_type_max = int(next(generate_galaxy_config))
        if "hazard_type_mean" in line:
            hazard_type_mean = int(next(generate_galaxy_config))
        if "hazard_spread_min" in line:
            hazard_spread_min = int(next(generate_galaxy_config))
        if "hazard_spread_max" in line:
            hazard_spread_max = int(next(generate_galaxy_config))
        if "hazard_spread_mean" in line:
            hazard_spread_mean = int(next(generate_galaxy_config))
        if "hazard_placed_min" in line:
            hazard_place_min = int(next(generate_galaxy_config))
    
    hazard_count = round(random.triangular(hazard_type_min,hazard_type_max,hazard_type_mean))
    reldmgtype = ['shield','hull','heat','fuel','energy']
    otherdmgtype= ['ion','disruption','slowing','discharge','corrosion','leak','burn']
    hazardeffect = {}
    hazardeffect['ion'] = ['ion hazard','ion spark','disruption spark']
    hazardeffect['hull'] = ['corrosion spark']
    hazardeffect['heat'] = ['burning spark']
    hazardeffect['fuel'] = ['leakage spark']
    hazardeffect['slow'] = ['slowing spark']
    hazardcloud = {}
    hazardcloud['ion'] = ['lbluecloud']
    hazardcloud['hull'] = ['greencloud']
    hazardcloud['heat'] = ['redcloud']
    hazardcloud['fuel'] = ['orangecloud']
    hazardcloud['slow'] = ['purplecloud']
    hazardhaze = {}
    hazardhaze['ion'] = ['haze/lbluehaze']
    hazardhaze['hull'] = ['haze/greenhaze']
    hazardhaze['heat'] = ['_menu/haze-red']
    hazardhaze['fuel'] = ['haze/orangehaze']
    hazardhaze['slow'] = ['haze/purplehaze']

    hazardlist = []
    for n in range(hazard_count):
        hazarddmgtype = random.choice(['relative','const','both'])
        reldmcount = round(random.triangular(1,3,1))
        hazardreldmgtype = random.choices(reldmgtype,k=round(reldmcount))
        hazardreldamage = [random.triangular(0.00001,0.002,0.0003) for n in range(len(hazardreldmgtype))]

        constdmgcount = 3-reldmcount
        hazarddmgtype = random.choices(otherdmgtype,k=(constdmgcount))
        hazarddmgweight = [random.random() for n in range(constdmgcount)]
        hazarddps = random.randrange(1,1000)
        hazarddamage = [(hazarddps/3)*a for a in hazarddmgweight]

        hazardpiercing = 0
        hazardpiercingchance = .2
        if hazardpiercingchance > random.random():
            hazardpiercing = random.random()

        hazardduration_min = random.randrange(1,3000)
        #hazardperiod_min = random.range(1,3000)
        hazardrange_min = random.randrange(1,6000)
        hazardduration = [hazardduration_min,hazardduration_min+random.randrange(1,3000)]
        hazardperiod = random.randrange(1,3000)
        hazardrange = [hazardrange_min,hazardrange_min+random.randrange(1,6000)]
        hazardstrength = random.randrange(1,3)

        hzclustersize = 1
        #hzclustersize = random.randrange(3,12)
        hzclustercount = 1
        #hzclustercount = random.randrange(1,3)

        hazardconststr = random.random() < .3
        
        for i in range(len(hazardreldamage)): #Sort by highest damage
            for j in range(i+1,len(hazardreldamage)):
                if hazardreldamage[i] < hazardreldamage[j]:
                    hazardreldmgtype[i],hazardreldmgtype[j] = hazardreldmgtype[j],hazardreldmgtype[i]
                    hazardreldamage[i],hazardreldamage[j] = hazardreldamage[j],hazardreldamage[i]
        for i in range(len(hazarddamage)): #Sort by highest damage
            for j in range(i+1,len(hazarddamage)):
                if hazarddamage[i] < hazarddamage[j]:
                    hazarddmgtype[i],hazarddmgtype[j] = hazarddmgtype[j],hazarddmgtype[i]
                    hazarddamage[i],hazarddamage[j] = hazarddamage[j],hazarddamage[i]
        hazardname = ""
        if len(hazarddamage) == 0:
            hazarddamage.append(0)
        if len(hazardreldamage) == 0:
            hazardreldamage.append(0)
        if (hazardreldamage[0]*14000) >= hazarddamage[0]:
            if hazardreldmgtype[0] == 'shield' or hazardreldmgtype[0] == 'energy':
                hazardeffchoice = 'ion'
            elif hazardreldmgtype[0] == 'hull':
                hazardeffchoice = 'hull'
            elif hazardreldmgtype[0] == 'heat':
                hazardeffchoice = 'heat'
            elif hazardreldmgtype[0] == 'fuel':
                hazardeffchoice = 'fuel'
            hazardname = hazardname.join(hazardreldmgtype)
            hazardname = hazardname.capitalize()
            hazardname = namegen.completelyRandomNames() + " " + hazardname + " Hazard"
        else:
            if hazarddmgtype[0] == 'ion' or hazarddmgtype[0] == 'disruption' or hazarddmgtype[0] == 'discharge':
                hazardeffchoice = 'ion'
            elif hazarddmgtype[0] == 'corrosion':
                hazardeffchoice = 'hull'
            elif hazarddmgtype[0] == 'burn':
                hazardeffchoice = 'heat'
            elif hazarddmgtype[0] == 'leak':
                hazardeffchoice = 'fuel'
            elif hazarddmgtype[0] == 'slowing':
                hazardeffchoice = 'slow'
            hazardname = hazardname.join(hazarddmgtype)
            hazardname = hazardname.capitalize()
            hazardname = namegen.completelyRandomNames() + " " + hazardname + " Hazard"
        
        hazardenveffect = random.choice(hazardeffect[hazardeffchoice])
        hazardcloudsel = random.choice(hazardcloud[hazardeffchoice])
        hazardhazesel = random.choice(hazardhaze[hazardeffchoice])

        if hazarddmgtype == 'relative':
            hazardenveffectnum = round(hazardreldamage[0]*4)
        elif hazarddmgtype == 'const':
            hazardenveffectnum = round(hazarddamage[0]*4)
        else:
            hazardenveffectnum = round(hazardreldamage[0]*4)
            hazardenveffectnum = round(hazarddamage[0]*4)
        hazardenveffectnum = max(1,hazardenveffectnum)
            
        
        
        with open(fileout, "a") as hazard_output:
            hazard_output.write(f'hazard "{hazardname}"' + '\n')
            if hazardconststr:
                hazard_output.write(f'\t"constant strength"' + '\n')
            hazard_output.write(f'\t"period" {hazardperiod}' + '\n')
            hazard_output.write(f'\t"duration" {hazardduration[0]} {hazardduration[1]}' + '\n')
            hazard_output.write(f'\t"range" {hazardrange[0]} {hazardrange[1]}' + '\n')
            hazard_output.write(f'\t"strength" {hazardstrength}' + '\n')
            hazard_output.write(f'\t"environmental effect" "{hazardenveffect}" {hazardenveffectnum}' + '\n')
            hazard_output.write(f'\tweapon\n')
            if hazarddmgtype == 'relative':
                for d in range(len(hazardreldmgtype)):
                    hazard_output.write(f'\t\t"relative {hazardreldmgtype[d]} damage" {hazardreldamage[d]:.5f}'  + '\n')
            elif hazarddmgtype == 'const':
                for d in range(len(hazarddamage)):
                    hazard_output.write(f'\t\t"{hazarddmgtype[d]} damage" {hazarddamage[d]:.5f}' + '\n')
            else:
                for d in range(len(hazardreldmgtype)):
                    if hazardreldmgtype[0] == 0: break
                    hazard_output.write(f'\t\t"relative {hazardreldmgtype[d]} damage" {hazardreldamage[d]:.5f}' + '\n')
                for d in range(len(hazarddamage)):
                    if hazarddamage[0] == 0: break
                    hazard_output.write(f'\t\t"{hazarddmgtype[d]} damage" {hazarddamage[d]:.5f}' + '\n')
            if hazardpiercing > 0:
                hazard_output.write(f'\t\t"piercing" {hazardpiercing:.2f}' + '\n')

            hazard_output.write("\n")
        nhazad = hazard_class(hazardname)
        nhazad.conststr = hazardconststr
        nhazad.period = hazardperiod
        nhazad.duration = hazardduration
        nhazad.strength = hazardstrength
        nhazad.range = hazardrange
        nhazad.enveffect = hazardenveffect
        nhazad.cloud = hazardcloudsel
        nhazad.haze = hazardhazesel
        nhazad.cluster = [hzclustersize,hzclustercount] 
        hazardlist.append(nhazad)
        #print(f"Made hazard {hazardname} with {nhazad.haze}")
    return hazardlist

def pick_within(center_x,center_y,galaXmin,galaXmax,galaYmin,galaYmax):
    r = galaXmax-center_x
    pos = [0,0]
    #myprint(f"pickwithin: {center_x,center_y,galaXmin,galaXmax,galaYmin,galaYmax}")
    for x in range(1000): #To avoid infinite loop
        pos[0] = round(random.triangular(galaXmin,galaXmax),2)
        pos[1] = round(random.triangular(galaYmin,galaYmax),2)
        hypot = int(math.hypot(center_x - pos[0], center_y - pos[1]))
        if hypot < r:
            return pos
    myprint("Failed to find a pos.")
    return 0,0

def galaxy_place_systems():
    #this dictionary contains everything related to the system's level.
    level_desc_file_dict = {}

    generate_galaxy_config = open(galaxy_config_file, "r")
    for line in generate_galaxy_config: #reads lines in galaxy config and assigns variables
        if "use_seed" in line:
            use_seed_check = next(generate_galaxy_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if "galaxy_seed" in line:
            galaxy_seed = int(next(generate_galaxy_config))
        if "galaxy_systems" in line:
            global galaxy_systems
            galaxy_systems = next(generate_galaxy_config).strip()
        if "galaxy_is_circle" in line:
            galaxy_is_circle = next(generate_galaxy_config)
            if str(galaxy_is_circle) in ['true', 'True', 'true\n', 'True\n']:
                galaxy_is_circle = True
            #elif galaxy_is_circle in ['false', 'False', 'false\n', 'False\n']:
            #    galaxy_is_circle = False
            else:
                galaxy_is_circle = False

        random_gx_pos = True
        global galaxy_center_x, galaxy_center_y
        if "galaxy_randomize_center" in line:
            random_gx_pos = next(generate_galaxy_config)
            if str(random_gx_pos) in ['false', 'False', 'false\n', 'False\n']:
                random_gx_pos = False
            else:
                random_gx_pos = True
                galaxy_center_x = random.randrange(10000,550000) * -1
                galaxy_center_y = random.randrange(10000,550000) * -1
        if "galaxy_center_x" in line and (random_gx_pos == False):
            galaxy_center_x = int(next(generate_galaxy_config))
        if "galaxy_center_y" in line and (random_gx_pos == False):
            galaxy_center_y = int(next(generate_galaxy_config))
        if "galaxy_radius_x" in line:
            galaxy_radius_x = int(next(generate_galaxy_config))
        if "galaxy_radius_y" in line:
            galaxy_radius_y = int(next(generate_galaxy_config))

        if "system_delete_distance" in line:
            system_delete_distance = next(generate_galaxy_config).strip()

        if "hyperlane_min_distance" in line:
            hyperlane_min_distance = next(generate_galaxy_config)
        if "hyperlane_max_distance" in line:
            hyperlane_max_distance = next(generate_galaxy_config)

        global wormhole_chance
        wormhole_chance = .001
        if "wormhole_chance" in line:
            wormhole_chance = next(generate_galaxy_config)
            
        global config_enable_infinite_asteroid
        config_enable_infinite_asteroid = True
        if "infinite_asteroid_field" in line:
            infastroid = next(generate_galaxy_config)
            if str(infastroid) in ['false', 'False', 'false\n', 'False\n', '0']:
                config_enable_infinite_asteroid = False

        if "system_namelist_file" in line:
            system_namelist_file = next(generate_galaxy_config)
        if "galaxy_government" in line:
            galaxy_government = next(generate_galaxy_config).strip()


        if "planet_name_list" in line:
            level_desc_file_dict['planet_namelist_file'] = next(generate_galaxy_config)
        if "galaxy_government" in line:
            level_desc_file_dict['galaxy_government'] = next(generate_galaxy_config)

        if "system_level_generation_type" in line:
            system_level_generation_type = next(generate_galaxy_config).strip().lower()
            if 'random' in system_level_generation_type:
                system_level_generation_type = 'random'
            if 'radial' in system_level_generation_type:
                system_level_generation_type = 'radial'
            else:
                system_level_generation_type = 'random'

        if "num_points_level_5" in line:
            num_points_level_5 = int(next(generate_galaxy_config))
        if "effect_radius_level_5" in line:
            effect_radius_level_5 = int(next(generate_galaxy_config))

        if "min_radius_from_center_level_5" in line:
            min_radius_from_center_level_5 = int(next(generate_galaxy_config))
        if "max_radius_from_center_level_5" in line:
            max_radius_from_center_level_5 = int(next(generate_galaxy_config))

        if "level_1_description" in line:
            level_desc_file_dict[1] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_2_description" in line:
            level_desc_file_dict[2] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_3_description" in line:
            level_desc_file_dict[3] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_4_description" in line:
            level_desc_file_dict[4] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_5_description" in line:
            level_desc_file_dict[5] = next(generate_galaxy_config).replace('.txt', '').strip()

        if "level_1_spaceport" in line:
            level_desc_file_dict['sp1'] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_2_spaceport" in line:
            level_desc_file_dict['sp2'] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_3_spaceport" in line:
            level_desc_file_dict['sp3'] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_4_spaceport" in line:
            level_desc_file_dict['sp4'] = next(generate_galaxy_config).replace('.txt', '').strip()
        if "level_5_spaceport" in line:
            level_desc_file_dict['sp5'] = next(generate_galaxy_config).replace('.txt', '').strip()

        if "level_1_fleet" in line:
            level_desc_file_dict['fleet1'] = next(generate_galaxy_config).strip().replace(', ', ',').split(',')
        if "level_2_fleet" in line:
            level_desc_file_dict['fleet2'] = next(generate_galaxy_config).strip().replace(', ', ',').split(',')
        if "level_3_fleet" in line:
            level_desc_file_dict['fleet3'] = next(generate_galaxy_config).strip().replace(', ', ',').split(',')
        if "level_4_fleet" in line:
            level_desc_file_dict['fleet4'] = next(generate_galaxy_config).strip().replace(', ', ',').split(',')
        if "level_5_fleet" in line:
            level_desc_file_dict['fleet5'] = next(generate_galaxy_config).strip().replace(', ', ',').split(',')
            
        if "system_level_debug" in line:
            system_level_debug = next(generate_galaxy_config)
            if str(system_level_debug) in ['true', 'True', 'true\n', 'True\n']:
                system_level_debug = True
            elif system_level_debug in ['false', 'False', 'false\n', 'False\n']:
                system_level_debug = False
            else:
                system_level_debug = False

        if "planet_sprites_config" in line:
            planet_sprites_config = next(generate_galaxy_config).strip()
    generate_galaxy_config.close()

    global system_layer #puts each galaxy on a seperate system layer each time a new galaxy is created
    system_layer += 1

    if galaxy_is_circle is True:
        myprint("Galaxy is circle")
    else:
        myprint("Galaxy is not circle")

    global planet_sprites_config_dict
    planet_sprites_config_dict = {}

    planet_sprites_config_list = []
    planet_sprites_config_file = open('config/planet config/planet sprites config/' + str(planet_sprites_config) + '.txt', 'r')
    for line in planet_sprites_config_file:
        line = line.strip('\n').replace(', ', ',').split(',')
        planet_sprites_config_list.append((line[0], float(line[1]), float(line[2])))
    planet_sprites_config_file.close()
    planet_sprites_config_dict[planet_sprites_config] = planet_sprites_config_list

    galaxy_min_x = galaxy_center_x - abs(galaxy_radius_x) #abs() is to ensure the radius is positive
    galaxy_max_x = galaxy_center_x + abs(galaxy_radius_x)
    galaxy_min_y = galaxy_center_y - abs(galaxy_radius_y)
    galaxy_max_y = galaxy_center_y + abs(galaxy_radius_y)
    myprint('galaxy min (' + str(galaxy_min_x) + ', ' + str(galaxy_min_y) + ') galaxy max (' + str(galaxy_max_x) + ', ' + str(galaxy_max_y) + ')')

    #galaxy_name = galaxy_config_file.replace("config/galaxy config/", "").replace(".txt", "")
    #================MARK GALAXY CLASS USED
    galaxy_name = namegen.completelyRandomNames()
    galaxy_list.append(galaxy(galaxy_name, galaxy_min_x, galaxy_max_x, galaxy_min_y, galaxy_max_y, system_layer, galaxy_is_circle, level_desc_file_dict, planet_sprites_config, galaxy_government, galaxy_center_x, galaxy_center_y))
    galaxy_list[len(galaxy_list)-1].radius_x = galaxy_radius_x
    galaxy_list[len(galaxy_list)-1].radius_y = galaxy_radius_y
    if 'auto' in galaxy_systems:
        galaxy_systems = int(round(((galaxy_radius_x * 2) * (galaxy_radius_y * 2))/ 3000))
        myprint('Auto systems amount: ' + str(galaxy_systems))

    if(use_seed == True):
        random.seed(galaxy_seed)

    #Creates System Coordinates
    myprint('Creating system coordinates...')
    system_coordinates = []
    system_count = 1
    while system_count <= int(galaxy_systems):
        system_x_value = round(random.uniform(int(galaxy_min_x), int(galaxy_max_x)))
        system_y_value = round(random.uniform(int(galaxy_min_y), int(galaxy_max_y)))
        system_coordinates.append((system_x_value, system_y_value))
        system_count += 1

    #Deletes extra systems that are too close together 
    myprint("Deleting extraneous systems... please wait. This may take some time depending on how many systems are generated.\n...")
    for pt in system_coordinates:
        for PT in system_coordinates:
            if (abs(pt[0]-PT[0])+abs(pt[1]-PT[1]))!=0 and abs(pt[0]-PT[0])< int(system_delete_distance) and abs(pt[1]-PT[1]) < int(system_delete_distance):
                system_coordinates.remove(PT)
                #myprint("Removed system at coordinates " + str(PT))

    #Deletes systems outside circle if the galaxy is a circle
    myprint("Deleting extraneous systems outside circle... please wait. This may take some time depending on how many systems are generated.\n...")
    if galaxy_is_circle is True:
        #a and b are denominators of x and y
        a = galaxy_radius_x * galaxy_radius_x
        b = galaxy_radius_y * galaxy_radius_y
        h = galaxy_center_x
        k = galaxy_center_y
        #(x-h)^2/a + (y-k)^2/b = 1
        systems_to_delete = []
        for pt in system_coordinates:
            if ((pt[0] - h) **2)/a + ((pt[1] - k) **2)/b  >= 1:
                systems_to_delete.append(pt)
                #myprint("Removed system at coordinates circle " + str(pt))
            else:
                #myprint('coord in circle ' + str(pt))
                pass
        for pt in systems_to_delete:
            system_coordinates.remove(pt)

    #Reads in names and adds them to a list, if one has already been used, remove it
    myprint('Reading namelist...')
    system_namelist_file = open("names/" + str(system_namelist_file).replace('\n', '') + '.txt', "r")
    system_name_list = []
    i = 0
    for line in system_namelist_file:
        system_name = (str(line).strip('\n'))
        if system_name not in system_used_namelist:
            system_name_list.append(str(system_name))
            #myprint('system name ' + system_name + ' in namelist')
    system_namelist_file.close()
    myprint('Generating Hyperlanes...')
    #Calculates and assigns hyperlanes
    dict_coordinates_links = {}
    hyperlane_check_count = 0
    #myprint("system coordinates " + str(system_coordinates))
    while hyperlane_check_count < 1:
        for pt in system_coordinates:
            for PT in system_coordinates:
                hypot = int(math.hypot(pt[0] - PT[0], pt[1] - PT[1]))
                if hypot <= int(hyperlane_max_distance) and hypot >= int(hyperlane_min_distance):
                    #myprint("Confirmed hyperlane at " + str(PT) + " and " + str(pt))
                    if pt in dict_coordinates_links.keys(): # If key is in dict
                        dict_coordinates_links[pt].append(PT)
                        #myprint("key in dictionary")
                    else: # If key isn't in dict
                        dict_coordinates_links[pt] = []
                        dict_coordinates_links[pt].append(PT)
                        #myprint("key not in dictionary")

                    if PT in dict_coordinates_links.keys(): # If key is in dict
                        dict_coordinates_links[PT].append(pt)
                        #myprint("key in dictionary")
                    else: # If key isn't in dict
                        dict_coordinates_links[PT] = []
                        dict_coordinates_links[PT].append(pt)
                        #myprint("key not in dictionary")

        hyperlane_check_count += 1
    """
    print("DictCoorlink: ", dict_coordinates_links) [x,y]: ([x,y],[x,y])

    #Todo: Remove crosslinks
    for keys in dict_coordinates_links.keys():
        for systems in dict_coordinates_links[keys]:
            for endpoint in systems:
                dx = (keys[0][0]-endpoint[0][0], )
                pass
    """
    #chances
    #generate given number of points within min and max x and y
        #if point is outside radius, delete it and try again (i = i to continue the loop)
        #if point is in radius (i + 1)
        #if random.uniform() <= .05      - 5% chance of happening
        #if random.uniform() <= .9       - 90% chance of happening

    #Selects system level generation type and assigns coordinates to system level centers
    if system_level_generation_type == 'random':
        myprint('System level generation type: random')
    elif system_level_generation_type == 'radial':
        myprint('System level generation type: radial')
        myprint('Generating center points...')
        system_level_points = []
        i = 0
        math_hypot = math.hypot(galaxy_center_x, galaxy_center_y)
        min_radius = min_radius_from_center_level_5 + math_hypot
        max_radius = max_radius_from_center_level_5 + math_hypot
        while i < num_points_level_5:
            x = int(random.randint(-max_radius_from_center_level_5, max_radius_from_center_level_5) + galaxy_center_x)
            y = int(random.randint(-max_radius_from_center_level_5, max_radius_from_center_level_5) + galaxy_center_y)
            distance = int(math.hypot(x, y))
            
            if distance >= min_radius and distance <= max_radius:
                myprint("\tx: " + str(x) + " y: " + str(y))
                system_level_points.append((x, y))
                i += 1
            else:
                myprint('\tpoint ('  + str(x) + ', ' + str(y) + ') not within radii, generating another')
        #myprint('generated ' + str(num_points_level_5) + ' points')

    #Assigns coordinates and system levels to system names
    dict_pos_name = {}
    for key in dict_coordinates_links:
        if system_level_generation_type == 'random':
            system_level = random.randint(1, 5)
        if system_level_generation_type == 'radial':
            x1 = key[0]
            y1 = key[1]
            possible_system_levels = []
            for item in system_level_points:
                x2 = item[0]
                y2 = item[1]
                #myprint("x: " + str(x2) + " y: " + str(y2))
                distance = int(math.hypot(x2 - x1, y2 - y1))
                #myprint("distance: " + str(distance))
                percent_distance = round((1 - (distance / effect_radius_level_5)), 2)
                #myprint('percent distance: ' + str(percent_distance))
                if percent_distance >= .8:
                    possible_system_levels.append(5)
                elif percent_distance >= .6:
                    possible_system_levels.append(4)
                elif percent_distance >= .4:
                    possible_system_levels.append(3)
                elif percent_distance >= .2:
                    possible_system_levels.append(2)
                else:
                    possible_system_levels.append(1)
            try:
                system_level = max(possible_system_levels)
            except: #number of level 5 points is 0, so every system gets a system level of 1
                system_level = 1
            #myprint("System level: " + str(system_level))
        if system_level_debug is True:
            name = system_name_list.pop(random.randint(0, len(system_name_list) - 1))
            system_used_namelist.append(name)
            dict_pos_name[key] = (name + ' [' + str(system_level) + ']', system_level) #puts name and level in tuple (name, level)
        else:
            completely_random_name = True #temporary, todo
            if(completely_random_name == True):
                name = namegen.completelyRandomNames()
                #myprint("Using completely random name.\n")
            else:
                name = system_name_list.pop(random.randint(0, len(system_name_list) - 1))
                #myprint("Using name from name list.\n")
            system_used_namelist.append(name)
            dict_pos_name[key] = (name, system_level)

        

    #myprint("dict pos name         " + str(dict_pos_name))           Useful for debugging
    #myprint("dict coordinates list " + str(dict_coordinates_links))

    #Commodities
    myprint('Creating commodities...')
    commodity_file_list = glob.glob("config/planet config/commodities/*.txt") #Imports files in directory
    commodity_line_dict = {}
    names_list = []
    for item in commodity_file_list:
        name = item.replace("config/planet config/commodities\\", "").replace(".txt", "")
        names_list.append(name)

        i = 1
        commodity_line_list = []
        commodity_file = open(item, 'r')
        for line in commodity_file:
            lines = line.split(',')
            line2 = (int(lines[0].strip()), int(lines[1].strip()))
            commodity_line_list.append(line2)
        commodity_line_dict[name] = commodity_line_list
        commodity_file.close()
    #myprint('commodity line dict: ' + str(commodity_line_dict))
    
    global commodity_dict
    commodity_dict = {}
    i = 1
    while i <= 5:
        commodity_list = []
        for name in names_list:
            commodity = (name, commodity_line_dict[name][i - 1][0], commodity_line_dict[name][i - 1][1]) #commodity, min for i level, max for i level
            commodity_list.append(commodity)
        commodity_dict[i] = commodity_list
        i += 1
    #myprint(commodity_dict)
    #Renames keys and dict data from coordinates to system names
    myprint('Assigning names to coordinates and finalizing systems...')
    for key in dict_coordinates_links.keys():
        list1 = dict_coordinates_links[key]
        links_name_list = []
        links_name_list.clear()
        #links_name_list = []
        i = 0
        while i < len(list1):
            item_from_list1 = list1.pop()
            links_name_list.append(str(dict_pos_name[item_from_list1][0]))
        system_name = str(dict_pos_name[key][0])
        system_level = dict_pos_name[key][1]

        system_list.append(system(system_name, key, links_name_list, galaxy_name, system_layer, [], system_level))
    myprint("Galaxy finished.\n\n\n")
    #myprint(system_used_namelist)
    
def galaxy_delete_overlapping_systems():
    #deletes overlapping systems in overlapping galaxies
    myprint("Deleting systems in overlapping galaxies... please wait. This may take some time.")

    generate_galaxy_config = open(galaxy_config_file, "r")
    for line in generate_galaxy_config:
        if "system_delete_distance" in line:
            system_delete_distance = int(next(generate_galaxy_config))

    system_list_to_be_deleted = []

    for galaxy in galaxy_list:
        galaxy_name = str(galaxy.name)
        galaxy_min_x = int(galaxy.min_x)
        galaxy_max_x = int(galaxy.max_x)
        galaxy_min_y = int(galaxy.min_y)
        galaxy_max_y = int(galaxy.max_y)
        galaxy_layer = int(galaxy.layer)

        myprint('\t' + galaxy_name)

        #Deletes system coordinates that are too close together
        #galaxy_name_current = [galaxy_name]
        #works

        for system in system_list:
            if system.system_layer < galaxy_layer:
                pt = system.pos
                #myprint("less than layer")
                #myprint(str(pt[0]) +" "+ str(pt[1]))
                if pt[0] >= galaxy_min_x - system_delete_distance and pt[0] <= galaxy_max_x + system_delete_distance and pt[1] >= galaxy_min_y - system_delete_distance and pt[1] <= galaxy_max_y + system_delete_distance:
                    #myprint("in area")
                    if system in system_list:
                        system_list_to_be_deleted.append(system)
                        #myprint("Removed system " + "layer " + str(system.system_layer) + " coordinates " + str(system.pos))
            elif system.system_layer >= galaxy_layer:
                #myprint("skipped system layer " + str(system.system_layer) + " coordinates " + str(system.pos))
                pass

    for system in system_list_to_be_deleted:
        if system in system_list:
            system_list.remove(system)
        else:
            pass

    generate_galaxy_config.close()
    myprint("\n\n")

class planet_properties():
    def __init__(self, attribute, shipyard, outfitter, required_reputation, bribe, security, tribute, threshold, fleet, name, sprite, landscape, population):
        self.attribute = attribute
        self.shipyard = shipyard
        self.outfitter = outfitter
        self.required_reputation = required_reputation
        self.bribe = bribe
        self.security = security 
        self.tribute = tribute
        self.threshold = threshold
        self.fleet = fleet
        self.name = name
        self.sprite = sprite
        self.landscape = landscape
        self.population = population

class planet():
    def __init__(self, sprite, distance, period, is_habitable, name, planet_properties, descriptions):
        self.sprite = sprite
        self.distance = distance
        self.period = period
        self.is_habitable = is_habitable
        self.name = name
        self.planet_properties = planet_properties
        self.descriptions = descriptions

def load_description_data():
    myprint("loading description data...")
    planet_desc_list = glob.glob("config/description config/descriptions/*.txt") #Imports files in directory

    global planet_desc_dict
    planet_desc_dict = {}
    global planet_desc_dict_keys
    planet_desc_dict_keys = []

    for item in planet_desc_list:
        name = item.replace("config/description config/descriptions\\", "").replace(".txt", "")
        temp_items_list = []
        item = open(item, "r")
        for line in item:
            temp_items_list.append(line.strip('\n'))
        item.close()
        planet_desc_dict_keys.append(name)
        planet_desc_dict[name] = temp_items_list

    #myprint("keys " + str(planet_desc_dict_keys))
    #myprint("dict " + str(planet_desc_dict))
    #myprint("\n")


    myprint("loading word data...")
    planet_word_list = glob.glob("config/description config/words/*.txt") #Imports files in directory

    global planet_word_dict
    planet_word_dict = {}
    global planet_word_dict_keys
    planet_word_dict_keys = []

    for item in planet_word_list:
        name = item.replace("config/description config/words\\", "").replace(".txt", "")
        temp_items_list = []
        item = open(item, "r")
        for line in item:
            temp_items_list.append(line.strip('\n'))
        item.close()
        if "_properties" in str(item):
            pass
        else:
            planet_word_dict_keys.append(name)
            planet_word_dict[name] = temp_items_list

    #myprint("keys " + str(planet_word_dict_keys))
    #myprint("dict " + str(planet_word_dict))
    #=====================================LOAD PLANET NAMES
    myprint("loading planet names...")
    global planet_name_dict
    planet_name_dict = {}
    for galaxy in galaxy_list:
        default = False
        if default == True:
            temp_items_list = []
            name_list_file = open('names/' + str(galaxy.desc_files['planet_namelist_file'].strip('\n')) + '.txt', "r")
            for line in name_list_file:
                temp_items_list.append(line.rstrip('\n'))
            name_list_file.close()
            planet_name_dict[galaxy.desc_files['planet_namelist_file']] = temp_items_list
        else:
            temp_items_list = []
            for name in range(int(galaxy_systems)): 
                temp_items_list.append(namegen.completelyRandomNames(6,12))
            planet_name_dict[galaxy.desc_files['planet_namelist_file']] = temp_items_list

    #===================================LOAD LANDSCAPES
    myprint("loading landscapes...")
    landscape_desc_list = glob.glob("config/planet config/landscape images/*.txt") #Imports files in directory
    global landscape_dict
    landscape_dict = {}

    for item in landscape_desc_list:
        name = item.replace("config/planet config/landscape images\\", "").replace(".txt", "")
        temp_items_list = []
        item = open(item, "r")
        for line in item:
            temp_items_list.append(line.strip('\n'))
        item.close()
        landscape_dict[str(name)] = temp_items_list

    #myprint("Landscape dict: " + str(landscape_dict) + '\n')

    #==========================================LOAD STARS
    # Read config at .\config\planet config\planet sprites\000 stars.txt for list of stars in ES format.
    myprint("loading stars...")
    global available_star_list
    available_star_list = []

    star_config = open(star_config_file, "r")
    checkpow = False
    checkwind = False
    starinit = False
    for line in star_config:
        line = line.removeprefix("\t\t")
        line = line.removeprefix("\t")
        if line.startswith("#"):
            pass
        if not checkpow and not checkwind and starinit:
            habitable = (float(starpower) * 800) * float(starwind) #50 is random magic number, I don't think people would notice
            available_star_list.append((star[1].replace('"', ''), int(habitable)))
            starinit = False
        if line.startswith("star"):
            star = line.split()
            starinit = True
            checkpow = True
            checkwind = True
        elif line.startswith("power") and checkpow:
            starpower = line.split()
            starpower = starpower[1] 
            checkpow = False
        elif line.startswith("wind") and checkwind:
            starwind = line.split()
            starwind = starwind[1] 
            checkwind = False
            
    star_config.close()

    myprint("loading planet sprites...")
    global planet_sprite_dict
    planet_sprite_dict = {}

    planet_sprite_list = glob.glob("config/planet config/planet sprites/*.txt") #Imports files in directory

    for item in planet_sprite_list:
        name = item.replace("config/planet config/planet sprites\\", "").replace(".txt", "")
        temp_items_list = []
        item = open(item, "r")
        for line in item:
            temp_items_list.append(line.strip('\n'))
        item.close()
        planet_sprite_dict[name] = temp_items_list
    myprint('Successfully loaded data.\n\n\n')
        
def planet_desc_word_replace(description): #**UNUSED**
    appending_characters = False
    this_desc_words_list = []
    for char in description:
        if char == ">":
            appending_characters = False
            temp_string = ""
            for item in chars_list:
                temp_string = temp_string + item
            this_desc_words_list.append(temp_string)
        if appending_characters is True:
            chars_list.append(char)
        if char == "<":
            appending_characters = True
            chars_list = []

    this_planets_properties_list = []
    for item in this_desc_words_list:
        if item in planet_word_dict_keys:
            if len(planet_word_dict[item]) != 0:
                len_description = random.randint(0, len(planet_word_dict[item]) - 1)
                description = description.replace("<"+str(item)+">", str(planet_word_dict[item][len_description]))
            else:
                description = description.replace("<"+str(item)+">", '')

        else:
            myprint("!!!word <" + str(item) + "> not in list!!!")
        
        try: #Get properties from file
            sprite_list_list = []
            landscape_list_list = []
            attribute_list = []
            shipyard_list = []
            outfitter_list = []
            word_properties_file = open("config/description config/words/" + item + "_properties.txt", "r")
            for line in word_properties_file:
                #if "name_list" in line:      #This was so each <word> could have a different namelist file, this has changed so all planets in one galaxy share a master planet name list
                #    name_list = next(word_properties_file).strip()
                name_list = ''
                if "sprite_list" in line:
                    for item2 in next(word_properties_file).strip().replace(', ', ',').split(','):
                        sprite_list_list.append(item2)
                    sprite_list = sprite_list_list
                if "landscape_list" in line:
                    for item2 in next(word_properties_file).strip().replace(', ', ',').split(','):
                        landscape_list_list.append(item2)
                    landscape_list = landscape_list_list
                if "attribute" in line:
                    for item2 in next(word_properties_file).strip().replace(', ', ',').split(','):
                        attribute_list.append(item2)
                    attribute = attribute_list
                if "shipyard" in line:
                    for item2 in next(word_properties_file).strip().replace(', ', ',').split(','):
                        shipyard_list.append(item2)
                    shipyard = shipyard_list
                if "outfitter" in line:
                    for item2 in next(word_properties_file).strip().replace(', ', ',').split(','):
                        outfitter_list.append(item2)
                    outfitter = outfitter_list
                if "required_reputation" in line:
                    required_reputation = next(word_properties_file).strip()
                if "bribe" in line:
                    bribe = next(word_properties_file).strip()
                if "security" in line:
                    security = next(word_properties_file).strip()
                if "tribute" in line:
                    tribute = next(word_properties_file).strip()
                if "threshold" in line:
                    threshold = next(word_properties_file).strip()
                if "fleet" in line:
                    fleet = next(word_properties_file).strip()

            this_planets_properties_list.append(planet_properties(attribute, shipyard, outfitter, required_reputation, bribe, security, tribute, threshold, fleet, name_list, sprite_list, landscape_list))
            #myprint("\tadded properties from <" + item + ">")
            word_properties_file.close()
        except: #Property file does not exist, do nothing (this is intended, not an error)
            #myprint("\tno properties from <" + item + ">")
            pass
        
    return description, this_planets_properties_list

def create_planet_properties(system, galaxy):
    i = 0
    is_spaceport = False
    descriptions_temp = []
    properties_list = []
    while i < 2:
        if is_spaceport is False:
                    #V Global var
            key = planet_desc_dict[galaxy.desc_files[system.level]] #key = lines within the description file (were added to dict earlier in load_description_data)
            description = key[random.randint(0, len(key) - 1)] #gets a random description
            #description = planet_desc_dict[system.level][random.randint(0, len(planet_desc_dict[description_key]) - 1)]
        else:
            key = planet_desc_dict[galaxy.desc_files['sp' + str(system.level)]] #gets the spaceport description file used for this system level
            description = key[random.randint(0, len(key) - 1)] 

        while i > -1:
            if "<" and ">" in description:
                previous_description = description
                description = planet_desc_word_replace(description)
                properties_list.append(description[1])
                description = description[0]
                if previous_description is description:
                    break    
            else:
                break
        descriptions_temp.append(description)
        is_spaceport = True
        i += 1
    #properties_list2 = filter(None, properties_list)
    return descriptions_temp, properties_list

def condense_planet_properties(properties_list):
    #myprint("Condensing planet properties...")
    properties_list = [x for x in properties_list if x != []]
    if len(properties_list) == 0:
        myprint("No properties to add. Continuing.")
        pass
    else:
        attribute_list = []
        shipyard_list = []
        outfitter_list = []
        for list1 in properties_list:
            for item in list1:
                for item2 in item.attribute:
                    attribute_list.append(item2)
                attribute = attribute_list
                for item2 in item.shipyard:
                    shipyard_list.append(item2)
                shipyard = shipyard_list
                for item2 in item.outfitter:
                    outfitter_list.append(item2)
                outfitter = outfitter_list
                required_reputation = item.required_reputation
                bribe = item.bribe
                security = item.security
                tribute = item.tribute
                threshold = item.threshold
                fleet = item.fleet
                name = item.name
                landscape = landscape_dict[item.landscape[random.randint(0, len(item.landscape) - 1)]][random.randint(0, len(landscape_dict[item.landscape[random.randint(0, len(item.landscape) - 1)]]) - 1)]
                sprite = planet_sprite_dict[item.sprite[random.randint(0, len(item.sprite) - 1)]][random.randint(0, len(planet_sprite_dict[item.sprite[random.randint(0, len(item.sprite) - 1)]]) - 1)]

        #myprint("Planet properties condensed.")
        return planet_properties(attribute, shipyard, outfitter, required_reputation, bribe, security, tribute, threshold, fleet, name, sprite, landscape)

def pick_landscape(planet_type):
    forest_list = ['water','valley','forest','fields','fog'] #0-6
    desert_list = ['dune','badlands','lava'] #0-6
    ice_list = ['snow','moutain','dmottl'] #0-5
    if(planet_type == "forest"):
        landscape = random.choice(forest_list)+str(random.randrange(0,6))
    elif(planet_type == "desert"):
        landscape = random.choice(desert_list)+str(random.randrange(0,6))
    elif(planet_type == "ocean"):
        landscape = random.choice(forest_list)+str(random.randrange(0,6))
    elif(planet_type == "dust"):
        landscape = random.choice(desert_list)+str(random.randrange(0,6))
    elif(planet_type == "cloud"):
        landscape = random.choice(forest_list)+str(random.randrange(0,6))
    elif(planet_type == "ice"):
        landscape = random.choice(ice_list)+str(random.randrange(0,5))
    elif(planet_type == "rock"):
        landscape = random.choice(desert_list)+str(random.randrange(0,6))
    return landscape

#Returns dict of with lists of possible description
def read_planet_description():
    description_dict = {}
    tempdesclist = []
    read_begin = False
    with open("config/planet config/planet descriptions.txt", 'r') as file:
        filedata = file.readlines()
        for line in filedata:
            if line.startswith("#"):
                pass
            elif line.startswith("type"):
                if read_begin:
                    description_dict[key]=tempdesclist.copy()
                    tempdesclist.clear()
                read_begin = True
                key = line[5:]
                key = key.removesuffix("\n")
            elif line.startswith("\t") and read_begin:
                templine = line.removesuffix("\n")
                tempdesclist.append(templine.removeprefix("\t"))
    global glo_description_dict
    glo_description_dict = description_dict
    return description_dict

def generate_spaceport(planet_type,attributes,population):
    factory_desc = "The spaceport have a lot of warehouses along with various trucks moving containers around all the time. "
    farm_desc = "Farming seems to one of the major export here guessing from number of farm vehicles parked near the spaceport. "
    medical_desc = "Rather clean and large spaceport with reserved landing pad right next to hospital entrance. "
    mining_desc = "Smoggy spaceport flooded with noise from heavy mining vehicles and cranes loading minerals into freighters. "
    oil_desc = "Located close to an oil refinery connected with large pipes and surrounded with liquid tanks. "
    research_desc = "The spaceport sits not too far away from a large research facility. "
    military_desc = "Well defended and patrolled spaceport close to a military base. "

    tinypop_desc = "The spaceport is tiny with flat areas enough only for a few ships. The spaceport control tower is the tallest building around the area. "
    lowpop_desc = "A small spaceport with old solid landing pads. "
    mediumpop_desc = "A medium-sized spaceport. "
    highpop_desc = "A large spaceport. "
    vhighpop_desc = "A massive spaceport. "

    tempspaceport = []
    if population < 2:
        tempspaceport.append(tinypop_desc)
    elif population >= 2 and population < 5:
        tempspaceport.append(lowpop_desc)
    elif population >= 5 and population < 7:
        tempspaceport.append(mediumpop_desc)
    elif population >= 7 and population < 10:
        tempspaceport.append(highpop_desc)
    elif population >= 10:
        tempspaceport.append(vhighpop_desc)

    if attributes != ['']:
        for attr in attributes:
            if attr == 'factory' or attr == 'manufacturing':
                tempspaceport.append(factory_desc)
            if attr == 'farming':
                tempspaceport.append(farm_desc)
            if attr == 'medical':
                tempspaceport.append(medical_desc)
            if attr == 'mining':
                tempspaceport.append(mining_desc)
            if attr == 'oil':
                tempspaceport.append(oil_desc)
            if attr == 'research':
                tempspaceport.append(research_desc)
            if attr == 'military':
                tempspaceport.append(military_desc)

    finspaceport = "".join(tempspaceport)
    return finspaceport
        

def generate_inhabited_planet(system,name):
    #TODO repalce with stuffs loaded from folder/config file
    attributes_reg = 'factory farming fishing manufacturing medical mining oil research military'.split()
    planet_type = random.choice(['forest','desert','ocean','dust','cloud','ice','rock'])
    base_outfitter_chance = .5
    base_shipyard_chance = .2
    #description_dict = glo_description_dict
    #spaceport_dict = {}
    global shipyard_chance
    global outfitter_chance
    if shipyard_chance != None:
        base_shipyard_chance = shipyard_chance
    if outfitter_chance != None:
        base_outfitter_chance = outfitter_chance

    planet_sprite = planet_type+str(random.randrange(0,6))
    landscape = pick_landscape(planet_type)
    attributes = ['']
    n = 0
    while n < random.randrange(0,3):
        attributes = random.choices(attributes_reg)
        n += 1
    military = 0
    if attributes.count('military') >= 1:
        military = 1
    population = random.randrange(1,11)

    try:
        descriptionlist = glo_description_dict[planet_type]
    except KeyError:
        descriptionlist = ['Default planet description. (Description for this type not found)']
    description = random.choice(descriptionlist)
    spaceport = generate_spaceport(planet_type,attributes,population)
    outfitterlist = None
    shipyardlist = None

    outfitter_roll = random.random() * (system.government.age/3) + round(population/8,1) + round(military/2)
    shipyard_roll = random.random() * (system.government.age/3) + round(population/10,1) + round(military/5)

    if outfitter_roll > base_outfitter_chance:
        outfitterlist = system.government.outfitterlist
        xo = min(len(outfitterlist)-1,random.randrange(len(outfitterlist)) + round(population/8))
        outfitterlist = outfitterlist[xo]
    if shipyard_roll > base_shipyard_chance:
        shipyardlist = system.government.shipyardlist
        outfitterlist = system.government.outfitterlist
        xs = random.randrange(len(shipyardlist))
        #xo = random.randrange(len(outfitterlist))
        shipyardlist = shipyardlist[xs]
        outfitterlist = outfitterlist[xs]
    
    #TODO: Add other planet stuffs
    if shipyardlist != None:
        shipyard = [shipyardlist.name] #For when multi shipyard is supported.
    else:
        shipyard = ['']
    if outfitterlist != None:
        outfitter = [outfitterlist.name]
    else:
        outfitter = ['']
    required_reputation = 0
    if system.government.player_rep < 0:
        required_reputation += 1
    if military >= 1:
        required_reputation += random.randrange(0,50)
    bribe = 0.1
    security = 0 #0.2
    #if military >= 1:
    #    security += random.uniform(.2,.5)
    #Pure guess work
    threshold = round(random.randrange(55,1097) + math.exp(system.government.tier) + math.exp((military+population)/2))
    tribute = round((threshold/2) * (population/6))
    fleet_name = random.choice(system.government.patrolfleets)
    fleet_num = random.randrange(max(1,round(threshold/1000)),max(2,round(threshold/50)))
    fleet = str(fleet_name) + " " + str(fleet_num)
    descriptionFinal = [description,spaceport]
    #return planet_name,planet_sprite,landscape,attributes,description,spaceport,outfitterlist,shipyardlist
    return planet_properties(attributes,
                             shipyard, 
                             outfitter, 
                             required_reputation, 
                             bribe, 
                             security, 
                             tribute, 
                             threshold, 
                             fleet, 
                             name, 
                             planet_sprite, 
                             landscape,
                             population), descriptionFinal

#Generate in-system stuffs.
def system_planets(system, galaxy): #Generates planets in system
    #myprint("Working on planets in system " + str(system.name))
    sprite_controls = planet_sprites_config_dict[galaxy.planet_config]

    #system_level = system.level

    name_length_min = 6
    name_length_max = 12
    
    #https://en.wikipedia.org/wiki/Stellar_classification#Luminosity_class
    #Habitable inner: sqrt(Luminosity/1.1) outer: sqrt(Luminosity/.53)
    #belt 1000 to 2000
    #Generate basic planets from in to out based on hab zone: molten, desert, forest/water if right conditions, gas giants with moons
    #Invisible fence = 10,000 units
    this_system_planet_list = []    #list of planets for this system, resets each time function called, contains planet object

    star = available_star_list[random.randint(0, len(available_star_list) - 1)]

    habitable_zone = star[1]
    star = star[0]
    #myprint(star)

    this_system_planet_list.append(planet(star, None, 10, False, None, None, None))
    system.habitable = habitable_zone

    min_distance_from_center = 50
    planet_radius = 120
    max_habitable_planets = 3
    is_habitable_chance = 1
    number_of_planets = random.randint(4, 5)

    temp_wormhole_chance = 0
    for existing_wormhole in wormhole_dict.keys():
        if wormhole_dict[existing_wormhole] < 2:
            temp_wormhole_chance += .015
    generate_wormholes = random.random() < wormhole_chance + temp_wormhole_chance
    max_wormhole_links = random.randint(2, 5)

    wormhole_sprite_list = ['wormhole']

    distance = min_distance_from_center
    habitable_planets = 0
    number_of_planets += int(generate_wormholes)
    i = 0
    while i < number_of_planets:
        #Determines habitable planets
        #distance = distance + random.randint(abs(distance - 100), distance * random.randint(1,2))
        distance = distance + (planet_radius * 2) + random.randint(50, 100)
        fraction = round(distance / habitable_zone, 2)
        if fraction > 2:
            planet_radius = 200

        #============Generate Wormhole last
        #Look for existing wormholes to connect to first before generating new one.
        wormhole_made = False
        if i == number_of_planets and generate_wormholes:
            sprite = "planet/" + random.choice(wormhole_sprite_list)
            for existing_wormhole in wormhole_dict.keys():
                if wormhole_dict[existing_wormhole] < max_wormhole_links:
                    name = existing_wormhole
                    wormhole_dict[name] = wormhole_dict[existing_wormhole]+1
                    wormhole_made = True
                    this_system_planet_list.append(planet(sprite, distance, period, is_habitable, name, None, None))   
                    system.attributes.append("wormhole")
                    system.attributes.append(name)
            if not wormhole_made:
                i2 = 0
                noinfinite = 0 #Prevent infinite loop of there're more planets than name list.
                while (i2 < 1) and (noinfinite <= int(galaxy_systems)*number_of_planets):
                    #name = planet_name_dict[galaxy.desc_files['planet_namelist_file']][random.randint(0, len(planet_name_dict[galaxy.desc_files['planet_namelist_file']]) - 1)]
                    if system.government != None:
                        name = namegen.generateNameFromRules(name_length_min,
                                                            name_length_max,
                                                            wordlen=system.government.lang_wordlen,
                                                            spacechance=system.government.lang_spacechance,
                                                            lang_charweight=system.government.lang_charweight)
                    else:
                        name = namegen.completelyRandomNames(name_length_min,
                                                            name_length_max)
                    name += " Wormhole"
                    if name not in planet_used_namelist:
                        planet_used_namelist.append(name)
                        wormhole_dict[name] = 1
                        wormhole_made = True
                        this_system_planet_list.append(planet(sprite, distance, period, is_habitable, name, None, None))   
                        system.attributes.append("wormhole")
                        system.attributes.append(name)
                        i2 += 1
                    noinfinite += 1

        #Generate Habitable planet if possible
        if (fraction > .5 and fraction < 2) and not wormhole_made:
            if random.uniform(0, 1) < is_habitable_chance and habitable_planets < max_habitable_planets:
                #Make sure the planets' system have government, will require this when assigning sales
                if system.government != None:
                    is_habitable = True
                    habitable_planets += 1
                else:
                    is_habitable = False
            else:
                is_habitable = False
        else:
            is_habitable = False

        possible_sprites = []
        if not is_habitable:
            for item in sprite_controls:
                if fraction >= item[1] and fraction <= item[2]:
                    possible_sprites.append(planet_sprite_dict[item[0]])

            if len(possible_sprites) == 0:
                #myprint('!!! WARNING !!! Planet was not assigned a sprite from the planet sprite config file, assigning rock0 as default sprite')
                possible_sprites.append('rock0')

            popped_sprite_list = possible_sprites[random.randint(0, len(possible_sprites) - 1)]
            sprite = "planet/" + str(popped_sprite_list[random.randint(0, len(popped_sprite_list) - 1)])
        #the period calculation is WIP, trying to figure out a good way to do it
        #period = (2 * math.pi) * sqrt((distance * distance * distance)/266470)
        period = round((distance ** 2) ** (1 / 3), 4)

        if not is_habitable:
            this_system_planet_list.append(planet(sprite, distance, period, is_habitable, None, None, None))        ##########################################################
            pass
        if is_habitable:
            i2 = 0
            noinfinite = 0 #Prevent infinite loop of there're more planets than name list.
            while (i2 < 1) and (noinfinite <= int(galaxy_systems)*number_of_planets):
                #name = planet_name_dict[galaxy.desc_files['planet_namelist_file']][random.randint(0, len(planet_name_dict[galaxy.desc_files['planet_namelist_file']]) - 1)]
                name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=system.government.lang_wordlen,
                                                    spacechance=system.government.lang_spacechance,
                                                    lang_charweight=system.government.lang_charweight)
                if name not in planet_used_namelist:
                    planet_used_namelist.append(name)
                    i2 += 1
                noinfinite += 1
            condensed_properties,description = generate_inhabited_planet(system,name)
            #planet_properties_returned = create_planet_properties(system, galaxy)
            #descriptions_temp = planet_properties_returned[0]
            #properties_list = planet_properties_returned[1]
            #condensed_properties = condense_planet_properties(properties_list)     #sorts and overrides properties
                    
            sprite = 'planet/' + str(condensed_properties.sprite)
            this_system_planet_list.append(planet(sprite, distance, period, is_habitable, name, condensed_properties, description))   #Adds this planet to the planet list for this system
            planet_names_list.append(planet(condensed_properties.sprite, distance, period, is_habitable, name, condensed_properties, description))
            #planet_names_dict["Name!"] = planet_properties("Name!") #for "Name!" add it to dict with planet_properties(properties) as properties for that planet when its name is called from planet_names_dict
        i += 1

    for item in this_system_planet_list:
        system.planet_list.append(item)
        #myprint("Appended " + str(item))

    mineables_list = ['copper','iron','lead','silicon','tungsten','titanium','gold','platinum','uranium']
    random_mineables_list = random.choices(mineables_list,k=random.randint(0,5))
    for minables in random_mineables_list:
        astrd_num = random.randrange(0,50)
        astrd_ener = random.uniform(0.1,5)
        system.mineables[minables] = [astrd_num,astrd_ener]

    global config_enable_infinite_asteroid
    if config_enable_infinite_asteroid:
        asteroids_list = ['small rock','medium rock','large rock','small metal','medium metal','large metal']
        random_asteroids_list = random.choices(asteroids_list,k=random.randint(0,6))
        for astrd in random_asteroids_list:
            astrd_num = random.randrange(0,50)
            astrd_ener = random.uniform(0.1,5)
            system.asteroids[astrd] = [astrd_num,astrd_ener]

def galaxy_write_systems(galaxy,galaxy_center_x,galaxy_center_y,galaxy_image):
    myprint('Writing systems for galaxy ' + str(galaxy.name) + '...')
    galaxy_output = open("data/galaxy" + str(galaxy.name) + galaxy_output_file, "w")

    #========Write Galaxy definition + sprite
    galaxy_output.write('galaxy ' + '"' + str(galaxy.name) + '"\n')
    galaxy_output.write('\tpos ' + str(galaxy_center_x) + ' ' + str(galaxy_center_y) + '\n')
    galaxy_output.write('\tsprite ' + '"' + str(galaxy_image) + '"\n')
    galaxy_output.write('\n')
    first_sys = 0
    hazardprint = 0
    for system in system_list:                #WRITES SYSTEMS
        #name
        galaxy_output.write('system ' + '"' + str(system.name) + '"' + "\n")
        #position
        galaxy_output.write('\tpos ' + str(system.pos).replace('(', '').replace(')', '').replace(',', '') + "\n")

        #government
        try:
            galaxy_output.write('\tgovernment ' + '"' + str(system.government.name) + '"' + "\n")
        except AttributeError:
            galaxy_output.write('\tgovernment ' + '"' + str('Uninhabited') + '"' + "\n")

        galaxy_output.write('\tattributes ')
        for attr in system.attributes:
            galaxy_output.write(f'"{attr}" ')
        galaxy_output.write('\n')

        #habitable
        galaxy_output.write(f'\thabitable {system.habitable}' + "\n")
        
        #arrival
        galaxy_output.write(f'\tarrival {max(500, min(10000, system.habitable))}' + "\n")
        
        #belt
        galaxy_output.write('\tbelt ' + str(random.randint(1000, 1500)) + "\n")

        links_temp_list = system.links
        links_temp_list_write = list(set([str(e) for e in links_temp_list ]))
        for str1 in links_temp_list_write:
            galaxy_output.write('\tlink ' + '"' + str(str1) + '"' + "\n")

        if system.haze != '':
            galaxy_output.write(f'\thaze "{system.haze}"' + "\n")

        if len(system.hazard) > 0:
            for hz in system.hazard:
                galaxy_output.write(f'\thazard "{hz.name}" '+ '\n')
                hazardprint = 1
        else:
            hazardprint = 0
        #asteroids
        #asteroids_list = ['small rock','medium rock','large rock','small metal','medium metal','large metal']
        for astrd in system.asteroids.keys():
            #astrd_num = random.randrange(0,50)
            #astrd_ener = random.uniform(0.1,5)
            galaxy_output.write(f'\tasteroids "{astrd}" {system.asteroids[astrd][0]} {system.asteroids[astrd][1]}'+'\n')
        #mineables
        #mineables_list = ['copper','iron','lead','silicon','tungsten','titanium','gold','platinum','uranium']
        #random_mineables_list = random.choices(mineables_list,k=random.randint(0,5))
        for minables in system.mineables.keys():
            galaxy_output.write(f'\tminables "{minables}" {system.mineables[minables][0]} {system.mineables[minables][1]}'+'\n')
            

        #commodities
        for commodity in commodity_dict[system.level]:
            galaxy_output.write('\ttrade ' + '"' + str(commodity[0]) + '"' + ' ' + str(random.randint(commodity[1], commodity[2])) + "\n")

        #fleet
        newFleetDistribution = True
        if newFleetDistribution:
            for key in system.fleetdicts.keys():
                galaxy_output.write(f'\tfleet "{key}" ' + str(system.fleetdicts[key]) + '\n')
        else: #===Even fleet distribution
            fleet_freq_max = 1800
            fleet_freq_min = 600
            for xx in range(len(system.fleets)): #selfNOTE: fleets were stored as list of fleets.
                for ii in range(len(system.fleets[xx])): 
                    fleetfreq = roundup100(random.randrange(fleet_freq_min,fleet_freq_max))
                    if system.capital:
                        fleetfreq *= 2
                    galaxy_output.write(f'\tfleet "{system.fleets[xx][ii]}" ' + str(fleetfreq) + '\n')
        
        
        #planets
        for planet in system.planet_list:
            if planet.name is None:
                galaxy_output.write('\tobject' + "\n")
            else:
                galaxy_output.write('\tobject "' + str(planet.name) + '"\n')
            galaxy_output.write('\t\tsprite ' + str(planet.sprite)+ "\n")
            if "star" in planet.sprite:
                pass
            else:
                galaxy_output.write('\t\tdistance ' + str(planet.distance)+ "\n")
            galaxy_output.write('\t\tperiod ' + str(planet.period)+ "\n")
        if first_sys == 0:
            galaxy_output.write('\tobject "EES Wormhole"' + "\n")
            galaxy_output.write('\t\tsprite "planet/wormhole"'+ "\n")
            galaxy_output.write('\t\tdistance 3500'+ '\n')
            galaxy_output.write('planet "EES Wormhole"' + "\n")
            first_sys += 1
        galaxy_output.write('\n')

        if hazardprint > 0:
            galaxy_output.write('galaxy ' + f'"{system.name} Hazard"\n')
            galaxy_output.write('\tpos ' + str(system.pos).replace('(', '').replace(')', '').replace(',', '') + "\n")
            galaxy_output.write('\tsprite ' + '"galaxyoverlay/' + str(system.hazard[0].cloud) + '"\n')
            galaxy_output.write('\n')

    for planet in planet_names_list:
        galaxy_output.write('planet "' + planet.name + '"\n')
        #myprint(planet.planet_properties.attribute)
        if planet.planet_properties.attribute[0] != '':
            galaxy_output.write('\tattributes ' + str(planet.planet_properties.attribute).replace('[','').replace(']','').replace("'","").replace(',','').strip() + '\n')
        galaxy_output.write('\tlandscape land/' + str(planet.planet_properties.landscape).strip('\n') + '\n')
        galaxy_output.write('\tdescription `' + str(planet.descriptions[0]) + '`\n')
        galaxy_output.write('\tspaceport `' + str(planet.descriptions[1]) + '`\n')

        if planet.planet_properties.shipyard[0] != '':
            for item in planet.planet_properties.shipyard:
                galaxy_output.write('\tshipyard "' + str(item) + '"\n')
        if planet.planet_properties.outfitter[0] != '':
            for item in planet.planet_properties.outfitter:
                galaxy_output.write('\toutfitter "' + str(item) + '"\n')

        if planet.planet_properties.required_reputation != '':
            galaxy_output.write('\t"required reputation" ' + str(planet.planet_properties.required_reputation) + '\n')
        if planet.planet_properties.bribe != '':
            galaxy_output.write('\tbribe ' + str(planet.planet_properties.bribe) + '\n')
        if planet.planet_properties.security != '':
            galaxy_output.write('\tsecurity ' + str(planet.planet_properties.security) + '\n')
        if planet.planet_properties.tribute != '':
            galaxy_output.write('\ttribute ' + str(planet.planet_properties.tribute) + '\n')
        if planet.planet_properties.threshold != '':
            galaxy_output.write('\t\tthreshold ' + str(planet.planet_properties.threshold) + '\n')
        if planet.planet_properties.fleet != '':
            galaxy_output.write('\t\tfleet ' + str(planet.planet_properties.fleet) + '\n')


        galaxy_output.write('\n')

    #    myprint("Wrote system data " + str(system_list[system_write_count].name))
    #Put a wormhole system in Milky Way
    temp_sys_name = namegen.completelyRandomNames()
    galaxy_output.write('system ' + f'"{temp_sys_name}"' + "\n")
        #position
    temp_pos_x = round(random.randrange(115,190) )
    temp_pos_y = round(random.randrange(25,50)) * -1
    galaxy_output.write(f'\tpos {temp_pos_x} {temp_pos_y}' + "\n")
    galaxy_output.write('\tobject "EES Wormhole"' + "\n")
    galaxy_output.write('\t\tsprite "planet/wormhole"'+ "\n")
    galaxy_output.write('\t\tdistance 3500'+ '\n')
    #myprint("Wrote all systems")
    galaxy_output.close()

def load_planet_config():
    planet_config_file = "config/planet config.txt"
    generate_planet_config = open(planet_config_file, "r")

    global outfitter_chance
    outfitter_chance = None
    global shipyard_chance
    shipyard_chance = None
    #Searches config file for values and creates variables
    for line in generate_planet_config: #Creates vars from txt file
        line = line.rstrip('\n')
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_planet_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("planet_seed" in line) and use_seed == True:
            pla_seed = next(generate_planet_config)
            random.seed(int(pla_seed))
        if ("planet_outfitter_chance" in line):
            outfitter_chance = float(next(generate_planet_config))
        if ("planet_shipyard_chance" in line):
            shipyard_chance = float(next(generate_planet_config))


def load_galaxy_configs(government_list):
    if government_list[0].devmode:
        random.seed(99)
    global namegen
    namegen = namegenerator.Namegenerator(government_list[0])
    galaxy_configs_list = glob.glob("config/galaxy config/*.txt") #Imports files in directory
    galaxy_configs_amount = len(galaxy_configs_list) #Gets amount of items in list\
    
    load_planet_config()
    
    galaxy_sprite_list = glob.glob("images/galaxy/*.jpg") #Get galaxy images, jpg only, png cause problems in ES.

    read_planet_description()

    global galaxy_center_x, galaxy_center_y
    galaxy_center_x = 0
    galaxy_center_y = 0

    global system_list
    system_list = []
    global galaxy_list
    galaxy_list = []
    global system_used_namelist
    system_used_namelist = []
    global system_layer
    system_layer = -1

    global planet_names_list
    planet_names_list = []

    galaxy_configs_iterations = 0
    while galaxy_configs_iterations < galaxy_configs_amount: #Creates galaxies for each config files
        global galaxy_config_file #Config File
        galaxy_config_file = str(galaxy_configs_list[galaxy_configs_iterations]).replace("\\", "/")

        global galaxy_output_file #Output file
        galaxy_output_file = ""
        galaxy_output_file = str(galaxy_configs_list[galaxy_configs_iterations]).replace("\\", "/").replace("config/galaxy config/", "" + ' ')   #This is for dynamic galaxy output with a seperate file for each galaxy config
        
        global star_config_file
        star_config_file = "config/planet config/planet sprites/000 stars.txt"

        global config_enable_infinite_asteroid
        config_enable_infinite_asteroid = True

        galaxy_place_systems()

        
        galaxy_configs_iterations += 1

    galaxy_delete_overlapping_systems()

    #Generates planets for each system in system list
    load_description_data()

    global planet_used_namelist
    planet_used_namelist = []
    global wormhole_dict
    wormhole_dict = {}
    radiusfull = 300
    radiusblackbody = 500
    assign_haze(system_list,radiusfull,radiusblackbody)
    

    for galaxy in galaxy_list:
        #myprint(f'Galaxy Radius: {galaxy.radius_x} {galaxy.radius_y}')
        hazardlist = generate_hazards(government_list[0],galaxy)
        add_hazards(system_list,hazardlist)
        galaxy_layer = galaxy.layer
        myprint(f'Generating government sectors..')
        #===============Assign government
        for government in government_list:
            #radiusX = galaxy.radius_x+galaxy.radius_x/4 #Off the edge center points.
            #radiusY = galaxy.radius_y+galaxy.radius_y/4
            minradiusX = galaxy.radius_x*government.radius[0]
            maxradiusX = galaxy.radius_x*government.radius[1]
            meanradiusX = galaxy.radius_x*government.radius[2]
            minradiusY = galaxy.radius_y*government.radius[0]
            maxradiusY = galaxy.radius_y*government.radius[1]
            meanradiusY = galaxy.radius_y*government.radius[2]
            center_pos = pick_within(galaxy.center_x,galaxy.center_y,galaxy.min_x,galaxy.max_x,galaxy.min_y,galaxy.max_y)
            region_radius_x = round(random.triangular(minradiusX,maxradiusX,meanradiusX))
            region_radius_y = round(random.triangular(minradiusY,maxradiusY,meanradiusY))
            #myprint(f"GovRegion: {center_pos} {region_radius_x}")
            government_region(center_pos[0],center_pos[1],region_radius_x,region_radius_y,system_list,government) 
        
        avgrad,bleedrad = avghyptdiff(system_list)
        myprint('Creating planets in galaxy ' + galaxy.name)
        for system in system_list:
            if system.system_layer is galaxy_layer:
                system_planets(system, galaxy)
        myprint('Placing fleets...')
        for government in government_list:
            place_fleets(government,bleedrad)
        myprint('\n\n\n')
        #todo: load image before generating system and use it as bounding box , maybe even detect features for system clusters.
        galaxy_image = random.choice(galaxy_sprite_list).removeprefix("images/").removesuffix(".jpg").replace("\\", "/")
        galaxy_write_systems(galaxy,galaxy_center_x,galaxy_center_y,galaxy_image)

    myprint("Success!")
    input("Enter to exit.")

#load_galaxy_configs()