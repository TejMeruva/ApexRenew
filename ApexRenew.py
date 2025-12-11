import streamlit as st
import os

# --- Protect all pages: if no token & not on login page → redirect ---
if "crm_headers" not in st.session_state:
    st.session_state.crm_headers = None

if "colab_headers" not in st.session_state:
    st.session_state.colab_headers = None

current_page = st.context.page.page_path if hasattr(st.context, "page") else None

if st.session_state.crm_headers is None:
    st.switch_page(os.path.join('pages', 'applied_epic_login.py'))

if st.session_state.colab_headers is None:
    st.switch_page(os.path.join('pages', 'ms_teams_login.py'))

#setting up navigation
dashboard_page = st.Page(os.path.join('pages', 'dashboard.py'), title="Dashboard")
chatbot_page = st.Page(os.path.join('pages', 'chatbot.py'), title="Chatbot")
renewal_pipeline_page = st.Page(os.path.join('pages', 'renewal_pipeline.py'), title='Renewal Pipeline')
about_page = st.Page(os.path.join('pages', 'about.py'), title='About')
emails_page = st.Page(os.path.join('pages', 'emails.py'), title='E-Mails')

pg = st.navigation([
    dashboard_page,
    chatbot_page,
    renewal_pipeline_page,
    emails_page,
    about_page
], position='top')
st.set_page_config(page_title="ApexRenew Dashbaord")
pg.run()

#logo
st.logo(
    os.path.join('pages', 'icons', 'ApexRenewLogo.png'),
    size='medium'
    )