import pandas as pd
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

users = pd.read_json('users.json')
# print(users)

def User(BaseModel):
    username: str

@app.get('/status')
async def get_auth_status(user: Annotated[User, Depends(oauth2_scheme)]):
    return {'detail': 'Access Granted'}

@app.get('/clients')
def get_client_data(user: Annotated[User, Depends(oauth2_scheme)]):
    data = pd.read_csv(
        '../fake_CRM_data/clients.csv'
    )
    return data.to_json()

@app.get('/policies')
def get_policy_data(user: Annotated[User, Depends(oauth2_scheme)]):
    data = pd.read_csv(
        '../fake_CRM_data/policies.csv'
    )
    return data.to_json()

@app.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    uname = form_data.username
    passwd = form_data.password

    if uname in users.username.values:
        if passwd == users[users.username == uname].password.item():
            return {'detail':'authorized',
                    'token': users[users.username == uname].access_token.item(),
                    'username':uname
                    }
        else:
            raise HTTPException(
                status_code=400,
                detail='User Not Available'
            )
    else:
        raise HTTPException(
            status_code=400,
            detail='User Not Available'
        )


