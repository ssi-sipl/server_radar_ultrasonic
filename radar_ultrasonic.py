import requests
import json
import RPi.GPIO as GPIO
import time
import serial
import sys
import threading
import re

# Set the GPIO mode to BOARD (physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# Define the physical pin numbers for ultrasonic sensor
trig_pin = 12  # Physical pin 12 (GPIO 18)
echo_pin = 18  # Physical pin 18 (GPIO 24)

# Set the GPIO directions for ultrasonic sensor
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Radar sensor serial communication setup
port = "/dev/ttyS0"
baudrate = 115200

# Function to measure distance using ultrasonic sensor
def measure_distance_ultrasonic():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(trig_pin, GPIO.LOW)

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

# Function to handle reading from the radar sensor's serial port


def read_from_port(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # Read all data available in the buffer
                decoded_data = data.decode('utf-8', errors='ignore').strip()  # Decode and strip extra spacesnewlines
                
                # Extract numeric values from the string using regular expression
                numeric_values = re.findall(r'\d+(\.\d+)?', decoded_data)  # Find all numbers (integers or floats)
                
                if numeric_values:
                    for value in numeric_values:
                        sys.stdout.write(value + "\n")  # Print the extracted numeric value
                        sys.stdout.flush()
                else:
                    print(f"Discarded non-numeric data: {decoded_data}")
    except Exception as e:
        print(f"Error while reading from serial port: {e}")


# Function to send HTTP requests based on sensor data
def send_http_command(url, method='POST', params=None, data=None, headers=None):
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to check if distance is within the valid range and send HTTP request
def check_and_send_request(distance):
    if 120 <= distance <= 780:
        #url = 'http://192.168.1.5:3300/analyticEvent' url for ai box
        url = 'http://192.168.1.2:80'  # Local server URL
        data = {
            "cameraId": "RD001",
            "eventTime": int(time.time()),
            "timestampStr": time.strftime("%Y-%m-%d %H:%M:%S"),
            "eventType": "SensorBox",
            "distance": distance  # Send the measured distance
        }
        headers = {'Content-Type': 'application/json'}
        response = send_http_command(url, method='POST', data=json.dumps(data), headers=headers)
        if response:
            print("HTTP Response:", response)
        else:
            print("Failed to send HTTP request.")
    else:
        print(f"Distance {distance:.2f} cm is out of the valid range (120 - 780 cm).")

# Main function to manage both sensors
def main():
    try:
        # Initialize the radar sensor serial port
        with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud")

            # Start a thread to read data from the radar sensor
            read_thread = threading.Thread(target=read_from_port, args=(ser,))
            read_thread.daemon = True  # Ensure the thread exits when the main program exits
            read_thread.start()

            while True:
                # Read distance from the radar sensor
                uart_data = ser.readline().decode('utf-8').strip()
                if uart_data:
                    try:
                        distance = float(uart_data)  # Convert the data to a float (distance)
                        print(f"Radar Sensor Distance: {distance} cm")
                        check_and_send_request(distance)  # Check and send HTTP request
                    except ValueError:
                        print("Invalid data received from radar sensor.")
                else:
                    print("No data from radar sensor, using ultrasonic sensor.")

                # Read distance from the ultrasonic sensor if radar data is not available
                distance_ultrasonic = measure_distance_ultrasonic()
                if distance_ultrasonic != -1:
                    print(f"Ultrasonic Sensor Distance: {distance_ultrasonic:.2f} cm")
                    check_and_send_request(distance_ultrasonic)  # Check and send HTTP request

                time.sleep(3)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        GPIO.cleanup()  # Clean up GPIO pins
        print("GPIO cleaned up. Exiting program.")

if __name__ == "__main__":
    main()
