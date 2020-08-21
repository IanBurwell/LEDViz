import time 
import colorsys 
import random 
import math

################################################################
# Music Visualisers           
################################################################

def sound_original(pixels, melspectrum):
    for i in range(len(pixels)//2):
        value = None
        if melspectrum[i] > 0.6:
            value = (255,0,0)
        elif melspectrum[i] > 0.4:
            value = (0,0,255)
        elif melspectrum[i] > 0.2:
            value = (0,255,0)

        if value is not None:
            pixels[len(pixels)//2+i] = value
            pixels[len(pixels)//2-i] = value
    pixels.show()

def sound_rgb(pixels, melspectrum):
    for i in range(len(pixels)//2):
        r, g, b = colorsys.hls_to_rgb(max(0, 1-melspectrum[i]),0.5,1)
        bright = min(1, max(0, (melspectrum[i]-0.1)/4))
        pixels[len(pixels)//2+i] = (int(r*255*bright), int(g*255*bright), int(b*255*bright))
        pixels[len(pixels)//2-i] = (int(r*255*bright), int(g*255*bright), int(b*255*bright))
    pixels.show()

def sound_pulse(pixels, melspectrum, color):
    for i in range(len(pixels)):
        pixels[i] = color

    pixels.set_brightness(min(1, sum(melspectrum[:15]/15)/4))
