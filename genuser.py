import requests
import json

url = 'https://randomuser.me/api/'

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data:", response.status_code)


jsondata = json.dumps(data, indent=4)

print(data["results"][0]["gender"])