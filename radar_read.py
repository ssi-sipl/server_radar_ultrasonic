import serial
import time

# Open the serial port (ttyS0) with a baud rate of 115200
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

# Variable to store the accumulated numeric data
accumulated_data = ''

# Infinite loop to continuously read UART data
try:
    while True:
        if ser.in_waiting > 0:
            # Read all available data as a string
            data = ser.read(ser.in_waiting).decode('ascii', errors='ignore')  # Decode to string

            # Accumulate only numeric characters
            for c in data:
                if c.isdigit():
                    accumulated_data += c
                else:
                    # If non-numeric character, reset the accumulator
                    if accumulated_data:
                        print(f"Received numeric data: {accumulated_data}")
                        accumulated_data = ''  # Reset after printing the accumulated number

        # Check if we have accumulated data and there has been a pause in input
        elif accumulated_data:
            # Add a small delay to allow for pauses in input
            time.sleep(0.1)  # Adjust the sleep time as necessary
            
            if accumulated_data:  # If there is data, print it
                print(f"Received numeric data: {accumulated_data}")
                accumulated_data = ''  # Reset after printing the accumulated number

except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()
