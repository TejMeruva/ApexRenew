**28 November 2025** by Teja
1. [Fake Data Generator](CRMDataGenerator.ipynb)
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
   - uses OAuth2.0 tokens using the fastapi.security module

3. [CRMRetrieval_Script](Retrieval_Scripts/CRMRetrieval.py)
   - uses a post request to get the OAuth2.0 token
   - makes get requests to get the clients table and the policies table. 