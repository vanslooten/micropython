Code created from tutorial at\
https://www.instructables.com/How-to-Use-MPU6050-With-Raspberry-Pi-Pico-or-Pico-/

But code uses different pins! see warning below. so wire the sensor to GP10 and GP11.

This project needs two library files:\
https://github.com/shillehbean/youtube-channel/blob/main/vector3d.py
https://github.com/shillehbean/youtube-channel/blob/main/imu.py
which you should save in the 'lib' folder.

Do not forget to upload the entire project to the Pico before running any of the scripts.

WARNING: The sensor wiring must match the I2C definition in the code. This project uses\
I2C(1) with SDA connected to Pico GP10 and SCL connected to Pico GP11. Connect the\
sensor VCC to 3V3 and GND to GND. If you use different pins, update the I2C bus and\
pin definitions in the Python scripts as well.
