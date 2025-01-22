import RPi.GPIO as GPIO
import time
import serial
import requests
import subprocess
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='radar_ultrasonic_uart_server_communication.log',
                    filemode='a')

logger = logging.getLogger(__name__)

# Set the GPIO mode to BOARD (physical pin numbers)
GPIO.setmode(GPIO.BOARD)

# Define the physical pin numbers for ultrasonic sensor
trig_pin = 12  # Physical pin 12 (GPIO 18)
echo_pin = 18  # Physical pin 18 (GPIO 24)

# Set the GPIO directions
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Function to measure the distance using ultrasonic sensor
def measure_distance_ultrasonic():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microseconds pulse
    GPIO.output(trig_pin, GPIO.LOW)

    pulse_start = None
    pulse_end = None
    max_distance = 800  # Max measurable distance in cm
    timeout_duration = max_distance / 17150 * 2  # Timeout based on max distance (seconds)

    start_time = time.time()

    # Wait for echo to go high (pulse start)
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
        if pulse_start - start_time > timeout_duration:
            logger.warning("Ultrasonic sensor timed out waiting for pulse start.")
            return float('inf')  # Out of range

    # Wait for echo to go low (pulse end)
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()
        if pulse_end - pulse_start > timeout_duration:
            logger.warning("Ultrasonic sensor timed out waiting for pulse end.")
            return float('inf')  # Out of range

    # Calculate the pulse duration and convert it to distance
    if pulse_start and pulse_end:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound is 343 m/s or 17150 cm/s
        return distance
    else:
        return float('inf')  # Out of range

def contains_numeric(data):
    """Check if the data contains any numeric value."""
    return bool(re.search(r'\d', data))  # Regular expression to find any digit

def execute_rpi_client():
    """Execute the rpi_client.py script located in the specified folder."""
    try:
        script_path = '/home/rudra/server_radar_ultrasonic/https_server.py'
        subprocess.Popen(['python3', script_path])
        logger.info("rpi_client.py executed.")
    except Exception as e:
        logger.error(f"Error executing rpi_client.py: {e}")

def check_and_execute(data):
    """Check if the data is numeric and within range; execute script if valid."""
    try:
        numeric_value = re.search(r'\d+', data)
        if numeric_value:
            value = int(numeric_value.group())
            if 110 < value < 820:
                logger.info(f"Value {value} is in range (1.1m to 8m). Executing rpi_client.py...")
                execute_rpi_client()
            else:
                logger.info(f"Value {value} is out of range.")
        else:
            logger.info("Non-numeric data or out of range.")
    except ValueError as e:
        logger.error(f"Error parsing data: {e}")

def main():
    # UART setup
    port = '/dev/ttyS0'
    baud_rate = 115200
    server_url = 'http://192.168.1.2:80'

    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            logger.info(f"Connected to {port} at {baud_rate} baud")

            while True:
                # Read data from UART (Radar sensor)
                try:
                    uart_data = ser.readline().decode('utf-8').strip()
                    distance = None

                    if uart_data:
                        logger.info(f"Received from UART (Radar sensor): {uart_data}")
                        check_and_execute(uart_data)

                        numeric_value = re.search(r'\d+(\.\d+)?', uart_data)
                        if numeric_value:
                            distance = float(numeric_value.group())
                        else:
                            logger.info("Target not in range. No numeric data received from radar sensor.")
                    else:
                        logger.info("No data from radar sensor, using ultrasonic sensor.")
                        distance = measure_distance_ultrasonic()

                    if distance is not None:
                        try:
                            current_time = int(time.time())
                            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            response = requests.post(
                                server_url,
                                data={
                                    "cameraId": "RD001",
                                    "eventTime": current_time,
                                    "timestampStr": timestamp_str,
                                    "eventType": "Sensor_Event",
                                    "eventTag": "RADAR_SENSOR" if uart_data else "ULTRASONIC_SENSOR",
                                },
                                timeout=5  # Set a timeout of 5 seconds
                            )
                            if response.status_code == 200:
                                logger.info(f"Server response: {response.json()}")
                            else:
                                logger.warning(f"Unexpected status code: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            logger.error(f"Error sending data to server: {e}")
                    else:
                        logger.warning("Failed to get distance from both sensors.")

                except Exception as e:
                    logger.error(f"Error in main loop: {e}")

                # Wait for 3 seconds before reading again
                time.sleep(3)

    except serial.SerialException as e:
        logger.error(f"Error opening serial port: {e}")

    except KeyboardInterrupt:
        logger.info("Program terminated by user.")

    finally:
        GPIO.cleanup()
        logger.info("GPIO cleaned up.")

if __name__ == "__main__":
    main()
