# Copyright (c) 2020 by Nucleartaxi

#Imports
import math
from math import sqrt
#import time
import glob
import random
import os

import namegenerator


def roundup1000(x):
    return int(math.ceil(x / 1000.0)) * 1000
def roundup100(x):
    return int(math.ceil(x / 100.0)) * 100
def roundup10(x):
    return int(math.ceil(x / 10.0)) * 10
def roundup5(x):
    return int(math.ceil(x / 5.0)) * 5

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

class class_Outfit():
    def __init__(self,name,outfit_category,cost,thumbnail,mass,outfit_space=0,weapon_space=0,engine_space=0) -> None:
        self.name = name
        self.category = outfit_category
        self.cost = cost
        self.thumbnail = thumbnail
        self.mass = mass
        self.outfit_space = outfit_space
        self.weapon_space = weapon_space
        self.engine_space = engine_space
        
        #=====================Note: Not complete.
        self.cooling = 0
        self.active_cooling = 0
        self.cooling_ener = 0
        self.cooling_ineffi = 0

        self.energy_cap = 0
        self.energy_gen = 0
        self.energy_use = 0 #energy consumption
        self.heat_gen = 0

        self.shields = 0
        self.shields_gen = 0
        self.shields_ener = 0
        self.shields_heat = 0
        self.shields_fuel = 0
        self.shields_delay = 0
        self.shields_empty_delay = 0
        self.shields_gen_mult = 0
        self.shields_ener_mult = 0
        self.shields_heat_mult = 0
        self.shields_fuel_mult = 0
        
        self.hull = 0
        self.hull_repair = 0
        self.hull_ener = 0
        self.hull_heat = 0
        self.hull_fuel = 0
        self.hull_delay = 0
        self.hull_dis_delay = 0
        self.hull_repair_mult = 0
        self.hull_ener_mult = 0
        self.hull_heat_mult = 0
        self.hull_fuel_mult = 0

        self.ramscoop = 0
        self.solar_ener = 0
        self.solar_heat = 0

        self.fuel_cap = 0
        self.fuel_use = 0
        self.fuel_use_heat = 0
        self.fuel_use_ener = 0
        self.fuel_gen = 0

        self.thrust = 0
        self.thrust_ener = 0
        self.thrust_heat = 0
        self.turn = 0
        self.turn_ener = 0
        self.turn_heat = 0
        self.reverse = 0
        self.reverse_ener = 0
        self.reverse_heat = 0
        self.thrust_flare_sprite = 0

        self.boarding_atk = 0
        self.boarding_def = 0


#Deletes Files
#filelist = glob.glob(os.path.join("output/", "*.txt"))
#for f in filelist:
#    os.remove(f)

#Outfits
def create_battery(faction,fileout=''):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    battery_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    for line in generate_outfits_config: #Creates vars from txt file
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_outfits_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("outfit_seed" in line) and use_seed == True:
            outfit_seed = next(generate_outfits_config)
            random.seed(int(outfit_seed))
    if faction.devmode:
        random.seed(faction.devmodeseed)


    battery_type_amount = 1

    battery_types_generated_count = 1
    while battery_types_generated_count <= int(battery_type_amount):

        #Calculates new values
        battery_outfit = random.randint(5, 10)
        battery_energy = roundup10(random.randint(int(2000*random.uniform(1.1*faction.tier,2*faction.tier)), int(5000*random.uniform(1.1*faction.tier,2*faction.tier))))
        battery_cost = roundup100(random.randint(round((battery_energy/battery_outfit)*500),round((battery_energy/battery_outfit)*600)))

        battery_cost_curve = .9
        battery_outfit_curve = round(random.gauss(1, .1),1)
        battery_energy_curve = round(1.1*(max(1,faction.tier/2)),1)
        battery_iterations = round(random.gauss(4, 1))

        battery_type = random.choice(['Battery','Capacitor','Battery Pack','Capacitor Pack','Battery Rack','Capacitor Rack','Storage Device','Power Storage', 'Power Cache'])
        
        battery_iterations_count = 1
        #Battery Name
        battery_name_list=[]
        for n in range(battery_iterations):
            name_length_min = 3
            name_length_max = 7
            battery_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=faction.devmodeseed+n)
            battery_name_list.append(battery_name)
        battery_name_list.sort() #Sort like vanilla names.
        battery_thumb_list = ['tiny battery','small battery','medium battery', 'large battery','huge battery']
        if random.random() < .3:
            battery_thumb_list = ['battery-s 1','battery-m 1','battery-l 1', 'battery-h 1','battery-h 1']
        if random.random() < faction.tier*.5:
            battery_thumb_list = ['tiny battery hai','small battery hai','medium battery hai', 'large battery hai','huge battery hai']
       

        for aa in range(battery_iterations):
            battery_name_final = battery_name_list[battery_iterations_count-1] + " " + battery_type

            battery_thumb = battery_thumb_list[min(4,aa)]
            #Writes ES code to file, use \n for line break
            battery_output.write('outfit "' + battery_name_final + '"' + "\n")
            battery_output.write('\tcategory "Power"\n')
            battery_output.write('\tcost ' + str(battery_cost) + "\n")
            battery_output.write(f'\tthumbnail "outfit/{battery_thumb}"\n')
            battery_output.write('\t"mass" ' + str(battery_outfit) + "\n")
            battery_output.write('\t"outfit space" -' + str(battery_outfit) + "\n")
            battery_output.write('\t"energy capacity" ' + str(battery_energy) + "\n")
            battery_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Battery"\n')
            battery_output.write('\n')

            outfitter_output.write(f'\t"{battery_name_final}"' + '"\n')

            outfit = class_Outfit(battery_name_final,'Power',battery_cost,battery_thumb,battery_outfit,battery_outfit)
            outfit.energy_cap = battery_energy
            faction.outfitlist.append(outfit)
            print(f'Created battery "{battery_name_final}"')

            #Iterate for next run of loop
            battery_cost = roundup100((battery_cost * 2) * float(battery_cost_curve))
            battery_outfit = round((battery_outfit * 2) * float(battery_outfit_curve))
            battery_energy = roundup10((battery_energy * 2) * float(battery_energy_curve))

        battery_types_generated_count += 1
    battery_output.write('\n')
    outfitter_output.close()
    generate_outfits_config.close()
    battery_output.close()
