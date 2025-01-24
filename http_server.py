from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Define the host and port to run the HTTP server
HOST = '192.168.1.2'  # Listen on all available interfaces
PORT = 80       # Default port for the HTTP server

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler to handle POST requests."""

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            # Parse the JSON data
            data = json.loads(post_data)
            print(f"Received POST request on {self.path} with data: {data}")

            # Process the data (modify this as per your needs)
            response = {
                "status": "success",
                "message": "Data received successfully",
                "receivedData": data
            }

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))

    def log_message(self, format, *args):
        # Customize log format
        print("[HTTP Server]", self.address_string(), "-", format % args)

if __name__ == "__main__":
    try:
        # Create an HTTP server instance
        server = HTTPServer((HOST, PORT), CustomHTTPRequestHandler)
        print(f"Starting HTTP server on {HOST}:{PORT}...")
        print("Press Ctrl+C to stop the server.")
        
        # Run the server
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        server.server_close()
        print("Server stopped.")
    except Exception as e:
        print(f"Error: {e}")