import pandas as pd
from scipy.stats import percentileofscore

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