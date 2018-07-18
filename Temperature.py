### Circuit Playground Express (CPX) termistor demo
### v1.0

### rename this to main.py if not called main.py
##import serial
import board
import digitalio
import time

import neopixel
import adafruit_thermistor

### this code does not belong here
##ser = serial.Serial('/dev/ttyAMA0')

### Inspire by https://learn.adafruit.com/adafruit-circuit-playground-express/playground-temperature
### Some values specific to CPX
series_resistor     = 10000
nominal_resistance  = 10000
nominal_temperature = 25
b_coefficient       = 3950
thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE,
                                            series_resistor,
                                            nominal_resistance,
                                            nominal_temperature,
                                            b_coefficient)

redled = digitalio.DigitalInOut(board.D13)
redled.direction = digitalio.Direction.OUTPUT

black = (0, 0, 0)
cyan = (0, 0x20, 0x20)
yellow = (0x20, 0x20, 0)
red   = (0x20, 0, 0)
green = (0, 0x20, 0)
magenta = (0x20, 0, 0x20)
blue  = (0, 0, 0x20)
white = (0x20, 0x20,0x20)

### CPX has 10 leds
leds = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)

tempbits = 8
tempbitsfmt = '{0:0' + str(tempbits) + 'b}'

redled.value = False
colours = [red, green, blue, magenta, cyan, yellow, white]
colouridx=0
while True:
    temp_c = thermistor.temperature
    print("\n Temperature is: {:.2f}C".format(temp_c))
    if 26 < temp_c < 30.7:
        print ("Its normal in here")
        if colouridx >= len(blue):
            colouridx = 0
        #leds[idx] = white
    elif temp_c > 30.7:
        print ("Its too hot")
        #if colouridx >= len(red):
        colouridx = 1
        #leds[idx] = red
        
##    print(ser.name)
##    ser.write(b'hello')
    temp_c_binarystr = tempbitsfmt.format(int(temp_c + 0.5))
    for idx in range(len(temp_c_binarystr)):
        if 26 < temp_c < 30.7:
            leds[idx] = green
        else:
            leds[idx] = red
        #if temp_c_binarystr[idx] == '0':
            #leds[idx] = black
        #elif temp_c_binarystr[idx] == '1':
            #leds[idx] = blue
            
    ### lightshow on the remaining two leds
    leds[tempbits:] = [colours[colouridx]] * (len(leds) - tempbits)
    colouridx += 1
    if colouridx >= len(colours):
        colouridx = 0
    
    leds.show()
    redled.value = not redled.value
    time.sleep(2)

