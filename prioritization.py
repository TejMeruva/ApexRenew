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

    # pred = pd.Series(model.predict(X).argmax(axis=1)).apply(lambda x:  ['churn', 'not_churn'][x])
    op = model.predict_proba(X)[:, 1] * 10
    
    return pd.Series(op, name='not_churn_prob') # prob for not_churn

def client_priority_GPA(df:pd.DataFrame) -> pd.Series:
    time_to_expiry_score_wt = 0.154170 # weights from RF Model 
    premium_at_risk_score_wt = 0.210162
    sentiment_score_wt = 0.205210
    client_responsiveness_score_wt = 0.228554
    not_churn_prob_score_wt = 0.201903
    return (time_to_expiry_score_wt * time_to_expiry_score(df._time_to_expiry_days)
            + premium_at_risk_score_wt * premium_at_risk_score(df.premium_amount)
            + sentiment_score_wt * sentiment_score(df.avg_user_sentiment_score) 
            + client_responsiveness_score_wt * client_responsiveness_score(df.avg_days_between_logins)
            + not_churn_prob_score_wt * not_churn_prob_score(df.premium_amount, df.avg_days_between_logins, df.avg_user_sentiment_score)) \
            /(time_to_expiry_score_wt + premium_at_risk_score_wt + sentiment_score_wt + client_responsiveness_score_wt + not_churn_prob_score_wt)

def justify(df: pd.DataFrame) -> pd.Series:

    def get_comment(row):
        return f'date of expiry is {row.iloc[0]},\npreimum at risk is {row.iloc[1]},\nclient satisfaction with company is {row.iloc[2]},\nclient responsiveness is {row.iloc[3]},\nchurn probability is {row.iloc[4]}'
    scores = [
    time_to_expiry_score(df._time_to_expiry_days),
    premium_at_risk_score(df.premium_amount),
    sentiment_score(df.avg_user_sentiment_score),
    client_responsiveness_score(df.avg_days_between_logins),
    not_churn_prob_score(df.premium_amount, df.avg_days_between_logins, df.avg_user_sentiment_score)
    ]

    time_to_expiry_str = pd.Series(pd.cut(scores[0], bins=3, labels=['far', 'near', 'very near']))
    premium_at_risk_str = pd.Series(pd.cut(scores[1], bins=3, labels=['less', 'moderate', 'high']))
    sentiment_str = pd.Series(pd.cut(scores[2], bins=3, labels=['low', 'moedrate', 'high']))
    client_responsiveness_str = pd.Series(pd.cut(scores[3], bins=3, labels=['low', 'moedrate', 'high']))
    not_churn_prob_str = pd.Series(pd.cut(scores[4], bins=3, labels=['high', 'moedrate', 'low']))

    return pd.concat([time_to_expiry_str, premium_at_risk_str, sentiment_str, client_responsiveness_str, not_churn_prob_str], axis=1).apply(get_comment, axis=1)

