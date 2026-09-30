# Complete project details at
#  https://RandomNerdTutorials.com/raspberry-pi-pico-dht11-dht22-micropython/
# Install CircuitPython:
# https://randomnerdtutorials.com/getting-started-raspberry-pi-pico-w/#install-thonny-ide
# Set sensor (line 10-11), check/alter pin
#
# This script needs the dht library, which is included in MicroPython.
# you can verify that by running the following command in the REPL:
# help('modules')
#
# related:
# Wifi, webserver:
# https://circuitdigest.com/microcontroller-projects/temperature-and-humidity-monitoring-webserver-with-raspberry-pi-pico-w-and-dht11-sensor
# bluetooth:
# https://www.makeuseof.com/raspberry-pi-pico-w-read-sensor-using-bluetooth/
# https://electrocredible.com/raspberry-pi-pico-w-bluetooth-ble-micropython/

from machine import Pin
from time import sleep
import dht 

# Intialize DHT11 sensor, change pin if needed, here we use GP16
sensor = dht.DHT11(Pin(16))

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0 # convert to Fahrenheit
    print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
  except OSError as e:
    print('Failed to read sensor.')
