import requests
import pandas as pd
from io import StringIO

def get_crm_headers(uname: str, passwd: str):
    url = "http://localhost:8000/token"
    data = {
        "username": uname,
        "password": passwd
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return {"Authorization": f"Bearer {response.json()['token']}"}
    else:
        raise Exception('Incorrect uname and/or passwd!')
    
def get_colab_headers(uname: str, passwd: str):
    url = "http://localhost:8001/token"
    data = {
        "username": uname,
        "password": passwd
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return {"Authorization": f"Bearer {response.json()['token']}"}
    else:
        raise Exception('Incorrect uname and/or passwd!')


# def get_client_data(crm_headers):
#     url = "http://localhost:8000/clients"
#     resp = requests.get(url, headers=crm_headers)
#     return pd.read_json(StringIO(resp.json()))

# def get_policies_data(crm_headers):
#     url = "http://localhost:8000/policies"
#     resp = requests.get(url, headers=crm_headers)
#     return pd.read_json(StringIO(resp.json()))

def get_placements_data(crm_headers):
    url = "http://localhost:8000/placements"
    resp = requests.get(url, headers=crm_headers)
    return pd.read_json(StringIO(resp.json()))

def get_ms_emails_data(colab_headers):
    url = "http://localhost:8001/me/emails"
    resp = requests.get(url, headers=colab_headers)
    return pd.read_json(StringIO(resp.json()))

def get_ms_teams_users_data(colab_headers):
    url = "http://localhost:8001/teams/users"
    resp = requests.get(url, headers=colab_headers)
    return pd.read_json(StringIO(resp.json()))

def get_calendar_events_data(colab_headers):
    url = "http://localhost:8001/me/events"
    resp = requests.get(url, headers=colab_headers)
    return pd.read_json(StringIO(resp.json()))
