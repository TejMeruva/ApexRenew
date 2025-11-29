#!/usr/bin/env zsh

cd '/Users/msreeramulu/SWD/ML/Sigma/TechFest/ApexRenew/'
source venv/bin/activate
cd 'FastAPI_Scripts'

uvicorn ColabAPI:app --port 8001 --reload &
PID1=$!
echo 'Colab API Started...'

uvicorn CRMAPI:app --port 8000 --reload &
echo 'CRM API Started...'
PID2=$!

trap "echo 'Stopping APIs...'; kill $PID1 $PID2; exit" INT

cd '/Users/msreeramulu/SWD/ML/Sigma/TechFest/ApexRenew/'
python3 main.py
