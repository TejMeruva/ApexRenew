import streamlit as st
import pandas as pd
from preprocessing import preprocess, add_score_cols, add_interpreted_cols
from retrieval import get_placements_data
from textGenerator import get_client_brief
from retrieval import placementsSource, get_carrier_facing_template_names, get_client_facing_template_names, get_template_body, autofill_template

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

col1, col2 = st.columns([3, 1])

with st.form('email_info'):
    with col1:
        clients = st.session_state.df.Client.unique().tolist()
        carriers = st.session_state.df.CarrierGroup.unique().tolist()
        recipient = st.selectbox(label='To', options=clients + carriers)

    with col2:
        role = st.selectbox(label='Client/Carrier', options=['client_facing', 'carrier_facing'])

    template = st.selectbox(
        label='Select Template',
        options=get_client_facing_template_names() if( role == 'client_facing') else get_carrier_facing_template_names()
        )   
    
    submitted = st.form_submit_button()

if submitted:
    ser = st.session_state.df.loc[st.session_state.df.PlacementClientLocalID == recipient, :].any()
    body = st.text_area(label=f'E-Mail to {role}', 
                        value=ser,
                        height='content'
                        )