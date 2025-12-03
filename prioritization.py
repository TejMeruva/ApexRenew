import pandas as pd
from scipy.stats import percentileofscore
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

def sentiment_score(nps_score_col: pd.Series) -> pd.Series:
    get_score = lambda x: (percentileofscore(
                    a=nps_score_col,
                    score=x
                ))/10
    return nps_score_col.apply(get_score)

def client_responsiveness_score(time_per_col: pd.Series) -> pd.Series:
    get_score = lambda x: (100 - percentileofscore(
                    a=time_per_col,
                    score=x
                ))/10
    return time_per_col.apply(get_score)

def not_churn_prob_score(premium_amount_col: pd.Series,
                     avg_days_between_logins_col: pd.Series,
                     avg_user_sentiment_score_col: pd.Series):
    scaler = joblib.load(os.path.join('models', 'scaler.pkl'))
    model = joblib.load(os.path.join('models', 'churn_predictor.pkl'))
    X = pd.concat([premium_amount_col, avg_days_between_logins_col, avg_user_sentiment_score_col], axis=1).to_numpy()
    X = scaler.transform(X)

    pred = pd.Series(model.predict(X).argmax(axis=1)).apply(lambda x: ['churn', 'not_churn'][x])

    return model.predict_proba(X)[:, 1] * 10 # prob for not_churn

def client_priority_GPA(df:pd.DataFrame)->pd.Series:
    time_to_expiry_score_wt = 1
    premium_at_risk_score_wt = 1
    sentiment_score_wt = 1
    client_responsiveness_score_wt = 1
    not_churn_prob_score_wt = 1
    return (time_to_expiry_score_wt * time_to_expiry_score(df._time_to_expiry_days)
            + premium_at_risk_score_wt * premium_at_risk_score(df.premium_amount)
            + sentiment_score_wt * sentiment_score(df.avg_user_sentiment_score) 
            + client_responsiveness_score_wt * client_responsiveness_score(df.avg_days_between_logins)
            + not_churn_prob_score_wt * not_churn_prob_score(df.premium_amount, df.avg_days_between_logins, df.avg_user_sentiment_score))/5