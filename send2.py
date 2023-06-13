import time
import random
from pythonosc import udp_client

ip = "127.0.0.1"
port = 5000

if __name__ == "__main__":
    client = udp_client.SimpleUDPClient(ip, port)
    start_time = time.time()  # Save the current time to calculate elapsed time later
    while time.time() - start_time < 60:  # While less than 60 seconds have passed
        message = "/test"
        data = random.randint(1, 10)  # Generate a random integer between 1 and 10
        print(f"Sending OSC message: {message} with data: {data}")
        client.send_message(message, data)
        time.sleep(1)  # Wait for 0.5 seconds before sending the next message
