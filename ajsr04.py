import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BOARD (physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# Define the physical pin numbers
trig_pin = 12  # Physical pin 12 (GPIO 18)
echo_pin = 18  # Physical pin 18 (GPIO 24)

# Set the GPIO directions
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Function to measure the distance
def measure_distance():
    # Trigger the sensor
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(trig_pin, GPIO.LOW)

    # Measure the echo
    pulse_start = time.time()
    timeout_start = pulse_start  # To handle timeout

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.02:  # Timeout after 20ms
            return -1  # No object detected

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > 0.02:  # Timeout after 20ms
            return -1  # No object detected

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 340 m/s

    # Filter out unrealistic distances
    if distance < 2 or distance > 800:  # HC-SR04 typical range
        return -1  # Out of range

    return distance

try:
    while True:
        distance = measure_distance()
        if distance == -1:
            print("No object detected or out of range")
        else:
            print(f"Distance: {distance:.2f} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO cleaned up. Exiting program.")
