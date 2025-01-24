import serial
import sys
import time

def read_from_port(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # Read available data
                decoded_data = data.decode('utf-8', errors='ignore')  # Decode and strip extra spaces/newlines
                if decoded_data:
                    sys.stdout.write(decoded_data)  # Print the data to the terminal
                    sys.stdout.flush()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial connection closed.")

def run_serial_communication(port, baudrate=115200, timeout=1):
    try:
        # Set up the serial connection
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baud rate.")

        # Start reading data from the serial port
        read_from_port(ser)

    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. {e}")

if __name__ == "__main__":
    # Adjust the port to match your system (e.g., COM3 on Windows or /dev/ttyS0 on Linux)
    port = "/dev/ttyS0"  # Example for Linux; update for your platform (e.g., COM3 on Windows)
    baudrate = 115200
    run_serial_communication(port, baudrate)
