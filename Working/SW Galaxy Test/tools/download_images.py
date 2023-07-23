import urllib.request
import common

fmt = "http://1.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/3/{z}/{x}/{y}.png"
sector_fmt = "http://1.gusc.cartocdn.com/hbernberg/api/v1/map/6d07251cec293f14ef440bb0a2411372:1577570329193/1/{z}/{x}/{y}.png"

download_image = urllib.request.urlretrieve
	
galaxyf = '''
galaxy "{name}"
	pos {x} {y}
	sprite "{filename}"
'''
z = 1

pixel_x = int(common.size_x / z ** 2)
pixel_y = int(common.size_y / z ** 2)
	
for x in range(0, z ** 2+1):
	for y in range(0, z ** 2+1):
		for format, filename in (
			(fmt, f"dev_images/ui/sw_hyperlanes_{x}_{y}.png"),
			(sector_fmt, f"dev_images/ui/sw_sectors_{x}_{y}.png"),
		):
			print("Downloading")
			download_image(format.format(z=z, x=x, y=y), filename)
			filename = filename[len("images/"):]
			filename = filename[:-len(".png")]
			print(galaxyf.format(
				x = common.top_left_x + (x + .5) * pixel_x,
				y = common.top_left_y + (y + .5) * pixel_y,
				name = filename,
				filename = filename,
			))
		
#print((common.size_x / z ** 2), (common.size_y / z ** 2))

from os import system

#system(f'mogrify -auto-orient -thumbnail {pixel_x}x{pixel_y}! "dev_images/ui/sw_*.png"')