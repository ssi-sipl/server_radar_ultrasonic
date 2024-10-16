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
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 340 m/s
    return distance

try:
    while True:
        distance = measure_distance()
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
