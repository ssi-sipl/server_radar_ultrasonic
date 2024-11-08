import serial
import sys
import time
import threading

# Define a function to handle reading from the serial port
def read_from_port(ser):
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)  # Read all data available in the buffer
            sys.stdout.write(data.decode('utf-8', errors='ignore'))  # Print data to console
            sys.stdout.flush()

# Main function to initialize serial port and handle communication
def run_serial_communication(port, baudrate=9600, timeout=1):
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
    # Corrected: Port should be a string, not a raw path
    port = "/dev/ttyS0"  # Example for Linux
    baudrate = 115200
    run_serial_communication(port, baudrate=baudrate)
