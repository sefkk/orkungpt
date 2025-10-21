# app.py

import streamlit as st
from langchain_helper import execute_user_query
import sys
import sqlite3
sys.modules["pysqlite3"] = sqlite3


st.title("Orkun GPT")

# Sidebar with clear chat button
with st.sidebar:
    # Custom CSS for a prettier info box
    st.markdown(
        """
        <style>
        * {
            transition: transform 0.3s ease;
        }

        button, .stButton>button {
            transition: transform 0.3s ease;
        }

        .orkun-info-box {
            background-color: #1e1e2f; 
            color: #f0f0f0; 
            border-radius: 12px;
            padding: 18px 22px 15px 20px;
            margin-bottom: 18px;
            box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.8); 
        }

        .orkun-info-box:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.8); 
        }

        .orkun-info-title {
            font-size: 1.32rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: #ffffff; 
            letter-spacing: 0.6px;
        }
        .orkun-info-desc {
            font-size: 1.03rem;
            margin-bottom: 10px;
            color: #ffffff;
        }
        .orkun-info-list {
            margin: 0 0 0 18px;
            padding: 0;
            color: #ffffff;
            font-size: 0.99rem;
        }
        .orkun-info-list li {
            margin: 2px 0;
            padding-left: 2px;
        }
        </style>
        <div class="orkun-info-box">
            <div class="orkun-info-title">Info about Orkun GPT</div>
            <div class="orkun-info-desc">This GPT was created using the following data:</div>
            <ul class="orkun-info-list">
                <li>Orkun's CV</li>
                <li>Orkun's personal portfolio</li>
                <li>Orkun's university course grades</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.header("Chat Controls")
    if st.button("Clear Chat", help="Clear all chat messages", use_container_width=True):
        # Clear messages but preserve the welcome message
        st.session_state.messages = [{"role": "assistant", "content": "Hi, You can ask me anything about Orkun Sefik!"}]
        st.rerun()

    # st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message to history
    st.session_state.messages.append({"role": "assistant", "content": "Hi, You can ask me anything about Orkun Sefik!"})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if query_text := st.chat_input("Ask anything!"):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(query_text)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query_text})
    
    # Show thinking indicator
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        with thinking_placeholder.container():
            st.markdown("*Thinking...*")
        
        # Process the query
        response = execute_user_query(query_text)
        
        # Clear thinking indicator and show response
        thinking_placeholder.empty()
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to show the new messages
    st.rerun()
