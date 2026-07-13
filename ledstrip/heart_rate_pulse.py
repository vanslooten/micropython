# combination of heart_rate.py and pulse.py, with the heart rate monitor integrated
# see full tutorial at https://home.et.utwente.nl/slootenvanf/2025/07/24/heartrate-sensor-raspberry-pi-pico/

import array
from time import sleep, time, ticks_ms
from machine import Pin, SoftI2C
from utime import ticks_diff, ticks_ms
from rp2 import StateMachine, asm_pio, PIO

from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM # type: ignore

NUM_LEDS = 6
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (10, 10, 10) # dimmed version of 255,255,255

class HeartRateMonitor:
    """A simple heart rate monitor that uses a moving window to smooth the signal and find peaks."""

    def __init__(self, sample_rate=100, window_size=10, smoothing_window=5):
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.smoothing_window = smoothing_window
        self.samples = []
        self.timestamps = []
        self.filtered_samples = []

    def add_sample(self, sample):
        """Add a new sample to the monitor."""
        timestamp = ticks_ms()
        self.samples.append(sample)
        self.timestamps.append(timestamp)

        # Apply smoothing
        if len(self.samples) >= self.smoothing_window:
            smoothed_sample = (
                sum(self.samples[-self.smoothing_window :]) / self.smoothing_window
            )
            self.filtered_samples.append(smoothed_sample)
        else:
            self.filtered_samples.append(sample)

        # Maintain the size of samples and timestamps
        if len(self.samples) > self.window_size:
            self.samples.pop(0)
            self.timestamps.pop(0)
            self.filtered_samples.pop(0)

    def find_peaks(self):
        """Find peaks in the filtered samples."""
        peaks = []

        if len(self.filtered_samples) < 3:  # Need at least three samples to find a peak
            return peaks

        # Calculate dynamic threshold based on the min and max of the recent window of filtered samples
        recent_samples = self.filtered_samples[-self.window_size :]
        min_val = min(recent_samples)
        max_val = max(recent_samples)
        threshold = (
            min_val + (max_val - min_val) * 0.5
        )  # 50% between min and max as a threshold

        for i in range(1, len(self.filtered_samples) - 1):
            if (
                self.filtered_samples[i] > threshold
                and self.filtered_samples[i - 1] < self.filtered_samples[i]
                and self.filtered_samples[i] > self.filtered_samples[i + 1]
            ):
                peak_time = self.timestamps[i]
                peaks.append((peak_time, self.filtered_samples[i]))

        return peaks

    def calculate_heart_rate(self):
        """Calculate the heart rate in beats per minute (BPM)."""
        peaks = self.find_peaks()

        if len(peaks) < 2:
            return None  # Not enough peaks to calculate heart rate

        # Calculate the average interval between peaks in milliseconds
        intervals = []
        for i in range(1, len(peaks)):
            interval = ticks_diff(peaks[i][0], peaks[i - 1][0])
            intervals.append(interval)

        average_interval = sum(intervals) / len(intervals)

        # Convert intervals to heart rate in beats per minute (BPM)
        heart_rate = (
            60000 / average_interval
        )  # 60 seconds per minute * 1000 ms per second

        return heart_rate


@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
         autopull=True, pull_thresh=24)
def ws2812():
    # https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]

def update_pixels(sm: StateMachine, pixel_array: array.array, color, brightness: float):
    # https://theorycircuit.com/raspberry-pi-pico-projects/interfacing-ws2812b-neopixel-led-strip-with-raspberry-pi-pico/
    dimmer_array = array.array("I", [0 for _ in range(NUM_LEDS)])
    for ii, cc in enumerate(pixel_array):
        r = int(((cc >> 8) & 0xFF) * brightness)
        g = int(((cc >> 16) & 0xFF) * brightness)
        b = int((cc & 0xFF) * brightness)
        dimmer_array[ii] = (g << 16) + (r << 8) + b
    sm.put(dimmer_array, 8)

    for ii in range(len(pixel_array)):
        pixel_array[ii] = (color[1] << 16) + (color[0] << 8) + color[2]


def get_heart_rate_color(heart_rate: int):
    if heart_rate >= 100:
        return RED
    if heart_rate <= 60:
        return BLUE
    return GREEN



