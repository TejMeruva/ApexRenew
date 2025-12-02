**28 November 2025** by Teja
1. [Fake Data Generator](RandomDataGenerator.ipynb)
   - uses `Faker` package.
   - used almost the actual schema of clients and policies tables of `Applied Epic API` response body. [Reference](https://www.insuredmine.com/knowledge-base/applied-epic-integration-2/)
   - lognormalvariates were generated for the premium amounts
   - assumptions for premium amount generation:
   - 70% term life (cheaper, smaller variance)
   - 30% whole life (expensive, high variance)
   - Both generated using log-normal approximation via random.lognormvariate().
   - % vroker commision generated as a normalvariate. (8-15%)
   - all insurance assumerd ot be of a term of 20 years. 

2. [CRM_API_Script](FastAPI_Scripts/CRMAPI.py)
   - uses `fastapi` [Reference](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#get-your-own-user-data)
   - made to replicate `AppliedEpic` API. 
   - uses OAuth2.0 tokens using the `fastapi.security` module
   - implements post requests for token retrieval
   - implements get requests for clients, policies tables retrieval

3. [CRMRetrieval_Script](Retrieval_Scripts/CRMRetrieval.py)
   - uses a post request to get the OAuth2.0 token
   - makes get requests to get the clients table and the policies table.

**29 November 2025** by Teja

1. [Fake Data Generator](RandomDataGenerator.ipynb)
   - added `MS Graph API` Fake Data generators. [Reference](https://stackoverflow.com/questions/48448529/different-user-objects-returning-in-microsoft-graph-explorer?utm_source=chatgpt.com)
   - followed the same schema as `MS Graph API`
   - generated the fake data for 3 tables:
     - users
     - calendar events
     - emails
2. [Colab_API_Script](FastAPI_Scripts/ColabAPI.py)
   - made to replicate `MS Graph` API 
   - uses `fastapi`
   - uses OAuth2.0 tokens using the `fastapi.security` module
   - implements post requests for token retrieval
   - implements get requests for clients, policies tables retrieval
3. [boot_script](bootApexRenew.sh)
   - starts and hosts the 2 APIs on different ports (8000, 8001)
   - kind of like a play button for the entire project.
   - will run the future main.py script
4. [prettyPrint](prettyPrint.py)
   - decorator tools for CLI, for preliminary CLI version of ApexRenew
5. [main.py](main.py)
   - completed a primilary CLI version of `ApexRenew` app.
   - obtains useranme and password from the user and then retrieves the tokens from the 2 APIs.
   - obtains the data only on user request.
   - uses `figlet` for CLI art.

**02 December 2025** by Teja 
1. [prioritization.py](prioritization.py)
   - pulls data from `clients` table and `policies` table.