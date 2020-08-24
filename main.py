import neopixel_dev
import led_animations
import led_visualizers
'''
TODO:
more meteor (bounce, random size/speeds)
modify melspectrum to only pass half the data (other not needed)
Visualizers: rolling peak volume
'''

DEVELOPER_MODE = neopixel_dev.WLED
    
with neopixel_dev.NeoPixels(DEVELOPER_MODE, ip="192.168.137.222") as pixels: #Start NeoPixels
    #led_animations.quick_sort(pixels)

    pixels.run_visualizer_socket(led_visualizers.sound_rgb, num_segments=150)
    #pixels.run_visualizer_socket(led_visualizers.sound_pulse, ((128,0,128)), num_segments=15, input_mode=neopixel_dev.PYAUDIO_IN)
    #pixels.run_visualizer_socket(led_visualizers.sound_pulse, ((133, 235, 240)), num_segments=15, input_mode=neopixel_dev.PYAUDIO_IN)

