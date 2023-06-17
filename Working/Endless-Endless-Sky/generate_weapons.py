from math import sqrt
import random
import math
import os

from generate_outfits import class_Outfit

import namegenerator
#namegen = namegenerator.Namegenerator()


def roundup1000(x):
    return int(math.ceil(x / 1000.0)) * 1000
def roundup100(x):
    return int(math.ceil(x / 100.0)) * 100
def roundup10(x):
    return int(math.ceil(x / 10.0)) * 10
def roundup5(x):
    return int(math.ceil(x / 5.0)) * 5

#Change a range of values to another range of values
def remap(value, fromLow, fromHigh, toLow, toHigh): 
    return (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
def remap_outmax(value, fromLow, fromHigh, toLow, toHigh, maxvalue): 
    return max(maxvalue,(value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow)
#Inherits stuffs from outfit class
class class_Weapon(class_Outfit):
    def __init__(self,name,outfit_category,cost,thumbnail,mass,outfit_space,weapon_space) -> None:
        self.weapon_type = 'None'

        self.projectilesprite = ''
        self.hardpoint = ''
        self.hardpoint_offset = [0,0]
        self.sound = ''
        self.ammo = ''
        self.ammo_cap = 0
        self.icon = ''

        self.fire_effect = ''
        self.live_effect = ''
        self.hit_effect = ''
        self.die_effect = ''

        self.submunition = {} #'name':count
        self.stream = True
        self.cluster = False
        self.safe = False
        self.phasing = False

        self.lifetime = 0
        self.rand_life = 0
        self.velocity = 0
        self.rand_vel = 0
        self.inaccuracy = 0
        self.reload = 0

        self.accel = 0
        self.drag = 0
        self.turn = 0
        self.turret_turn = 4

        self.fire_ener = 0
        self.fire_force = 0
        self.fire_heat = 0
        self.fire_fuel = 0
        
        self.homing = 0
        self.tracking = {'infrared tracking':0,'optical tracking':0,'radar tracking':0,'tracking':0}
        self.misl_str = 0
        self.at_misl = 0

        self.damage_types = {'hit force': 0,'piercing': 0,'shield damage': 0,'hull damage': 0,'fuel damage': 0, 'energy damage': 0}
        self.spe_damage_types = {'ion damage': 0}

        super().__init__(name,outfit_category,cost,thumbnail,mass,outfit_space,weapon_space)


def create_weapon(faction,fileout='',weapon_amount = 0,weapon_min_outfit = 5, weapon_max_outfit = 80):
    
    namegen = namegenerator.Namegenerator(faction)

    projectile_list = os.listdir("images/projectile")
    projectile_list = [f.removesuffix(".png") for f in projectile_list]

    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} weapons.txt'

    weapon_config_file = "config/weapon config/weapons 1.txt"
    generate_weapons_config = open(weapon_config_file, "r")
    weapon_output = open(fileout, "a")
    #Searches config file for values and creates variables
    for line in generate_weapons_config: #Creates vars from txt file

        line = line.rstrip('\n')
        use_seed = False
        if "use_seed" in line:
            use_seed_check = next(generate_weapons_config)
            if str(use_seed_check) in ['true', 'True', 'true\n', 'True\n']:
                use_seed = True
            else:
                use_seed = False
        if ("weapon_seed" in line) and use_seed == True:
            weapon_seed = next(generate_weapons_config)
            random.seed(int(weapon_seed))
#End reading data from config file
    if faction.devmode:
        random.seed(99)
    if weapon_amount == 0:
        weapon_amount = max(1,random.gauss(4,2))

    print("\n")
    weapon_types_generated_count = 1
    while weapon_types_generated_count <= int(weapon_amount):
        
        beam_wep_weight = 25 * min(1,remap(faction.tier,0.1,4,0.1,1))
        projectile_wep_weight = 25 + (beam_wep_weight-25)
        weapon_type_weight = [projectile_wep_weight,25,beam_wep_weight,25]
        weapon_type = random.choices(('projectile','missile','beam','anti-missile'),weights=weapon_type_weight)
        weapon_type = weapon_type[0]
        weapon_outfit = round(random.randint(math.floor(weapon_min_outfit),max(1,weapon_max_outfit)))
        weapon_mass = weapon_outfit

        weapon_is_burst = int(random.paretovariate(5)) #1 = no burst
        #Burst doesn't do anything at the moment, will use later.
        create_turrets = False
        if random.randrange(round(weapon_outfit/3),max(1,weapon_outfit)) <= 40:
            create_turrets = True
        print("Weapon type: " + (str(weapon_type)))

        if weapon_is_burst > 1:
            print("Weapon is burst: True")
        print("Create turrets: ", create_turrets)


        #Weapon calculations
        weapon_damagepersec = random.uniform(weapon_outfit*(8*faction.tier),weapon_outfit*(16*faction.tier))
        wep_cost_min = int((weapon_damagepersec/weapon_outfit)*65*weapon_outfit*sqrt(100*faction.tier))
        wep_cost_max = int((weapon_damagepersec/weapon_outfit)*75*weapon_outfit*sqrt(150*faction.tier))
        weapon_cost = roundup100(random.randint(int(wep_cost_min),int(wep_cost_max)))
        weapon_shieldhull_ratio = random.uniform(.1,.9) # .1 shield, .9 hull
        weapon_energy_ratio = random.uniform(.1,2) # 
        weapon_heat_ratio = random.uniform(.1,2) # 
        #weapon_outfit = random.randint(int(weapon_min_outfit_space), int(weapon_max_outfit_space))
        weapon_special_ratio = random.triangular(0,.9,-2/faction.tier)
        
        weapon_hit_force = 0
        if weapon_type == "beam":
            weapon_shotpersec = 60
            weapon_range = random.choice([300,350,400,450,490,540]) #fixed because avaliable beam sprites
            weapon_velocity = weapon_range
            weapon_max_inaccuracy = 3
            if(random.random()<=0.1):
                weapon_hit_force = round(random.gauss(1, 5))
        elif weapon_type == 'anti-missile':
            weapon_shotpersec = random.uniform(0.1,random.randrange(10,60))
            weapon_range = roundup10(random.randrange(100,round(max(200,350*faction.tier))))
            weapon_velocity = weapon_range
            weapon_max_inaccuracy = 0
        else:
            weapon_shotpersec = random.triangular(0.1,random.randrange(10,60)) #too many single digit reload ffs
            weapon_range = roundup10(random.weibullvariate(350, 1))
            if weapon_type == 'missile':
                weapon_range = max(300,weapon_range)
            weapon_velocity = round(random.uniform(7,50))
            weapon_max_inaccuracy = round(random.weibullvariate(5, 1),1)
            #print(f"Projectile stats: range:{weapon_range} shotpSec {weapon_shotpersec}")
            if(random.random()<=0.3):
                weapon_hit_force = round(random.weibullvariate(20, 4))
  
        weapon_inaccuracy = round(random.uniform(0, weapon_max_inaccuracy),1)
        weapon_lifetime = round(weapon_range / weapon_velocity)

        weapon_reload = max(1,math.ceil(60 / weapon_shotpersec)) #Please don't be zero and break stuffs.
        if weapon_is_burst and not weapon_type == "beam":
            if weapon_reload <= 1:
                weapon_reload = 3
            weapon_burst_reload = random.randint(1,weapon_reload-1)
            weapon_burst_count = random.randint(2,round(max(3,60/weapon_burst_reload)))
        elif weapon_is_burst and weapon_type == "beam":
            weapon_reload = 1 + random.uniform(0,3)
            weapon_burst_reload = 1
            weapon_burst_count = random.randint(10,round(max(12,60/weapon_burst_reload)))
        #print("Shot Per Sec: ", weapon_shotpersec)
        #==============================Regular Damages
        weapon_shield_dps = weapon_damagepersec * weapon_shieldhull_ratio
        weapon_shield_dpshot = round(weapon_shield_dps / weapon_shotpersec,1)

        weapon_hull_dps = weapon_damagepersec * (1-weapon_shieldhull_ratio)
        weapon_hull_dpshot = round(weapon_hull_dps / weapon_shotpersec,1)

        weapon_firing_energypershot = round((weapon_shield_dpshot*weapon_energy_ratio)/faction.tier,1)
        weapon_firing_heatpershot = round((weapon_shield_dpshot*weapon_heat_ratio)/faction.tier,1)
        #=============================Special Damages todo
        weapon_special_dpshot = {
            'heat':0,
            'fuel':0,
            'energy':0,
            'ion':0,
            'disrupt':0,
            'slow':0,
            'discharge':0,
            'corrosion':0,
            'leak':0,
            'burn':0,
        }
        if random.random() < .1:
            weapon_heat_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['heat'] = round(weapon_heat_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_special_dmg_picks = random.choices(list(weapon_special_dpshot.keys()))
            for dmg_type in weapon_special_dmg_picks:
                weapon_special_mult = weapon_special_ratio/len(weapon_special_dmg_picks)
                weapon_special_mult += random.uniform(.01,max(.05,weapon_special_mult)) #Add minor variation, TODO: properly calculate it.
                weapon_special_dps = weapon_damagepersec * weapon_special_mult
                weapon_special_dpshot[dmg_type] = round(weapon_special_dps / weapon_shotpersec,1)
        """
        if random.random() < .1 * (faction.tier/3):
            weapon_fuel_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['fuel'] = round(weapon_fuel_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_energy_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['energy'] = round(weapon_energy_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_ion_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['ion'] = round(weapon_ion_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_disrupt_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['disrupt'] = round(weapon_disrupt_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_slow_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['slow'] = round(weapon_slow_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_discharge_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['discharge'] = round(weapon_discharge_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_corrosion_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['corrosion'] = round(weapon_corrosion_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_leak_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['leak'] = round(weapon_leak_dps / weapon_shotpersec,1)
        if random.random() < .1 * (faction.tier/3):
            weapon_burn_dps = weapon_damagepersec * weapon_special_ratio
            weapon_special_dpshot['burn'] = round(weapon_burn_dps / weapon_shotpersec,1)
        """

        #=======Create Special Projectile with submunitions (shotgun,flak,etc.)
        projectile_type = 'none'
        special_proj_chance = .3
        submunition_parent_stats = {
            'split range': 0,
        }
        submunition_stats = {
            'velocity': 0,
            'lifetime': 0,
            'inaccuracy': 0,
            'shield damage': 0,
            'hull damage': 0,
            'homing': 0,
            'tracking': 0,
        }
        if weapon_type != 'beam':
            if random.random() > special_proj_chance:
                projectile_type = random.choice(['shotgun','flak']) #todo, boost/staged, turret
                if projectile_type == 'shotgun':
                    submunition_count = random.randint(3,22)
                    weapon_splitdelay = random.uniform(.1,.3)
                    submunition_stats['lifetime'] = max(1,weapon_lifetime*(1-weapon_splitdelay))
                    weapon_lifetime = max(1,weapon_lifetime*weapon_splitdelay)
                    submunition_stats['inaccuracy'] = random.uniform(12,45)
                    submunition_stats['shield damage'] = weapon_shield_dpshot/submunition_count
                    submunition_stats['hull damage'] = weapon_hull_dpshot/submunition_count
                    for sp_dmg in list( weapon_special_dpshot.keys()):
                        submunition_stats[sp_dmg+' damage'] = weapon_special_dpshot[sp_dmg]/submunition_count
                    if faction.tier > 3 and random.random() < .3:
                        sub_tracking_weight = [1,1,1,0.2*faction.tier]
                        sub_tracking_type = random.choices(['infrared tracking','optical tracking','radar tracking','tracking'],weights=sub_tracking_weight)
                        submunition_stats[sub_tracking_type[0]] = round(random.uniform(min(.98,.1*(faction.tier)), .99), 2)
                        submunition_stats['turn'] = round(random.uniform(1, 30*max(1,faction.tier)), 1)
                        submunition_stats['homing'] = random.randrange(1,4)
                        if submunition_count < 12/weapon_reload or random.random() > .1 or weapon_type == "missile":
                            submunition_stats['missile strength'] = max(1,round(random.uniform((weapon_reload*.5)*(faction.tier**3), (weapon_reload*3)*(faction.tier**3))/submunition_count, 1))
                if projectile_type == 'flak':
                    weapon_flakrange = random.randrange(30,60)
                    submunition_parent_stats['split range'] = round(weapon_flakrange*random.uniform(.3,.7))
                    weapon_flakvelocity = random.randrange(30,60)
                    if weapon_flakvelocity > weapon_velocity:
                        submunition_stats['velocity'] = weapon_velocity-weapon_flakvelocity
                    elif weapon_flakvelocity < weapon_velocity:
                        submunition_stats['velocity'] = weapon_flakvelocity-weapon_velocity
                    submunition_stats['lifetime'] = weapon_flakrange/weapon_flakvelocity
                    submunition_count = random.randint(6,32)
                    submunition_stats['inaccuracy'] = 360
                    submunition_stats['shield damage'] = weapon_shield_dpshot/submunition_count
                    submunition_stats['hull damage'] = weapon_hull_dpshot/submunition_count
                    for sp_dmg in list( weapon_special_dpshot.keys()):
                        submunition_stats[sp_dmg+' damage'] = weapon_special_dpshot[sp_dmg]/submunition_count
                    if faction.tier > 3 and random.random() < .3:
                        sub_tracking_weight = [1,1,1,0.2*faction.tier]
                        sub_tracking_type = random.choices(['infrared tracking','optical tracking','radar tracking','tracking'],weights=sub_tracking_weight)
                        submunition_stats[sub_tracking_type[0]] = round(random.uniform(min(.98,.1*(faction.tier)), .99), 2)
                        submunition_stats['turn'] = round(random.uniform(1, 30*max(1,faction.tier)), 1)
                        submunition_stats['homing'] = random.randrange(1,4)
                        if submunition_count < 12 / weapon_reload or random.random() > .1 or weapon_type == "missile":
                            submunition_stats['missile strength'] = max(1,round(random.uniform((weapon_reload*.5)*(faction.tier**3), (weapon_reload*3)*(faction.tier**3))/submunition_count, 1))

        #Missile Calculations
        missile_cost = random.randint(weapon_cost/5, weapon_cost/4)
        missile_mass = round(random.uniform(.01, .1), 2)

        #Missile storage calculations
        missile_store_outfit = random.randint(math.ceil(missile_mass*100), math.ceil(missile_mass*300))
        missile_store_cap = round(missile_store_outfit/missile_mass)
        missile_storage_cost = random.randint(round(missile_cost*5), round(missile_cost*10))
        missile_storage_mass = random.randint(round(missile_store_outfit-missile_mass*missile_store_cap), round(missile_store_outfit-missile_mass*missile_store_cap)+3)

        #Missile launcher calculations
        missile_tracking_type = 'none'
        if weapon_type == "missile":
            tracking_weight = [1,1,1,1,0.2*faction.tier]
            missile_tracking_type = random.choices(['none','infrared','optical','radar','tracking'],weights=tracking_weight)
            missile_tracking_type = missile_tracking_type[0]
            weapon_lifetime = weapon_lifetime*100
            #print("Missile tracking type: " + str(missile_tracking_type))

        if missile_tracking_type == 'none':
            missile_tracking_amount = 0
            missile_turn = 0
            missile_homing = 0
        else:
            missile_tracking_amount = round(random.uniform(min(.98,.1*(faction.tier)), .99), 2)
            missile_turn = round(random.uniform(1, 30*max(1,faction.tier)), 1)
            missile_homing = random.randrange(1,4)
        missile_strength = round(random.uniform((weapon_reload*.5)*(faction.tier**3), (weapon_reload*3)*(faction.tier**3)), 1)
        missile_acceleration = round(random.uniform((weapon_velocity/4)*.1, (weapon_velocity/2)*.1), 1)
        missile_drag = round(random.uniform(.1, .2), 1)
        #Anti Missile
        anti_missile_strength = round(random.uniform(6*(faction.tier**3), 20*(faction.tier**3))/weapon_shotpersec, 1)

        turret_gun_num = random.randrange(1,4)
        #If have more than 1 gun and already at 1 reload, increase damage. Else increse fire-rate
        #todo: should consider if reload goes below 1 at 3+ guns but later.
        turret_special_dpsh = {}
        if (weapon_reload == 1 or weapon_type =='beam') and turret_gun_num >= 2:
            turret_hull_dpshot = weapon_hull_dpshot*turret_gun_num
            turret_shield_dpshot = weapon_shield_dpshot*turret_gun_num
            turret_hit_force = weapon_hit_force*turret_gun_num
            for spdmgtype,spdmgvalue in weapon_special_dpshot.items():
                if(spdmgvalue > 0):
                    turret_special_dpsh[spdmgtype] = spdmgvalue * turret_gun_num
        else:
            turret_hull_dpshot = weapon_hull_dpshot
            turret_shield_dpshot = weapon_shield_dpshot
            turret_hit_force = weapon_hit_force
            for spdmgtype,spdmgvalue in weapon_special_dpshot.items():
                if(spdmgvalue > 0):
                    turret_special_dpsh[spdmgtype] = spdmgvalue
        turret_reload = round(max(1,weapon_reload/turret_gun_num))
        turret_extra_outfit = random.randrange(round(weapon_outfit/3*(weapon_outfit/10)),round(weapon_outfit/3*(weapon_outfit/5)))
        turret_turn = round(weapon_outfit*1.5/turret_extra_outfit*(turret_gun_num*0.3),1)

        #=============Visuals/Names
        gun_types = ['Gun','Cannon','Blaster','Culverin','Howizer','Mortar','Bombard','Basilisk','Ballista']
        gun_types_mod_fast = ['Auto ','Machine ','Rapid ','Assault ','','']
        gun_types_mod_slow = ['Heavy ','Siege ','Mega ','','','']
        beam_types = ['Laser','Beam','Beam Projector','Lance','Tachyon Projector']
        missile_types = ['Torpedo','Missile','Guided Rocket','Tracker','Chaser']
        launcher_types = ['Launcher','Deployer','Catapult','Tube']
        mini_launcher_types = ['Pod','Pylon','Mini-Launcher','Micro-Launcher']

        gun_thumb_list = ['blaster','bombardment cannon','inhibitor','ion rain gun','proton gun','pulse']
        turret_thumb_list = ['blaster turret','bombardment turret','inhibitor turret','ion rain turret','proton turret','pulse turret']
        beam_thumb_list = ['laser','heavy laser','electron laser','moonbeam','sunbeam','slicer']
        soundgun_list = ['blaster','bombardment','detainer','disruptor','explosion tiny','hion','inhibitor','plasma','proton','particle','pulse']
        soundbeam_list = ['laser','hion','skylance','zapper','heavy laser','electron beam','disruptor','heliarch attractor','heliarch repulsor']
        #soundmissile_list = ['finisher','meteor','sidewinder','torpedo','tracker','rocket']
        effectsmall_list = ['small explosion','proton impact','electron impact','heavy laser impact','blaster impact']
        effectlarge_list = ['nuke explosion','large explosion','torpedo hit','plasma explosion','particle impact']
        effect_list = effectsmall_list
        if weapon_reload >= 120:
            effect_list = effectlarge_list

        name_length_min = 3
        name_length_max = 5
        #weapon_name = namegen.randomfromExisting(faction.name)
        weapon_name = namegen.generateNameFromRules(name_length_min,
                                                    name_length_max,
                                                    wordlen=faction.lang_wordlen,
                                                    spacechance=faction.lang_spacechance,
                                                    lang_charweight=faction.lang_charweight)
        
        weapon_effect = random.choice(effect_list)
        #Writes ES code to file, use \n for line break
        if weapon_type == "projectile": #Write projectile weapon
            weapon_type_name = random.choices(gun_types)
            weapon_type_name = weapon_type_name[0]
            if weapon_reload <= 12:
                gun_type_mod = random.choice(gun_types_mod_fast)
            elif weapon_reload >= 120:
                gun_type_mod = random.choice(gun_types_mod_slow)
            else:
                gun_type_mod = ''

            weapon_name_final = f"{weapon_name} {gun_type_mod}{weapon_type_name}"
            thumb_select = random.randrange(0,len(gun_thumb_list))
            weapon_thumb_final = gun_thumb_list[thumb_select]

            
            weapon_projectile = random.choice(projectile_list)
            weapon_sound = random.choice(soundgun_list)

            weapon_output.write(f'outfit "{weapon_name_final}"\n')
            weapon_output.write('\tcategory "Guns"\n')
            weapon_output.write('\tcost ' + str(weapon_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{weapon_thumb_final}"\n')
            weapon_output.write('\t"mass" ' + str(weapon_mass) + "\n")
            weapon_output.write('\t"outfit space" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"weapon capacity" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"gun ports" -1' + "\n")
            weapon_output.write('\tweapon' + "\n")
            weapon_output.write(f'\t\t"sprite" "projectile/{weapon_projectile}"'+ "\n")
            weapon_output.write(f'\t\tsound "{weapon_sound}"'+ "\n")
            weapon_output.write(f'\t\t"hit effect" "{weapon_effect}"'+ "\n")
            weapon_output.write('\t\t"inaccuracy" ' + str(weapon_inaccuracy) + "\n")
            weapon_output.write('\t\t"velocity" ' + str(weapon_velocity) + "\n")
            weapon_output.write('\t\t"lifetime" ' + str(weapon_lifetime) + "\n")
            if projectile_type != 'none':
                weapon_sub_name = f"{weapon_name} sub 1"
                weapon_output.write(f'\t\t"submunition" "{weapon_sub_name}" {submunition_count}' + "\n")
                for thing,value in submunition_parent_stats.items(): #split range
                    if value:
                        weapon_output.write(f'\t\t"{thing}" {value}' + "\n")
            weapon_output.write('\t\t"reload" ' + str(weapon_reload) + "\n")
            if weapon_is_burst:
                weapon_output.write(f'\t\t"burst reload" {weapon_burst_reload}' + "\n")
                weapon_output.write(f'\t\t"burst count" {weapon_burst_count}' + "\n")             
            weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
            weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
            if projectile_type == 'none':
                weapon_output.write('\t\t"shield damage" ' + str(weapon_shield_dpshot) + "\n")
                weapon_output.write('\t\t"hull damage" ' + str(weapon_hull_dpshot) + "\n")
            if(round(weapon_hit_force) > 0):
                weapon_output.write('\t\t"hit force" ' + str(weapon_hit_force) + "\n")
            for spdmgtype,spdmgvalue in weapon_special_dpshot.items():
                if(spdmgvalue > 0):
                    weapon_output.write(f'\t\t"{spdmgtype} damage" {spdmgvalue}' + "\n")
            if projectile_type == 'none':
                weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} projectile weapon"\n')
            else:
                weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} {projectile_type} projectile weapon"\n')
            weapon_output.write('\n')

            #======Write Submunition if have one.
            if projectile_type != 'none':
                weapon_output.write(f'outfit "{weapon_sub_name}"\n')
                weapon_output.write('\tweapon' + "\n")
                weapon_output.write(f'\t\t"sprite" "projectile/{weapon_projectile}"'+ "\n")
                for thing,value in submunition_stats.items(): #Should include lifetime, velo, inaccu
                    if value:
                        weapon_output.write(f'\t\t"{thing}" {value:.3f}'+ "\n")
                weapon_output.write(f'\t\t"hit effect" "{weapon_effect}"'+ "\n")
                weapon_output.write('\n')
            
            gun = class_Weapon(weapon_name_final,'Guns',weapon_cost,weapon_thumb_final,weapon_mass,weapon_outfit,weapon_outfit)
            gun.weapon_type = 'gun' #Used for finding weapon in ship outfitting
            gun.fire_ener = weapon_firing_energypershot
            gun.reload = weapon_reload
            faction.weaponlist.append(gun)

            if create_turrets == True:
                turret_cost = random.uniform(2,5)
                turret_thumb_final = turret_thumb_list[thumb_select]
                turret_name_final = weapon_name_final + ' Turret'
                turret_cost_final = weapon_cost*turret_cost
                turret_mass = weapon_mass+turret_extra_outfit
                turret_outfit = weapon_outfit+turret_extra_outfit

                weapon_output.write('outfit "' + turret_name_final + '"' + "\n")
                weapon_output.write('\tcategory "Turrets"\n')
                weapon_output.write(f'\tcost {roundup100(turret_cost_final)}' + "\n")
                weapon_output.write(f'\tthumbnail "outfit/{turret_thumb_final}"\n')
                weapon_output.write('\t"mass" ' + str(turret_mass) + "\n")
                weapon_output.write('\t"outfit space" -' + str(turret_outfit) + "\n")
                weapon_output.write('\t"weapon capacity" -' + str(turret_outfit) + "\n")
                weapon_output.write('\t"turret mounts" -1' + "\n")
                weapon_output.write('\tweapon' + "\n")
                weapon_output.write(f'\t\t"sprite" "projectile/{weapon_projectile}"'+ "\n")
                weapon_output.write(f'\t\t"hardpoint sprite" "hardpoint/{turret_thumb_final}"'+ "\n")
                weapon_output.write(f'\t\tsound "{weapon_sound}"'+ "\n")
                weapon_output.write(f'\t\t"hit effect" "{weapon_effect}"'+ "\n")
                weapon_output.write('\t\t"inaccuracy" ' + str(weapon_inaccuracy) + "\n")
                weapon_output.write('\t\t"turret turn" ' + str(turret_turn) + '\n')
                weapon_output.write('\t\t"velocity" ' + str(weapon_velocity) + "\n")
                weapon_output.write('\t\t"lifetime" ' + str(weapon_lifetime) + "\n")
                if projectile_type != 'none':
                    weapon_sub_name = f"{weapon_name} sub 1"
                    weapon_output.write(f'\t\t"submunition" "{weapon_sub_name}" {submunition_count}' + "\n")
                    for thing,value in submunition_parent_stats.items(): #split range
                        if value:
                            weapon_output.write(f'\t\t"{thing}" {value}' + "\n")
                weapon_output.write('\t\t"reload" ' + str(turret_reload) + "\n")
                if weapon_is_burst:
                    weapon_output.write(f'\t\t"burst reload" {weapon_burst_reload}' + "\n")
                    weapon_output.write(f'\t\t"burst count" {weapon_burst_count}' + "\n")    
                weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
                weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
                if projectile_type == 'none':
                    weapon_output.write('\t\t"shield damage" ' + str(weapon_shield_dpshot) + "\n")
                    weapon_output.write('\t\t"hull damage" ' + str(weapon_hull_dpshot) + "\n")
                if(weapon_hit_force > 0):
                    weapon_output.write('\t\t"hit force" ' + str(turret_hit_force) + "\n")
                for spdmgtype,spdmgvalue in turret_special_dpsh.items():
                    if(spdmgvalue > 0):
                        weapon_output.write(f'\t\t"{spdmgtype} damage" {spdmgvalue}' + "\n")
                weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} projectile weapon {turret_gun_num} gun turret"\n')
                weapon_output.write('\n')
                turret = class_Weapon(turret_name_final,'Turrets',turret_cost_final,turret_thumb_final,turret_mass,turret_outfit,turret_outfit)
                turret.weapon_type = 'turret' #Used for finding weapon in ship outfitting
                turret.fire_ener = weapon_firing_energypershot
                turret.reload = turret_reload
                faction.weaponlist.append(turret)
            print("Created " + str(weapon_type) + weapon_name)
            
        #================================================BEAM WEAPON
        elif weapon_type == "beam":
            weapon_type_name = random.choices(beam_types)
            weapon_type_name = weapon_type_name[0]
            weapon_name_final = weapon_name + ' ' + weapon_type_name
            weapon_thumb_final = random.choice(beam_thumb_list)
            weapon_sound = random.choice(soundbeam_list)
            if weapon_range == 300:
                laser_projectile = 'laser'
                laser_hit_effect = 'beam laser impact'
            elif weapon_range == 350:
                laser_projectile = 'fire-lance'
                laser_hit_effect = 'fire-lance impact'
            elif weapon_range == 400:
                laser_projectile = 'heavy laser'
                laser_hit_effect = 'heavy laser impact'
            elif weapon_range == 450:
                laser_projectile = 'electron'
                laser_hit_effect = 'electron impact'
            elif weapon_range == 490:
                laser_projectile = 'moonbeam'
                laser_hit_effect = 'moonbeam impact'
            elif weapon_range == 540:
                laser_projectile = 'sunbeam'
                laser_hit_effect = 'sunbeam impact'

            weapon_output.write('outfit "' + weapon_name_final +  '"' + "\n")
            weapon_output.write('\tcategory "Guns"\n')
            weapon_output.write('\tcost ' + str(weapon_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{weapon_thumb_final}"\n')
            weapon_output.write('\t"mass" ' + str(weapon_mass) + "\n")
            weapon_output.write('\t"outfit space" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"weapon capacity" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"gun ports" -1' + "\n")
            weapon_output.write('\tweapon' + "\n")
            weapon_output.write(f'\t\t"sprite" "projectile/{laser_projectile}"'+ "\n")
            weapon_output.write('\t\t\t"frame rate" 1'+ "\n")
            weapon_output.write(f'\t\tsound "{weapon_sound}"'+ "\n")
            weapon_output.write(f'\t\t"hit effect" "{laser_hit_effect}"'+ "\n")
            weapon_output.write('\t\t"inaccuracy" ' + str(weapon_inaccuracy) + "\n")
            weapon_output.write('\t\t"velocity" ' + str(weapon_range) + "\n") #because velocity * lifetime = range
            weapon_output.write('\t\t"lifetime" ' + str(1) + "\n")
            weapon_output.write('\t\t"reload" ' + str(round(weapon_reload,2)) + "\n")
            if weapon_is_burst:
                weapon_output.write(f'\t\t"burst reload" {weapon_burst_reload}' + "\n")
                weapon_output.write(f'\t\t"burst count" {weapon_burst_count}' + "\n")   
            weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
            weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
            weapon_output.write('\t\t"shield damage" ' + str(weapon_shield_dpshot) + "\n")
            weapon_output.write('\t\t"hull damage" ' + str(weapon_hull_dpshot) + "\n")
            if(round(weapon_hit_force) > 0):
                weapon_output.write('\t\t"hit force" ' + str(weapon_hit_force) + "\n")
            for spdmgtype,spdmgvalue in weapon_special_dpshot.items():
                if(spdmgvalue > 0):
                    weapon_output.write(f'\t\t"{spdmgtype} damage" {spdmgvalue}' + "\n")
            weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Beam weapon"\n')
            weapon_output.write('\n')
            print("Created " + str(weapon_type) + " weapon " + weapon_name)
            gun = class_Weapon(weapon_name_final,'Guns',weapon_cost,weapon_thumb_final,weapon_mass,weapon_outfit,weapon_outfit)
            gun.weapon_type = 'gun' #Used for finding weapon in ship outfitting
            gun.fire_ener = weapon_firing_energypershot
            gun.reload = weapon_reload
            faction.weaponlist.append(gun)
            if create_turrets == True:
                turret_cost = random.uniform(2,5)
                turret_thumb_final = weapon_thumb_final+' turret'
                turret_name_final = weapon_name_final + ' Turret'
                turret_cost_final = roundup10(weapon_cost*turret_cost)
                turret_mass = weapon_mass+turret_extra_outfit
                turret_outfit = weapon_outfit+turret_extra_outfit

                weapon_output.write('outfit "' + turret_name_final + '"' + "\n")
                weapon_output.write('\tcategory "Turrets"\n')
                weapon_output.write('\tcost ' + str(turret_cost_final) + "\n")
                weapon_output.write(f'\tthumbnail "outfit/{turret_thumb_final}"\n')
                weapon_output.write('\t"mass" ' + str(turret_mass) + "\n")
                weapon_output.write('\t"outfit space" -' + str(turret_outfit) + "\n")
                weapon_output.write('\t"weapon capacity" -' + str(turret_outfit) + "\n")
                weapon_output.write('\t"turret mounts" -1' + "\n")
                weapon_output.write('\tweapon' + "\n")
                weapon_output.write(f'\t\t"sprite" "projectile/{laser_projectile}"'+ "\n")
                weapon_output.write(f'\t\t"hardpoint sprite" "hardpoint/{turret_thumb_final}"'+ "\n")
                weapon_output.write(f'\t\tsound "{weapon_sound}"'+ "\n")
                weapon_output.write(f'\t\t"hit effect" "{laser_hit_effect}"'+ "\n")
                weapon_output.write('\t\t"inaccuracy" ' + str(weapon_inaccuracy) + "\n")
                weapon_output.write('\t\t"turret turn" ' + str(turret_turn) + '\n')
                weapon_output.write('\t\t"velocity" ' + str(weapon_range) + "\n")
                weapon_output.write('\t\t"lifetime" ' + str(1) + "\n")
                weapon_output.write('\t\t"reload" ' + str(round(weapon_reload,2)) + "\n")
                if weapon_is_burst:
                    weapon_output.write(f'\t\t"burst reload" {weapon_burst_reload}' + "\n")
                    weapon_output.write(f'\t\t"burst count" {weapon_burst_count}' + "\n")   
                weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
                weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
                weapon_output.write('\t\t"shield damage" ' + str(turret_shield_dpshot) + "\n")
                weapon_output.write('\t\t"hull damage" ' + str(turret_hull_dpshot) + "\n")
                if(weapon_hit_force > 0):
                    weapon_output.write('\t\t"hit force" ' + str(turret_hit_force) + "\n")
                for spdmgtype,spdmgvalue in turret_special_dpsh.items():
                    if(spdmgvalue > 0):
                        weapon_output.write(f'\t\t"{spdmgtype} damage" {spdmgvalue}' + "\n")
                weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Beam weapon ' + str(turret_gun_num) + 'gun' + ' Turret"\n')
                weapon_output.write('\n')
                turret = class_Weapon(turret_name_final,'Turrets',turret_cost_final,turret_thumb_final,turret_mass,turret_outfit,turret_outfit)
                turret.weapon_type = 'turret' #Used for finding weapon in ship outfitting
                turret.fire_ener = weapon_firing_energypershot
                turret.reload = turret_reload
                faction.weaponlist.append(turret)

        elif weapon_type == "missile": #Write missile weapon
            missile_thumb_list = ['sidewinder','torpedo','typhoon']
            launcher_thumb_list = ['sidewinder launcher','torpedo launcher', 'typhoon launcher']
            pod_thumb_list = ['sidewinder pod','torpedopod','typhoonpod']
            storage_thumb_list = ['sidewinder storage','torpedo storage','typhoon storage']
            missile_thumb_sel = round(random.randrange(0,3))
            #Note!!!! Never put space in missile weapon name, ship outfitting depends on this.
            weapon_name = weapon_name.replace(' ','')
            if missile_tracking_type == 'none':
                missile_type = 'Rocket'
            else:
                missile_type = random.choice(missile_types)
            if missile_store_cap <= 4:
                launcher_type = random.choice(mini_launcher_types)
                launcher_thumb_final = pod_thumb_list[missile_thumb_sel]
            else:
                launcher_type = random.choice(launcher_types)
                launcher_thumb_final = launcher_thumb_list[missile_thumb_sel]
            missile_name_final = f'{weapon_name} {missile_type}'
            missile_thumb_final = missile_thumb_list[missile_thumb_sel]
            storage_thumb_final = storage_thumb_list[missile_thumb_sel]
            

            weapon_output.write(f'outfit "{missile_name_final}"\n')
            weapon_output.write('\tcategory "Ammunition"\n')
            weapon_output.write('\tcost ' + str(missile_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{missile_thumb_final}"\n')
            weapon_output.write('\t"mass" ' + str(missile_mass) + "\n")
            weapon_output.write('\t"' + str(missile_name_final) + ' capacity" -1' + "\n")
            weapon_output.write(f'\tdescription "{faction.name} Missile"\n')
            weapon_output.write('\n')
            print("Created " + str(weapon_type) + " weapon " + weapon_name + " Missile")

            missile = class_Weapon(missile_name_final,'Ammunition',missile_cost,missile_thumb_final,missile_mass,0,weapon_space=0)
            missile.weapon_type = 'missileammo'
            faction.weaponlist.append(missile)

            missile_stor_name_final = missile_name_final + ' Storage'
            
            weapon_output.write(f'outfit "{missile_stor_name_final}"' "\n")
            weapon_output.write('\tcategory "Ammunition"\n')
            weapon_output.write('\tcost ' + str(missile_storage_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{storage_thumb_final}"\n')
            weapon_output.write('\t"mass" ' + str(missile_storage_mass) + "\n")
            weapon_output.write('\t"outfit space" -' + str(missile_store_outfit) + "\n")
            weapon_output.write('\t"' + str(missile_name_final) + ' capacity" ' + str(missile_store_cap) + "\n")
            weapon_output.write('\tammo "' + str(missile_name_final) + '"' + "\n")
            weapon_output.write(f'\tdescription "{missile_name_final} Storage"\n')
            weapon_output.write('\n')
            print("Created " + str(weapon_type) + " weapon " + weapon_name + " Missile Rack")

            missilestor = class_Weapon(missile_stor_name_final,'Ammunition',missile_storage_cost,storage_thumb_final,missile_storage_mass,missile_store_outfit,weapon_space=0)
            missilestor.weapon_type = 'missilestorage'
            missilestor.ammo_cap = missile_store_cap
            faction.weaponlist.append(missilestor)

            launcher_name_final = missile_name_final + ' ' + launcher_type
            launcher_mass = weapon_outfit-(missile_storage_mass)
            missile_framerate = random.uniform(.1,1)

            weapon_output.write('outfit "' + launcher_name_final + '"' + "\n")
            weapon_output.write('\tcategory "Secondary Weapons"\n')
            weapon_output.write('\tcost ' + str(weapon_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{launcher_thumb_final}"\n')
            weapon_output.write('\t"mass" ' + str(launcher_mass) + "\n")
            weapon_output.write('\t"outfit space" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"weapon capacity" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"gun ports" -1' + "\n")
            weapon_output.write('\t"' + str(missile_name_final) + ' capacity" ' + str(missile_store_cap) + "\n")
            weapon_output.write('\tweapon' + "\n")
            weapon_output.write(f'\t\t"sprite" "projectile/{missile_thumb_final}"'+ "\n")
            weapon_output.write('\t\t\t"no repeat"' + "\n")
            weapon_output.write(f'\t\t\t"frame rate" {missile_framerate:.2f}' + "\n")
            weapon_output.write(f'\t\tsound "{missile_thumb_final}"'+ "\n")
            weapon_output.write('\t\tammo "' + str(missile_name_final) + '"'+ "\n")
            weapon_output.write(f'\t\ticon "icon/{missile_thumb_final}"'+ "\n")
            weapon_output.write('\t\t"fire effect" "sidewinder fire"'+ "\n")
            weapon_output.write('\t\t"die effect" "missile death"'+ "\n")
            weapon_output.write('\t\t"hit effect" "missile hit"'+ "\n")
            weapon_output.write('\t\t"inaccuracy" ' + str(weapon_inaccuracy) + "\n")
            weapon_output.write('\t\t"velocity" ' + str(weapon_velocity) + "\n")
            weapon_output.write('\t\t"lifetime" ' + str(weapon_lifetime) + "\n")
            if projectile_type != 'none':
                weapon_sub_name = f"{weapon_name} sub 1"
                weapon_output.write(f'\t\t"submunition" "{weapon_sub_name}" {submunition_count}' + "\n")
                for thing,value in submunition_parent_stats.items(): #split range
                    if value:
                        weapon_output.write(f'\t\t"{thing}" {value}' + "\n")
            weapon_output.write('\t\t"reload" ' + str(weapon_reload) + "\n")
            if weapon_is_burst:
                weapon_output.write(f'\t\t"burst reload" {weapon_burst_reload}' + "\n")
                weapon_output.write(f'\t\t"burst count" {weapon_burst_count}' + "\n")   
            weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
            weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
            weapon_output.write('\t\t"acceleration" ' + str(missile_acceleration) + "\n")
            weapon_output.write('\t\t"drag" ' + str(missile_drag) + "\n")
            weapon_output.write('\t\t"turn" ' + str(missile_turn) + "\n")
            weapon_output.write('\t\t"homing" ' + str(missile_homing) + "\n")
            if missile_tracking_type == "none":
                pass
            elif missile_tracking_type == "infrared":
                weapon_output.write('\t\t"infrared tracking" ' + str(missile_tracking_amount) + "\n")
            elif missile_tracking_type == "optical":
                weapon_output.write('\t\t"optical tracking" ' + str(missile_tracking_amount) + "\n")
            elif missile_tracking_type == "radar":
                weapon_output.write('\t\t"radar tracking" ' + str(missile_tracking_amount) + "\n")
            elif missile_tracking_type == "tracking":
                weapon_output.write('\t\t"tracking" ' + str(missile_tracking_amount) + "\n")
            if projectile_type == 'none':
                weapon_output.write('\t\t"shield damage" ' + str(weapon_shield_dpshot) + "\n")
                weapon_output.write('\t\t"hull damage" ' + str(weapon_hull_dpshot) + "\n")
            if(round(weapon_hit_force) > 0):
                weapon_output.write('\t\t"hit force" ' + str(weapon_hit_force) + "\n")
            for spdmgtype,spdmgvalue in weapon_special_dpshot.items():
                if(spdmgvalue > 0):
                    weapon_output.write(f'\t\t"{spdmgtype} damage" {spdmgvalue}' + "\n")
            weapon_output.write('\t\t"missile strength" ' + str(missile_strength) + "\n")
            weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Missile weapon"\n')
            weapon_output.write('\n')
            print("Created " + str(weapon_type) + " weapon " + weapon_name + " Missile Launcher")

            #======Write Submunition if have one.
            if projectile_type != 'none':
                weapon_output.write(f'outfit "{weapon_sub_name}"\n')
                weapon_output.write('\tweapon' + "\n")
                if projectile_type == 'flak':
                    weapon_projectile = random.choice(projectile_list)
                    weapon_output.write(f'\t\t"sprite" "projectile/{weapon_projectile}"'+ "\n")
                else:
                    weapon_output.write(f'\t\t"sprite" "projectile/{missile_thumb_final}"'+ "\n")
                for thing,value in submunition_stats.items(): #Should include lifetime, velo, inaccu
                    if value:
                        weapon_output.write(f'\t\t"{thing}" {value:.3f}'+ "\n")
                weapon_output.write(f'\t\t"hit effect" "missile hit"'+ "\n")
                weapon_output.write('\n')

            missilelauncher = class_Weapon(launcher_name_final,'Secondary Weapons',weapon_cost,launcher_thumb_final,launcher_mass,weapon_outfit,weapon_outfit)
            missilelauncher.weapon_type = 'missile'
            missilelauncher.fire_ener = weapon_firing_energypershot
            missilelauncher.ammo_cap = missile_store_cap
            missilelauncher.ammo = missile_name_final
            missilelauncher.reload = weapon_reload
            missilelauncher.drag = missile_drag
            missilelauncher.misl_str = missile_strength
            faction.weaponlist.append(missilelauncher)

        if weapon_type == "anti-missile": #Write projectile weapon
            anti_missile_thumb_list = ['anti-missile','anti-missile hai','heavy anti-missile','heavy anti-missile hai','pug anti-missile']
            anti_missile_thumb = random.choice(anti_missile_thumb_list)
            weapon_output.write('outfit "' + weapon_name + ' Anti-Missile"' + "\n")
            weapon_output.write('\tcategory "Turrets"\n')
            weapon_output.write('\tcost ' + str(weapon_cost) + "\n")
            weapon_output.write(f'\tthumbnail "outfit/{anti_missile_thumb}"\n')
            weapon_output.write('\t"mass" ' + str(weapon_mass) + "\n")
            weapon_output.write('\t"outfit space" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"weapon capacity" -' + str(weapon_outfit) + "\n")
            weapon_output.write('\t"turret mounts" -1' + "\n")
            weapon_output.write('\tweapon' + "\n")
            weapon_output.write(f'\t\t"hardpoint sprite" "hardpoint/{anti_missile_thumb}"'+ "\n")
            weapon_output.write('\t\t"hardpoint offset" 4.'+ "\n")
            weapon_output.write(f'\t\t"hit effect" "{weapon_effect}"'+ "\n")
            weapon_output.write('\t\t"fire effect" "tiny explosion"'+ "\n")
            weapon_output.write('\t\t"anti-missile" ' + str(anti_missile_strength) + "\n")
            weapon_output.write('\t\t"velocity" ' + str(weapon_velocity) + "\n")
            weapon_output.write('\t\t"lifetime" ' + str(weapon_lifetime) + "\n")
            weapon_output.write('\t\t"reload" ' + str(weapon_reload) + "\n")
            weapon_output.write('\t\t"firing energy" ' + str(weapon_firing_energypershot) + "\n")
            weapon_output.write('\t\t"firing heat" ' + str(weapon_firing_heatpershot) + "\n")
            weapon_output.write(f'\tdescription "{faction.name} T{faction.tier:.1f} Anti-missile"\n')
            weapon_output.write('\n')
            print("Created " + str(weapon_type) + " weapon " + weapon_name)

            antimissile = class_Weapon(weapon_name+' Anti-Missile','Turrets',weapon_cost,anti_missile_thumb,weapon_mass,weapon_outfit,weapon_outfit)
            antimissile.weapon_type = 'antimissile'
            antimissile.fire_ener = weapon_firing_energypershot
            antimissile.reload = weapon_reload
            faction.weaponlist.append(antimissile)


        weapon_types_generated_count += 1
#    weapon_output.write('\n')
    generate_weapons_config.close()
    weapon_output.close()