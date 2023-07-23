import requests
import urllib
from urllib.parse import quote
import argparse
from bs4 import BeautifulSoup

SEARCH_F = 'https://starwars.fandom.com/wiki/{name}'

parser = argparse.ArgumentParser()
parser.add_argument('planet')

args = parser.parse_args()

def replace_planet_description(name, text):
	with open("data/map.txt") as f:
		contents = f.read()
	
	contents = contents.replace(f"\"{name}_DESC\"", f"`{text}`")
	
	
	with open("data/map.txt", "w") as f:
		f.write(contents)
		
		


b = BeautifulSoup(requests.get(SEARCH_F.format(name=args.planet)).text, features="html5lib")

for i in b.select("body article #content .mw-parser-output > p"):
	if i.text.strip():
		replace_planet_description(args.planet, i.text)
		break
