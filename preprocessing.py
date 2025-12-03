import pandas as pd
from datetime import datetime, timedelta
from prioritization import time_to_expiry_score, premium_at_risk_score, sentiment_score, client_responsiveness_score, not_churn_prob_score, client_priority_GPA, justify

def get_merged(clients: pd.DataFrame,
               policies: pd.DataFrame) -> pd.DataFrame:
    clients.issued_on = pd.to_datetime(clients.issued_on)
    clients.updated_on = pd.to_datetime(clients.updated_on)

    policies.expiry_date = pd.to_datetime(policies.expiry_date)
    policies.last_updated = pd.to_datetime(policies.last_updated)
    policies.issued_on = pd.to_datetime(policies.issued_on)

    merged = pd.merge(left=clients, right=policies, how='right', on='client_id')
    return merged

def add_interpreted_cols(merged: pd.DataFrame,
                         today=datetime(year=2025, month=11, day=28)) -> pd.DataFrame:
    merged['_time_to_expiry_days'] = (today - merged.expiry_date).apply(lambda x: x.days)
    return merged

def add_score_cols(merged: pd.DataFrame) -> pd.DataFrame:
    merged['time_to_expiry_score'] = time_to_expiry_score(merged['_time_to_expiry_days'])
    merged['premium_at_risk_score'] = premium_at_risk_score(merged['premium_amount'])
    merged['client_sentiment_score'] = sentiment_score(merged['avg_user_sentiment_score'])
    merged['client_activity_score'] = client_responsiveness_score(merged['avg_days_between_logins'])
    merged['not_churn_prob_score'] = not_churn_prob_score(merged.premium_amount, merged.avg_days_between_logins, merged.avg_user_sentiment_score)
    merged['client_priority_GPA'] = client_priority_GPA(merged)
    merged['justification'] = justify(merged)

    return merged

