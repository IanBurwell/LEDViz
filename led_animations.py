import time 
import colorsys 
import random 
import math

################################################################
# Patterns           
################################################################

def rainbow(pixels, speed):
    offset = 0
    
    while True:
        time.sleep(0.001)
        offset = (offset+speed/10000)%1
        for i in range(len(pixels)):
            r, g, b = colorsys.hls_to_rgb(offset,0.5,1)
            pixels[i] = (int(r*255), int(g*255), int(b*255))
        pixels.show()
        
def pulse(pixels, speed, color):    
    brightness = 0
    r, g, b = color
    
    while True:
        time.sleep(0.005)
        if brightness >= 1000: speed = -1*abs(speed)
        elif brightness <= 0: speed = abs(speed)
        brightness += speed
        
        pixels.fill((int(r*brightness/1000), int(g*brightness/1000), int(b*brightness/1000)))
        pixels.show()

def pulse_sin(pixels, speed, color):
    brightness = 0
    r, g, b = color
    
    while True:
        time.sleep(0.001)
        brightness = (math.sin(speed/2*math.pi*time.time())+1)/2

        pixels.fill((int(r*brightness), int(g*brightness), int(b*brightness)))
        pixels.show()
            
def gradient(pixels, delay, color, number=2):
    offset = 0
    r, g, b = color

    while True:
        time.sleep(delay)
        offset = (offset-1)%len(pixels)
        pixels.fill((0,0,0))
        for i in range(len(pixels)):
            lightness = (i+offset)*number%len(pixels)/len(pixels)
            pixels[i] = (int(r*lightness), int(g*lightness), int(b*lightness))
        pixels.show()
        
def dot_bounce(pixels, speeds, colors, radius=15):        
    number = len(speeds) #of dots
    positions = [0]*number

    for i in range(number):
        speeds[i] /= 100
        positions[i] = i*(len(pixels)/number)

    while True:
        time.sleep(0.001)
        for i in range(number):
            if positions[i]+speeds[i] >= len(pixels)-1:
                speeds[i] = -abs(speeds[i])
            elif positions[i]-speeds[i] <= 0:
                speeds[i] = abs(speeds[i])
            positions[i] += speeds[i]
        
        pixels.fill((0,0,0))
            
        for p in range(number):
            for i in range(radius):
                position = int(positions[p])
                r, g, b = colors[p]
                if position+i <= len(pixels)-1:
                    rf, gf, bf, = pixels[position+i]
                    pixels[(position+i)%len(pixels)] = (min(255, int(rf+r/radius*(radius-i))), min(255, int(gf+g/radius*(radius-i))), min(255, int(bf+b/radius*(radius-i))))
                if position-i >= 0:
                    rf, gf, bf, = pixels[position-i]
                    pixels[(position-i)%len(pixels)] = (min(255, int(rf+r/radius*(radius-i))), min(255, int(gf+g/radius*(radius-i))), min(255, int(bf+b/radius*(radius-i))))
        pixels.show()
        
def dot_pan(pixels, delay, color, dots, radius=15):
    offset = 0
    spacing = (len(pixels)/dots)
    r, g, b = color

    while True:
        time.sleep(delay)
        offset = (offset+1)%len(pixels)

        pixels.fill((0,0,0))
        
        for dot in range(dots):
            position = int(offset+spacing*dot)%len(pixels)
            for i in range(radius):
                rf, gf, bf, = pixels[(position+i)%len(pixels)]
                pixels[(position+i)%len(pixels)] = (min(255, int(rf+r/radius*(radius-i))), min(255, int(gf+g/radius*(radius-i))), min(255, int(bf+b/radius*(radius-i))))

                rf, gf, bf, = pixels[(position-i)%len(pixels)]
                pixels[(position-i)%len(pixels)] = (min(255, int(rf+r/radius*(radius-i))), min(255, int(gf+g/radius*(radius-i))), min(255, int(bf+b/radius*(radius-i))))
        pixels.show()

def dot_pan_rainbow(pixels, delay, dots, radius=15):
    offset = 0
    spacing = (len(pixels)/dots)

    while True:
        time.sleep(delay)
        offset = (offset+1)%len(pixels)

        pixels.fill((0,0,0))
        
        for dot in range(dots):
            position = int(offset+spacing*dot)%len(pixels)
            for i in range(radius):
                brightness = 255/radius*(radius-i)
                
                r,g,b = colorsys.hls_to_rgb((position+i)%len(pixels)/len(pixels),0.5,1)
                pixels[(position+i)%len(pixels)] = (int(r*brightness),int(g*brightness),int(b*brightness))

                r,g,b = colorsys.hls_to_rgb((position-i)%len(pixels)/len(pixels),0.5,1)
                pixels[(position-i)%len(pixels)] = (int(r*brightness),int(g*brightness),int(b*brightness))
        pixels.show()
        
