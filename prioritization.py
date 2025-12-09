import pandas as pd
from scipy.stats import percentileofscore
from sklearn.compose._column_transformer import ColumnTransformer
from sklearn.preprocessing._label import LabelEncoder
from xgboost.sklearn import XGBClassifier
import os 
import joblib
import os

def time_to_expiry_score(time_to_expiry_col: pd.Series) -> pd.Series:
    get_score = lambda x: (100 - percentileofscore(
                    a=time_to_expiry_col,
                    score=x
                ))/10
    return time_to_expiry_col.apply(get_score)

def premium_at_risk_score(premium_col: pd.Series) -> pd.Series:
    get_score = lambda x: (percentileofscore(
                    a=premium_col,
                    score=x
                ))/10
    return premium_col.apply(get_score)

def past_performance_score(frac_renewals_col: pd.Series) -> pd.Series:
    get_score = lambda x: (percentileofscore(
                    a=frac_renewals_col,
                    score=x
                ))/10
    return frac_renewals_col.apply(get_score)

def churn_prob_score(data: pd.DataFrame) -> pd.Series:
    transformer:ColumnTransformer = joblib.load(os.path.join('models', 'data_transformer.pkl'))
    features:list = joblib.load(os.path.join('models', 'features.pkl'))
    label_encoder: LabelEncoder = joblib.load(os.path.join('models', 'label_encoder.pkl'))
    model: XGBClassifier = joblib.load(os.path.join('models', 'churn_model.pkl'))

    X = data[features]
    X.PlacementClientSegmentCode.replace(pd.NA, 'null', inplace=True)
    X.IncumbentIndicator.replace(pd.NA, 'null', inplace=True)
    y = data[['_ChurnStatus']]
    XTf = transformer.transform(X)

    ser = pd.Series(model.predict_proba(XTf)[:, 0])

    get_score = lambda x: (100 - percentileofscore(
                    a=ser,
                    score=x
                ))/10
    return ser.apply(get_score)

def client_priority_GPA(data: pd.DataFrame) -> list:
    weights = {
        'time_to_expiry': 0.013407330790384362,
        'premium_at_risk': 0.02308539217907349,
        'client_past_performance': 0.343102480247099,
        'carrier_past_performance': 0.0146269602786327,
        'churn_prob': 0.6057778365048104
        }
    
    sers = {
    '_TimeToExpiryScore' : time_to_expiry_score(data._DaysToExpiry),
    '_PremiumAtRiskScore' : premium_at_risk_score(data.TotalPremium),
    '_ClientPastPerformanceScore' : past_performance_score(data._FracPlacementsRenewedByClient),
    '_CarrierPastPerformanceScore' : past_performance_score(data._FracPlacementsRenewedByCarrier),
    '_ChurnProbScore' : churn_prob_score(data)
    }

    op = pd.Series([0. for _ in range(data.shape[0])], dtype='float')

    for ind in range(len(weights)):
        op += list(weights.values())[ind] * list(sers.values())[ind]

    return op
 
def justify(data: pd.DataFrame) -> pd.Series:

    def get_comment(row):
        return f'date of expiry is {row.iloc[0]},\npreimum at risk is {row.iloc[1]},\nclient has had {row.iloc[2]} renewals in the past\nCarrier has had {row.iloc[3]} renewals in the past\nChurn probability is {row.iloc[4]}'
    scores = [
        time_to_expiry_score(data._DaysToExpiry),
        premium_at_risk_score(data.TotalPremium),
        past_performance_score(data._FracPlacementsRenewedByClient),
        past_performance_score(data._FracPlacementsRenewedByCarrier),
        churn_prob_score(data),
        client_priority_GPA(data)
    ]

    time_to_expiry_str = pd.Series(pd.cut(scores[0], bins=3, labels=['far', 'near', 'very near']))
    premium_at_risk_str = pd.Series(pd.cut(scores[1], bins=3, labels=['less', 'moderate', 'high']))
    client_past_performance_str = pd.Series(pd.cut(scores[2], bins=3, labels=['less', 'moderate', 'high']))
    carrier_past_performance_str = pd.Series(pd.cut(scores[3], bins=3, labels=['less', 'moderate', 'high']))
    churn_prob_str = pd.Series(pd.cut(scores[4], bins=3, labels=['high', 'moderate', 'low']))

    return pd.concat([time_to_expiry_str,
                      premium_at_risk_str,
                      client_past_performance_str,
                      carrier_past_performance_str,
                      churn_prob_str
                      ], axis=1).apply(get_comment, axis=1)