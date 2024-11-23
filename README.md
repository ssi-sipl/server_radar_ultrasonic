# Radar and Ultrasonic Sensor Communication System

This Python script integrates a **radar sensor** (using UART communication) and an **ultrasonic sensor** (using GPIO pins) to measure distances. It processes sensor data, sends it to an HTTP server, and logs activity.

## Features
1. **Ultrasonic Sensor Distance Measurement**  
   - Uses GPIO pins to interface with the ultrasonic sensor.
   - Measures distance by calculating the echo pulse duration.

2. **Radar Sensor Data Handling**  
   - Reads data from a radar sensor over a UART interface.
   - Processes the received data to extract numeric values.
   - Triggers additional actions based on the data received.

3. **Data Transmission**  
   - Sends sensor data to an HTTP server as a POST request.
   - Includes sensor type, event timestamp, and event details.

4. **Logging and Debugging**  
   - Logs all operations, errors, and sensor data into a log file (`radar_ultrasonic_uart_server_communication.log`).

5. **Failsafe Mechanism**  
   - Uses the ultrasonic sensor as a fallback when radar sensor data is unavailable.
   - Handles non-numeric or out-of-range data gracefully.

## Dependencies
### Python Modules
Install these modules using `pip` if not already available:
```bash
pip install RPi.GPIO pyserial requests
