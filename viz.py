import socket
import sys
import audioop
import librosa
import numpy
import math

# Choose the frequency range
SCREEN_WIDTH = 90
ENERGY_THRESHOLD = 0.4
N_FFT = 4096
#F_LO = librosa.note_to_hz('C2')
#F_HI = librosa.note_to_hz('C9')
F_HI = 20
F_LO = 20000
M = librosa.filters.mel(44100, N_FFT, SCREEN_WIDTH, fmin=F_LO, fmax=F_HI)

def generate_string_from_audio(audio_data):
    # Compute real FFT.
    x_fft = numpy.fft.rfft(audio_data, n=N_FFT)

    # Compute mel spectrum.
    melspectrum = M.dot(abs(x_fft))

    # Initialize output characters to display.
    char_list = [' ']*SCREEN_WIDTH

    for i in range(SCREEN_WIDTH):
#        if i == 0:
#            print(melspectrum[i])

        # If there is energy in this frequency bin, display an asterisk.
        if melspectrum[i] is not 0 and math.log10(abs(melspectrum[i])) > ENERGY_THRESHOLD:
            char_list[i] = '*'

        # Draw frequency axis guidelines.
        elif i % 30 == 29:
            char_list[i] = '|'

    # Return string.
    return ''.join(char_list)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(('127.0.0.1', 5555))
    while True:
        data, addr = s.recvfrom(16384)
        in_data = audioop.tomono(data,2,1,1)
        #print(data)
#       sys.stdout.buffer.write(data)
        #print("."*int(audioop.rms(in_data, 2)/250),"##")

        audio_data = numpy.frombuffer(in_data, dtype="<i2") #as little endian int16
        audio_data = audio_data.astype(numpy.float32)/32767 #make float from -1 to 1

        print( generate_string_from_audio(audio_data) )
        
