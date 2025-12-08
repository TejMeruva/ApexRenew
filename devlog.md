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
   - all scoring guidelines specified in [PrioritizationPlayground](_prioritization_playground.ipynb)
   - finalized guidelines implemented in [prioritization.py](prioritization.py)
   - scoring similar to calcualtion GPA.
   - factors affecting GPA:
     - time to expiry score (out of 10)
     - premium at risk score (out of 10)
     - user sentiment score (based on avg rating form Net Prmotor Surveys)
     - client past performance (based on frequesncy of user logins)
     - likelihood of churn (predicted by XGB model)
2. [churn_model for churn score components of GPA](models\churn_rate_predictor.ipynb)
   - made more fake data using [RandomDataGenerator](RandomDataGenerator.ipynb) for training the `XGB Model`.
   - different factors affecting churn status:
     - avg_user_sentiment_score (from NPS Surveys)
     - avg_days_between_logins
     - premium_amount
   - weights for churn or not churn in random sample decided using these factors and activating using `sigmoid function`.
   - generated assumed churn state (using guidelines detailed in the ipynb file.), using the `random.choices` function.
   - trained `XGB Model` for classification.
   - saved the model and wrote `not_churn_prob_score` in [prioritization](prioritization.py) module
3. [RandomDataGenerator.ipynb](RandomDataGenerator.ipynb)
   - prevented the duplication of ids.

**03 December 2025** by Teja 
1. [client_priority_GPA](prioritization.py)
   - created the function that finds prioritization scores of clients.
   - added `justification string` for interpretability.
2. [RF Model](models/churn_rate_predictor.ipynb)
   - generated weights for each of the factors affection `client_priority_GPA` by training an `RF Model`.
3. [main.py](main.py)
   - added the option to see the top clients.

**8 December 2025**
1. [incorporating_new_data](_dataAnalysis.ipynb)
   - understood the kind of data provided in [dataAnalysis.ipynb](_dataAnalysis.ipynb)
   - corrections made in provided data:
     - changed `1026-01-08` in the PlacementsExpiryDate Column to `08/01/26` to make the date actually possible.
   - changes made:
     - replace policies table and clients table with provided table: [placements.csv](fake_CRM_data\placements.csv) i.e., the `merged` table is now replaced by a sinlge cohesive table which is the table they provided. 
     - modified [CRM_API](FastAPI_Scripts\CRMAPI.py)
     - modified [Retrieval](D:\TejaMeruva\ApexRenew\retrieval.py) module.
     - modified [main](main.py).
     - modified [prioritzation](prioritization.py)
     - modified [preprocessing](preprocessing.py)
2. [prioritization_scheme](prioritization.py)
   - the following factors are rated out of 10:
     - premium at risk: *one-tenth the percentile of each sample*
     - time to expiry: *one-tenth of (100 - percentile of the days to expiry)*
     - claims (no columns available)
     - past performance (of carrier): *10 times the percentile of the fraction of placements renewed for each carrier*
     - past performance (of client): *10 times the percentile of the fraction of the placements renewed for each client*
     - carrier responsiveness: *one-tenth of (100 - percentile of the days taken for response)*
     - likelihood of chrun