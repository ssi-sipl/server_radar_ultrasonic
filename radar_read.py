import serial
import time

def read_uart():
    # Configure the serial connection
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

    try:
        while True:
            if ser.in_waiting > 0:  # Check if there is data waiting to be read
                line = ser.readline().decode('utf-8').rstrip()  # Read a line and decode it
                # Attempt to extract numeric values only
                numeric_values = ''.join(filter(str.isdigit, line))
                if numeric_values:  # Only print if there are numeric values
                    print(numeric_values)  # Print the numeric values
            time.sleep(0.1)  # Sleep briefly to avoid busy waiting
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()  # Ensure the serial port is closed on exit

if __name__ == "__main__":
    read_uart()
