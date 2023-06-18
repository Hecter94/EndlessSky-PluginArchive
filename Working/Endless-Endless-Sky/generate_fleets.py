import random

def ship_sort(shiplist,sortby="installed weapons"):
    if sortby=="installed weapons":
        for i in range(len(shiplist)):
            for j in range(i+1,len(shiplist)):
                if shiplist[i].installed_weapons < shiplist[j].installed_weapons:
                    shiplist[i].installed_weapons,shiplist[j].installed_weapons = shiplist[j].installed_weapons,shiplist[i].installed_weapons
    if sortby=="installed weapons":
        for i in range(len(shiplist)):
            for j in range(i+1,len(shiplist)):
                if shiplist[i].installed_weapons < shiplist[j].installed_weapons:
                    shiplist[i].installed_weapons,shiplist[j].installed_weapons = shiplist[j].installed_weapons,shiplist[i].installed_weapons

    return shiplist

def gen_miningfleet_variant(faction):
    fleet_composition = {}
    #personalities = ["coward"]
    shuffledlist = faction.shiplist
    random.shuffle(shuffledlist)
    lp = 0
    while len(fleet_composition) <= 0 and lp < 20:
        for ship in shuffledlist:
            fleetcompcount = len(fleet_composition) <= round(1)
            inlw = (ship.category == 'Interceptor') or (ship.category == 'Light Warship')
            if ship.installed_weapons > 0 and (inlw) and fleetcompcount and ship.cargo_space > 0:
                fleet_composition[ship.name] = random.randint(2,4)
                for ccat,cnum in ship.carried.items():
                    for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                        if shipc.category == ccat:
                            fleet_composition[shipc.name] = cnum
                            break
        if len(fleet_composition) <= 0:
            for n in range(random.randrange(3,6)):
                ship = random.choice(shuffledlist)
                if (ship.category != 'Fighter' or ship.category != 'Drone') and ship.installed_weapons > 0 and ship.cargo_space > 0:
                    fleet_composition[ship.name] = random.randrange(2,4)
                    for ccat,cnum in ship.carried.items():
                        for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                            if shipc.category == ccat:
                                fleet_composition[shipc.name] = cnum
                                break
        lp += 1
    return fleet_composition

