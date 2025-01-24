import requests
import json
import RPi.GPIO as GPIO
import time
import serial
import threading
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO Configuration
GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 23  # Hardcoded GPIO pin for trigger
ECHO_PIN = 24  # Hardcoded GPIO pin for echo
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Radar sensor serial communication setup
RADAR_PORT = '/dev/ttyS0'  # Hardcoded serial port for radar sensor
RADAR_BAUDRATE = 115200        # Hardcoded baud rate for radar sensor

# Server configuration
SERVER_URL = '192.168.0.79:80'  # Hardcoded server URL

# Valid range for triggering HTTP requests
VALID_RANGE_MIN = 120
VALID_RANGE_MAX = 780

def measure_distance_ultrasonic():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = time.time()
    timeout_start = pulse_start

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.02:  # Timeout for no echo received
            return -1

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > 0.02:  # Timeout for long echo
            return -1

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Convert to cm

    if distance < 2 or distance > 800:
        return -1

    return distance

def read_from_port(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # Read all data available in the buffer
                decoded_data = data.decode('utf-8', errors='ignore').strip()  # Decode and strip extra spaces/newlines

                # Extract numeric values from the string using regular expression
                numeric_values = re.findall(r'\d+(\.\d+)?', decoded_data)  # Find all numbers (integers or floats)

                if numeric_values:
                    for value in numeric_values:
                        logging.info(f"Radar Sensor Value: {value} cm")  # Log the extracted radar sensor value
                        try:
                            distance_radar = float(value)  # Convert value to float
                            check_and_send_request(distance_radar)  # Call the function to check and send request
                        except ValueError:
                            logging.error("Error: Invalid radar sensor data received.")
                else:
                    logging.info(f"Discarded non-numeric data: {decoded_data}")

    except Exception as e:
        logging.error(f"Error while reading from radar sensor: {e}")

def send_http_command(url, method='POST', params=None, data=None, headers=None):
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        return None

def check_and_send_request(distance):
    if VALID_RANGE_MIN <= distance <= VALID_RANGE_MAX:
        data = {
            "cameraId": "RD001",
            "eventTime": int(time.time()),
            "timestampStr": time.strftime("%Y-%m-%d %H:%M:%S"),
            "eventType": "SensorBox",
            "EventTag": distance
        }
        headers = {'Content-Type': 'application/json'}
        response = send_http_command(SERVER_URL, method='POST', data=json.dumps(data), headers=headers)
        if response:
            logging.info(f"HTTP Response: {response}")
        else:
            logging.error("Failed to send HTTP request.")
    else:
        logging.info(f"Distance {distance:.2f} cm is out of the valid range ({VALID_RANGE_MIN} - {VALID_RANGE_MAX} cm).")

def main():
    try:
        with serial.Serial(RADAR_PORT, baudrate=RADAR_BAUDRATE, timeout=1) as ser:
            logging.info(f"Connected to {RADAR_PORT} at {RADAR_BAUDRATE} baud")

            # Start reading the radar sensor data in a separate thread
            read_thread = threading.Thread(target=read_from_port, args=(ser,))
            read_thread.daemon = True
            read_thread.start()

            while True:
                # Ultrasonic Sensor
                distance_ultrasonic = measure_distance_ultrasonic()
                if distance_ultrasonic != -1:
                    logging.info(f"Ultrasonic Sensor Distance: {distance_ultrasonic:.2f} cm")
                    check_and_send_request(distance_ultrasonic)

                time.sleep(3)

    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
    finally:
        GPIO.cleanup()
        logging.info("GPIO cleaned up. Exiting program.")

if __name__ == "__main__":
    main()
