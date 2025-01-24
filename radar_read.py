import serial

# Open the serial port (ttyS0)
ser = serial.Serial('/dev/ttyS0', baudrate=15200, timeout=1)

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
                    # If non-numeric character, print and reset the accumulator
                    if accumulated_data:
                        print(f"Received numeric data: {accumulated_data}")
                        accumulated_data = ''  # Reset after printing the accumulated number
        else:
            # If no data, print accumulated data and reset
            if accumulated_data:
                print(f"Received numeric data: {accumulated_data}")
                accumulated_data = ''
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()
