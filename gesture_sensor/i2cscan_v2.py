# https://www.reddit.com/r/raspberrypipico/comments/1layi2i/raspberry_pi_pico_2_troubleshooting_i2c/

from machine import Pin, I2C

I2C_ADDR = 0x39
REG_PART_ID = 0x92
expected_part_ids = { 0xAB, 0x9e, 0xA8, 0x9c}

led = Pin("LED", Pin.OUT)
led.toggle()
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
print("I2C Scan ...")
scan_results = i2c.scan()
print(scan_results)

for addr in scan_results:
    print(f"Device found at I2C address: {hex(addr)}")
    I2C_ADDR = addr

print(f"Using I2C address: {hex(I2C_ADDR)} to read Part ID...")

# Read 1 byte from the Part ID register
part_id_bytes = i2c.readfrom_mem(I2C_ADDR, REG_PART_ID, 1)
part_id = part_id_bytes[0]

if(part_id in expected_part_ids):
    print(f"APDS-9960 Detected (ID: {hex(part_id)})")
else:
    print(f"Unknown part detected (ID: {hex(part_id)})")
