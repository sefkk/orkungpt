# app.py

import streamlit as st
from langchain_helper import execute_user_query
import sys
import sqlite3
sys.modules["pysqlite3"] = sqlite3

# Configure page for mobile with comprehensive settings
st.set_page_config(
    page_title="Orkun GPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Orkun GPT - Your personal AI assistant"
    }
)

# Custom CSS for comprehensive mobile-friendly design
st.markdown("""
<style>
    /* Universal mobile-first responsive design */
    
    /* Extra small phones (320px and up) */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem !important;
            max-width: 100% !important;
            margin-left: 0 !important;
        }
        
        /* Force sidebar to be completely hidden on mobile */
        .stSidebar {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
        }
        
        /* Ensure main content takes full width */
        .main {
            width: 100% !important;
            margin-left: 0 !important;
        }
        
        /* Stack columns on very small screens */
        .stColumns {
            flex-direction: column !important;
        }
        
        .stColumns > div {
            width: 100% !important;
            margin-bottom: 0.5rem;
        }
        
        /* Smaller text on tiny screens */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-size: 1.2rem !important;
        }
        
        .stMarkdown p {
            font-size: 0.9rem !important;
        }
    }
    
    /* Small phones (481px to 768px) */
    @media (min-width: 481px) and (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
            margin-left: 0 !important;
        }
        
        /* Force sidebar to be completely hidden on small phones too */
        .stSidebar {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
        }
        
        /* Ensure main content takes full width */
        .main {
            width: 100% !important;
            margin-left: 0 !important;
        }
    }
    
    /* Tablets and larger phones (769px to 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 1.5rem !important;
        }
        
        .stSidebar {
            width: 300px !important;
        }
    }
    
    /* Enhanced mobile-friendly buttons for all screen sizes */
    .stButton > button {
        width: 100%;
        min-height: 48px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
        touch-action: manipulation;
        -webkit-tap-highlight-color: transparent;
        border: none;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* Mobile-friendly chat input for all devices */
    .stChatInput > div > div > input {
        font-size: 16px !important;
        min-height: 48px !important;
        border-radius: 24px !important;
        padding: 12px 16px !important;
        -webkit-appearance: none;
        -moz-appearance: none;
        appearance: none;
    }
    
    /* Prevent zoom on input focus for iOS */
    @media screen and (-webkit-min-device-pixel-ratio: 0) {
        .stChatInput > div > div > input {
            font-size: 16px !important;
        }
    }
    
    /* Responsive chat messages */
    .stChatMessage {
        margin-bottom: 16px;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    .stChatMessage .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
        word-break: break-word;
    }
    
    /* Responsive columns for different screen sizes */
    @media (max-width: 480px) {
        .stColumns > div {
            width: 100% !important;
            margin-bottom: 0.5rem;
        }
    }
    
    @media (min-width: 481px) and (max-width: 768px) {
        .stColumns > div {
            width: 50% !important;
        }
    }
    
    /* Prevent horizontal scrolling */
    .main .block-container {
        max-width: 100% !important;
        overflow-x: hidden;
    }
    
    /* Responsive text sizing */
    @media (max-width: 480px) {
        .stMarkdown h1 { font-size: 1.5rem !important; }
        .stMarkdown h2 { font-size: 1.3rem !important; }
        .stMarkdown h3 { font-size: 1.1rem !important; }
        .stMarkdown p { font-size: 0.9rem !important; }
    }
    
    @media (min-width: 481px) {
        .stMarkdown h1 { font-size: 2rem !important; }
        .stMarkdown h2 { font-size: 1.5rem !important; }
        .stMarkdown h3 { font-size: 1.2rem !important; }
        .stMarkdown p { font-size: 1rem !important; }
    }
    
    /* Mobile-specific optimizations */
    @media (max-width: 768px) {
        /* Hide unnecessary elements on mobile */
        .stDeployButton {
            display: none !important;
        }
        
        /* Optimize spacing for mobile */
        .stApp > div {
            padding-top: 1rem !important;
        }
        
        /* Better touch targets */
        .stButton > button {
            min-height: 44px !important;
            padding: 12px 16px !important;
        }
        
        /* Prevent text selection on buttons */
        .stButton > button {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Optimize sidebar for mobile */
        .stSidebar .sidebar-content {
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
    }
    
    /* iOS Safari specific fixes */
    @supports (-webkit-touch-callout: none) {
        .stChatInput > div > div > input {
            font-size: 16px !important;
            transform: translateZ(0);
        }
        
        .stButton > button {
            -webkit-tap-highlight-color: transparent;
        }
    }
    
    /* Android Chrome specific fixes */
    @media screen and (-webkit-min-device-pixel-ratio: 0) and (min-resolution: .001dpcm) {
        .stChatInput > div > div > input {
            font-size: 16px !important;
        }
    }
    
    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        .stButton > button {
            border: 0.5px solid rgba(0,0,0,0.1);
        }
    }
    
    /* Enhanced info boxes */
    .orkun-info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .orkun-info-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .orkun-info-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 12px;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    
    .orkun-info-desc {
        font-size: 1.1rem;
        margin-bottom: 12px;
        color: #f0f0f0;
        line-height: 1.5;
    }
    
        .orkun-info-list {
        margin: 0 0 0 20px;
            padding: 0;
            color: #ffffff;
        font-size: 1rem;
        }
    
        .orkun-info-list li {
        margin: 8px 0;
        padding-left: 4px;
        line-height: 1.4;
    }
    
    /* Feature cards - matching app vibe */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.25);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .feature-title {
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 10px;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    
    .feature-desc {
        font-size: 0.95rem;
        opacity: 0.95;
        line-height: 1.5;
        color: #f0f0f0;
    }
    
    /* Mobile chat improvements */
    .stChatMessage {
        margin-bottom: 16px;
    }
    
    .stChatMessage .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
    }
    
    /* Quick action buttons - matching app vibe */
    .quick-action {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px 18px;
        margin: 6px 0;
        width: 100%;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .quick-action::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .quick-action:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .quick-action:hover::before {
        left: 100%;
        }
        </style>
""", unsafe_allow_html=True)