#============================================================================================
#============================================COOLING=========================================
#============================================================================================

def create_cooling(faction,fileout='',max_outfit_count=8, min_outfit_space=1, max_outfit_space = 10,coolingmin=None):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    cooling_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    for line in generate_outfits_config: #Creates vars from txt file
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_outfits_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("outfit_seed" in line) and use_seed == True:
            outfit_seed = next(generate_outfits_config)
            random.seed(int(outfit_seed))
    if faction.devmode:
        random.seed(faction.devmodeseed)
    if max_outfit_count > 1:
        cooling_type_amount = random.randrange(1,max(2,max_outfit_count))
    else:
        cooling_type_amount = max_outfit_count

    coolingmin = max(coolingmin,1)
    cooling_types_generated_count = 1
    while cooling_types_generated_count <= int(cooling_type_amount):
        #Calculates new values
        
        if coolingmin != None:
            for n in range(max_outfit_space*2):
                cooling_cooling = round(((random.randrange(int(coolingmin), int(coolingmin*2)))), 1)
                cooling_outfit = random.randrange(round(max(1,cooling_cooling)/(2.5+faction.tier)), round(max(2,cooling_cooling/2+(faction.tier/2))))
                if cooling_outfit < max_outfit_space:
                    break
        else:
            cooling_outfit = random.randrange(int(max(1,min_outfit_space)), int(max(2,max_outfit_space)))
            cooling_cooling = round(random.randrange(int(1), int(5*cooling_outfit)), 1)
        cooling_outfit = max(1,cooling_outfit)
        cooling_cost = roundup100(random.randrange(int(8500*(cooling_outfit/cooling_cooling)), int(10000*(cooling_outfit/cooling_cooling)))*faction.tier)
        cooling_ener = 0
        cooling_active = 0
        if random.random() > .7:
            cooling_ener = random.gauss(.3/min(.7,faction.tier),.1)
            cooling_active = round(((random.randint(int(1), int(15*cooling_outfit)))), 1)
            if random.random()>.5:
                cooling_cooling = 0
            cooling_ener *= cooling_cooling

        #cooling Name        
        cooling_type_name = ['Cooling','Cooler','Heat Shunt','Heatsink','Heat Pump','Temperature Control']
        cooling_type = random.choice(cooling_type_name)
        cooling_name_list = []

        cooling_iterations = int(random.randrange(1,max(2,cooling_type_amount/2)))

        for n in range(cooling_iterations):
            name_length_min = 3
            name_length_max = 7
            seedy =0 
            if faction.devmode:
                seedy = faction.devmodeseed+n
            cooling_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=seedy)
            cooling_name = cooling_name + ' ' + cooling_type
            cooling_name_list.append(cooling_name)
        cooling_name_list.sort()
        
        cooling_cost_curve = .85
        cooling_outfit_curve = 1.1
        cooling_cooling_curve = random.uniform(1.1,1.3)
        cooling_small = random.choice(['cooling ducts','cooling ducts hai','water cooling','cooling module','small heat shunt','small sheragi cooling','thermoelectric cooler'])
        cooling_large = random.choice(['wanderer heat sink','hai williwaw','large heat shunt','liquid helium','liquid nitrogen'])
        #Iterates Values
        cooling_iterations_count = 1
        while cooling_iterations_count <= cooling_iterations:
            cooling_name_final = cooling_name_list[cooling_iterations_count-1]
            if cooling_outfit < 20:
                cooling_thumb = cooling_small
            else:
                cooling_thumb = cooling_large
            #Writes ES code to file, use \n for line break
            cooling_output.write('outfit "' + cooling_name_final + '"' + "\n")
            cooling_output.write('\tcategory "Systems"\n')
            cooling_output.write('\tcost ' + str(cooling_cost) + "\n")
            cooling_output.write(f'\tthumbnail "outfit/{cooling_thumb}"\n')
            cooling_output.write('\t"mass" ' + str(cooling_outfit) + "\n")
            cooling_output.write('\t"outfit space" -' + str(cooling_outfit) + "\n")
            if cooling_cooling != 0:
                cooling_output.write('\t"cooling" ' + str(round(cooling_cooling,1)) + "\n")
            if cooling_active != 0:
                cooling_output.write('\t"active cooling" ' + str(round(cooling_active,1)) + "\n")
            if cooling_ener != 0:
                cooling_output.write('\t"cooling energy" ' + str(cooling_ener) + "\n")
            cooling_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Cooling"\n')
            cooling_output.write('\n')

            outfitter_output.write(f'\t"{cooling_name_final}"' + '\n')
            outfit = class_Outfit(cooling_name_final,'Systems',cooling_cost,cooling_outfit,cooling_outfit,cooling_outfit)
            outfit.cooling_ener = cooling_ener
            outfit.active_cooling = cooling_active
            outfit.cooling = cooling_cooling
            faction.outfitlist.append(outfit)

            print(f'Created cooling {faction.name} ' + cooling_name_list[cooling_iterations_count-1] + '.')

            #Iterate for next run of loop
            cooling_cost = roundup100((cooling_cost * 2) * float(cooling_cost_curve))
            cooling_outfit = round((cooling_outfit * 2) * float(cooling_outfit_curve))
            cooling_cooling = round((cooling_cooling * 2) * float(cooling_cooling_curve), 1)

            cooling_iterations_count += 1
        cooling_types_generated_count += 1
    cooling_output.write('\n')
    #outfitter_output.close()
    generate_outfits_config.close()
    cooling_output.close()
