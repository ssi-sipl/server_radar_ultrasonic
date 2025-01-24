import requests
import json
import RPi.GPIO as GPIO
import time
import serial
import threading
import re
import logging
import configparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('sensor_config.ini')

# GPIO Configuration
GPIO.setmode(GPIO.BOARD)

trig_pin = int(config['UltrasonicSensor']['TrigPin'])
echo_pin = int(config['UltrasonicSensor']['EchoPin'])
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Radar sensor serial communication setup
port = config['RadarSensor']['Port']
baudrate = int(config['RadarSensor']['BaudRate'])

# Server configuration
server_url = config['Server']['Url']

# Valid range for triggering HTTP requests
VALID_RANGE_MIN = 120
VALID_RANGE_MAX = 780

def measure_distance_ultrasonic():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(trig_pin, GPIO.LOW)

    pulse_start = time.time()
    timeout_start = pulse_start

    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.02:
            return -1

    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > 0.02:
            return -1

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    if distance < 2 or distance > 800:
        return -1

    return distance

def read_from_port(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore').strip()
                numeric_values = re.findall(r'\d+(\.\d+)?', data)

                if numeric_values:
                    for value in numeric_values:
                        try:
                            distance = float(value)
                            logging.info(f"Radar Sensor Distance: {distance} cm")
                            check_and_send_request(distance)
                        except ValueError:
                            logging.warning(f"Invalid radar data: {value}")
                else:
                    logging.warning(f"Discarded non-numeric data: {data}")
    except Exception as e:
        logging.error(f"Error reading from serial port: {e}")

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
        response = send_http_command(server_url, method='POST', data=json.dumps(data), headers=headers)
        if response:
            logging.info(f"HTTP Response: {response}")
        else:
            logging.error("Failed to send HTTP request.")
    else:
        logging.info(f"Distance {distance:.2f} cm is out of the valid range ({VALID_RANGE_MIN} - {VALID_RANGE_MAX} cm).")

def main():
    try:
        with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
            logging.info(f"Connected to {port} at {baudrate} baud")

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
