import random
import math

def avg_deviation(numlist):
    totalnum = 0
    for num in numlist:
        totalnum += num
    avg = totalnum/len(numlist)
    x = 0
    for num in numlist:
        x += (num-avg)**2
    return avg, math.sqrt(x/totalnum)


def outfit_sort(outfitlist,sortby="outfit space"):
    if sortby=="outfit space":
        for i in range(len(outfitlist)):
            for j in range(i+1,len(outfitlist)):
                if outfitlist[i].outfit_space < outfitlist[j].outfit_space:
                    outfitlist[i].outfit_space,outfitlist[j].outfit_space = outfitlist[j].outfit_space,outfitlist[i].outfit_space
    return outfitlist

def ship_sort(shiplist,sortby="mass"):
    if sortby=="mass":
        for i in range(len(shiplist)):
            for j in range(i+1,len(shiplist)):
                if shiplist[i].mass < shiplist[j].mass:
                    shiplist[i].mass,shiplist[j].mass = shiplist[j].mass,shiplist[i].mass
    return shiplist

class class_Outfitter():
    def __init__(self,name) -> None:
        self.name = name
        self.outfitlist = []

class class_Shipyard():
    def __init__(self,name) -> None:
        self.name = name
        self.shiplist = []



def generate_outfitter(faction, fileout=''):
    if faction.devmode:
        random.seed(99)
    
    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} sales.txt'
    
    outfitter_count = 3

    ammolist = []

    for weapon in faction.weaponlist:
        if weapon.weapon_type == 'missileammo':
            ammolist.append(weapon)

    all_outfits = faction.outfitlist
    all_outfits.extend(faction.weaponlist)
    outfitlist_sorted = outfit_sort(all_outfits)
    outfitperoutfitter = math.floor(len(outfitlist_sorted)/outfitter_count)
    outfitterlist = []

    for outfitter_n in range(outfitter_count):
        outfitterlist.append(class_Outfitter(str(faction.name+" "+str(outfitter_n+1))))
        for n in range(outfitperoutfitter*(outfitter_n+1)):
            try:
                outfitterlist[outfitter_n].outfitlist.append(outfitlist_sorted[n])
            except IndexError:
                pass
    
    faction.outfitterlist = outfitterlist

    with open(fileout, "a") as sales_output:
        sales_output.write(f'outfitter "{faction.name} Ammo"' + '\n')
        for ammo in ammolist:
            sales_output.write('\t' + f'"{ammo.name}"' + "\n")
        sales_output.write('\t' + f'"Local Map"' + "\n")
        for outfitter_print in outfitterlist:
            sales_output.write("\n")
            sales_output.write(f'outfitter "{outfitter_print.name}"' + '\n')
            for outfit in outfitter_print.outfitlist:
                sales_output.write('\t' + f'"{outfit.name}"' + "\n")

            sales_output.write('\t' + f'"Local Map"' + "\n")
            sales_output.write('\t' + f'"Outfits Expansion"' + "\n")
            sales_output.write('\t' + f'"Cargo Expansion"' + "\n")
            sales_output.write('\t' + f'"Small Bunk Room"' + "\n")
            sales_output.write('\t' + f'"Bunk Room"' + "\n")
            sales_output.write("\n")

#todo : make shipyard categorize by mass.
def generate_shipyard(faction, fileout = ''):

    if fileout == '':
        fileout = f'data/{faction.name}/{faction.name} sales.txt'

    shipyard_count = 3

    shiplist_sorted = ship_sort(faction.shiplist)
    shipspershipyard = math.ceil(len(shiplist_sorted)/shipyard_count)
    shipyardlist = []
    
    for shipyard_n in range(shipyard_count):
        newshipyard = class_Shipyard(str(faction.name+" "+str(shipyard_n+1)))
        shipyardlist.append(newshipyard)
        #print(f"Shipyard {shipyard_n}")
        #print(f'shipyard "{shipyardlist[shipyard_n].name}"')
        for n in range(shipspershipyard*(shipyard_n+1)):
            try:
                shipyardlist[shipyard_n].shiplist.append(shiplist_sorted[n])
                #print(f" added {shiplist_sorted[n].name} to {shipyardlist[shipyard_n].name}")
            except IndexError:
                pass
    
    faction.shipyardlist = shipyardlist

    with open(fileout, "a") as sales_output:
        for shipyard_print in shipyardlist:
            sales_output.write("\n")
            sales_output.write(f'shipyard "{shipyard_print.name}"' + '\n')
            for ship in shipyard_print.shiplist:
                sales_output.write('\t' + f'"{ship.name}"' + "\n")
            sales_output.write("\n")