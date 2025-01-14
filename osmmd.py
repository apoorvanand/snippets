import socket
import time
import random
import urllib.parse

def generate_gps_data():
    # Generate random latitude and longitude
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    
    # Generate a fixed device ID (you should replace this with your actual device ID)
    device_id = "123456789"
    
    # Generate other random data
    speed = random.uniform(0, 100)
    bearing = random.uniform(0, 360)
    altitude = random.uniform(0, 1000)
    accuracy = random.uniform(0, 100)
    
    timestamp = int(time.time())
    
    return device_id, lat, lon, speed, bearing, altitude, accuracy, timestamp

def create_osmand_message(device_id, lat, lon, speed, bearing, altitude, accuracy, timestamp):
    params = {
        'id': device_id,
        'lat': f"{lat:.6f}",
        'lon': f"{lon:.6f}",
        'speed': f"{speed:.2f}",
        'bearing': f"{bearing:.2f}",
        'altitude': f"{altitude:.2f}",
        'hdop': f"{accuracy:.2f}",
        'timestamp': str(timestamp)
    }
    return f"/?{urllib.parse.urlencode(params)}"

def send_data_to_traccar(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    try:
        while True:
            device_id, lat, lon, speed, bearing, altitude, accuracy, timestamp = generate_gps_data()
            message = create_osmand_message(device_id, lat, lon, speed, bearing, altitude, accuracy, timestamp)
            sock.sendall(message.encode() + b'\r\n')
            print(f"Sent: {message}")
            time.sleep(5)  # Send data every 5 seconds
    except KeyboardInterrupt:
        print("Stopping data transmission")
    finally:
        sock.close()

if __name__ == "__main__":
    traccar_host = "localhost"  # Replace with your Traccar server IP if not running locally
    traccar_port = 5055  # Default port for OsmAnd protocol
    
    send_data_to_traccar(traccar_host, traccar_port)
