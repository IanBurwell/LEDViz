# UDPixelViz
Visualiser for UDP pcm streams using RPi and NeoPixel

Mopidy setup to stream on "jack" audio device and stream udp under `[audio]`
`output = tee name=t ! queue ! alsasink device=jack t. ! queue ! udpsink host=127.0.0.1 port=5555`

/etc/asound.conf: 
```
pcm.jack{
	type hw
	card Headphones
}
```