def main():
    i2c = SoftI2C(sda=Pin(10),  # Here, use your I2C SDA pin (GP.. number, so this is GP10)
                  scl=Pin(11),  # Here, use your I2C SCL pin (GP.. number)
                  freq=400000)  # Fast: 400kHz, slow: 100kHz

    print("Starting I2C scan...")
    i2c_devices = i2c.scan()
    print(i2c_devices)

    # Sensor instance
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required

    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c_devices:
        print("Sensor", sensor.i2c_address, " not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    # Load the default configuration
    print("Setting up sensor with default configuration.", "\n")
    sensor.setup_sensor()

    # Set the sample rate to 400: 400 samples/s are collected by the sensor
    sensor_sample_rate = 400
    sensor.set_sample_rate(sensor_sample_rate)

    # Set the number of samples to be averaged per each reading
    sensor_fifo_average = 8
    sensor.set_fifo_average(sensor_fifo_average)

    # Set LED brightness to a medium value
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    # Expected acquisition rate: 400 Hz / 8 = 50 Hz
    actual_acquisition_rate = int(sensor_sample_rate / sensor_fifo_average)

    sleep(1)

    print(
        "Starting data acquisition from RED & IR registers...",
        "press Ctrl+C to stop.",
        "\n",
    )
    sleep(1)

    # Initialize the heart rate monitor
    hr_monitor = HeartRateMonitor(
        # Select a sample rate that matches the sensor's acquisition rate
        sample_rate=actual_acquisition_rate,
        # Select a significant window size to calculate the heart rate (2-5 seconds)
        window_size=int(actual_acquisition_rate * 3),
    )

    # Setup to calculate the heart rate every 2 seconds
    hr_compute_interval = 2  # seconds
    ref_time = ticks_ms()  # Reference time

    runAve = 0 # running average of the heart rate
    readings = 0 # number of readings

    # Create the StateMachine with the ws2812 program, outputting on Pin(6).
    sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(6))
    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)

    # Display a pattern on the LEDs via an array of LED RGB values.
    pixel_array = array.array("I", [0 for _ in range(NUM_LEDS)])

    duration = 0.01 # variable duration for sleep between updates, in seconds
    heart_rate = 90 # default heart rate value, in beats per minute

    while True:
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()

        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()

            # Add the IR reading to the heart rate monitor
            # Note: based on the skin color, the red, IR or green LED can be used
            # to calculate the heart rate with more accuracy.
            hr_monitor.add_sample(ir_reading)

        # Periodically calculate the heart rate every `hr_compute_interval` seconds
        if ticks_diff(ticks_ms(), ref_time) / 1000 > hr_compute_interval:
            # Calculate the heart rate
            heart_rate = hr_monitor.calculate_heart_rate()
            if heart_rate is not None:
                # Print the heart rate in beats per minute (BPM), with the running avarage after 10 readings
                runAve =9/10*runAve +1/10*heart_rate
                readings += 1
                if (readings > 10):
                    print("Heart Rate: {:.0f} BPM (Av. {:.0f})".format(heart_rate, runAve))
                else:
                    print("Heart Rate: {:.0f} BPM".format(heart_rate))
            else:
                print("Not enough data to calculate heart rate")
            # Reset the reference time
            ref_time = ticks_ms()

        
        if heart_rate is None:
            # turn off the LEDs if no heart rate is detected
            update_pixels(sm, pixel_array, WHITE, 0)
            continue
        # Calculate the timing for the pulse effect based on the heart rate:
        beat_period_ms = max(100, int(60000 / heart_rate))
        pulse_ms = max(30, int(beat_period_ms * 0.12))
        fade_ms = max(60, int(beat_period_ms * 0.30))

        colour = get_heart_rate_color(heart_rate)
        elapsed_ms = ticks_ms() % beat_period_ms

        if elapsed_ms < pulse_ms:
            brightness = 0.15 + 0.85 * (elapsed_ms / pulse_ms)
        elif elapsed_ms < pulse_ms + fade_ms:
            fade_progress = (elapsed_ms - pulse_ms) / fade_ms
            brightness = 1.0 - (0.85 * fade_progress)
        else:
            brightness = 0.15

        update_pixels(sm, pixel_array, colour, brightness)

if __name__ == "__main__":
    main()
