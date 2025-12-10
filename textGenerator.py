from openai import OpenAI
from preprocessing import preprocess, add_interpreted_cols, add_score_cols
import pandas as pd
from transformers import pipeline
import torch
import os
from retrieval import DataSource

client = OpenAI(api_key='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')

device = 'mps' if torch.backends.mps.is_available() else 'cpu'

classifier = pipeline(
    task = 'zero-shot-classification',
    model = 'facebook/bart-large-mnli',
    device=device        
)

def warm_up():
    try:
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": ""}]
        )
        print("Model warmed up.")
    except Exception as e:
        print(f"Warmup failed: {e}")

def generate_template():
    pass

def get_suggestions(client_id:str, data: pd.DataFrame, source: DataSource):
    question = ''
    question += 'Based on the given information,'
    question += 'Give any suggestions for how I can make this client renew the placement.'
    return get_chatbot_response(
        q= question,
        data=data,
        source=source,
        client_id=client_id
    )

def get_chatbot_response(q: str, data: pd.DataFrame, source: DataSource, client_id: str = None, confidence=False) -> str:
    if client_id is None:
        client_id = get_client_id(q)
        if client_id == 'ID not provided' : return 'Provide the ID of the Client.'
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
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

    op = response
    op += f'\n\nSources:\n{source}'
    if confidence:
        op += f'\n\nConfidence Score (derived using Zero Shot Classification):\n'
        op += f'{get_confidence_score(q, response)}'

    return op


def get_client_brief(client_id:str, data: pd.DataFrame, source: DataSource):
    question = ''
    question += 'Generate a brief about this client, preferably in tabular form, mentioning all the information about the client, relevant numbers/metrics and their inferences.'
    question += 'For each score, meantion the meaning of the score.'
    question += 'Give any suggestions for how I can make this client renew the placement.'
    return get_chatbot_response(
        q= question,
        data=data,
        client_id=client_id,
        source=source
    )

def get_client_id(prompt: str) -> str:
    ref = 'SCR-0b810b6f4c20'
    start_ind = 0
    try:
        start_ind = prompt.index('SCR-')
    except ValueError:
        return 'ID not provided'
    end_ind = start_ind + len(ref)
    return prompt[start_ind:end_ind]

def get_confidence_score(q: str, response: str, classifier = classifier) -> float:
    inp = ''
    inp += 'The following question was asked:\n\n'
    inp += q
    inp += '\n\nThe following answer was given:\n\n'
    inp += response

    labels = ['answer is correct', 'answer is incorrect']
    res = classifier(inp, candidate_labels=labels)
    op = dict(zip(res['labels'], res['scores']))['answer is correct']
    return op



# data = pd.read_csv(os.path.join('fake_CRM_data', 'placements.csv'))
# preprocess(data, inplace=True)
# add_interpreted_cols(data, inplace=True)
# add_score_cols(data, inplace=True)
# print()
# q = input('Enter Question: ')

# AppliedEpicAPI = DataSource(
#     request_url='https://localhost::8000/placements',
#     service_title='Mock Applied Epic (CRM) API',
#     table_name='placements'
# )

# print(get_chatbot_response(
#     q='How reliable is SCR-dd20d4b02b6b?',
#     data=data,
#     source=AppliedEpicAPI,
#     confidence=True
# ))
# # print(get_client_id('blah blah blah bkaha feihfoeihwf febfeo SCR-0b810b6f4c20 meow meow mwogjroiewgnoea j94u3985u3498nfkls jsd'))
