import requests
import pandas as pd
import json

def headers():
    url = "http://localhost:8000/token"
    data = {
        "username": "TejaMeruva2006",
        "password": "Nitt2028"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return {"Authorization": f"Bearer {response.json()['token']}"}
    else:
        raise Exception('Incorrect uname and/or passwd!')


url = "http://localhost:8000/clients"
resp = requests.get(url, headers=headers())
clients = pd.read_json(resp.json())

url = "http://localhost:8000/policies"
resp = requests.get(url, headers=headers())
policies = pd.read_json(resp.json())

print(clients.head(3))
print()
print(policies.head(3))
    