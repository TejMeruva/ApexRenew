#!/usr/bin/env zsh

cd '/Users/msreeramulu/SWD/ML/Sigma/TechFest/ApexRenew/'
source venv/bin/activate
cd 'FastAPI_Scripts'

wait_for_port() {
    local port=$1
    echo "Waiting for port $port to open..."

    # Keep checking until something is listening on the port
    while ! nc -z localhost $port 2>/dev/null; do
        sleep 0.5
    done

    echo "Port $port is active!"
}

uvicorn ColabAPI:app --port 8001 --reload &
PID1=$!
echo 'Colab API Started...'

wait_for_port 8001
uvicorn CRMAPI:app --port 8000 --reload &
echo 'CRM API Started...'
PID2=$!

wait_for_port 8000
cd '/Users/msreeramulu/SWD/ML/Sigma/TechFest/ApexRenew/'
python3 main.py
PID3=$!

trap "echo 'Stopping APIs...'; kill $PID1 $PID2 $PID3; exit" INT
wait
