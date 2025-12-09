import pandas as pd
from datetime import datetime, timedelta
from prioritization import time_to_expiry_score, \
    premium_at_risk_score, past_performance_score, \
        churn_prob_score, client_priority_GPA

def preprocess(data: pd.DataFrame, inplace=False) -> pd.DataFrame:
    if not inplace:
        data = data.copy(deep=True) # not inplace
    # chaning column names to camelCase
    def camelCase(names: list) -> list:
        return [name\
                .strip() \
                .replace('_', ' ') \
                #   .title() \
                .replace(' ', '') \
                .replace('(', '_') \
                .replace(')', '') \
                for name in names]
    
    #changing dtypes
    def setColsToDatetime(df: pd.DataFrame, cols: list) -> None:
        for col in cols:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='ignore')

    data.columns = camelCase(data.columns)
    data.rename({'PlacementCreatedDate/Time': 'PlacemenCreatedDatetime'}, inplace=True)

    for col in data.columns:
        data[col] = data[col].replace('-', pd.NA)

    setColsToDatetime(
        df=data, 
        cols=\
            ['ResponseReceivedDate', 'PlacementEffectiveDate',
        'PlacementExpiryDate', 'SubmissionSentDate']
    )

    return data

def add_interpreted_cols(data: pd.DataFrame, inplace=False) -> pd.DataFrame:

    def fracRenewed(group):
        x = group[group == 'N'].size
        y = group.size
        return x/(x+y)
    
    if not inplace:
        data = data.copy(deep=True) # not inplace

    #adding interpreted columns
    data['_DaysToExpiry'] = (data.PlacementExpiryDate - data.PlacementEffectiveDate).apply(lambda x: x.days)
    data['_CarrierResponseTime'] = (data.ResponseReceivedDate - data.SubmissionSentDate).apply(lambda x: x.days)

    # client past performance
    fracPlacementsRenewedByClient = data.groupby(['PlacementClientLocalID'])['_ChurnStatus'].agg(fracRenewed)
    clients = fracPlacementsRenewedByClient.index.unique()
    data['_FracPlacementsRenewedByClient'] = pd.Series([0. for _ in range(data.shape[0])], dtype='float')
    for client in clients:
        clientMask = (data.PlacementClientLocalID == client)
        data.loc[clientMask, '_FracPlacementsRenewedByClient'] = fracPlacementsRenewedByClient[client]

    # carrier past performance
    fracPlacementsRenewedByCarrier = data.groupby(['CarrierGroupLocalID'])['_ChurnStatus'].agg(fracRenewed)
    carriers = fracPlacementsRenewedByCarrier.index.unique()
    data['_FracPlacementsRenewedByCarrier'] = pd.Series([0. for _ in range(data.shape[0])], dtype='float')
    for carrier in carriers:
        carrierMask = (data.CarrierGroupLocalID == carrier)
        data.loc[carrierMask, '_FracPlacementsRenewedByCarrier'] = fracPlacementsRenewedByCarrier[carrier]

    return data

def add_score_cols(data: pd.DataFrame, inplace=False) -> pd.DataFrame:
    if not inplace:
        data = data.copy(deep=True) # not inplace
    data['_TimeToExpiryScore'] = time_to_expiry_score(data._DaysToExpiry)
    data['_PremiumAtRiskScore'] = premium_at_risk_score(data.TotalPremium)
    data['_ClientPastPerformanceScore'] = past_performance_score(data._FracPlacementsRenewedByClient)
    data['_CarrierPastPerformanceScore'] = past_performance_score(data._FracPlacementsRenewedByCarrier)
    data['_ChurnProbScore'] = churn_prob_score(data)
    data['_ClientPriorityGPA'] = client_priority_GPA(data)

    return data
    