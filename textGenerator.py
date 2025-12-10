from openai import OpenAI
from preprocessing import preprocess, add_interpreted_cols, add_score_cols
import pandas as pd

client = OpenAI(api_key='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')

#intial testing
# response = client.responses.create(
#     model="gpt-5-nano",
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# print(response.output_text)

def generate_template():
    pass

def get_suggestions(client_id:str, data: pd.DataFrame):
    question = ''
    question += 'Based on the given information,'
    question += 'Give any suggestions for how I can make this client renew the placement.'
    return get_chatbot_response(
        q= question,
        data=data,
        client_id=client_id
    )

def get_client_id(prompt: str) -> str:
    ref = 'SCR-0b810b6f4c20'
    start_ind = prompt.index('SCR-')
    end_ind = start_ind + len(ref)
    return prompt[start_ind:end_ind]

def get_chatbot_response(q: str, data: pd.DataFrame, client_id: str = None) -> str:
    if client_id is None:
        client_id = get_client_id(q)
    if not (client_id in data.PlacementClientLocalID.to_list()):
        return f'Client ID {client_id} not found'
    client_ser = data.loc[data.PlacementClientLocalID == client_id, :]
    prompt = ''

    prompt += 'I am an insurance broker and I have some data about a client:\n'
    prompt += 'a few scores, each out of 10 were calculated for the client as specified:\n'
    prompt += 'premium at risk: one-tenth the percentile of each sample'
    prompt += 'time to expiry: one-tenth of (100 - percentile of the days to expiry)'
    prompt += 'past performance (of carrier): one-tenth of the percentile of the fraction of placements renewed for each carrier'
    prompt += 'past performance (of client): one-tenth of the percentile of the fraction of the placements renewed for each client'
    prompt += 'carrier responsiveness: one-tenth of (100 - percentile of the days taken for response)*'
    prompt += 'churn_prob_score: one-tenth of (100 - precentile of the churn probability as predicted by a trained XGBClassifier)'
    prompt += 'here is all the information I have about the client, in the form of a csv table:'
    prompt += client_ser.to_csv()
    prompt += '\nAnswer the following question based on the provided information:\n'
    prompt += q
    
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


def get_client_brief(client_id:str, data: pd.DataFrame):
    question = ''
    question += 'Generate a brief about this client, preferably in tabular form, mentioning all the information about the client, relevant numbers/metrics and their inferences.'
    question += 'For each score, meantion the meaning of the score.'
    question += 'Give any suggestions for how I can make this client renew the placement.'
    return get_chatbot_response(
        q= question,
        data=data,
        client_id=client_id
    )

def get_client_id(prompt: str) -> str:
    ref = 'SCR-0b810b6f4c20'
    start_ind = prompt.index('SCR-')
    end_ind = start_ind + len(ref)
    return prompt[start_ind:end_ind]


data = pd.read_csv('fake_CRM_data\\placements.csv')
preprocess(data, inplace=True)
add_interpreted_cols(data, inplace=True)
add_score_cols(data, inplace=True)
print()
q = input('Enter Question: ')
print(get_suggestions('SCR-51dd14cf0f45', data))
# print(get_client_id('blah blah blah bkaha feihfoeihwf febfeo SCR-0b810b6f4c20 meow meow mwogjroiewgnoea j94u3985u3498nfkls jsd'))