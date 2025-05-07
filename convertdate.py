from datetime import datetime

# Example time string
time_str = "2025-05-07 13:30:00"

# Convert to datetime object
dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

# Convert to Unix timestamp
unix_timestamp = int(dt.timestamp())

print(unix_timestamp)
