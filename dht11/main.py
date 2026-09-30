# DHT11/22 tutorial:
# https://RandomNerdTutorials.com/raspberry-pi-pico-dht11-dht22-micropython/
#
# get the ssd1306.py file from:
# https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306
#
# Using the display and basics of micropython on the Pico:
# https://dronebotworkshop.com/pi-pico/
#
# Bluetooth:
# https://www.makeuseof.com/raspberry-pi-pico-w-read-sensor-using-bluetooth/
# https://electrocredible.com/raspberry-pi-pico-w-bluetooth-ble-micropython/
#
# related:
# Wifi, webserver:
# https://circuitdigest.com/microcontroller-projects/temperature-and-humidity-monitoring-webserver-with-raspberry-pi-pico-w-and-dht11-sensor

import machine
from time import sleep
import dht
from ssd1306 import SSD1306_I2C

# for regular Pico:
#led_onboard = machine.Pin(25, machine.Pin.OUT)
# for Pico W/WH:
led_onboard = machine.Pin("LED", machine.Pin.OUT)

led_onboard.value(0)

#sensor = dht.DHT22(machine.Pin(16))
sensor = dht.DHT11(machine.Pin(16))

# I2C pin setting: use GP2 and GP3 on I2C1:
sda=machine.Pin(2)
scl=machine.Pin(3)

# use I2C bus 1:
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)

# Scan for devices
devices = i2c.scan()
if devices:
    print("I2C devices found:", [hex(dev) for dev in devices])
else:
    print("No I2C devices found")

oled = SSD1306_I2C(128, 64, i2c)

while True:
  try:
    #sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    #print('Temperature: %3.1f C' %temp)
    #print('Temperature: %3.1f F' %temp_f)
    #print('Humidity: %3.1f %%' %hum)
    oled.fill(0)
    oled.text('Temperature:', 0, 0)
    oled.text('Temperature F:', 0, 20)
    oled.text('Humidity:', 0, 40)
    oled.text('%3.1f C' %temp, 0, 10)
    oled.text('%3.1f F' %temp_f, 0, 30)
    oled.text('%3.1f %%' %hum, 0, 50)
    oled.show()

  except OSError as e:
    print('Failed to read sensor.')

  # Blink led to show updating:
  led_onboard.value(1)
  sleep(1)
  led_onboard.value(0)
  #sleep(10)
