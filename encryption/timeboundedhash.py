import hashlib
import os
import time
from datetime import datetime, timedelta

# Function to generate a salted hash
def generate_salted_hash(password, expiration_seconds=60):
    # Generate a random salt
    salt = os.urandom(16)
    # Define hashing parameters
    iterations = 100000
    key_length = 64
    hash_name = 'sha256'
    
    # Derive the password hash using PBKDF2
    password_hash = hashlib.pbkdf2_hmac(
        hash_name=hash_name,
        password=password.encode('utf-8'),
        salt=salt,
        iterations=iterations,
        dklen=key_length
    )
    
    # Calculate expiration timestamp
    expiration_time = datetime.now() + timedelta(seconds=expiration_seconds)
    
    return {
        "salt": salt,
        "hash": password_hash,
        "expires_at": expiration_time
    }

# Function to verify the password before expiration
def verify_password(stored_data, password):
    current_time = datetime.now()
    
    # Check if the hash has expired
    if current_time > stored_data["expires_at"]:
        return False, "Hash expired"
    
    # Recompute the hash with the stored salt
    recomputed_hash = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=stored_data["salt"],
        iterations=100000,
        dklen=64
    )
    
    # Compare hashes securely
    if recomputed_hash == stored_data["hash"]:
        return True, "Password verified"
    else:
        return False, "Invalid password"

# Example Usage

# Generate a salted hash with a 30-second expiration
password = "my_secure_password"
stored_data = generate_salted_hash(password, expiration_seconds=30)

print("Stored Data:", stored_data)

# Wait for some time (simulate delay)
time.sleep(10)

# Verify within valid time frame
is_valid, message = verify_password(stored_data, password)
print("Verification Result:", message)

# Wait until after expiration period
time.sleep(25)

# Verify after expiration
is_valid, message = verify_password(stored_data, password)
print("Verification Result:", message)
