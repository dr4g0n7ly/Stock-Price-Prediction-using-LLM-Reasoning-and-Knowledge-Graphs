import requests
import json
from config import API_KEY, API_SECRET

url = 'https://data.alpaca.markets/v1beta1/news?symbols=TSLA'
headers = {
    'Apca-Api-Key-Id': API_KEY,
    'Apca-Api-Secret-Key': API_SECRET
}

response = requests.get(url, headers=headers)

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Print formatted JSON response
    formatted_response = json.dumps(response.json(), indent=4)
    print(formatted_response)
else:
    print(f"Request failed with status code {response.status_code}")
