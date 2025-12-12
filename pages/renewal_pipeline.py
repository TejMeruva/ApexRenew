import streamlit as st
import pandas as pd
from preprocessing import preprocess, add_score_cols, add_interpreted_cols
from retrieval import get_placements_data
from textGenerator import get_client_brief
from retrieval import placementsSource

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

#website
st.set_page_config(layout="wide")
st.title('Renewal Pipeline')
col1, col2 = st.columns([3, 1])


with col2:
    st.markdown('##### Filters')
    with st.form('filter_form'):
        col = st.selectbox(label='Select Column', options=list(st.session_state.df.select_dtypes(include='number').columns))
        op = st.selectbox(label="Select Operation", options=['>', '>=', '<', '<=', '=='])
        value = int(st.number_input(label='Enter Value'))
        submitted = st.form_submit_button("Apply Filter")
    if submitted:
        match op:
            case '>':
                st.session_state.df = placements[placements[f'{col}'] > value]
            case '>=':
                st.session_state.df = placements[placements[f'{col}'] >= value]
            case '<':
                st.session_state.df = placements[placements[f'{col}'] < value]
            case '<=':
                st.session_state.df = placements[placements[f'{col}'] <= value]
            case '==':
                st.session_state.df = placements[placements[f'{col}'] == value]
    clearButton = st.button(label='Clear Filter')
    if clearButton:
        st.session_state.df = st.session_state.df_og

with col1:
    st.dataframe(
        data= st.session_state.df
    )

#brief pdf
st.markdown('##### Generate Brief PDF')
with st.form('breif_form'):
    client_id = st.selectbox(label='Enter `PlacementClientLocalID`', options=st.session_state.df.PlacementClientLocalID.unique())
    
    brief_needed = st.form_submit_button('Get Client Brief')
if brief_needed: 
    brief = get_client_brief(client_id=client_id, data=st.session_state.df, source=st.session_state.placements_source)
    st.markdown(brief)


st.space('small')
st.caption('##### Data Source')
st.caption(f'`Title of Service`: {st.session_state.placements_source.service_title}')
st.caption(f'`URL`: {st.session_state.placements_source.request_url}')
st.caption(f'`Table Name`: {st.session_state.placements_source.table_name}')
st.caption('It is to be noted that the data is not stored locally and is fetched freshly from the specified source upon opening of the Renewal Pipeline by the user.')