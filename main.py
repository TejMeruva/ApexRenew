import retrieval
from prettyPrint import divPrint, centerPrint
import os
import pandas as pd
pd.set_option('display.max_columns', None)
from preprocessing import get_merged, add_interpreted_cols, add_score_cols
from prioritization import justify

#printing the title
text = ''
with open('title.txt', 'r') as file:
    text = file.read()

centerPrint(text)

#printing the menu

divPrint()
os.system('figlet Menu')
menu = \
"""
1. Get OAuth2.0 Tokens
2. Get Placements Data (uses Mock-AppliedEpic_API)
3. Get MS Teams Users Data (uses Mock-MS_Graph_API)
4. Get E-Mails Data (uses Mock-MS_Graph_API)
5. Get MS Calendar Data (uses Mock-MS_Graph_API)
6. Preprocess Data and Make Pipeline 
7. Justify GPA
8. Top 5 Clients
9. Exit
"""

print(menu)

#retrieved data
authenticated = False
crm_headers = ''
colab_headers = ''

clients = pd.DataFrame()
policies = pd.DataFrame()
merged = pd.DataFrame()

while True:
    divPrint()
    inp = input('Choice: ')
    match inp:
        case '1':
            if not authenticated:
                crm_uname = input('Enter AppliedEpic username: ')
                crm_paasswd = input('Enter AppliecEpic password: ')
                ms_uname = input('Enter MS username: ')
                ms_passwd = input('Enter MS passwd: ')

                crm_headers = retrieval.get_crm_headers(crm_uname, crm_paasswd)
                colab_headers = retrieval.get_colab_headers(ms_uname, ms_passwd)

                authenticated = True
                print('Authenticated!')
            else:
                print('Authorization already complete!')
        case '2':
            if authenticated: 
                clients = retrieval.get_placements_data(crm_headers=crm_headers)
                print(clients.head(3))
            else:
                print('First obtain authorization. Press 1!')
        case '3':
            if authenticated:
                users = retrieval.get_ms_teams_users_data(colab_headers=colab_headers)
                print(users.head(3))
            else:
                print('First obtain authorization. Press 1!')
        case '4':
            if authenticated:
                emails = retrieval.get_ms_emails_data(colab_headers=colab_headers)
                print(emails.head(3))
            else:
                print('First obtain authorization. Press 1!')
        case '5':
            if authenticated:
                emails = retrieval.get_calendar_events_data(colab_headers=colab_headers)
                print(emails.head(3))
            else:
                print('First obtain authorization. Press 1!')
        case '6':
            merged = get_merged(clients, policies)
            merged = add_interpreted_cols(merged)
            merged = add_score_cols(merged)
            print(merged.iloc[:, :-1].head(10))

        case '7' :
            ind = input('Enter the client_id: ')
            print((merged[merged.client_id == ind])['justification'].item())
        case '8':
            print(merged.sort_values(by='client_priority_GPA', ascending=False).head(5))
        case '9':
            centerPrint('Thank You for using ApexRenewCLI!')
            break
        case _:
            continue
