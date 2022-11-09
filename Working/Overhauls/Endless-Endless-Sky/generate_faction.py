# Copyright (c) 2021 by 1010todd

import random
import os
#import math

import namegenerator
from generate_sprite_ship_PIL import get_overlay_pattern

#A faction in reality is extremely complex, here I'll increase the complexity later.

class government():
    def __init__(self,name,display_name=None,swizzle=0,color=[0,0,0,1],player_rep=0,boarding=[1,2],relationsdict={},penalty=[],hails=[],agg=0,age=1,tier=1):
        self.name = name
        self.display_name = display_name
        if self.display_name == None:
            self.display_name = self.name
        self.swizzle = swizzle
        self.color = color
        self.player_rep = player_rep
        self.boarding = boarding
        self.relations = relationsdict #For other factions
        self.penalty = penalty
        self.hails = hails
        #self.language
        #self.raid
        #self.bribe
        #self.fine
        #====================Background stuffs for generation
        self.age = age
        self.agg = agg
        self.tier = tier
        self.shieldhullFactor = 0.1
        self.spriteset = 'default'
        self.partset = ''
        self.designpriority = []
        self.lang_wordlen = 3
        self.lang_spacechance = .5
        self.lang_charweight = None
        self.civienametype = 'parts'
        self.militnametype = 'pregen'
        self.fleet_tactic = 'balance'
        self.civiefleetvariants = 6
        self.ftl = 'Hyperdrive'
        self.automation = 0
        self.dronechance = 0
        self.ship_speciality = ''
        self.ship_protection = {}
        self.militaryname = ''
        self.militaryinit = ''
        self.military = .5
        self.lenwid = .5 #-Ship lenght-width ratio
        self.shipsymmode = True #-Ship symmetry
        self.radius = [] #min max mean

        self.devmode = False
        self.devmodeseed = 0
        #====================Content owned by the faction
        self.shipcount = 3
        self.shiplist = []
        self.weaponlist = []
        self.outfitlist = [] #for other stuffs
        self.engineslist = []
        self.patrolfleets = []
        self.civilianfleets = []
        self.miningfleets = []
        self.outfitterlist = []
        self.shipyardlist = []
        self.systemlist = []

class SpriteData():
    def __init__(self) -> None:
        self.name = ''
        self.category = [] #If sprite can fit many category
        self.gunports = []
        self.turretmounts = []
        self.fighterbays = []
        self.dronebays = []
        self.engines = []

def get_faction_spriteset(): #Todo
    file_list = [f for f in os.listdir("factions/") if not f.startswith('000') and f.endswith(".txt")]
    select = random.choice(file_list)
    spritelist = parse_spriteset(select)
    return spritelist

def get_partset():
    file_list = [f for f in os.listdir("imgparts/") if not f.startswith('000')]
    return random.choice(file_list)
