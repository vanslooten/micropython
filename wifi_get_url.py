# connect to iotroam network and get an url
# in this example we use an online service to read and write variables or data in a simple way
# more info: https://home.et.utwente.nl/val/?help

from time import sleep
import network
import requests
import random
import ubinascii

# Wi-Fi credentials (change these to reflect your Wifi credentials!)
# For the UT iotroam network, use 'iotroam' for the ssid, get the password from Canvas
ssid = 'iotroam'
password = '*************'

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
    sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to connect to network')
    exit()
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

# proceed with requesting a webpage

while True:
  try:
    # generate a value to store, as an example a random number between 0-40:
    value = random.randint(0,40)
    # make request url to store the value online:
    url = request_url + str(value)
    print('Sending request: ', url)
    response = requests.get(url)
    # Get response code
    response_code = response.status_code
    # Get response content
    response_content = response.content

    # Print results
    print('Response code: ', response_code)
    print('Response content:', response_content)
  except OSError as e:
    print('Failed send values to website (check Wifi connection?).')
  sleep(60)
