cd .\FastAPI_Scripts
Start-Job -ScriptBlock { uvicorn ColabAPI:app --port 8001 }
Start-Job -ScriptBlock { uvicorn CRMAPI:app --port 8000 }
cd ..