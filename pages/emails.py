import streamlit as st
import pandas as pd
from preprocessing import preprocess, add_score_cols, add_interpreted_cols
from retrieval import get_placements_data
import os
from textGenerator import get_client_brief_pdf, warm_up
from retrieval import placementsSource, get_carrier_facing_template_names, get_client_facing_template_names, get_template_body, autofill_template

if "GPT_initialized" not in st.session_state:
    warm_up()
    st.session_state.GPT_initialized = True

if 'body' not in st.session_state:
    st.session_state.body = ''

#getting data
if ("df" not in st.session_state) or ("placements_source" not in st.session_state):
    placements = get_placements_data(
        crm_headers=st.session_state.crm_headers
    )
    preprocess(placements, inplace=True)
    add_interpreted_cols(placements, inplace=True)
    add_score_cols(placements, inplace=True)
    placements_new = placements.copy(deep=True)
    st.session_state.placements_source = placementsSource
    st.session_state.df = placements.copy(deep=True)
    st.session_state.df_og = placements.copy(deep=True)

# website
st.set_page_config(layout="centered")
st.title('E-Mails')

col1, col2, col3 = st.columns([1, 1, 3])

with st.form('email_search'):
    with col1:
        ind = int(st.number_input('Enter Row Index'))

    with col2:
        role = st.selectbox(label='Client/Carrier', options=['client_facing', 'carrier_facing'])

    with col3:
        template = st.selectbox(
            label='Select Template',
            options=get_client_facing_template_names() if(role == 'client_facing') else get_carrier_facing_template_names()
            )   
    submitted = st.form_submit_button()

ser = st.session_state.df.loc[ind, :]

if submitted:
    st.session_state.body = autofill_template(
        template_body=get_template_body(fname=template, role=role),
        data=ser
    )

if 'body' in st.session_state:
    body = st.text_area(
        label=f'modify E-Mail to {role}',
        value= st.session_state.body,
        height='content'
    )
    
    # st.write(p)

with st.form('submission_form'):
    incl = st.radio(label='Include client brief PDF?', options=['Yes', 'No'])
    date = st.date_input(label='Schedule E-Mail', value='today')
    send = st.form_submit_button(label='Send')


if send:
    if incl == 'Yes':
        p = os.path.join(os.getcwd(), 'brief_pdfs', 'email.pdf')
        st.session_state.body += f'\n\n{p}'
        get_client_brief_pdf(data=st.session_state.df, p=p, client_id=st.session_state.df.PlacementClientLocalID[ind], source=st.session_state.placements_source)
        st.markdown(f'Brief PDF attached and saved!')
    st.write(f'E-mail to be sent via MS Graph API on {date}!')