#============================================================================================
#============================================POWER===========================================
#============================================================================================
def create_power(faction,fileout = '',power_type_amount=0, min_outfit_space=10, max_outfit_space = 20): 
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    power_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    for line in generate_outfits_config: #Creates vars from txt file
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_outfits_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("outfit_seed" in line) and use_seed == True:
            outfit_seed = next(generate_outfits_config)
            random.seed(int(outfit_seed))
    if faction.devmode:
        random.seed(99)
    if power_type_amount <= 0:
        power_type_amount = max(1,round(random.gauss(2, 1),1))

    #Generate sets of energy generators;
    for n in range(int(power_type_amount)):
        #Calculates new values
        
        power_outfit = random.randint(int(min_outfit_space), int(max_outfit_space))
        power_power = round(((random.uniform(float((1)*faction.tier), float((1.3)*faction.tier)))), 1)
        power_heat = round(((random.uniform(float(power_power), float((power_power)*3)))), 1)
        power_cost = roundup100(random.uniform(round(((power_power*60)/power_outfit)*1500*faction.tier), round(((power_power*60)/power_outfit)*3500*faction.tier)))

        power_iterations = round(random.gauss(3, 1))
        power_type = random.choice(['Generator','Core','Reactor', 'Cell'])
        
        pow_heat_effciency = random.gauss(max(1,faction.tier), 1)/max(1,faction.tier)

        pow_intbattery = random.uniform(0.1,.9)
        pow_battchance = .3

        pow_batter = 0
        if random.random() < pow_battchance:
            batterylow = roundup10((pow_intbattery*power_outfit)*150*random.uniform(1.1*faction.tier,2*faction.tier))
            batteryhigh = roundup10((pow_intbattery*power_outfit)*550*random.uniform(1.1*faction.tier,2*faction.tier))
            pow_batter = random.randrange(batterylow,batteryhigh)

        #Power Name
        power_name_list=[]
        for n in range(power_iterations):
            name_length_min = 3
            name_length_max = 7
            seedy =0 
            if faction.devmode:
                seedy = faction.devmodeseed+n
            power_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=seedy)
            power_name_list.append(power_name)
        power_name_list.sort()

        power_cost_curve = .85
        power_outfit_curve = round(random.gauss(1, .1),1)
        power_power_curve = round(1.1*(max(1,faction.tier/2)),1)
        power_heat_curve = round(1.1*pow_heat_effciency,1)
        battery_energy_curve = round(1.1*(max(1,random.uniform(faction.tier/3,faction.tier/2))),1)

        power_thumb_list = ['tiny fuel cell','small fuel cell','medium fuel cell','large fuel cell','huge fuel cell']
        if power_iterations <= 3:
            powfusions = ['dwarf core','fusion','core']
            powhfusions = ['dwarf core hai','fusion hai','hai boulder']
            powhfusions2 = ['hai pebble core','hai geode','hai boulder']
            powplasma = ['plasma core','double plasma core','triple plasma core']
            powfission = ['fission','breeder','stack core']
            powrem = ['millennium cell','epoch cell','aeon cell']
            power_thumb_list = random.choice([powfusions,powhfusions,powhfusions2,powplasma,powfission,powrem])
        elif power_iterations <= 4:
            power_thumb_list = ['red sun','yellow sun','white sun','blue sun']
        #Iterates Values
        power_iterations_count = 1
        while power_iterations_count <= int(power_iterations):
            power_name = power_name_list[power_iterations_count-1] + ' ' + power_type
            power_thumb = power_thumb_list[min(4,power_iterations_count-1)]
            #Writes ES code to file, use \n for line break
            power_output.write('outfit "' + power_name + '"\n')
            power_output.write('\tcategory "Power"\n')
            power_output.write('\tcost ' + str(power_cost) + "\n")
            power_output.write(f'\tthumbnail "outfit/{power_thumb}"\n')
            power_output.write('\t"mass" ' + str(power_outfit) + "\n")
            power_output.write('\t"outfit space" -' + str(power_outfit) + "\n")
            power_output.write('\t"energy generation" ' + str(power_power) + "\n")
            if pow_batter != 0:
                power_output.write(f'\t"energy capacity" {pow_batter}' + "\n")
            power_output.write('\t"heat generation" ' + str(power_heat) + "\n")
            power_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Power generator"\n')
            power_output.write('\n')

            outfitter_output.write('\t"' + power_name + '"\n')

            outfit = class_Outfit(power_name,'Power',power_cost,power_thumb,power_outfit,power_outfit)
            outfit.energy_gen = power_power
            outfit.energy_cap = pow_batter
            outfit.heat_gen = power_heat
            faction.outfitlist.append(outfit)
            #Name
            print(f"Created power {faction.name}" + power_name_list[power_iterations_count-1] + ' ' + power_type)

            #Iterate for next run of loop
            power_cost = roundup100((power_cost * 2) * float(power_cost_curve))
            power_outfit = round((power_outfit * 2) * float(power_outfit_curve))
            power_power = round((power_power * 2) * float(power_power_curve), 1)
            power_heat = round((power_heat * 2) * float(power_heat_curve), 1)
            pow_batter = round((pow_batter * 2) * float(battery_energy_curve), 1)

            power_iterations_count += 1
    power_output.write('\n')
    outfitter_output.close()
    generate_outfits_config.close()
    power_output.close()

