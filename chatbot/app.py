import streamlit as st
from chatbot import workflow
from langchain_core.messages import HumanMessage

with st.sidebar:
    st.title("Settings")
    st.write("Choose Options")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []





# User input
prompt = st.chat_input("Ask Everything...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })


    # Call LangGraph
    initial_state = {
        "messages": [
            HumanMessage(content=prompt)
        ]
    }



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


    with st.chat_message("assistant"):
       ai_msg =  st.write_stream( 
         message_chunk.content for message_chunk , metadata  in  workflow.stream(
           initial_state, 
           config = {"configurable":{"thread_id":"1"}},
           stream_mode= "messages",

       )
        )
       st.session_state.messages.append({
       "role": "assistant",
       "content": ai_msg
        })