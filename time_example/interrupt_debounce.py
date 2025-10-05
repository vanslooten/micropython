# Interrupts in MicroPython let your microcontroller instantly pause its main job to handle sudden events,
# like a button being pressed.
# The special, brief code that runs when an event happens is called an Interrupt Service Routine (ISR) or handler.
# ISRs must be very fast and should mainly just set a flag (a variable) to tell the main program what happened.
# The main program then checks this flag and performs the slower, complex work safely outside the interrupt.
# This system ensures your program is responsive without wasting time constantly checking for events.
#
# A simple interrupt example often results in a single button press being registered multiple times due to contact bounce
# (the physical contacts briefly opening and closing).
# To fix this, we implement software debouncing by using the system timer to ignore subsequent interrupts for a short period
# after the first one is detected.
# 
# Here time.ticks_diff() is used to compute the difference between two calls of the button handler() function and only
# allows the action to be taken if DEBOUNCE_TIME_MS has passed since the last registered interrupt.

from machine import Pin
import time

# --- Configuration ---
BUTTON_PIN = 16  # GPIO pin number where the button is connected
DEBOUNCE_TIME_MS = 200  # Ignore presses for 200 milliseconds

# --- Global State Variables ---
button_pressed = False
last_interrupt_time = 0

# Initialize a Pin object with an internal pull-up resistor
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# --- Interrupt Service Routine (ISR) ---
def button_handler(pin):
    # We must use 'global' to modify these variables from within the ISR
    global button_pressed
    global last_interrupt_time
    
    # 1. Get the current time
    current_time = time.ticks_ms()
    
    # 2. Check for debouncing
    # If the time since the last registered interrupt is greater than DEBOUNCE_TIME_MS, proceed.
    if time.ticks_diff(current_time, last_interrupt_time) > DEBOUNCE_TIME_MS:
        # Action: Set the flag and update the last registered time
        button_pressed = True
        last_interrupt_time = current_time
        
        # NOTE: Do NOT print() or perform heavy work here!

# --- Setup the Interrupt ---
# Trigger on the falling edge (pin goes from HIGH to LOW when button is pressed)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# --- Main Program Loop ---
print("System ready. Press the button.")
while True:
    # Safely handle the event outside the ISR
    if button_pressed:
        print("Button event detected!")
        
        # Reset the flag immediately
        button_pressed = False
        
        # Perform the actual task (e.g., toggle an LED, send a message)
        time.sleep(0.1) # Simulate some work
    
    # The main loop continues running very fast, checking the flag
    time.sleep_ms(1)