# connect to iotroam network and sync time
#
# this example is used in this tutorial:
# https://home.et.utwente.nl/slootenvanf/2025/09/03/connect-to-wi-fi-raspberry-pi-pico-w/
#
# sync time code based on:
# https://www.picademie.nl/index.php/2025/02/22/de-juiste-tijd-met-ntp-pico-w/

import time
import ntptime
import machine
import network
import requests
import random
import ubinascii


# Wi-Fi credentials (change these to reflect your Wifi credentials!)
# For the UT iotroam network, use 'iotroam' for the ssid, for the password, see the tutorial
ssid = 'iotroam'
password = '***********'

# base URL
base_url = 'https://home.et.utwente.nl/val/check'

wlan = network.WLAN(network.STA_IF)

# get mac address:
mac = ubinascii.hexlify(wlan.config('mac'),':').decode().replace(":", "")
print("Mac:", mac)

# construct the request url:
request_url = base_url + '-' + ssid + '-' + mac + '/'

print("Connecting to", ssid, "...")

# Connect to network
wlan.active(True)

# Connect to your network
wlan.connect(ssid, password)

# Wait for Wi-Fi connection:
connection_timeout = 10 # we will do 10 attempts to connect, with a 1 sec. interval
while connection_timeout > 0:
    status = wlan.status()
    # if status >= 3, connection was made:
    if status >= 3:
        break # break from the loop
    connection_timeout -= 1
    print("Waiting for Wi-Fi connection... (", status, ")")
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to connect to network')
    exit()
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

# connect to time server and setup the RTC

rtc = machine.RTC()

rtc.datetime((2000, 1, 1, 0, 0, 0, 00, 0))
print(time.localtime())

ntptime.settime()
time.sleep(2)

dstadjust = 2 # adjust for summer time (DST) if needed, eg. by using the value 1 for summer time, and 0 for winter time.
    # This is a simple example, in practice you would need to check the date and adjust accordingly.

while True:
    print ("Year   = ", time.localtime()[0])
    print ("Month  = ", time.localtime()[1])
    print ("Day    = ", time.localtime()[2])
    hour = time.localtime()[3]
    hour = hour + dstadjust
    print ("Hour   = ", hour)
    print ("Minute = ", time.localtime()[4])
    print ("===============")
    time.sleep(10)