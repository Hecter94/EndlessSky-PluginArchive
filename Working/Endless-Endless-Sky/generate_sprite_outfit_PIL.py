from PIL import Image
import numpy as np
import colorsys

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    arr = [r, g, b, a]
    return arr

def shift_col(arr, hout): #adjust rgb individually
    pass