import time
import colorsys
import math
import socket
import struct
import _thread

"""
TODO:
knowing the bitrate, chop large sample of audio into pieces for visualization, preforming separate fft and playing at correct speed

fade/brightness keeping color ratio
adjust color setting to be more accurate
adjust brightness to be more linear
"""

class NeoPixels():
    #init
    def __init__(self, DEVEL=True, count=300, fade=False, brightness=1.0):
        self.size = count
        self.DEVEL = DEVEL
        self.updatePygame = True
        self.lock = _thread.allocate_lock()
        self.brightness = brightness
        self._fade_thread = None
        self.fadeDelay = 0.5
        self.fadeAmount = 20

        if fade:
            self.enable_fade()

        if self.DEVEL:
            self.pixels = [(0,0,0)] * self.size
            self._display_thread = _thread.start_new_thread(self._display,())
        else:
            import board
            import neopixel
            self.pixels = neopixel.NeoPixel(board.D18, 300, auto_write=False)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if not self.DEVEL:
            self.pixels.deinit()
        else:
            self._display_thread = None
        self.stop_fade()

    def __getitem__(self, index):
        with self.lock:
            val = self.pixels[index]
        return val

    def __setitem__(self, index, val):
        with self.lock:
            self.pixels[index] = (int(val[0]),int(val[1]),int(val[2]))

    def __len__(self):
        return len(self.pixels)
        
    #updates the leds with the data in pixels
    def show(self):
        if not self.DEVEL:
            self.pixels.show()
        else:
            self.updatePygame = True

    #fills pixels with a given color
    def fill(self, color):
        with self.lock:
            if self.DEVEL:
                for i in range(self.size):
                    self.pixels[i] = color
            else:
                self.pixels.fill(color)

    def set_brightness(self, amount=1.0):
        if not self.DEVEL:
            self.pixels.brightness(amount)            
        else:
            self.show()
        self.brightness = amount

    #starts a thread constantly fading all pixels
    def enable_fade(self, fadeDelay=0.01, fadeAmount=10):
        self.fadeDelay = fadeDelay
        self.fadeAmount = fadeAmount
        if self._fade_thread is None:
            self._fade_thread = _thread.start_new_thread(self._fade, ())

    #stops the fade thread
    def stop_fade(self):
        if self._fade_thread is not None:
            self._fade_thread = None

    #sets the delay of the fade        
    def fade_setup(self, delay=0.05, fadeAmount=20):
        self.fadeDelay = delay
        self.fadeAmount = fadeAmount

    #listens with a socket and gives sound data to the sound_handler
    def run_visualizer_socket(self, sound_handler, args=None, port=5555, host="127.0.0.1", 
                                                   num_segments=None, f_low=65, f_high=8372):
        import audioop
        import librosa
        import numpy

        if num_segments is None: #default number of segments/bins in the melspectrum (max 4096 i think idk)
            num_segments = self.size
        
        if self.DEVEL: #play wav file if in dev mode
            self._wav_thread = _thread.start_new_thread(self._wav_stream,())
            host="127.0.0.1"
            port=5555

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((host, port))
            while True:
                data, addr = s.recvfrom(65565)#recive data in 16k chunks
                #data, addr = s.recvfrom(16384)#recive data in 16k chunks
                in_data = audioop.tomono(data,2,1,1)#convert to mono stream

                audio_data = numpy.frombuffer(in_data, dtype="<i2") #read as little endian int16
                audio_data = audio_data.astype(numpy.float32)/32767 #make float from -1 to 1
                
                N_FFT = 4096
                x_fft = numpy.fft.rfft(audio_data, n=N_FFT) # Compute real fast foriere transform
                M = librosa.filters.mel(44100, N_FFT, num_segments, fmin=f_low, fmax=f_high)
                melspectrum = M.dot(abs(x_fft)) # Compute mel spectrum.

                if args is not None:
                    sound_handler(melspectrum, args)
                else:
                     sound_handler(melspectrum)                


    def _fade(self):
        while self._fade_thread is not None:
            time.sleep(self.fadeDelay)
            with self.lock:
                for i in range(self.size):
                    self.pixels[i] = (max(0,self.pixels[i][0]-self.fadeAmount),
                                      max(0,self.pixels[i][1]-self.fadeAmount),
                                      max(0,self.pixels[i][2]-self.fadeAmount))                
            self.show()

    def _display(self):
        import pygame
        import pygame.gfxdraw

        FPS = 90

        pygame.init()
        screen = pygame.display.set_mode((900, 50), pygame.RESIZABLE)
        pygame.display.set_caption("Simulated Neopixels")
        clock = pygame.time.Clock()

        while self._display_thread is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    _thread.interrupt_main()
                    return
                if event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if self.updatePygame:
                screen.fill((0, 0, 0))
                w, h = screen.get_size()
                for i in range(self.size):
                    pygame.gfxdraw.box(screen,
                                       (w/self.size*i, 0, w/self.size,h),
                                       tuple( map(lambda x: int(x*self.brightness), self.pixels[i]) ))
                self.updatePygame = False

            pygame.display.update() #aka flip
            clock.tick(FPS)

    def _wav_stream(self, filename="bensound.com-energy.wav"):
    #def _wav_stream(self, filename="test.wav"):
        import wave
        import pyaudio
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            wf = wave.open(filename, 'rb')
            p = pyaudio.PyAudio()

            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            # play/send stream
            chunk_size = 2048 #lower is more latend but higher fps
            data = wf.readframes(chunk_size)
            while len(data) > 0:
                stream.write(data)
                s.sendto(data,("127.0.0.1", 5555))
                data = wf.readframes(chunk_size)

            stream.stop_stream()
            stream.close()
            p.terminate()




            
            
            
            

if __name__ == "__main__":
    pixels = NeoPixels(True)

    def rainbow_pan(speed, numWaves=4):
        offset = 0

        while True:
            time.sleep(0.001)
            offset = (offset+speed/10)%len(pixels)
            for i in range(len(pixels)):
                r, g, b = colorsys.hls_to_rgb((i+offset)*numWaves%len(pixels)/len(pixels), 0.5,1)
                pixels[i] = (int(r*255), int(g*255), int(b*255))
            pixels.show()
    rainbow_pan(1)
   
