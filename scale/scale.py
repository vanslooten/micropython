# Uses PIO library from https://github.com/robert-hh/hx711/
# Example for micropython.org device, RP2040 PIO mode
# Connections:
# Pin # | HX711
# ------|-----------
# 14    | data_pin (DT)
# 15    | clock_pin (SCK)

from hx711_pio import HX711
from machine import Pin
import time

pin_OUT = Pin(14, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(15, Pin.OUT)

scale = HX711(pin_SCK, pin_OUT, state_machine=0)

scale.set_gain(128)

# Tare: read current zero point
print("Taring...")
tare = 0
for _ in range(20):
    tare += scale.read()
    time.sleep_ms(50)
tare //= 20 # divide the total by 20 (using floor division '//': rounds result down to the nearest whole number)
print("Tare value:", tare)

# Replace with your calibrated scale factor
SCALE_FACTOR = 429.16 #420.0

print("HX711 Load Cell Demo")
print("Place an item on the scale.")

while True:
    raw = scale.read()
    weight_g = (raw - tare) / SCALE_FACTOR
    print("Weight: {:.2f} g".format(weight_g), "Raw:", raw)
    time.sleep_ms(500)

