from machine import Pin

# 1. Define the ISR (handler function)
# The handler function takes the Pin object as an argument.
def button_handler(pin):
    # This is the flag that the main loop will check
    global button_pressed
    button_pressed = True

# Initialize a Pin object (e.g., connected to a button)
button = Pin(16, Pin.IN, Pin.PULL_UP)
button_pressed = False

# 2. Attach the ISR to the pin's interrupt
# trigger=Pin.IRQ_FALLING means execute the handler 
# when the pin voltage goes from HIGH to LOW (typical for a button press)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 3. The Main Program Loop
while True:
    if button_pressed:
        print("Button was pressed! Handling the event...")
        # Clear the flag so it can be set again
        button_pressed = False
        # Do the necessary non-interrupt work here