#============================================================================================
#============================================ENGINE===========================================
#============================================================================================
def create_engines(faction,fileout=''):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    engines_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    for line in generate_outfits_config: #Creates vars from txt file
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_outfits_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("outfit_seed" in line) and use_seed == True:
            outfit_seed = next(generate_outfits_config)
            random.seed(int(outfit_seed))
    if faction.devmode:
        random.seed(99)
    
    global engine_type_amount
    engine_type_amount = random.randrange(1,2)

    engine_types_generated_count = 1
    while engine_types_generated_count <= int(engine_type_amount):

        engines_outfit = random.randint(int(8), int(20))
        engines_thrust = round(((random.uniform(float(18000), float(25000))) / 3600), 1) #3600 to turn to in-game value thing.
        engines_energy = round(((random.uniform(float(60/max(.8,faction.tier)), float(80/max(.8,faction.tier)))) / 60), 1)
        engines_heat = round(((random.uniform(float(engines_energy*60), float((engines_energy*60)*2))) / 60), 1)
        engines_cost = roundup100(random.uniform(round((engines_thrust*3600)/engines_outfit)*1000, round((engines_thrust*3600)/engines_outfit)*2500))
        engines_framerate = random.uniform(1,1.5)
        engines_frameiteration = random.uniform(.1,.2)

        steering_modifier = random.uniform(1.1,1.5)
        
        steering_outfit = int(engines_outfit/steering_modifier)
        steering_thrust = int(engines_thrust*random.uniform(25,30))
        steering_energy = round(float(engines_energy/steering_modifier),1)
        steering_heat = round(float(engines_heat/steering_modifier),1)
        steering_cost = int(engines_cost/steering_modifier)

        engines_iterations = max(1,round(random.gauss(4, 1)))

        engine_name_list=[]
        for n in range(engines_iterations):
            name_length_min = 3
            name_length_max = 7
            seedy =0 
            if faction.devmode:
                seedy = faction.devmodeseed+n
            engine_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=seedy)
            engine_name_list.append(engine_name)
        engine_name_list.sort()
        #print("EngineNameList: ",engine_name_list)

        engines_cost_curve = .85
        engines_outfit_curve = round(random.gauss(1, .1),1)
        engines_thrust_curve = round(1.1+(max(1,faction.tier/3)/10),1)
        engines_engines_curve = round(1.1*(max(1,2/faction.tier)),1)
        engines_heat_curve = round(1.1*(max(1,2/faction.tier)),1)

        engines_flare_list = ['ion flare','plasma flare','atomic flare','remnant flare',"ka'het flare"]
        engines_flare_size = ['small','medium','large']
        engines_flare_type = random.choice(engines_flare_list)

        #Iterates Values
        engines_iterations_count = 1
        for engine_name_loop in engine_name_list:
            engine_name_final = engine_name_loop + ' Thruster' #3 size for now.
            engine_type = engines_flare_type.split()[0]
            engine_thumb = engines_flare_size[min(2,engines_iterations_count-1)] + ' ' + engine_type + ' thruster'
            engine_flare = engines_flare_type + '/' + engines_flare_size[min(2,engines_iterations_count-1)]
            engine_sound = engine_type + ' ' + engines_flare_size[min(2,engines_iterations_count-1)]
            
            #Writes ES code to file, use \n for line break
            engines_output.write('outfit "' + engine_name_final + '"' + "\n")
            engines_output.write('\tcategory "Engines"\n')
            engines_output.write('\tcost ' + str(engines_cost) + "\n")
            engines_output.write(f'\tthumbnail "outfit/{engine_thumb}"\n')
            engines_output.write('\t"mass" ' + str(engines_outfit) + "\n")
            engines_output.write('\t"outfit space" -' + str(engines_outfit) + "\n")
            engines_output.write('\t"engine capacity" -' + str(engines_outfit) + "\n")
            engines_output.write('\t"thrust" ' + str(engines_thrust) + "\n")
            engines_output.write('\t"thrusting energy" ' + str(engines_energy) + "\n")
            engines_output.write('\t"thrusting heat" ' + str(engines_heat) + "\n")
            engines_output.write(f'\t"flare sprite" "effect/{engine_flare}"\n')
            engines_output.write(f'\t\t"frame rate" {engines_framerate}\n')
            engines_output.write(f'\t"flare sound" "{engine_sound}"\n')
            engines_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Thruster"\n')
            engines_output.write('\n')

            outfitter_output.write('\t"' + engine_name_final + '"\n')

            outfit = class_Outfit(engine_name_final,'Engines',engines_cost,engine_thumb,engines_outfit,engines_outfit,engine_space=engines_outfit)
            outfit.thrust = engines_thrust
            outfit.thrust_ener = engines_energy
            outfit.thrust_heat = engines_heat
            outfit.thrust_flare_sprite = engine_flare
            faction.engineslist.append(outfit)
            #Name
            print("Created engines " + engine_name_loop + ' Thruster')

            #Iterate for next run of loop
            engines_cost = roundup100((engines_cost * 2) * float(engines_cost_curve))
            engines_outfit = round((engines_outfit * 2) * float(engines_outfit_curve))
            engines_thrust = round((engines_thrust * 2) * float(engines_thrust_curve), 1)
            engines_energy = round((engines_energy * 2) * float(engines_engines_curve), 1)
            engines_heat = round((engines_heat * 2) * float(engines_heat_curve), 1)
            engines_framerate = round(max(.1,engines_framerate - engines_frameiteration))

            #=================================STEERING
            steering_name_final = engine_name_loop+ ' Steering'
            steer_thumb = engines_flare_size[min(2,engines_iterations_count-1)] + ' ' + engine_type + ' steering'

            engines_output.write('outfit "' + steering_name_final + '"' + "\n")
            engines_output.write('\tcategory "Engines"\n')
            engines_output.write('\tcost ' + str(steering_cost) + "\n")
            engines_output.write(f'\tthumbnail "outfit/{steer_thumb}"\n')
            engines_output.write('\t"mass" ' + str(steering_outfit) + "\n")
            engines_output.write('\t"outfit space" -' + str(steering_outfit) + "\n")
            engines_output.write('\t"engine capacity" -' + str(steering_outfit) + "\n")
            engines_output.write('\t"turn" ' + str(steering_thrust) + "\n")
            engines_output.write('\t"turning energy" ' + str(steering_energy) + "\n")
            engines_output.write('\t"turning heat" ' + str(steering_heat) + "\n")
            engines_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} steering"\n')
            engines_output.write('\n')

            outfitter_output.write('\t"' + steering_name_final + '"\n')

            outfit2 = class_Outfit(steering_name_final,'Engines',steering_cost,engine_thumb,steering_outfit,steering_outfit,engine_space=steering_outfit)
            outfit2.turn = steering_thrust
            outfit2.turn_ener = steering_energy
            outfit2.turn_heat = steering_heat
            #outfit.thrust_flare_sprite = engine_flare
            faction.engineslist.append(outfit2)

            print("Created steering " + engine_name_loop+ ' Steering')

            steering_cost = roundup100((engines_cost * 2) * float(engines_cost_curve))
            steering_outfit = round((steering_outfit * 2) * float(engines_outfit_curve))
            steering_thrust = round((steering_thrust * 2) * float(engines_thrust_curve), 1)
            steering_energy = round((steering_energy * 2) * float(engines_engines_curve), 1)
            steering_heat = round((steering_heat * 2) * float(engines_heat_curve), 1)

            engines_iterations_count += 1
        engine_types_generated_count += 1
    engines_output.write('\n')
    outfitter_output.close()
    generate_outfits_config.close()
    engines_output.close()

