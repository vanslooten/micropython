# Based on the Blink example, an example of a heart rate pulse effect using WS2812 LEDs
# In this example, the heart rate is simulated and the LEDs pulse in a color based on the heart rate value.
# The heart_rate variable (line 63) in this example is set to a default value, but in a real application, it would be updated based on readings from a heart rate sensor.

import array
from time import sleep, time, ticks_ms
from machine import Pin, SoftI2C
from utime import ticks_diff, ticks_ms
from rp2 import StateMachine, asm_pio, PIO

NUM_LEDS = 6
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (10, 10, 10) # dimmed version of 255,255,255

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
         autopull=True, pull_thresh=24)
def ws2812():
    # https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]

def update_pixels(sm: StateMachine, pixel_array: array.array, color, brightness: float):
    # https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/
    dimmer_array = array.array("I", [0 for _ in range(NUM_LEDS)])
    for ii, cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness)
        g = int(((cc >> 16) & 0xFF) * brightness)
        b = int((cc & 0xFF) * brightness)
        dimmer_array[ii] = (g << 16) + (r << 8) + b
    sm.put(dimmer_array, 8)

    for ii in range(len(pixel_array)):
        pixel_array[ii] = (color[1] << 16) + (color[0] << 8) + color[2]


def get_heart_rate_color(heart_rate: int):
    if heart_rate >= 100:
        return RED
    if heart_rate <= 60:
        return BLUE
    return GREEN


def main():
    # Create the StateMachine with the ws2812 program, outputting on Pin(6).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(6))
    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    pixel_array = array.array("I", [0 for _ in range(NUM_LEDS)])

    duration = 0.01 # variable duration for sleep between updates, in seconds
    heart_rate = 90 # default heart rate value, in beats per minute

    while True:
        # Calculate the timing for the pulse effect based on the heart rate:
        beat_period_ms = max(100, int(60000 / heart_rate))
        pulse_ms = max(30, int(beat_period_ms * 0.12))
        fade_ms = max(60, int(beat_period_ms * 0.30))

        colour = get_heart_rate_color(heart_rate)
        elapsed_ms = ticks_ms() % beat_period_ms

        if elapsed_ms < pulse_ms:
            brightness = 0.15 + 0.85 * (elapsed_ms / pulse_ms)
        elif elapsed_ms < pulse_ms + fade_ms:
            fade_progress = (elapsed_ms - pulse_ms) / fade_ms
            brightness = 1.0 - (0.85 * fade_progress)
        else:
            brightness = 0.15

        update_pixels(sm, pixel_array, colour, brightness)
        sleep(duration)


if __name__ == "__main__":
    main()
