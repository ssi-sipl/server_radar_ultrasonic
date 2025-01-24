import serial

# Open the serial port (ttyS0)
ser = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=1)

# Infinite loop to continuously read UART data
try:
    while True:
        if ser.in_waiting > 0:
            # Read all available data as a string
            data = ser.read(ser.in_waiting).decode('ascii', errors='ignore')  # Decode to string

            # Filter out and print only numeric values
            numeric_data = ''.join(c for c in data if c.isdigit())  # Extract only digits
            if numeric_data:
                print(f"Received numeric data: {numeric_data}")
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()