#Parse one sprite definition file
def parse_spriteset(filename):
    filename = "factions/"+filename
    filein = open(filename, 'r')

    spritelist = {}
    category_list = []
    gun_pos = {}
    turret_pos = {}
    engine_pos = {}
    #ft_bay_pos = {}
    #dn_bay_pos = {}

    shipfound = False
    gun = False
    turret = False
    engine = False
    #full = filein.readlines()
    full = filein
    for line in full:
        line = line.removesuffix('\n')
        line = line.replace('"','')
        if line.startswith('ship') and (shipfound == True):
            spritelist[sprite_name] = [category_list.copy(),gun_pos.copy(),turret_pos.copy(),engine_pos.copy()]
            shipfound == False
            category_list = []
            gun_pos = {}
            turret_pos = {}
            engine_pos = {}
            gun = False
            turret = False
            engine = False
            #print("Spritesetparse: New ship")
        if line.startswith('ship'):
            sprite_name = line[5:]
            shipfound = True
            #print(f"Spritesetparse: Ship {line}")
        if line.startswith('\tcategory') and (shipfound == True):
            sprite_category = line[10:]
            category_list.append(sprite_category)
            #print(f"Spritesetparse: Category {line}")
            #print(f"Spritesetparse: Categorylist {category_list}")
        if line.startswith('\tgun') and (shipfound == True):
            #print(f"Spritesetparse: Gun {line}")
            sprite_gun = line[5:]
            sprite_gun = sprite_gun.removeprefix('"')
            sprite_gun = sprite_gun.removesuffix('"')
            sprite_gun = sprite_gun.split()
            while len(sprite_gun) > 2:
                sprite_gun.pop()
            sprite_gun = [float(i) for i in sprite_gun]
            gun_angle = 0
            gun_parallel = False
            gun_over = False
            gun = True
        if line.startswith('\t\tangle') and (gun == True):
            try:
                gun_angle = float(line[7:])
            except ValueError:
                pass
        if line.startswith('\t\tparallel') and (gun == True):
            gun_parallel = True
        if line.startswith('\t\tover') and (gun == True):
            gun_over = True
        if (gun == True):
            gun_pos[str(sprite_gun)] = [gun_angle,gun_parallel,gun_over]
            gun = False
        if line.startswith('\tturret') and (shipfound == True):
            sprite_turret = line[8:]
            sprite_turret = sprite_turret.split()
            while len(sprite_turret) > 2:
                sprite_turret.pop()
            sprite_turret = [float(i) for i in sprite_turret]
            turret_under = False
            turret = True
        if line.startswith('\t\tunder') and (turret == True):
            turret_under = True
        if(turret == True):
            turret_pos[str(sprite_turret)] = turret_under
        if line.startswith('\tengine') and (shipfound==True):
            sprite_engine = line[8:]
            sprite_engine = sprite_engine.split()
            while len(sprite_engine) > 2:
                sprite_engine.pop()
            sprite_engine = [float(i) for i in sprite_engine]
            zoom = 1
            angle = 0
            over = False
            engine = True
        if line.startswith('\t\tzoom') and (engine == True):
            zoom = float(line[7:])
        if line.startswith('\t\tangle') and (engine == True):
            angle = float(line[7:])
        if line.startswith('\t\tover') and (engine == True):
            over = True
        if engine == True:
            engine_pos[str(sprite_engine)] = [zoom,over,angle]

    filein.close()
    return spritelist

