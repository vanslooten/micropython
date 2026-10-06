# rfid driver from https://github.com/wendlers/micropython-mfrc522
# ssd1306 oled driver from https://github.com/stlehmann/micropython-ssd1306

from mfrc522 import MFRC522
import time

# define the SPI pins for the RFID reader:
SCK_PIN = 18
MOSI_PIN = 19
MISO_PIN = 16
RST_PIN = 22
CS_PIN = 17

DEBOUNCE_DELAY = 5000  # Cooldown period in milliseconds to ignore duplicate card taps
last_uid = None        # Stores the the card most recently scanned
last_scan_time = 0     # Stores the system timestamp when the card was last scanned

rdr = MFRC522(SCK_PIN, MOSI_PIN, MISO_PIN, RST_PIN, CS_PIN) # Initializes the MFRC522 RFID reader interface

print("\nPlace card at reader\n")

try:
    while True: # Continuous loop running the scanner 
        
        (stat, tag_type) = rdr.request(rdr.REQIDL) # Checks for the presence of a card in the RFID reader's range

        if stat == rdr.OK: # Checks if a card responded to the request
            (stat, raw_uid) = rdr.SelectTagSN() # Reads the UID bytes from the card
            if stat == rdr.OK: # Checks if the UID selection was successful
                
                card_id = "".join(["%02X" % i for i in raw_uid[:4]]) # Converts the raw data into a readable hexadecimal string 
                current_time = time.ticks_ms() # Captures the current system time to compare against the debounce 

               
                if card_id == last_uid and time.ticks_diff(current_time, last_scan_time) < DEBOUNCE_DELAY: # Debounce Check
                    pass # Skips execution to prevent double-logging 
                else:
                    print(f"Card detected! UID: {card_id}") # Prints detected card UID

                    # Updates tracking variables so the debounce filter can monitor subsequent scans properly
                    last_uid = card_id
                    last_scan_time = current_time

                    time.sleep_ms(5000)
                    print("System Ready")
                    print("Waiting for tag...")

        time.sleep_ms(100)

except KeyboardInterrupt:
    print("Program stopped.")
