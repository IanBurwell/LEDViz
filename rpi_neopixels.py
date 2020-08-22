

import neopixel_dev
import led_animations
import led_visualizers
'''
TODO:
more meteor (bouce, random size/speeds)
modify melspectrum to only pass half the data (other not needed)
Vizualisers: rolling peak volume
'''

DEVELOPER_MODE = False
    
with neopixel_dev.NeoPixels(DEVELOPER_MODE) as pixels: #Start NeoPixels with in simulation mode
    #led_animations.rainbow(pixels, 1)
    #led_animations.pulse(pixels, 4, (255, 0, 0))
    #led_animations.pulse_sin(pixels, 1, (0,255,255))
    #led_animations.gradient(pixels, 0.05, (0,0,255))
    #led_animations.dot_bounce(pixels, [8, 8, 8], [(255,0,0), (0,255,0), (0,0,255)])
    #led_animations.dot_pan(pixels, 0.01, (255,255,255), 4)
    #led_animations.dot_pan_rainbow(pixels, 0.01, 4)
    #led_animations.rainbow_pan(pixels, 1, 4)
    #led_animations.dart(pixels, (255,255,255), speed=100)
    #led_animations.strobe(pixels, 10)
    #led_animations.sparkle(pixels, 1)
    #led_animations.wave(pixels, 1, (255,255,255))
    #led_animations.wave_rgb(pixels, 10, -1)
    #led_animations.chaser(pixels, 5, (255,0,0), 5)
    #led_animations.chaser_rainbow(pixels, 4)
    #led_animations.meteor(pixels, (255,200,200), 8, 20, 1)
    #led_animations.random_fade(pixels, 2, (255,200,0))
    #led_animations.insertion_sort(pixels)
    #led_animations.selection_sort(pixels)
    #led_animations.merge_sort(pixels)
    #led_animations.quick_sort(pixels)

    #pixels.enable_fade()
    #pixels.run_visualizer_socket(led_visualizers.sound_original)
    #pixels.run_visualizer_socket(led_visualizers.sound_rgb, num_segments=150)
    pixels.run_visualizer_socket(led_visualizers.sound_pulse, ((128,0,128)), num_segments=15)

