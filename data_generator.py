import socket
import json
import time
import random
from faker import Faker

fake = Faker()

# Generate a random ride event
def generate_ride_event():
    return {
        "trip_id": fake.uuid4(),
        "driver_id": random.randint(1, 100),
        "distance_km": round(random.uniform(1, 50), 2),
        "fare_amount": round(random.uniform(5, 150), 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Start streaming using socket
def start_streaming(host="localhost", port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Add this line to allow reusing the address immediately
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)  # Increase backlog to allow multiple connections
        print(f"Streaming data to {host}:{port}...")

        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"New client connected: {addr}")

                while True:
                    try:
                        # Generate a ride event and send it to the connected client
                        ride_event = generate_ride_event()
                        conn.send((json.dumps(ride_event) + "\n").encode("utf-8"))
                        print("Sent:", ride_event)
                        time.sleep(1)
                    except (BrokenPipeError, ConnectionResetError):
                        print(f"Client {addr} disconnected. Waiting for a new client.")
                        break  # Exit the inner loop and wait for a new client

            except Exception as e:
                print(f"Error accepting connection: {e}")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print("Port is already in use. Try to kill the process using this port first.")
            print("You can use: 'lsof -i :9999' and then 'kill <PID>' on Linux/Mac")
            print("Or 'netstat -ano | findstr :9999' and then 'taskkill /PID <PID> /F' on Windows")
        else:
            print(f"Socket error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_streaming()