import generate_galaxy
import generate_ships
import generate_outfits
import generate_weapons
import generate_faction
import generate_fleets
import namegenerator
import generate_sales

noPIL = False
try:
    import PIL
except ModuleNotFoundError:
    print("Python Pillow library is not installed! Sprite generation disabled.")
    noPIL = True

DEVMODE = False #Broken, don't use
#for n in range(50): #for testing

government_list = generate_faction.create_faction(noPIL,devmode=DEVMODE)
generate_faction.generategovernmentRelations(government_list)
#Have to be in this order to work, most function depends on ones above
for faction in government_list: 
    generate_outfits.load_custom_configs(faction)
    generate_weapons.create_weapon(faction)
    generate_ships.load_ship_configs(faction)
    namegenerator.generate_namefile(faction)
    generate_fleets.generate_fleet(faction)
    generate_faction.write_government_file(faction)
    generate_sales.generate_shipyard(faction)
    generate_sales.generate_outfitter(faction)

generate_galaxy.load_galaxy_configs(government_list) #Generate complete galaxy