import math

from math import radians, copysign

offx = 197700
offy = 250500

scale_x = 20
scale_y = 1000

mercator_cap = 75

def mercator_y_transform(phi):
	return math.log(math.tan(math.pi/4+phi/2))
	
size_x = scale_x * 360
size_y = mercator_y_transform(math.radians(mercator_cap)) * scale_y * 4

top_left_x = offx - scale_x * 180 
top_left_y = offy + scale_y * mercator_y_transform(math.radians(-mercator_cap)) - size_y / 4


#print(top_left_x, top_left_y)
#print(top_left_x + size_x, top_left_y+size_y)

def complexless_power(x, y):
	return copysign(abs(x) ** y, x)
	
def transform_latitude(x):
	return complexless_power(-mercator_y_transform(radians(x)) * scale_y * 1.3, 0.999) + offy