st.title("Orkun GPT")
st.caption("Orkun's personal AI assistant powered by Orkun's documents")

# Mobile-friendly quick actions in main area
st.markdown("### ⚡ Quick Actions")

col1, col2 = st.columns(2)
with col1:
    if st.button("👤 About Orkun", help="Ask about Orkun's background", use_container_width=True):
        query = "Tell me about Orkun's background and experience"
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process the query and get AI response
        with st.spinner("🤔 Thinking..."):
            response = execute_user_query(query)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col2:
    if st.button("🎓 Education", help="Ask about education", use_container_width=True):
        query = "What is Orkun's educational background?"
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process the query and get AI response
        with st.spinner("🤔 Thinking..."):
            response = execute_user_query(query)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

col3, col4 = st.columns(2)
with col3:
    if st.button("💼 Skills", help="Ask about skills", use_container_width=True):
        query = "What are Orkun's technical skills and expertise?"
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process the query and get AI response
        with st.spinner("🤔 Thinking..."):
            response = execute_user_query(query)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

with col4:
    if st.button("🏆 Achievements", help="Ask about achievements", use_container_width=True):
        query = "What are Orkun's key achievements and accomplishments?"
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process the query and get AI response
        with st.spinner("🤔 Thinking..."):
            response = execute_user_query(query)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Clear chat button in main UI for mobile access
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("")  # Empty space for alignment
with col2:
    if st.button("🗑️ Clear Chat", help="Clear all chat messages", use_container_width=True, key="main_clear_chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Orkun GPT. You can ask me anything about Orkun Sefik - his background, skills, education, or achievements. What would you like to know?"}]
        st.rerun()

st.markdown("---")

# Sidebar with enhanced features (only visible on desktop)
with st.sidebar:
    # Desktop-only info section
    st.markdown("""
    <div class="orkun-info-box">
        <div class="orkun-info-title">📚 About Orkun GPT</div>
        <div class="orkun-info-desc">This AI assistant was trained on:</div>
        <ul class="orkun-info-list">
            <li>Orkun's CV & Resume</li>
            <li>University Transcript</li>
            <li>Some Other Personal Info</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Chat Controls
    st.subheader("Chat Controls")
    
    if st.button("🗑️ Clear Chat", help="Clear all chat messages", use_container_width=True, key="sidebar_clear_chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Orkun GPT. You can ask me anything about Orkun Sefik - his background, skills, education, or achievements. What would you like to know?"}]
        st.rerun()
    
    # Export chat option
    if st.button("📥 Export Chat", help="Download chat history", use_container_width=True):
        if "messages" in st.session_state and len(st.session_state.messages) > 1:
            chat_text = "\n\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in st.session_state.messages])
            st.download_button(
                label="Download Chat",
                data=chat_text,
                file_name="orkun_gpt_chat.txt",
                mime="text/plain"
            )
        else:
            st.warning("No chat history to export")
    
    st.markdown("---")
    
    # Features section
    st.subheader("Features")
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Smart Memory</div>
        <div class="feature-desc">Remembers conversation context for better responses</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Smart Search</div>
        <div class="feature-desc">Finds relevant information from all documents</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message to history
    st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm Orkun GPT. You can ask me anything about Orkun Sefik - his background, skills, education, or achievements. What would you like to know?"})

# Main chat interface
# st.markdown("### Chat with Orkun GPT")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input with enhanced mobile experience
if query_text := st.chat_input("Ask me anything about Orkun..."):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(query_text)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query_text})
    
    # Show enhanced thinking indicator
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        with thinking_placeholder.container():
            with st.spinner("🤔 Thinking..."):
                st.markdown("*Analyzing your question and searching through Orkun's documents...*")
        
        # Process the query
        response = execute_user_query(query_text)
        
        # Clear thinking indicator and show response
        thinking_placeholder.empty()
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to show the new messages
    st.rerun()

# Footer with helpful tips
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 20px;">
    💡 <strong>Tip:</strong> Try asking about Orkun's experience, education, skills, or specific projects. 
    The AI has access to his CV, portfolio, and academic records.
</div>
""", unsafe_allow_html=True)
