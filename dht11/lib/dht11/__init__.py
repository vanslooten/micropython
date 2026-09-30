# driver for DHT11 temperature and humidity sensor, based on
# https://github.com/szazo/DHT11_Python/blob/master/dht11/__init__.py
# but adapted for Raspberry Pi Pico

import time
import machine

class DHT11:
    'DHT11 sensor reader class for Raspberry Pi Pico'

    def __init__(self, pin):
        if isinstance(pin, machine.Pin):
            self.__pin = pin
        else:
            self.__pin = machine.Pin(pin, machine.Pin.OUT)
        self.__temperature = 0
        self.__humidity = 0

    def measure(self):
        try:
            self.__measure_once()
        except OSError:
            time.sleep_ms(1000)
            self.__measure_once()

    def __measure_once(self):
        self.__pin.init(machine.Pin.OPEN_DRAIN)
        self.__pin.value(1)
        time.sleep_ms(250)
        self.__pin.value(0)
        time.sleep_ms(18)
        self.__pin.value(1)
        time.sleep_us(10)

        the_bytes = bytearray(5)
        irq_state = machine.disable_irq()
        try:
            response_low = machine.time_pulse_us(self.__pin, 0, 100)
            if response_low < 0:
                raise OSError('DHT11: missing low response (code %d)' % response_low)
            response_high = machine.time_pulse_us(self.__pin, 1, 150)
            if response_high < 0:
                raise OSError('DHT11: missing high response (code %d)' % response_high)

            for byte_index in range(5):
                value = 0
                for bit_index in range(8):
                    high_pulse = machine.time_pulse_us(self.__pin, 1, 100)
                    if high_pulse < 0:
                        raise OSError('DHT11: high pulse failed at byte %d bit %d (code %d)' % (byte_index, bit_index, high_pulse))
                    value = (value << 1) | (high_pulse > 48)
                the_bytes[byte_index] = value
        finally:
            machine.enable_irq(irq_state)

        if the_bytes[4] != self.__calculate_checksum(the_bytes):
            raise OSError('DHT11: checksum error')

        temperature = the_bytes[2] + float(the_bytes[3] & 0x7f) / 10
        if the_bytes[3] & 0x80:
            temperature = -temperature
        humidity = the_bytes[0] + float(the_bytes[1]) / 10
        self.__temperature = temperature
        self.__humidity = humidity

    def temperature(self):
        return self.__temperature

    def humidity(self):
        return self.__humidity

    def __calculate_checksum(self, the_bytes):
        return (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 255