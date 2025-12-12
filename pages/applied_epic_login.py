import streamlit as st
from retrieval import get_crm_headers
import os

if 'username' not in st.session_state:
    st.session_state.username = ''

st.set_page_config(layout="centered")
st.title("Login to Applied Epic")

st.logo(
    os.path.join('pages', 'icons', 'ApexRenewLogo.png'),
    size='medium'
    )

with st.form("login_form"):
    username = st.text_input("Username")
    
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    st.session_state.username = username
    st.session_state.crm_headers = get_crm_headers(uname=username, passwd=password)
    st.switch_page('ApexRenew.py')