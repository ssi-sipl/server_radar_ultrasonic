import serial
import sys
import time
import threading
import re  # Import the regular expression module

# Define a function to handle reading from the serial port
def read_from_port(ser):
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # Read all data available in the buffer
                decoded_data = data.decode('utf-8', errors='ignore').strip()  # Decode and strip extra spaces/newlines
                
                # Extract integer values from the string using regular expression
                integer_values = re.findall(r'\b\d+\b', decoded_data)  # Find all integers (whole numbers)
                
                if integer_values:
                    for value in integer_values:
                        sys.stdout.write(value + "\n")  # Print the extracted integer value
                        sys.stdout.flush()
                else:
                    # Only print if the data contains integers, otherwise discard it quietly
                    pass
    except Exception as e:
        print(f"Error while reading from serial port: {e}")

# Main function to initialize serial port and handle communication
def run_serial_communication(port, baudrate=115200, timeout=1):
    try:
        # Set up the serial connection
        ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        print(f"Connected to {port} at {baudrate} baudrate.")
        
        # Start a separate thread to handle reading from the serial port
        read_thread = threading.Thread(target=read_from_port, args=(ser,))
        read_thread.daemon = True  # Ensure it exits when the main program exits
        read_thread.start()
        
        while True:
            # Read user input and send it over the serial port
            user_input = input("Send to Serial Port (type 'exit' to quit): ")
            if user_input.strip().lower() == 'exit':
                print("Exiting...")
                break
            else:
                ser.write(user_input.encode('utf-8'))  # Send user input to serial port
                time.sleep(0.1)  # Give some time for the data to be sent
                
    except serial.SerialException as e:
        print(f"Error: Could not open serial port {port}. {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        if ser.is_open:
            ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    port = "/dev/ttyS0"  # Example for Linux; update for your platform (e.g., COM3 on Windows)
    baudrate = 115200
    run_serial_communication(port, baudrate=baudrate)
