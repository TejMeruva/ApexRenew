import retrieval
from retrieval import placementsSource
from prettyPrint import divPrint, centerPrint
import os
import pandas as pd
pd.set_option('display.max_columns', None)
from preprocessing import preprocess, add_interpreted_cols, add_score_cols
from prioritization import justify
from textGenerator import get_chatbot_response, get_client_brief, DataSource, warm_up


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
7. Get Brief PDF
8. Ask Chatbot
9. Justify GPA
10. Top 5 Clients
11. Exit
"""

print(menu)

#retrieved data
authenticated = False
crm_headers = ''
colab_headers = ''

placements = pd.DataFrame()

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
                warm_up()
                print('GPT warmed up!')
            else:
                print('Authorization already complete!')
        case '2':
            if authenticated: 
                placements = retrieval.get_placements_data(crm_headers=crm_headers)
                print(placements.head(3))
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
            preprocess(placements, inplace=True)
            print('Changed dtypes and Column Names!')
            add_interpreted_cols(placements, inplace=True)
            print('Added interpreted columns!')
            add_score_cols(placements, inplace=True)
            print('Added score columns!')
            placements['_PriorityJustification'] = justify(placements)
            print(placements.iloc[:, :-1].head(3))

        case '7' :
            id = input('Enter Client ID: ')
            print(get_client_brief(
                client_id=id,
                data=placements,
                source=placementsSource
            ))
        case '8':
            inp = input('Enter prompt (mention the client ID): ')
            print(get_chatbot_response(
                q=inp,
                data=placements,
                source=placementsSource,
                confidence=True
            ))
        case '9':
            ind = int(input('Enter row index: '))
            print(placements.loc[ind, '_PriorityJustification'])
        case '10':
            print(placements.sort_values(by='_ClientPriorityGPA', ascending=False).head(5))
        case '11':
            print('Thank You for using ApexRenewCLI!')
            break
        case _:
            print('Invalid Input! Please refer to the Menu')
            