def gen_militaryfleet_variant(faction):
    fleet_composition = {}
    if faction.fleet_tactic == 'defense':
        hwcount = 0
        personalities = ["heroic","opportunistic"]
        shuffledlist = faction.shiplist
        random.shuffle(shuffledlist)
        lp = 0
        while len(fleet_composition) <= 0 or lp < 100:
            for ship in shuffledlist:
                if ship.category == 'Heavy Warship' and hwcount < 1:
                    fleet_composition[ship.name] = random.randint(1,3+round(faction.military))
                    hwcount += 1
                    for ccat,cnum in ship.carried.items():
                        for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                            if shipc.category == ccat:
                                fleet_composition[shipc.name] = cnum
                                break
                else:
                    #ship = random.choice(faction.shiplist)
                    if ship.installed_weapons > 0 and random.random() > .5:
                        fleet_composition[ship.name] = random.randint(1,5+round(faction.military))
            if len(fleet_composition) <= 0:
                for n in range(random.randrange(3,6)):
                    ship = random.choice(shuffledlist)
                    if ship.category != 'Fighter' or ship.category != 'Drone':
                        fleet_composition[ship.name] = random.randrange(2,4+round(faction.military))
            lp += 1
                    
    elif faction.fleet_tactic == 'offense':
        personalities = ["heroic"]
        shiplist_weapons = ship_sort(faction.shiplist)
        for ship in shiplist_weapons:
            if ship.installed_weapons > 0 and len(fleet_composition) <= 0:
                fleet_composition[ship.name] = random.randint(3,6+round(faction.military))
                for ccat,cnum in ship.carried.items():
                    for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                        if shipc.category == ccat:
                            fleet_composition[shipc.name] = cnum
                            break
            elif ship.installed_weapons > 0 and random.random() > .5:
                fleet_composition[ship.name] = random.randint(2,4+round(faction.military))
                for ccat,cnum in ship.carried.items():
                    for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                        if shipc.category == ccat:
                            fleet_composition[shipc.name] = cnum
                            break
    elif faction.fleet_tactic == 'hitrun':
        personalities = ["coward"]
        shuffledlist = faction.shiplist
        random.shuffle(shuffledlist)
        lp = 0
        while len(fleet_composition) <= 0 or lp < 100:
            for ship in shuffledlist:
                fleetcompcount = len(fleet_composition) <= round(random.random()+1)
                lwmw = (ship.category == 'Medium Warship') or (ship.category == 'Light Warship')
                if ship.installed_weapons > 0 and (lwmw or random.random() < .3) and fleetcompcount:
                    fleet_composition[ship.name] = random.randint(2,4+round(faction.military))
                    for ccat,cnum in ship.carried.items():
                        for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                            if shipc.category == ccat:
                                fleet_composition[shipc.name] = cnum
                                break
            if len(fleet_composition) <= 0:
                for n in range(random.randrange(3,6)):
                    ship = random.choice(shuffledlist)
                    if ship.category != 'Fighter' or ship.category != 'Drone':
                        fleet_composition[ship.name] = random.randrange(2,4+round(faction.military))
            lp += 1
    elif faction.fleet_tactic == 'kite':
        personalities = ["heroic"]
        shuffledlist = faction.shiplist
        random.shuffle(shuffledlist)
        lp = 0
        while len(fleet_composition) <= 0 or lp < 100:
            for ship in shuffledlist:
                fleetcompcount = len(fleet_composition) <= round(random.randint(1,3))
                lwmw = (ship.category == 'Medium Warship') or (ship.category == 'Light Warship')
                if ship.installed_weapons > 0 and (lwmw or random.random() < .3) and fleetcompcount:
                    fleet_composition[ship.name] = random.randint(2,4+round(faction.military))
                    for ccat,cnum in ship.carried.items():
                        for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                            if shipc.category == ccat:
                                fleet_composition[shipc.name] = cnum
                                break
            if len(fleet_composition) <= 0:
                for n in range(random.randrange(3,6)):
                    ship = random.choice(shuffledlist)
                    if ship.category != 'Fighter' or ship.category != 'Drone':
                        fleet_composition[ship.name] = random.randrange(2,4+round(faction.military))
            lp += 1
    else:
        personalities = ["heroic",'opportunistic']
        shuffledlist = faction.shiplist
        random.shuffle(shuffledlist)
        lp = 0
        while len(fleet_composition) <= 0 or lp < 100:
            for ship in shuffledlist:
                fleetcompcount = len(fleet_composition) <= round(random.randint(1,3))
                if ship.installed_weapons > 0 and fleetcompcount:
                    fleet_composition[ship.name] = random.randint(2,4+round(faction.military))
                    for ccat,cnum in ship.carried.items():
                        for shipc in faction.shiplist: #TODO: Could probably optimize, sort fighters out first?
                            if shipc.category == ccat:
                                fleet_composition[shipc.name] = cnum
                                break
            if len(fleet_composition) <= 0:
                for n in range(random.randrange(3,6)):
                    ship = random.choice(shuffledlist)
                    if ship.category != 'Fighter' or ship.category != 'Drone':
                        fleet_composition[ship.name] = random.randrange(2,4+round(faction.military))
            lp += 1
    return fleet_composition,personalities

