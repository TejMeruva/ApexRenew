import streamlit as st
import pandas as pd
from textGenerator import warm_up, get_chatbot_response
from retrieval import get_placements_data, placementsSource, DataSource
from preprocessing import preprocess, add_interpreted_cols, add_score_cols



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# warming up gpt    
if "GPT_initialized" not in st.session_state:
    warm_up()
    st.session_state.GPT_initialized = True

#getting data
placements = pd.DataFrame()

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

# website
st.set_page_config(layout="centered")
st.title("ApexRenew Chatbot")
if st.session_state.GPT_initialized:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"{get_chatbot_response(q=prompt, data=st.session_state.df, confidence=True, source=st.session_state.placements_source)}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})