#Create a single (currently) basic faction
def create_faction(noPIL,min_tier=0.1, max_tier=6.,devmode=False):
    #======Default values
    min_count = 8
    max_count = 12
    name_length_min = 4
    name_length_max = 9
    faction_list = []
    mean_rep = 0
    mean_tier = 1
    shipsymchance = .8


    gov_config_file = "config/government config.txt"
    generate_gov_config = open(gov_config_file, "r")
    #Searches config file for values and creates variables
    for line in generate_gov_config: #Creates vars from txt file
        line = line.rstrip('\n')
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_gov_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("government_seed" in line) and use_seed == True:
            gov_seed = next(generate_gov_config)
            random.seed(int(gov_seed))
        if ("government_min_tier" in line):
            min_tier = float(next(generate_gov_config))
        if ('government_max_tier' in line):
            max_tier = float(next(generate_gov_config))
        if ('government_mean_tier' in line):
            mean_tier = float(next(generate_gov_config))
        if ("government_radius_percent_min" in line):
            min_rad = float(next(generate_gov_config))
        if ('government_radius_percent_max' in line):
            max_rad = float(next(generate_gov_config))
        if ('government_radius_percent_mean' in line):
            mean_rad = float(next(generate_gov_config))
        if ('government_min_count' in line):
            min_count = int(next(generate_gov_config))
        if ('government_max_count' in line):
            max_count = int(next(generate_gov_config))
        if ('government_mean_count' in line):
            mean_count = int(next(generate_gov_config))
        if ('government_name_min_length' in line):
            name_length_min = int(next(generate_gov_config))
        if ('government_name_max_length' in line):
            name_length_max = int(next(generate_gov_config))
        if ('government_mean_aggression' in line):
            try:
                mean_rep = float(next(generate_gov_config))
            except StopIteration:
                pass
        if ('government_ships_per_gov_min' in line):
            min_ships = int(next(generate_gov_config))
        if ('government_ships_per_gov_max' in line):
            max_ships = int(next(generate_gov_config))
        if ('government_ships_per_gov_mean' in line):
            mean_ships = int(next(generate_gov_config))
        if ('government_militarization' in line):
            militarymean = float(next(generate_gov_config))
        if ('government_use_shipgen_chance' in line):
            shipgenchance = float(next(generate_gov_config))
        if ('government_ship_symmetrical_chance' in line):
            shipsymchance = float(next(generate_gov_config))

    if 'mean_count' not in locals():
        mean_count = min_count/max_count
    if 'militarymean' not in locals():
        militarymean = .5
    if 'mean_rep' not in locals():
        mean_rep = 0
    if 'shipgenchance' not in locals():
        shipgenchance = .8

    if devmode:
        random.seed(int(99))
    fakefac = government('fake')
    fakefac.devmode = devmode
    fakefac.devmodeseed = 89
    namegen = namegenerator.Namegenerator(fakefac)
    
    if min_count == max_count:
        government_count = round(max_count)
    else:
        government_count = round(random.triangular(min_count,max_count,mean_count))
    for n in range(government_count):
        #=======Set parameters
        faction_age = random.randrange(7) #1 = young, 6 = old
        try:
            faction_tier = random.triangular(min_tier,max_tier,mean_tier)
        except UnboundLocalError:
            faction_tier = random.triangular(min_tier,max_tier)

        faction_agg = random.triangular(-1,1,mean_rep)

        if random.random() > shipgenchance or noPIL:
            faction_sprite = get_faction_spriteset()
            faction_partset = ''
        else:
            faction_sprite = 'generated'
            faction_partset = get_partset()

        try:
            ships_count = random.triangular(min_ships,max_ships,mean_ships)
        except UnboundLocalError:
            ships_count = random.triangular(min_ships,max_ships)
        
        ships_count = max(min_ships,ships_count)
        ships_symmetry = random.random() <= shipsymchance

        color_width = random.randint(3,12)
        color_variation = random.randint(1,5)
        pattern_complexity = random.randint(1,5) # 1 just straight lines, 5 random turns

        ships_color_pattern_palette = random.randint(1,4)
        ships_color_pattern = get_overlay_pattern(ships_color_pattern_palette)

        faction_military = random.triangular(.1,1,militarymean)
        if faction_agg < 0:
            faction_military += random.uniform(.1,.3)
        faction_military = min(1,faction_military)

        JDchance = .5
        #I don't know much about this, suggestion welcome.
        policy_list = 'expansionist isolationist economist xenophobic explore'.split()
        ethics = []
        moral = []
        #behavior_list = 'neutral aggressive friendly'.split()

        #Standard stats faction could focus on.
        ship_regular_stats = 'shield hull shield_regen hull_regen fuel crew_req outfit weapon engine'.split()
        #ship_shield_hull = 'shield hull balance'.split()
        ship_shield_hull_factor = random.uniform(.1,.9) # .1 shield, .9 hull
        #Special stats faction could gain, weighted from reg stats
        #shield = piercing, disruption...
        ship_special_stats = random.choice('shielding armor heat agility'.split())
        ship_protection = {'hull': 0, 'shield': 0, 'heat': 0, 'burn': 0}
        tech_branches = {'armor': 0, 'shield': 0, 'heat': 0, 'mass': 0, 'space': 0}
        techpoints = random.randrange(2,5) + round(faction_tier) + round(faction_age)

        for point in range(techpoints):
            target_tech = random.choice(list(tech_branches.keys()))
            tech_branches[target_tech] += point
        if random.random() < .001 + min(.9,faction_tier/10):
            if random.random() < ship_shield_hull_factor:
                ship_protection['shield'] = tech_branches['shield'] * .1
            else:
                ship_protection['hull'] = tech_branches['armor'] * .1
            if random.random() < tech_branches['heat']/10:
                if random.random() > .3:
                    ship_protection['heat'] = tech_branches['heat'] * .1
                elif random.random() > .5:
                    ship_protection['burn'] = tech_branches['heat'] * .1
                else:
                    ship_protection['heat'] = tech_branches['heat'] * .05
                    ship_protection['burn'] = tech_branches['heat'] * .05
            
        civie_fleet_variant_min = 3
        civie_fleet_variant_max = 12
        civiefleetvariants = random.randrange(civie_fleet_variant_min,civie_fleet_variant_max)
        fleet_tactic = random.choice('defense offense balance hitrun kite'.split())
        designpriority = 'engine power defense weapon'.split()
        random.shuffle(designpriority)
        if faction_tier >= 2.5 and random.random() > JDchance+faction_tier/10:
            ftl_method = 'Jump Drive'
        else:
            ftl_method = 'Hyperdrive'

        ship_lenghtwidthratio = random.triangular(.3,.7)
        automation = random.random()
        dronechance = random.random() + (automation*.5)

        lang_civie_type = random.choice(['pregen','parts'])
        lang_milit_type = random.choice(['pregen','parts'])
        az = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split()
        lang_wordlen = random.choice([3,4,5])
        lang_spacechance = random.triangular(.01,.9,.2)
        lang_charweight =  []
        for nn in az:
            lang_charweight.append(random.random())

        name = namegen.generateNameFromRules(name_length_min,
                                             name_length_max,
                                             wordlen=lang_wordlen,
                                             spacechance=lang_spacechance,
                                             lang_charweight=lang_charweight)
        militaryname = namegen.generateNameFromRules(name_length_min,
                                             name_length_max,
                                             wordlen=lang_wordlen,
                                             spacechance=lang_spacechance,
                                             lang_charweight=lang_charweight)
        militaryinit = namegen.generateInitials(militaryname)
        swizzle = random.randrange(0,22)
        color = [random.random() for n in range(4)] #Randomize 0-1 for 4 times (RGBA)
        color[3] = max(color[3],.1) #Make sure alpha is at least .1
        player_reputation = round(faction_agg)

        faction = government(name,swizzle=swizzle,color=color,player_rep=player_reputation,age=faction_age,tier=faction_tier,agg=faction_agg)
        #action.shieldhull = random.choice(ship_shield_hull)
        faction.shieldhullFactor = ship_shield_hull_factor
        faction.spriteset = faction_sprite
        faction.partset = faction_partset
        faction.shipcount = ships_count
        faction.fleet_tactic = fleet_tactic
        faction.civiefleetvariants = civiefleetvariants
        faction.boarding[0] = round(faction.tier**(faction.tier/random.uniform(2.5,5)),1)
        faction.boarding[1] = round((faction.tier**(faction.tier/random.uniform(2.5,5)))*2,1)
        faction.lang_wordlen = lang_wordlen
        faction.lang_spacechance = lang_spacechance
        faction.lang_charweight = lang_charweight
        faction.ftl = ftl_method
        faction.automation = automation
        faction.dronechance = dronechance
        faction.ship_protection = ship_protection
        faction.ship_speciality = ship_special_stats
        faction.designpriority = designpriority
        faction.military = faction_military
        faction.lenwid = ship_lenghtwidthratio
        faction.shipsymmode = ships_symmetry
        faction.militaryname = militaryname
        faction.militaryinit = militaryinit
        faction.civienametype = lang_civie_type
        faction.militnametype = lang_milit_type
        faction.radius = [min_rad,max_rad,mean_rad]
        faction.devmode = devmode
        faction.devmodeseed = n+10

        print("faction name; ", name)
        print("faction tier " ,faction_tier)
        print("faction s/h ", ship_shield_hull_factor)
        #print("faction sprite ", faction_sprite)
        try:
            os.makedirs('data/'+name)
        except FileExistsError:
            pass
        faction_list.append(faction)
    generate_gov_config.close()
    return faction_list

