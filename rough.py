from retrieval import autofill_template, get_template_body
from preprocessing import preprocess, add_score_cols, add_interpreted_cols
import os
import pandas as pd

def autofill_template(template_body: str, data: pd.Series) -> str:
    op = 0
    while op != -1:
        # print(op, end='')
        start_ind = 0
        op = template_body.find(r'{')
        if op == -1:
            break
        else:
            start_ind = op
        end_ind = template_body.find(r'}')
        colName = template_body[(start_ind + 2): end_ind]
        to_replace = template_body[start_ind : (end_ind + 2)]
        template_body = template_body.replace(to_replace, data[colName])
        print(to_replace)

    return template_body

#getting data
placements = pd.read_csv('fake_CRM_data\placements.csv')
preprocess(placements, inplace=True)
add_interpreted_cols(placements, inplace=True)
add_score_cols(placements, inplace=True)



text = get_template_body(fname='Additional_Information_To_Carrier.txt', role='carrier_facing')
print(autofill_template(
    template_body=text,
    data=placements.loc[0, :]
))