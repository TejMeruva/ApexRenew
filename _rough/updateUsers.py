import pandas as pd
import os

users = pd.DataFrame({
    'username':[
        'TejaMeruva2006',
        'AdityaGupta2005',
        'LatashaNayak2005'
    ],
    'password':[
        'Nitt2028',
        'Nitt2027',
        'Nitt2027'
    ],
    'access_token':[
        'Token#00',
        'Token#01',
        'Token#03'
    ]

})


users.to_json(os.path.join('FastAPI_Scripts', 'users.json'))

# print(users[users.username == 'TejaMeruva2006']['password'].item())
