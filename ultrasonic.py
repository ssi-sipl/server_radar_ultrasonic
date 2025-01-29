import requests
import json
import RPi.GPIO as GPIO
import time
import logging

# Configure logging
logging.basicConfig(
    filename='ultrasonic.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# GPIO Configuration
GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 23  # Hardcoded GPIO pin for trigger
ECHO_PIN = 24  # Hardcoded GPIO pin for echo
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Server configuration
SERVER_URL = 'http://192.168.1.2:80'  # URL for testing on local server

# Valid range for triggering HTTP requests
VALID_RANGE_MIN = 120
VALID_RANGE_MAX = 780

# Function to send HTTP command
def send_http_command(url, method='POST', params=None, data=None, headers=None):
    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None

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
    distance = pulse_duration * 16200  # Convert to cm

    if distance < 5 or distance > 800:
        return -1
    
    logging.info(f"Measured Distance: {distance:.2f} cm")
    return distance

def check_and_send_request(distance):
    logging.info(f"Checking distance: {distance:.2f} cm")
    if VALID_RANGE_MIN <= distance <= VALID_RANGE_MAX:
        data = {
            "cameraId": "RD001",
            "eventTime": int(time.time()),
            "timestampStr": time.strftime("%Y-%m-%d %H:%M:%S"),
            "eventType": "Sensor_Event",
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
