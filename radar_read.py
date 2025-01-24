import serial
import sys
import time
import threading
import os
import termios
import tty

class MinicomMimic:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.running = True

    def open_serial_connection(self):
        try:
            # Set up the serial connection
            self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
            print(f"Connected to {self.port} at {self.baudrate} baud rate.")
        except serial.SerialException as e:
            print(f"Error: Could not open serial port {self.port}. {e}")
            sys.exit(1)

    def close_serial_connection(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")

    def read_from_port(self):
        while self.running:
            if self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)  # Read available data
                decoded_data = data.decode('utf-8', errors='ignore')  # Decode and strip extra spaces/newlines
                if decoded_data:
                    sys.stdout.write(decoded_data)  # Print the data to the terminal
                    sys.stdout.flush()

    def write_to_port(self, user_input):
        if self.ser:
            self.ser.write(user_input.encode('utf-8'))  # Send user input to serial port

    def start_reading_thread(self):
        # Start a thread to continuously read data from the serial port
        read_thread = threading.Thread(target=self.read_from_port)
        read_thread.daemon = True
        read_thread.start()

    def run(self):
        self.open_serial_connection()
        self.start_reading_thread()

        print("\nMimicking minicom interface.")
        print("Press 'Ctrl+C' to exit.")
        print("To send data, type your input and press 'Enter'.\n")

        try:
            while self.running:
                # Read user input from terminal
                user_input = self.read_input()
                if user_input.lower() == 'exit':
                    print("Exiting...")
                    self.running = False
                else:
                    self.write_to_port(user_input)

        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            self.running = False

        finally:
            self.close_serial_connection()

    def read_input(self):
        """
        Reads input from the user without requiring the enter key.
        This mimics the interactive behavior of `minicom`.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            user_input = sys.stdin.read(1)  # Read one character at a time
            while user_input != '\n':  # Continue reading until user presses Enter
                print(user_input, end="", flush=True)
                user_input += sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print()  # New line after input
        return user_input

if __name__ == "__main__":
    # Adjust the port to match your system (e.g., COM3 on Windows or /dev/ttyS0 on Linux)
    port = "/dev/ttyS0"  # Example for Linux; update for your platform (e.g., COM3 on Windows)
    baudrate = 115200

    minicom = MinicomMimic(port, baudrate)
    minicom.run()