def rainbow_pan(pixels, speed, numWaves=2):
    offset = 0
    
    while True:
        time.sleep(0.001)
        offset = (offset+speed/10)%len(pixels)
        for i in range(len(pixels)):
            r, g, b = colorsys.hls_to_rgb((i+offset)*numWaves%len(pixels)/len(pixels), 0.5,1)
            pixels[i] = (int(r*255), int(g*255), int(b*255))
        pixels.show()
        
def dart(pixels, color, speed=10, minWait=0.1, maxWait=3):
    position = 0
    dir = 1
    
    while True:
        goal = random.randint(0, len(pixels)-1)
        dir = int((goal-position)/abs(goal-position)) if goal is not position else 0
        print(dir, goal)
        while position is not goal:
            time.sleep(0.1/speed)
            position += dir
            
            pixels[position] = color
            pixels[position-1*dir] = (0,0,0)
        time.sleep(random.random()*(maxWait-minWait)+minWait)
        pixels.show()
        
def strobe(pixels, hz, color=(255,255,255)):
    while True:
        time.sleep(1/hz/2)
        for i in range(len(pixels)):
            pixels[i] = color
        time.sleep(1/hz/2)
        pixels.fill((0, 0, 0))
        pixels.show()
        
def sparkle(pixels, speed, color=(255,255,255)):
    while True:
        time.sleep(0.01/speed)
        pos = random.randint(0,len(pixels)-1)
        pixels[pos] = color
        pixels.show()

        time.sleep(0.01/speed)
        pixels[pos] = (0,0,0)
        pixels.show()
        
def wave(pixels, speed, color, waves=2):
    r, g, b = color
    while True:
        time.sleep(0.001)
        curTime = time.time()
        for i in range(len(pixels)):
            brightness = (math.sin(waves*2*math.pi/len(pixels)*i-4*curTime*speed)+1)/2
            pixels[i] = (int(r*brightness), int(g*brightness), int(b*brightness))
        pixels.show()

def wave_rgb(pixels, waves, speedR=1, speedG=2, speedB=3):
    while True:
        time.sleep(0.001)
        curTime = time.time()
        for i in range(len(pixels)):
            r = 255*(math.sin(waves*2*math.pi/len(pixels)*i-4*curTime*speedR)+1)/2
            g = 255*(math.sin(waves*2*math.pi/len(pixels)*i-4*curTime*speedG)+1)/2
            b = 255*(math.sin(waves*2*math.pi/len(pixels)*i-4*curTime*speedB)+1)/2
            pixels[i] = (int(r), int(g), int(b))
        pixels.show()

def chaser(pixels, speed, color, distance=3):
    offset = 0
    while True:
        offset = (offset+1)%distance
        for i in range(offset, len(pixels)-1, distance):
            pixels[i] = color
        
        time.sleep(0.1/speed)
        pixels.fill((0,0,0))
        pixels.show()

def chaser_rainbow(pixels, speed, distance=3):
    offset = 0
    while True:
        pixels.fill((0,0,0))
        offset = (offset+1)%distance
        for i in range(offset, len(pixels)-1, distance):
            r, g, b = colorsys.hls_to_rgb(i/len(pixels),0.5,1)
            pixels[i] = (int(r*255), int(g*255), int(b*255))
        pixels.show()
        time.sleep(0.1/speed)

def meteor(pixels, color, meteorSize, meteorTrailDecay, speed, meteorRandomDecay=True):  
    while True:
        for i in range(len(pixels)+meteorSize):
            # fade brightness all LEDs one step
            for j in range(len(pixels)):
                if not meteorRandomDecay or random.randint(0, 10)>5:
                    r, g, b = pixels[j]
                    r = 0 if r<=10 else int(r-(r*meteorTrailDecay/255))
                    g = 0 if g<=10 else int(g-(g*meteorTrailDecay/255))
                    b = 0 if b<=10 else int(b-(b*meteorTrailDecay/255))
                    pixels[j] = (int(r),int(g),int(b))
            
       
            # draw meteor
            for j in range(meteorSize):
                if i-j < len(pixels) and i-j >= 0:
                    pixels[i-j] = color

            pixels.show()
            time.sleep(0.02/speed)

