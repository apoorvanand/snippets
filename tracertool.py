import requests
import time
import json

# Traccar server details
BASE_URL = 'http://127.0.0.1:5056'  # Replace with your Traccar server's IP address or hostname and port

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

def send_gps_message(device_id, latitude, longitude, altitude, speed, course):
    time_stamp = int(time.time())
    data = {
        "id": device_id,
        "pos": [latitude, longitude],
        "alt": altitude,
        "speed": speed,
        "course": course,
        "time": time_stamp
    }
    response = requests.post(f'{BASE_URL}/gps', json=data)
    if response.status_code == 200:
        print(f"Sent GPS data: {json.dumps(data)}")
    else:
        print(f"Error sending GPS data: {response.status_code} - {response.text}")

# Send GPS messages in a continuous loop at the specified interval
while True:
    send_gps_message(DEVICE_ID, latitude, longitude, altitude, speed, course)
    time.sleep(INTERVAL)
