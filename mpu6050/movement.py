from imu import MPU6050
from time import sleep
from machine import Pin, I2C

# Shows Pi is on by turning on LED when plugged in:
LED = Pin("LED", Pin.OUT)
LED.on()

i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
imu = MPU6050(i2c)

# loop forever:
while True:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    temp=round(imu.temperature,2)
    #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",temp,"        ",end="\r")

    # Adjusted thresholds based on observed data
    THRESHOLD_AX = 0.8
    THRESHOLD_AY = 0.6
    movement = None
    # Forward: ax > 0.8 and ay near 0
    if ax > THRESHOLD_AX and abs(ay) < 0.2:
        movement = "forward"
    # Backward: ax < -0.6 and ay near 0
    elif ax < -0.6 and abs(ay) < 0.2:
        movement = "backward"
    # Right: ay > 0.6
    elif ay > THRESHOLD_AY:
        movement = "right"
    # Left: ay < -0.6
    elif ay < -THRESHOLD_AY:
        movement = "left"
    #print(f"ax: {ax} ay: {ay} az: {az} gx: {gx} gy: {gy} gz: {gz} temp: {temp}")
    if movement:
        print(f"Movement detected: {movement}")
    sleep(0.2)