#============================================================================================
#============================================SHIELD===========================================
#============================================================================================
def create_shield_generator(faction,fileout=''):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    shield_gen_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    #for line in generate_outfits_config: #Creates vars from txt file

    shield_gen_type_amount = random.randrange(1,2)

    shield_gen_types_generated_count = 1
    while shield_gen_types_generated_count <= int(shield_gen_type_amount):
        #Calculates new values
        shield_gen_delaychance = .1
        shield_gen_outfit = random.randint(int(5), int(20))
        shield_gen_shield_generation = round(random.uniform(float(0.1*max(1,faction.tier*faction.tier)), float(0.2*max(1,faction.tier*faction.tier))), 2)
        shield_gen_shield_energy = round(random.uniform(float(shield_gen_shield_generation), float(shield_gen_shield_generation*2)), 2)
        shield_gen_shield_heat = round(random.uniform(shield_gen_shield_energy*0,shield_gen_shield_energy*2))
        shield_gen_cost = roundup100(random.randint(round(((shield_gen_shield_generation*60*faction.tier)/shield_gen_outfit)*3200*faction.tier), round(((shield_gen_shield_generation*60*faction.tier)/shield_gen_outfit)*5500*faction.tier)))
        shield_gen_delay = 0
        if random.random() < shield_gen_delaychance:
            shield_gen_delay = round(random.uniform(1,120))
            shield_gen_shield_generation *= round(shield_gen_delay*random.uniform(1,3),1)
        shield_gen_type = random.choice(['Shield Generator','Shield Core','Shield Regenerator', 'Shielding', 'Shield Rejuvenator'])
        shield_gen_iterations = round(random.gauss(4,2))
        #shield_gen Name
        sheild_gen_name_list=[]
        for n in range(shield_gen_iterations):
            name_length_min = 3
            name_length_max = 7
            shield_gen_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=faction.devmodeseed+n)
            sheild_gen_name_list.append(shield_gen_name)
        sheild_gen_name_list.sort()

        shield_gen_cost_curve = .9
        shield_gen_outfit_curve = .75
        shield_gen_shield_generation_curve = 1
        shield_gen_shield_energy_curve = round(0.9/(max(1,faction.tier/2)),1)
        shield_gen_delay_curve = random.uniform(.6,1.2)

        #Iterates Values
        shield_gen_iterations_count = 1
        while shield_gen_iterations_count <= int(shield_gen_iterations):
            shield_gen_name_final = sheild_gen_name_list[shield_gen_iterations_count-1] + ' '+ shield_gen_type
            shield_size = ['tiny','small','medium','large','huge']
            shield_thumb =  shield_size[min(4,shield_gen_iterations_count-1)]+' shield'
            #Writes ES code to file, use \n for line break
            shield_gen_output.write('outfit "' + shield_gen_name_final + '"\n')
            shield_gen_output.write('\tcategory "Systems"\n')
            shield_gen_output.write('\tcost ' + str(shield_gen_cost) + "\n")
            shield_gen_output.write(f'\tthumbnail "outfit/{shield_thumb}"\n')
            shield_gen_output.write('\t"mass" ' + str(shield_gen_outfit) + "\n")
            shield_gen_output.write('\t"outfit space" -' + str(shield_gen_outfit) + "\n")
            shield_gen_output.write('\t"shield generation" ' + str(shield_gen_shield_generation) + "\n")
            if shield_gen_delay != 0:
                shield_gen_output.write('\t"shield delay" ' + str(shield_gen_delay) + "\n")
            shield_gen_output.write('\t"shield energy" ' + str(shield_gen_shield_energy) + "\n")
            if shield_gen_shield_heat != 0:
                shield_gen_output.write('\t"shield heat" ' + str(shield_gen_shield_heat) + "\n")
            shield_gen_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} shield gen"\n')
            shield_gen_output.write('\n')

            outfitter_output.write('\t"' + shield_gen_name_final + '"\n')

            outfit = class_Outfit(shield_gen_name_final,'Systems',shield_gen_cost,shield_thumb,shield_gen_outfit,shield_gen_outfit)
            outfit.shields_gen = shield_gen_shield_generation
            outfit.shields_ener = shield_gen_shield_energy
            outfit.shields_heat = shield_gen_shield_heat
            faction.outfitlist.append(outfit)

            print('Created shield gen ' + shield_gen_name_final)

            #Iterate for next run of loop
            shield_gen_cost = roundup100((shield_gen_cost * 2) * float(shield_gen_cost_curve))
            shield_gen_outfit = round((shield_gen_outfit * 2) * float(shield_gen_outfit_curve))
            shield_gen_shield_generation = round((shield_gen_shield_generation * 2) * float(shield_gen_shield_generation_curve), 1)
            shield_gen_shield_energy = round((shield_gen_shield_energy * 2) * float(shield_gen_shield_energy_curve), 1)
            shield_gen_delay *= shield_gen_delay_curve

            shield_gen_iterations_count += 1
        shield_gen_types_generated_count += 1
    shield_gen_output.write('\n')
    outfitter_output.close()
    generate_outfits_config.close()
    shield_gen_output.close()
