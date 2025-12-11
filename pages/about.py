import streamlit as st

st.set_page_config(layout="centered")
text = '' 
with open('README.md', 'r') as file:
    text += file.read()
st.markdown(text)