#Randomize government relationship, depending on their aggression value a well.
def generategovernmentRelations(government_list):
    print("Generating Government Relations...")
    for gov1 in government_list:
        temp_relation_dict = {}
        print("Current:", gov1.name)
        for gov2 in government_list:
            if gov1 == gov2:
                pass
            elif(round(gov1.agg + gov2.agg) <= -1):
                temp_relation_dict[str(gov2.name)] = -1
            elif(round(gov1.agg + gov2.agg) >= 1):
                temp_relation_dict[str(gov2.name)] = 0 + round(random.random())
            else:
                temp_relation_dict[str(gov2.name)] = round(random.randrange(-1,1))
        gov1.relations = temp_relation_dict
        print(temp_relation_dict)
    return government_list

def write_government_file(government,filepath=''):
    if filepath == '':
        filepath = f'data/{government.name}/government.txt'
    fileout = open(filepath, 'w')
    fileout.write(f'government "{government.name}"'+'\n')
    fileout.write(f'\t"display name" "{government.display_name}"'+'\n')
    fileout.write(f'\t"swizzle" {government.swizzle}'+'\n')
    fileout.write(f'\t"color" {government.color[0]:.3f} {government.color[1]:.3f} {government.color[2]:.3f} {government.color[3]:.3f}'+'\n')
    fileout.write(f'\t"player reputation" {government.player_rep}'+'\n')
    fileout.write(f'\t"crew attack" {government.boarding[0]}'+'\n')
    fileout.write(f'\t"crew defense" {government.boarding[1]}'+'\n')
    fileout.write(f'\t"attitude toward"'+'\n')
    for key in government.relations.keys():
        fileout.write(f'\t\t"{key}" {government.relations[key]}'+'\n')

    fileout.close()