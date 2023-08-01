import requests
import time
import random
import datetime

# Replace with your server's URL
url = "https://travelmail26-stunning-rotary-phone-qwwpw55jrf45pp-5000.preview.app.github.dev/"  

while True:
    data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'random_number': random.randint(1, 10)
    }
    print(f'Sending data: {data}')
    response = requests.post(url, json=data)
    print(f'Response from server: {response.text}')
    time.sleep(5)
