# Blink example from https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/

import array
import time
from machine import Pin
from rp2 import StateMachine, asm_pio, PIO

# Configure the number of WS2812 LEDs.
NUM_LEDS = 8

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
         autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

# Create the StateMachine with the ws2812 program, outputting on Pin(6).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(6))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
pixel_array = array.array("I", [0 for _ in range(NUM_LEDS)])

def updatePixel(brightness=1):
    dimmer_array = array.array("I", [0 for _ in range(NUM_LEDS)])
    for ii, cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness)
        g = int(((cc >> 16) & 0xFF) * brightness)
        b = int((cc & 0xFF) * brightness)
        dimmer_array[ii] = (g << 16) + (r << 8) + b
    sm.put(dimmer_array, 8)

def set_led_color(color):
    for ii in range(len(pixel_array)):
        pixel_array[ii] = (color[1] << 16) + (color[0] << 8) + color[2]

# Define LED Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Blink LEDs
def blink_leds(color, duration):
    set_led_color(color)
    updatePixel(1)
    time.sleep(duration)
    set_led_color((0, 0, 0))  # Turn off LEDs
    updatePixel(1)
    time.sleep(duration)

while True:
    blink_leds(RED, 0.5)    # Blink red
    blink_leds(GREEN, 0.5)  # Blink green
    blink_leds(BLUE, 0.5)   # Blink blue
    blink_leds(WHITE, 0.5)  # Blink white
