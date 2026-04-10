# Example of how to get MAC address of Raspberry Pi Pico W
# References:
# https://forums.raspberrypi.com/viewtopic.php?t=346400
#
# this example is used in this tutorial:
# https://home.et.utwente.nl/slootenvanf/2025/09/03/connect-to-wi-fi-raspberry-pi-pico-w/

import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = ubinascii.hexlify(wlan.config('mac'),':').decode().replace(":", "")
print(mac)
