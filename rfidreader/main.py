# https://toptechboy.com/rfid-lock-and-unlock-demonstration-project-raspberry-pi-pico-w/
# Video's:
# https://www.youtube.com/watch?v=b2Kgk16mtTY <- watch this first!
# https://www.youtube.com/watch?v=bM-mr9X-SiU
# library:
# https://github.com/sunfounder/kepler-kit

from mfrc522 import SimpleMFRC522
import time
from machine import Pin, PWM

unlockTime = 5
decPin = 20
incPin = 21
decBut=Pin(decPin,Pin.IN,Pin.PULL_UP)
incBut=Pin(incPin,Pin.IN,Pin.PULL_UP)

redPin=15
greenPin=14
bluePin=13
redLED=Pin(redPin,Pin.OUT)
greenLED=Pin(greenPin,Pin.OUT)
blueLED=Pin(bluePin,Pin.OUT)
redLED.on()
greenLED.off()
blueLED.off()

incButState=1
incButStateOld=1

decButState=1
decButStateOld=1

butCount = 0

reader=SimpleMFRC522(spi_id=0,sck=18,miso=16,mosi=19,cs=17,rst=9) # type: ignore

def readRFID():
    global cardID
    print()
    print("System LOCKED")
    print("Reading . . . Please Place the Card")
    cardID,readText = reader.read()
    print()
    print("ID: ",cardID)

while True:
    redLED.on()
    greenLED.off()
    blueLED.off()
    readRFID()
    print("System Unlocked by Card: ",cardID)
    unlockStart= time.time()
    while time.time()-unlockStart<unlockTime:
        redLED.off()
        greenLED.on()
        incButState=incBut.value()
        decButState=decBut.value()
        if incButState==0 and incButStateOld==1:
            butCount=butCount+1
            print("Button Count: ",butCount)
            unlockStart=time.time()
            time.sleep(.2)
        if decButState==0 and decButStateOld==1:
            butCount=butCount-1
            print("Button Count: ",butCount)
            unlockStart=time.time()
            time.sleep(.2)
        incButStateOld=incButState
        decButStateOld=decButState
