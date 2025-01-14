import requests
import json
import time
from datetime import datetime, timedelta

# Traccar server details
TRACCAR_URL = "http://localhost:8082"
USERNAME = "admin"
PASSWORD = "admin"

def authenticate():
    """
    Authenticate with the Traccar server and get a session cookie.
    """
    session = requests.Session()
    response = session.post(
        f"{TRACCAR_URL}/api/session",
        json={"email": USERNAME, "password": PASSWORD}
    )
    if response.status_code == 200:
        print("Authentication successful.")
        return session
    else:
        print(f"Failed to authenticate: {response.status_code}, {response.text}")
        return None

def create_device(session, name, unique_id):
    """
    Create a new device in Traccar.
    """
    device_data = {
        "name": name,
        "uniqueId": unique_id
    }
    response = session.post(
        f"{TRACCAR_URL}/api/devices",
        json=device_data
    )
    if response.status_code == 200:
        device = response.json()
        print("Device created successfully:", device)
        return device["id"]
    else:
        print(f"Failed to create device: {response.status_code}, {response.text}")
        return None

def send_device_data(session, device_id, latitude, longitude, timestamp):
    """
    Send GPS data to a device.
    """
    position_data = {
        "deviceId": device_id,
        "latitude": latitude,
        "longitude": longitude,
        "speed": 10,  # Simulating 10 m/s speed
        "course": 90,  # Simulating direction in degrees
        "altitude": 100,  # Simulating altitude in meters
        "attributes": {},
        "deviceTime": timestamp,
        "fixTime": timestamp,
        "valid": True
    }
    response = session.post(
        f"{TRACCAR_URL}/api/positions",
        json=position_data
    )
    if response.status_code == 200:
        print("Position data sent successfully:", response.json())
    else:
        print(f"Failed to send position data: {response.status_code}, {response.text}")

def simulate_gps_tracking(session, device_id, start_latitude, start_longitude, interval=5, total_updates=20):
    """
    Simulate continuous GPS data transmission.
    """
    latitude = start_latitude
    longitude = start_longitude
    timestamp = datetime.utcnow()

    for update in range(total_updates):
        print(f"Sending update {update + 1}/{total_updates}...")
        
        # Increment latitude and longitude to simulate movement
        latitude += 0.0001  # Simulating a small northward movement
        longitude += 0.0001  # Simulating a small eastward movement
        timestamp += timedelta(seconds=interval)

        # Send position data
        send_device_data(
            session,
            device_id=device_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp.isoformat() + "Z"
        )
        
        # Wait for the next update
        time.sleep(interval)

if __name__ == "__main__":
    # Authenticate
    session = authenticate()
    if session:
        # Create a device
        device_id = create_device(session, name="Test Device", unique_id="1234567890")
        
        if device_id:
            # Start GPS tracking simulation
            simulate_gps_tracking(
                session,
                device_id=device_id,
                start_latitude=37.7749,  # Starting latitude (e.g., San Francisco)
                start_longitude=-122.4194,  # Starting longitude
                interval=5,  # Send data every 5 seconds
                total_updates=20  # Total number of updates to send
            )
