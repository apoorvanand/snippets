import socket
import time
import random

def generate_gps_data():
    # Generate random latitude and longitude
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    
    # Generate dummy IMEI (15 digits)
    imei = ''.join([str(random.randint(0, 9)) for _ in range(15)])
    
    # Create GPRMC sentence
    gprmc = f"$GPRMC,{time.strftime('%H%M%S')},A,{abs(lat):02.4f},{('N' if lat >= 0 else 'S')},{abs(lon):03.4f},{('E' if lon >= 0 else 'W')},0.0,0.0,{time.strftime('%d%m%y')},,,A*00\r\n"
    
    return imei, gprmc

def send_data_to_traccar(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    try:
        while True:
            imei, gprmc = generate_gps_data()
            message = f"imei:{imei},{gprmc}"
            sock.sendall(message.encode())
            print(f"Sent: {message}")
            time.sleep(5)  # Send data every 5 seconds
    except KeyboardInterrupt:
        print("Stopping data transmission")
    finally:
        sock.close()

if __name__ == "__main__":
    traccar_host = "localhost"  # Replace with your Traccar server IP if not running locally
    traccar_port = 5056
    
    send_data_to_traccar(traccar_host, traccar_port)
