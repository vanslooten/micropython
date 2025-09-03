# Example of how to get MAC address of Raspberry Pi Pico W
# References:
# https://forums.raspberrypi.com/viewtopic.php?t=346400

import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = ubinascii.hexlify(wlan.config('mac'),':').decode().replace(":", "")
print(mac)
