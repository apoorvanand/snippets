import socket
import time

# Traccar server details
HOST = 'localhost'  # Replace with your Traccar server's IP address or hostname
PORT = 5056

# Device ID (replace with your device's ID)
DEVICE_ID = '12345'

# GPS data (latitude, longitude, altitude, speed, course)
latitude = 40.7128
longitude = -74.0060
altitude = 0
speed = 0
course = 0

# Message interval in seconds
INTERVAL = 10

def send_gps_message(sock, device_id, latitude, longitude, altitude, speed, course):
    time_stamp = int(time.time())
    message = f'{device_id}{latitude:09.6f}{longitude:010.6f}{altitude:06d}{speed:06d}{course:06d}{time_stamp:010d}\r\n'.encode()
    sock.sendall(message)
    print(f"Sent GPS data: {message.decode()}")

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to the Traccar server
    sock.connect((HOST, PORT))

    try:
        while True:
            send_gps_message(sock, DEVICE_ID, latitude, longitude, altitude, speed, course)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nTest server stopped.")
