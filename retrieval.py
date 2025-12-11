import requests
import pandas as pd
from io import StringIO
import os

class DataSource:
    request_url: str
    service_title: str
    table_name: str
    def __init__(self, request_url: str, service_title: str, table_name: str):
        self.request_url = request_url
        self.service_title = service_title
        self.table_name = table_name

    def __repr__(self):
        s = ''
        s += f'Title of Service: {self.service_title}\n'
        s += f'API Request URL used: {self.request_url}\n'
        s += f'Table name: {self.table_name}'
        return s
    
def get_client_facing_template_names():
    files:list = os.listdir(os.path.join('templates', 'client_facing'))
    return files

def get_carrier_facing_template_names():
    files:list = os.listdir(os.path.join('templates', 'carrier_facing'))
    return files

def get_template_body(fname:str, role:str) -> str:
    p = os.path.join('templates', role, fname)
    text = ''
    with open(p, 'r') as file:
        text = file.read()

    return text

def autofill_template(template_body: str, data: pd.Series) -> str:
    op = 0
    while op != -1:
        # print(op, end='')
        start_ind = 0
        op = template_body.find(r'{')
        if op == -1:
            break
        else:
            start_ind = op
        end_ind = template_body.find(r'}')
        colName = template_body[(start_ind + 2): end_ind]
        to_replace = template_body[start_ind : (end_ind + 2)]
        template_body = template_body.replace(to_replace, str(data[colName]))
        print(to_replace)

    return template_body

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

placementsSource = DataSource(
    request_url="http://localhost:8000/placements",
    service_title='Mock Applied Epic (CRM) API',
    table_name='placements'
)

emailsSource = DataSource(
    request_url = "http://localhost:8001/me/emails",
    service_title='Mock MS (Team Collaboration Service) Graph API',
    table_name='emails'
)

usersSource = DataSource(
    request_url = "http://localhost:8001/teams/users",
    service_title='Mock MS (Team Collaboration Service) Graph API',
    table_name='users'
)

calendarSource = DataSource(
    request_url = "http://localhost:8001/me/events",
    service_title='Mock MS (Team Collaboration Service) Graph API',
    table_name='events'
)
