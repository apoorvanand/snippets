import socket
import time
import random

# Traccar server details
SERVER_IP = '127.0.0.1'  # Replace with your Traccar server's IP
SERVER_PORT = 5056       # Traccar TCP port for GPS data

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def generate_dummy_gps_data():
    """
    Generate dummy GPS data in Traccar protocol format.
    Replace with the required format if your Traccar setup expects a specific structure.
    """
    # Example data format: "$<device_id>,<timestamp>,<latitude>,<longitude>,<speed>,<course>,<altitude>"
    device_id = "123456789012345"  # Replace with a valid device identifier
    timestamp = int(time.time())
    latitude = random.uniform(-90.0, 90.0)
    longitude = random.uniform(-180.0, 180.0)
    speed = random.uniform(0, 100)  # Speed in km/h
    course = random.uniform(0, 360)  # Course in degrees
    altitude = random.uniform(0, 5000)  # Altitude in meters
    
    # Formulate data packet
    data_packet = f"${device_id},{timestamp},{latitude:.6f},{longitude:.6f},{speed:.2f},{course:.2f},{altitude:.2f}"
    return data_packet

try:
    # Connect to the Traccar server
    print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the Traccar server.")

    while True:
        # Generate dummy GPS data
        gps_data = generate_dummy_gps_data()
        print(f"Sending data: {gps_data}")

        # Send data to the server
        client_socket.sendall(gps_data.encode('utf-8'))

        # Wait before sending the next packet
        time.sleep(2)  # Adjust the interval as needed
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Closing connection...")
    client_socket.close()
