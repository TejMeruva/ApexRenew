import streamlit as st
from datetime import datetime
from preprocessing import preprocess, add_score_cols, add_interpreted_cols
from retrieval import get_placements_data, placementsSource, get_ms_emails_data, emailsSource, get_templates_data
import matplotlib.pyplot as plt

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
    

if ('emails' not in st.session_state) or ('emails_source' not in st.session_state):
    st.session_state.emails = get_ms_emails_data(st.session_state.colab_headers)
    st.session_state.emails_source = emailsSource

if 'templates_data' not in st.session_state:
    st.session_state.templates_data = get_templates_data()

#website
st.set_page_config(layout="centered")
st.title(f'Hello, {st.session_state.username}!')

col1, col2 = st.columns(2)
data = st.session_state.df


with col1:
    st.write('Key Metrics')
    renewal_count = data[data._DaysToExpiry < 7].shape[0]
    emails = (st.session_state.emails.read_status == 'unread').sum()

    st.metric(label='Renewals Coming Up This Week', 
              value=renewal_count, 
              help=placementsSource.service_title,
              delta = '-3',
              delta_color='inverse' ,
              border=True)
    st.metric(label='Unread E-mails', 
              value=emails, 
              help=emailsSource.service_title, 
              delta='+3', 
              delta_color='inverse', 
              border=True)
    
    st.write('Top Templates')
    st.dataframe(st.session_state.templates_data.sort_values('successPct', ascending=False).head(5))

with col2:
    st.write('Top Clients this Month')
    st.dataframe(data[data._DaysToExpiry < 30.5].sort_values('_ClientPriorityGPA', ascending=False)[['Client', '_ClientPriorityGPA']].head(3))

    st.write('Renewal Progress (2025)')
    countByStatus = data[data.PlacementExpiryDate.apply(lambda x: x.year) == 2025]\
        .groupby(['PlacementRenewingStatusCode'])['PlacementRenewingStatusCode'].agg(['count']).reset_index()
    
    st.bar_chart(
        data = countByStatus, 
        x='PlacementRenewingStatusCode', 
        y='count', 
        height='content'
        )
st.caption('It is to be noted that the data is not stored locally and is fetched freshly from the specified source upon opening of the Dashboard by the user.')