def generate_fleet(faction,fileout=''):
    if faction.devmode:
        random.seed(99)
    military_names = ['Patrol','Navy','Guard','Security','Military','Defense']
    civilian_names = ['Merchant','Civilian','Privateer']
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} fleets.txt'
    fleetwrite = open(fileout, 'w')

    fleet_name = faction.name + ' ' + random.choice(military_names)
    names = faction.name + ' names'
    militarynames = faction.name + ' Military names'
    personalities = ["heroic","opportunistic"]

    fleetvariants = []

    #fleet_tactic = random.choice('defense offense balance hitrun kite'.split())
    for n in range(random.randrange(3,12)):
        fleet_composition,personalities = gen_militaryfleet_variant(faction)
        fleetvariants.append(fleet_composition.copy())
            
    if faction.agg >= 0 and random.random() < .5:
        personalities.append('disables')
    if faction.agg >= 0 and random.random() < .1:
        personalities.append('forbearing')

    personalities.append('confusion '+str(random.randint(10,max(11,round(30*(1.1-faction.military))))))

    fleetwrite.write(f'fleet "{fleet_name}"' + '\n')
    fleetwrite.write(f'\tgovernment "{faction.name}"' + '\n')
    fleetwrite.write(f'\tnames "{militarynames}"' + '\n')
    fleetwrite.write(f'\tpersonality' + '\n')
    for personality in personalities:
        fleetwrite.write(f'\t\t{personality}' + '\n')
    #variant is a dict of ships(fleet_composition)
    for variant in fleetvariants: #TODO, calculate fleet value and adjust accordingly
        weight = round(random.randrange(2,20))
        fleetwrite.write(f'\tvariant {weight}'+ '\n')
        for ship in variant.keys():
            fleetwrite.write(f'\t\t"{ship}" {variant[ship]}' + '\n')

    faction.patrolfleets.append(fleet_name)

    fleet_name = faction.name + ' ' + random.choice(civilian_names)
    personalities = ["timid"]

    if faction.agg >= 0 and random.random() < .5:
        personalities.append('disables')
    if faction.agg >= 0 and random.random() < .1:
        personalities.append('forbearing')

    personalities.append('confusion '+str(random.randint(20,max(21,round(30*(1.1-faction.military))))))

    fleetwrite.write(f'fleet "{fleet_name}"' + '\n')
    fleetwrite.write(f'\tgovernment "{faction.name}"' + '\n')
    fleetwrite.write(f'\tnames "{names}"' + '\n')
    fleetwrite.write(f'\tpersonality' + '\n')
    for personality in personalities:
        fleetwrite.write(f'\t\t{personality}' + '\n')
    for n in range(faction.civiefleetvariants):
        weight = round(n*random.randrange(2,20))
        ship1 = random.choice(faction.shiplist)
        ship2 = random.choice(faction.shiplist)
        ship3 = random.choice(faction.shiplist)
        ship1_count = random.randrange(1,5)
        ship2_count = random.randrange(1,5)
        ship3_count = random.randrange(1,5)
        fleetwrite.write(f'\tvariant {weight}'+ '\n')
        fleetwrite.write(f'\t\t"{ship1.name}" {ship1_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship2.name}" {ship2_count}' + '\n')
        fleetwrite.write(f'\t\t"{ship3.name}" {ship3_count}' + '\n')

    faction.civilianfleets.append(fleet_name)

    fleetcompo = []
    for n in range(round(faction.civiefleetvariants/2)):
        fleetcompo.append(gen_miningfleet_variant(faction))

    if len(fleetcompo) > 0:
        fleet_name = faction.name + ' ' + "Miner"
        personalities = "timid mining harvests".split()
        personalities.append('confusion '+str(random.randint(20,max(21,round(30*(1.1-faction.military))))))
        fleetwrite.write(f'fleet "{fleet_name}"' + '\n')
        fleetwrite.write(f'\tgovernment "{faction.name}"' + '\n')
        fleetwrite.write(f'\tnames "{names}"' + '\n')
        fleetwrite.write(f'\tpersonality' + '\n')
        for personality in personalities:
            fleetwrite.write(f'\t\t{personality}' + '\n')
        for variant in fleetcompo: #TODO, calculate fleet value and adjust accordingly
            weight = round(random.randrange(2,20))
            fleetwrite.write(f'\tvariant {weight}'+ '\n')
            for ship in variant.keys():
                fleetwrite.write(f'\t\t"{ship}" {variant[ship]}' + '\n')

        faction.miningfleets.append(fleet_name)

    fleetwrite.close()
