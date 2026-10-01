Example of use of a DHT11 sensor with the Raspberry Pi Pico.

This script uses the dht library, which is included in MicroPython.\
you can verify that by running the following command in the REPL (run it in the Terminal/Shell):
```
help('modules')
```
In case a library is not present, you may use the version in the lib folder.\
See comments in dht11.py how to do that.

**main.py**\
Combined version that displays the values on an SSD1306 OLED screen.
Needs the driver ssd1306.py (do not forget to upload all files in the project to the Pico).

**dht11.py**\
Basic script to test the DHT11 sensor and print the values.
