# UDPixelViz
Visualiser for UDP 16bit pcm streams using RPi and NeoPixel

Mopidy setup to stream on "jack" audio device and stream udp under `[audio]`
`output = tee name=t ! queue ! alsasink device=jack t. ! queue ! udpsink host=127.0.0.1 port=5555`

/etc/asound.conf: 
```
pcm.jack{
	type hw
	card Headphones
}
```
Helpful for librosa setup on RPi, make sure to download only the versions they mention:
https://raspberrypi.stackexchange.com/questions/111697/unable-to-pip-install-librosa-in-raspberry-pi-3-model-b-raspbian-stretch
PyAudio setup on Windows for development:
https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14