def random_fade(pixels, timeBetween, color, fadeSpeed=3, fadeUp=10):
    changeTime = time.time()
    cr, cg, cb = color
    
    while True:
        time.sleep(0.001)
        
        if changeTime <= time.time():
            changeTime = time.time()+timeBetween
            for j in range(1, fadeUp):
                time.sleep(0.01)
                for i in range(len(pixels)):
                    pixels[i] = (cr*j/fadeUp, cg*j/fadeUp, cb*j/fadeUp)
        
        #fade
        for i in range(len(pixels)):
            if random.randint(0, 10) > 5:
                r, g, b = pixels[i]
                r = 0 if r<=10 else int(r-(r*fadeSpeed/255))
                g = 0 if g<=10 else int(g-(g*fadeSpeed/255))
                b = 0 if b<=10 else int(b-(b*fadeSpeed/255))
                pixels[i] = (int(r),int(g),int(b))
        pixels.show()

################################################################
# Sorting Algorithms           
################################################################

def insertion_sort(pixels, ):
    def display_array(arr):
        for i, v in enumerate(arr):
            r, g, b = colorsys.hls_to_rgb(v, 0.5, 1)
            pixels[i] = (r*255, g*255, b*255)
        pixels.show()
    def shuffle(arr, shuffles=20):
        for i in range(shuffles):
            random.shuffle(arr)
            display_array(arr)
            time.sleep(0.1)
        
            
    arr = [x/len(pixels) for x in range(len(pixels))]
    while True:
        shuffle(arr)
        for i, e in enumerate(arr):
            for j, f in enumerate(arr[:i+1]):
                if f > e: break
            arr.pop(i)
            arr.insert(j, e)
            display_array(arr)
            time.sleep(10/len(pixels))
        time.sleep(5)

def selection_sort(pixels, ):
    def display_array(arr):
        for i, v in enumerate(arr):
            r, g, b = colorsys.hls_to_rgb(v, 0.5, 1)
            pixels[i] = (r*255, g*255, b*255)
        pixels.show()
    def shuffle(arr, shuffles=20):
        for i in range(shuffles):
            random.shuffle(arr)
            display_array(arr)
            time.sleep(0.1)
        
            
    arr = [x/len(pixels) for x in range(len(pixels))]
    while True:
        shuffle(arr)
        for i, _ in enumerate(arr):
            small = min(arr[i:])
            mini = arr.index(small)
            arr.pop(mini)
            arr.insert(i, small)
            display_array(arr)
            time.sleep(10/len(pixels))
        time.sleep(5)

def merge_sort(pixels, ):
    def display_array(arr):
        for i, v in enumerate(arr):
            r, g, b = colorsys.hls_to_rgb(v, 0.5, 1)
            pixels[i] = (r*255, g*255, b*255)
        pixels.show()
    def shuffle(arr, shuffles=20):
        for i in range(shuffles):
            random.shuffle(arr)
            display_array(arr)
            time.sleep(0.1)
            
    def mergeSorter(arr, first, last):
        if first >= last: return

        mid = (first + last)//2
        mergeSorter(arr, first, mid)
        mergeSorter(arr, mid+1, last)

        left, right = first, mid+1
        if arr[mid] <= arr[right]: return

        while left <= mid and right <= last:
            if arr[left] <= arr[right]:
                left += 1
            else:
                tmp = arr[right]
                arr[left+1:right+1] = arr[left:right]
                arr[left] = tmp
                left += 1
                mid += 1
                right += 1
                time.sleep(0.002)
                display_array(arr)
    
    arr = [x/len(pixels) for x in range(len(pixels))]
    while True:
        shuffle(arr)
        mergeSorter(arr, 0, len(pixels)-1)
        time.sleep(5)

def quick_sort(pixels, ):
    def display_array(arr):
        for i, v in enumerate(arr):
            r, g, b = colorsys.hls_to_rgb(v, 0.5, 1)
            pixels[i] = (r*255, g*255, b*255)
        pixels.show()
    def shuffle(arr, shuffles=20):
        for i in range(shuffles):
            random.shuffle(arr)
            display_array(arr)
            time.sleep(0.1)
            
    def quick_sorter(arr, first, last):
        if first >= last: return

        randpivot = random.randrange(first, last)
        arr[first], arr[randpivot] = arr[randpivot], arr[first]

        pivot = first
        i = first + 1
        for j in range(first+1, last+1):
            if arr[j] <= arr[pivot]:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                display_array(arr)
                time.sleep(0.002)

        arr[pivot], arr[i-1] = arr[i-1], arr[pivot]
        pivot = i-1

        quick_sorter(arr, first, pivot-1)
        quick_sorter(arr, pivot+1, last)
    
    arr = [x/len(pixels) for x in range(len(pixels))]
    while True:
        shuffle(arr)
        quick_sorter(arr, 0, len(pixels)-1)
        time.sleep(5)
