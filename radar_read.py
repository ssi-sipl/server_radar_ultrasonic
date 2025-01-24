import serial

# Open the serial port (ttyS0)
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

# Infinite loop to continuously read UART data
try:
    while True:
        if ser.in_waiting > 0:
            # Read one byte of data
            data = ser.read(1).decode('ascii', errors='ignore')  # Decode byte to string and ignore errors

            # Check if the character is a numeric value
            if data.isdigit():
                print(f"Received numeric data: {data}")
except KeyboardInterrupt:
    print("Program interrupted.")
finally:
    ser.close()
