import socket
import time

# Traccar server details
HOST = 'localhost'  # Replace with your Traccar server's IP address or hostname
PORT = 5056

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to the Traccar server
    sock.connect((HOST, PORT))

    # GPS data (latitude, longitude, altitude, speed, course, time)
    latitude = 40.7128
    longitude = -74.0060
    altitude = 0
    speed = 0
    course = 0
    time_stamp = int(time.time())

    # Send GPS data as a TCP message
    message = f'{"GPS".encode()}{latitude:09.6f}{longitude:010.6f}{altitude:06d}{speed:06d}{course:06d}{time_stamp:010d}\r\n'.encode()
    sock.sendall(message)

    print(f"Sent GPS data: {message.decode()}")

    # Keep the connection open for additional messages (if needed)
    # time.sleep(1)

# The connection is automatically closed when the 'with' block ends
