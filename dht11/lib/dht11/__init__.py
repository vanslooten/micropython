# driver for DHT11 temperature and humidity sensor, based on
# https://github.com/szazo/DHT11_Python/blob/master/dht11/__init__.py
# but adapted for Raspberry Pi Pico

import time
import machine

class DHT11Result:
    'DHT11 sensor result returned by DHT11.read() method'

    ERR_NO_ERROR = 0
    ERR_MISSING_DATA = 1
    ERR_CRC = 2

    def __init__(self, error_code, temperature, humidity):
        self.error_code = error_code
        self.temperature = temperature
        self.humidity = humidity

    def is_valid(self):
        return self.error_code == DHT11Result.ERR_NO_ERROR


class DHT11:
    'DHT11 sensor reader class for Raspberry Pi Pico'

    def __init__(self, pin):
        if isinstance(pin, machine.Pin):
            self.__pin = pin
        else:
            self.__pin = machine.Pin(pin, machine.Pin.OUT)

    def read(self):
        self.__pin.init(machine.Pin.OUT)
        self.__pin.value(1)
        time.sleep_ms(1)
        self.__pin.value(0)
        time.sleep_ms(20)
        self.__pin.value(1)
        time.sleep_us(40)
        self.__pin.init(machine.Pin.IN, machine.Pin.PULL_UP)

        response_low = machine.time_pulse_us(self.__pin, 0, 200)
        response_high = machine.time_pulse_us(self.__pin, 1, 200)
        if response_low < 0 or response_high < 0:
            return DHT11Result(DHT11Result.ERR_MISSING_DATA, 0, 0)

        the_bytes = []
        for _ in range(5):
            value = 0
            for _ in range(8):
                low_pulse = machine.time_pulse_us(self.__pin, 0, 200)
                high_pulse = machine.time_pulse_us(self.__pin, 1, 200)
                if low_pulse < 0 or high_pulse < 0:
                    return DHT11Result(DHT11Result.ERR_MISSING_DATA, 0, 0)
                value = (value << 1) | (high_pulse > 50)
            the_bytes.append(value)

        if the_bytes[4] != self.__calculate_checksum(the_bytes):
            return DHT11Result(DHT11Result.ERR_CRC, 0, 0)

        temperature = the_bytes[2] + float(the_bytes[3] & 0x7f) / 10
        if the_bytes[3] & 0x80:
            temperature = -temperature
        humidity = the_bytes[0] + float(the_bytes[1]) / 10
        return DHT11Result(DHT11Result.ERR_NO_ERROR, temperature, humidity)

    def __calculate_checksum(self, the_bytes):
        return (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 255