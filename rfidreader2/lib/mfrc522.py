from machine import Pin, SPI

class MFRC522:
    DEBUG = False
    OK = 0
    NOTAGERR = 1
    ERR = 2
    REQIDL = 0x26
    REQALL = 0x52
    AUTHENT1A = 0x60
    AUTHENT1B = 0x61
    PICC_ANTICOLL1 = 0x93
    PICC_ANTICOLL2 = 0x95
    PICC_ANTICOLL3 = 0x97

    def __init__(self, sck, mosi, miso, rst, cs, baudrate=1000000, spi_id=0):
        self.sck = Pin(sck, Pin.OUT)
        self.mosi = Pin(mosi, Pin.OUT)
        self.miso = Pin(miso)
        self.rst = Pin(rst, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        
        self.rst.value(0)
        self.spi = SPI(spi_id, baudrate=baudrate, polarity=0, phase=0, sck=self.sck, mosi=self.mosi, miso=self.miso)
        self.rst.value(1)
        self.init()

    def wreg(self, reg, val):
        self.cs.value(0)
        self.spi.write(bytes([reg << 1, val]))
        self.cs.value(1)

    def rreg(self, reg):
        self.cs.value(0)
        self.spi.write(bytes([((reg << 1) & 0x7E) | 0x80]))
        val = self.spi.read(1)
        self.cs.value(1)
        return val[0]

    def sbits(self, reg, mask):
        tmp = self.rreg(reg)
        self.wreg(reg, tmp | mask)

    def cbits(self, reg, mask):
        tmp = self.rreg(reg)
        self.wreg(reg, tmp & (~mask))

    def antenna_on(self):
        if(~(self.rreg(0x14) & 0x03)):
            self.sbits(0x14, 0x03)

    def init(self):
        self.wreg(0x01, 0x0f)
        self.wreg(0x2a, 0x8d)
        self.wreg(0x2b, 0x3e)
        self.wreg(0x2d, 30)
        self.wreg(0x2c, 0)
        self.wreg(0x15, 0x40)
        self.wreg(0x11, 0x3d)
        self.antenna_on()

    def tocard(self, command, send_data):
        back_data = []
        back_len = 0
        status = self.ERR
        irq_en = 0x00
        wait_irq = 0x00
        if command == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif command == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30
        self.wreg(0x02, irq_en | 0x80)
        self.cbits(0x04, 0x80)
        self.sbits(0x0A, 0x80)
        self.wreg(0x01, 0x00)
        for i in range(len(send_data)):
            self.wreg(0x09, send_data[i])
        self.wreg(0x01, command)
        if command == 0x0C:
            self.sbits(0x0D, 0x80)
        i = 2000
        while True:
            n = self.rreg(0x04)
            i -= 1
            if not ((i != 0) and not (n & 0x01) and not (n & wait_irq)):
                break
        self.cbits(0x0D, 0x80)
        if i != 0:
            if not (self.rreg(0x06) & 0x1B):
                status = self.OK
                if n & irq_en & 0x01:
                    status = self.NOTAGERR
                if command == 0x0C:
                    n = self.rreg(0x0A)
                    lbits = self.rreg(0x0C) & 0x07
                    if lbits:
                        back_len = (n - 1) * 8 + lbits
                    else:
                        back_len = n * 8
                    if n == 0:
                        n = 1
                    if n > 16:
                        n = 16
                    for i in range(n):
                        back_data.append(self.rreg(0x09))
            else:
                status = self.ERR
        return (status, back_data, back_len)

    def request(self, req_mode):
        self.wreg(0x0D, 0x07)
        (status, back_data, back_len) = self.tocard(0x0C, [req_mode])
        if (status != self.OK) or (back_len != 16):
            status = self.ERR
        return (status, back_len)

    def anticoll(self):
        back_data = []
        serial_number_check = 0
        self.wreg(0x0D, 0x00)
        ser_nr = [self.PICC_ANTICOLL1, 0x20]
        (status, back_data, back_len) = self.tocard(0x0C, ser_nr)
        if status == self.OK:
            if len(back_data) == 5:
                for i in range(4):
                    serial_number_check = serial_number_check ^ back_data[i]
                if serial_number_check != back_data[4]:
                    status = self.ERR
            else:
                status = self.ERR
        return (status, back_data)

    def SelectTagSN(self):
        return self.anticoll()