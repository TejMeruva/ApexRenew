import pandas as pd
# function to generate the brief pdf
# function to generate the e-mail templates
# function to get the recommended actions for each client.
# each function should return a confidence score for each openai output for data completeness

# refer [_prioritization_playground.ipynb] for merged table.

class Template: #template class 
    text: str
    placeholders: list

def get_brief(client_row: pd.Series) -> str: # returns the brief str for the passed client row, refer [_prioritization_playground.ipynb] for merged table.
    pass

def get_template(email_type: str) -> Template: #returns an email template
    pass

def recommended_action(client_row: pd.Series) -> str:
    pass