#============================================================================================
#============================================HULL===========================================
#============================================================================================
def create_hull_repair(faction,fileout=''):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    hull_rep_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    #for line in generate_outfits_config: #Creates vars from txt file

    hull_rep_type_amount = 0
    if (random.uniform(0,5*faction.tier) >= 4):
        hull_rep_type_amount = random.uniform(0+(1-faction.shieldhullFactor),2)

    hull_rep_types_generated_count = 1
    while hull_rep_types_generated_count <= int(hull_rep_type_amount):
        #Calculates new values
        hull_rep_outfit = random.randint(int(5), int(20))
        hull_rep_hull_rate = round(random.uniform(float(0.1*max(1,faction.tier*faction.tier)), float(0.2*max(1,faction.tier*faction.tier))), 2)
        hull_rep_shield_energy = round(random.uniform(float(hull_rep_hull_rate), float(hull_rep_hull_rate*2)), 2)
        hull_rep_shield_heat = round(random.uniform(hull_rep_shield_energy*0,hull_rep_shield_energy*2))
        hull_rep_cost = roundup100(random.randint(round(((hull_rep_hull_rate*60*faction.tier)/hull_rep_outfit)*3200*faction.tier), round(((hull_rep_hull_rate*60*faction.tier)/hull_rep_outfit)*5500*faction.tier)))

        hull_rep_type = random.choice(['Hull Repair','Nanite Repair','Hull Regenerator', 'Damage Control', 'Hull Reconstructor'])
        hull_rep_iterations = round(random.gauss(4,2))
        #hull_rep Name
        sheild_gen_name_list=[]
        for n in range(hull_rep_iterations):
            name_length_min = 3
            name_length_max = 7
            sheild_gen_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=faction.devmodeseed+n)
            sheild_gen_name_list.append(sheild_gen_name)
        sheild_gen_name_list.sort()

        hull_rep_cost_curve = .9
        hull_rep_outfit_curve = .75
        hull_rep_hull_rate_curve = 1
        hull_rep_shield_energy_curve = round(0.9/(max(1,faction.tier/2)),1)

        #Iterates Values
        hull_rep_iterations_count = 1
        while hull_rep_iterations_count <= int(hull_rep_iterations):
            hull_rep_name_final = sheild_gen_name_list[hull_rep_iterations_count-1] + ' '+ hull_rep_type
            shield_size = ['tiny','small','medium','large','huge']
            shield_thumb =  shield_size[min(4,hull_rep_iterations_count-1)]+' shield'
            #Writes ES code to file, use \n for line break
            hull_rep_output.write('outfit "' + hull_rep_name_final + '"\n')
            hull_rep_output.write('\tcategory "Systems"\n')
            hull_rep_output.write('\tcost ' + str(hull_rep_cost) + "\n")
            hull_rep_output.write(f'\tthumbnail "outfit/{shield_thumb}"\n')
            hull_rep_output.write('\t"mass" ' + str(hull_rep_outfit) + "\n")
            hull_rep_output.write('\t"outfit space" -' + str(hull_rep_outfit) + "\n")
            hull_rep_output.write('\t"hull repair rate" ' + str(hull_rep_hull_rate) + "\n")
            hull_rep_output.write('\t"hull energy" ' + str(hull_rep_shield_energy) + "\n")
            hull_rep_output.write('\t"hull heat" ' + str(hull_rep_shield_heat) + "\n")
            hull_rep_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Hull Repair"\n')
            hull_rep_output.write('\n')

            outfitter_output.write('\t"' + hull_rep_name_final + '"\n')

            outfit = class_Outfit(hull_rep_name_final,'Systems',hull_rep_cost,shield_thumb,hull_rep_outfit,hull_rep_outfit)
            outfit.hull_repair = hull_rep_hull_rate
            outfit.hull_ener = hull_rep_shield_energy
            outfit.hull_heat = hull_rep_shield_heat
            faction.outfitlist.append(outfit)

            print('Created shield gen ' + hull_rep_name_final)

            #Iterate for next run of loop
            hull_rep_cost = roundup100((hull_rep_cost * 2) * float(hull_rep_cost_curve))
            hull_rep_outfit = round((hull_rep_outfit * 2) * float(hull_rep_outfit_curve))
            hull_rep_hull_rate = round((hull_rep_hull_rate * 2) * float(hull_rep_hull_rate_curve), 1)
            hull_rep_shield_energy = round((hull_rep_shield_energy * 2) * float(hull_rep_shield_energy_curve), 1)

            hull_rep_iterations_count += 1
        hull_rep_types_generated_count += 1
    hull_rep_output.write('\n')
    outfitter_output.close()
    generate_outfits_config.close()
    hull_rep_output.close()

