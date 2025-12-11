import streamlit as st
from retrieval import get_colab_headers
import os

st.title("Login to MS Teams")
st.logo(
    os.path.join('pages', 'icons', 'ApexRenewLogo.png'),
    size='medium'
    )

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:

    st.session_state.colab_headers = get_colab_headers(uname=username, passwd=password)
    st.switch_page('ApexRenew.py')