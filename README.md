

# Rudrarakshak-SensorBox Documentation  

## Overview  
The **Rudrarakshak-SensorBox** project is a collection of Python scripts and configuration files designed to work with Raspberry Pi and sensors (e.g., ultrasonic and radar). It enables distance measurement, data processing, and server communication.  


![sensorbox_connections.png]()

This README provides a detailed explanation of each component of the project.  

---

## Table of Contents  
1. [activate_env.py](#1-activate_envpy)  
2. [requirements.txt](#2-requirementstxt)  
3. [ajsr04.py](#3-ajsr04py)  
4. [http_requests.py](#4-http_requestspy)  
5. [http_server.py](#5-http_serverpy)  
6. [radar_read.py](#6-radar_readpy)  
7. [radar_ultrasonic.py](#7-radar_ultrasonicpy)  

---

## 1. activate_env.py  

### Key Features  
- **System Updates and Upgrades**: Ensures the OS is up to date.  
- **Installs Python 3**: Verifies and installs Python 3 if missing.  
- **Installs Git**: Ensures Git is installed.  
- **Creates a Virtual Environment**: Prepares an isolated Python environment for the project.  
- **Activation Instructions**: Provides commands to activate the virtual environment.  

### Purpose  
This script ensures the system is updated and ready for dependency installation and development.  

---

## 2. requirements.txt  

### Usage  
Contains the list of external Python libraries and their required versions. To install dependencies:  
```bash  
pip install -r requirements.txt  
```  

---

## 3. ajsr04.py  

### Key Features  
- **GPIO Pin Configuration**:  
  - **Trig Pin**: Pin 12 (GPIO 18), sends a trigger signal.  
  - **Echo Pin**: Pin 18 (GPIO 24), reads the reflected signal.  
- **Ultrasonic Sensor Mechanism**:  
  - Sends a 10-microsecond pulse.  
  - Calculates distance using the formula:  
    ```text  
    Distance (cm) = Pulse Duration × 17150  
    ```  
- **Timeout Handling**: Returns `-1` if no object is detected within 20 ms.  
- **Valid Range Filtering**: Filters measurements outside the range (2–800 cm).  
- **Graceful Exit**: Ensures GPIO cleanup on interruption (Ctrl+C).  

### Purpose  
To verify the functionality of the HC-SR04 ultrasonic sensor.  

---

## 4. http_requests.py  

### Key Features  
- **Function**: `send_http_command`  
  - **Parameters**:  
    - `url`: Target URL.  
    - `method`: HTTP method (default: `POST`).  
    - `params`, `data`, `headers`: Optional parameters for the request.  
- **Error Handling**: Reports network or response errors.  
- **Return Value**: Returns response text on success or `None` on failure.  

### Purpose  
To test the ability to send HTTP requests to a server.  

---

## 5. http_server.py  

### Key Features  
- **Custom HTTP Handler**: Handles incoming POST requests.  
- **JSON Parsing**: Processes JSON data from POST requests and responds with a status.  
- **Error Handling**: Returns `400 Bad Request` for invalid JSON.  
- **Logging**: Logs incoming requests for debugging.  
- **Server Configuration**: Listens on:  
  - **Host**: `192.168.1.2`  
  - **Port**: `80`  

### Purpose  
To create a lightweight HTTP server for receiving and processing data.  

---

## 6. radar_read.py  

### Key Features  
- **Serial Port Configuration**: Uses `/dev/ttyS0` at a baud rate of 115200.  
- **Data Filtering**: Reads and processes incoming UART data.  
- **Real-Time Processing**: Continuously monitors incoming data.  
- **Graceful Exit**: Ensures the serial port is safely closed on interruption.  

### Purpose  
To verify the functionality of the radar sensor.  

---

## 7. radar_ultrasonic.py  

### Key Features  
- **Ultrasonic Sensor Integration**: Filters valid distance values (2–800 cm).  
- **Radar Sensor Integration**: Reads data asynchronously using threads.  
- **HTTP Requests**: Sends valid measurements (120–780 cm) to the server via POST requests.  
- **Concurrency**: Utilizes threads for parallel data collection.  
- **Logging**: Logs events and data for debugging.  
- **Graceful Shutdown**: Cleans up GPIO pins and serial ports on exit.  

### Workflow  
1. **Run the Script**: Starts both sensors on a Raspberry Pi.  
2. **Collect Sensor Data**: Measures distances using radar and ultrasonic sensors.  
3. **Send to Server**: Sends measurements as JSON payloads via HTTP POST.  

### Adjusting the Valid Range  
To modify the valid range, update these variables:  
- `VALID_RANGE_MIN`  
- `VALID_RANGE_MAX`  

---

## Summary  
The **Rudrarakshak-SensorBox** project integrates sensor-based distance measurement, data processing, and server communication into a cohesive system. It is modular, easy to use, and ideal for verifying hardware functionality, collecting measurements, and sending data for analysis.  

