import socket
import time
import random

# Traccar server details
SERVER_IP = '127.0.0.1'  # Replace with your Traccar server's IP
SERVER_PORT = 5056       # Traccar TCP port for GPS data

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def generate_osmand_frame():
    """
    Generate GPS data in OsmAnd protocol format for Traccar.
    """
    device_id = "123456789012345"  # Replace with your actual device ID
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    timestamp = int(time.time())  # UNIX timestamp
    altitude = random.uniform(0, 5000)  # Altitude in meters
    speed = random.uniform(0, 120)  # Speed in km/h
    
    # Format data for OsmAnd protocol
    frame = f"id={device_id},lat={latitude:.6f},lon={longitude:.6f},timestamp={timestamp},altitude={altitude:.2f},speed={speed:.2f}\n"
    return frame

try:
    # Connect to the Traccar server
    print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the Traccar server.")

    while True:
        # Generate and send data frame
        gps_frame = generate_osmand_frame()
        print(f"Sending frame: {gps_frame.strip()}")
        client_socket.sendall(gps_frame.encode('utf-8'))

        # Wait before sending the next packet
        time.sleep(2)
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Closing connection...")
    client_socket.close()