#============================================================================================
#============================================H2H=========================================
#============================================================================================

def create_h2h(faction,fileout='',max_outfit_count=4,h2hmin=1):
    namegen = namegenerator.Namegenerator(faction)
    generate_outfits_config = open(outfit_config_file, "r")
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} outfits.txt'
    h2h_output = open(fileout, "a")
    outfitter_output = open(outfitter_output_file,'a')
    #Searches config file for values and creates variables
    for line in generate_outfits_config: #Creates vars from txt file
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_outfits_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("outfit_seed" in line) and use_seed == True:
            outfit_seed = next(generate_outfits_config)
            random.seed(int(outfit_seed))
    if faction.devmode:
        random.seed(faction.devmodeseed)
    if max_outfit_count > 1:
        h2h_type_amount = random.randrange(1,max(2,max_outfit_count))
    else:
        h2h_type_amount = max_outfit_count

    h2hmin = max(h2hmin,1)
    h2h_types_generated_count = 1
    while h2h_types_generated_count <= int(h2h_type_amount):
        #Calculates new values
        h2h_tradeoff_capa_dict = {
            "outfit space": 0,
            "weapon space": 0,
            "cargo space": 0,
            #"cooling inefficiency": 0,
        }
        h2h_tradeoff_drain_dict = {
            "heat generation": 0,
            "energy consumption": 0,
            "fuel consumption": 0,
            "overheat damage rate": 0,
            "operating costs": 0
        }
        h2h_outfit = 0
        h2h_have_tradeoff = False
        h2h_takespace = False
        h2h_tradeoff = ''
        h2h_tradeoff_value = 0
        h2h_total = round(random.randrange(int(faction.tier*1.5), int(faction.tier*2)+1), 1)
        if random.random() < .3:
            h2h_total = round(random.randrange(int(faction.tier*3), int(faction.tier*4.5)), 1)
            h2h_have_tradeoff = True
            if random.random() < .3: #Todo Multi-tradeoff
                h2h_tradeoff = random.choice(list(h2h_tradeoff_drain_dict.keys()))
                h2h_tradeoff_value = random.random()
                h2h_total = round(random.randrange(int(faction.tier*3.5), int(faction.tier*5.5)), 1)
            else:
                h2h_tradeoff = random.choice(list(h2h_tradeoff_capa_dict.keys()))
                h2h_takespace = True
                h2h_outfit = random.randrange(0,5)
                h2h_tradeoff_value = -h2h_outfit
        h2h_cost = roundup100(random.randrange(int(9500*(h2h_total)), int(15000*(h2h_total)))*faction.tier)
        h2h_ratio = random.random() # .1 def, .9 atk
        h2h_atk = h2h_total*h2h_ratio
        h2h_def = h2h_total*(1-h2h_ratio)
        #h2h Name        
        h2h_type_name_small = ['Gun','Rifle','Assault Rifle','Machinegun','Shotgun','Staff','Blaster Rifle']
        h2h_type_name_large = ['Gun Station','Defense Station','Defense','Turret','Combat Station','Security']
        h2h_type = random.choice(h2h_type_name_small)
        if h2h_takespace:
            h2h_type = random.choice(h2h_type_name_large)
        h2h_name_list = []

        h2h_iterations = int(random.randrange(1,max(2,h2h_type_amount/2)))

        for n in range(h2h_iterations):
            name_length_min = 3
            name_length_max = 7
            seedy =0 
            if faction.devmode:
                seedy = faction.devmodeseed+n
            h2h_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight,
                                                    seed=seedy)
            h2h_name = h2h_name + ' ' + h2h_type
            h2h_name_list.append(h2h_name)
        h2h_name_list.sort()
        
        h2h_cost_curve = .85
        h2h_outfit_curve = 1.1
        h2h_h2h_curve = random.uniform(1.1,1.3)
        if not h2h_takespace:
            h2h_thumb = random.choice(['laser rifle','enforcer riot staff','enforcer confrontation gear','hai rifle','korath rifle','pug staff','h2h 1','h2h 2','h2h 3','h2h 4'])
        else:
            h2h_thumb = random.choice(['security station','intrusion countermeasure','microbot defense station','pug bio defense','liquid nitrogen','small systems core'])
        #Iterates Values
        h2h_iterations_count = 1
        while h2h_iterations_count <= h2h_iterations:
            h2h_name_final = h2h_name_list[h2h_iterations_count-1]
            #Writes ES code to file, use \n for line break
            h2h_output.write('outfit "' + h2h_name_final + '"' + "\n")
            h2h_output.write('\tcategory "Hand to Hand"\n')
            h2h_output.write('\tcost ' + str(h2h_cost) + "\n")
            h2h_output.write(f'\tthumbnail "outfit/{h2h_thumb}"\n')
            h2h_output.write(f'\t"boarding attack" {h2h_atk}\n')
            h2h_output.write(f'\t"boarding defense" {h2h_def}\n')
            h2h_output.write(f'\t"unplunderable" 1\n')
            h2h_output.write(f'{h2h_tradeoff} {h2h_tradeoff_value}' + "\n")
            h2h_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Hand to Hand"\n')
            h2h_output.write('\n')

            outfitter_output.write(f'\t"{h2h_name_final}"' + '\n')
            outfit = class_Outfit(h2h_name_final,'Hand to Hand',h2h_cost,h2h_thumb,h2h_outfit,h2h_outfit)
            outfit.boarding_atk = h2h_atk
            outfit.boarding_def = h2h_def
            faction.outfitlist.append(outfit)

            print(f'Created h2h {faction.name} ' + h2h_name_list[h2h_iterations_count-1] + '.')

            #Iterate for next run of loop
            h2h_cost = roundup100((h2h_cost * 2) * float(h2h_cost_curve))
            h2h_outfit = round((h2h_outfit * 2) * float(h2h_outfit_curve))
            h2h_atk = round((h2h_atk * 2) * float(h2h_h2h_curve), 1)
            h2h_def = round((h2h_def * 2) * float(h2h_h2h_curve), 1)

            h2h_iterations_count += 1
        h2h_types_generated_count += 1
    h2h_output.write('\n')
    #outfitter_output.close()
    generate_outfits_config.close()
    h2h_output.close()

def load_custom_configs(faction):
    if faction.devmode:
        random.seed(faction.devmodeseed)
    outfit_configs_list = glob.glob("config/outfit config/*.txt") #Imports files in directory
    outfit_configs_amount = len(outfit_configs_list) #Gets amount of items in list
    outfit_configs_iterations = 0
    global outfit_config_file #Config File
    outfit_config_file = str(outfit_configs_list[outfit_configs_iterations]).replace("\\", "/")
    global outfit_output_file #Output file
    outfit_output_file = str(outfit_configs_list[outfit_configs_iterations]).replace("\\", "/").replace("config/outfit config/", "")

    global outfitter_output_file
    outfitter_output_file = f"data/{faction.name}/dev sales.txt"
    outfitter_output = open(outfitter_output_file, "w")
    outfitter_output.write('outfitter "eesdev"\n')
    outfitter_output.close()

    create_battery(faction)
    create_power(faction)
    create_engines(faction)
    create_shield_generator(faction)
    create_hull_repair(faction)
    if random.randrange(1,3) > 2.3:
        create_cooling(faction)
    if random.random() > .5:
        create_h2h(faction)
