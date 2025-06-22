"""
Streamlit Chat Application for Business Analyst Agent
Interfaces with the Flask API backend to provide a user-friendly chat interface.
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configuration
FLASK_API_URL = "https://dc01-39-62-194-48.ngrok-free.app"

# Page configuration
st.set_page_config(
    page_title="Business Analyst Agent Chat",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_api_health():
    """Check if the Flask API is running."""
    try:
        response = requests.get(f"{FLASK_API_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except requests.exceptions.RequestException:
        return False, None

def send_chat_message(message, user_id):
    """Send a chat message to the Flask API."""
    try:
        payload = {
            "message": message,
            "user_id": user_id
        }
        response = requests.post(
            f"{FLASK_API_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Connection error: {str(e)}"}

def get_business_data(query_type, user_id, report_type=None):
    """Get business data from the Flask API."""
    try:
        params = {
            "type": query_type,
            "user_id": user_id
        }
        if report_type:
            params["report_type"] = report_type
            
        response = requests.get(
            f"{FLASK_API_URL}/data",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Connection error: {str(e)}"}

def get_sessions(user_id):
    """Get session information from the Flask API."""
    try:
        params = {"user_id": user_id}
        response = requests.get(
            f"{FLASK_API_URL}/sessions",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return False, {"error": f"Connection error: {str(e)}"}

def main():
    st.title("📊 Business Analyst Agent")
    st.markdown("Your AI-powered business assistant for CRM, financial management, and business analytics!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "user_id" not in st.session_state:
        st.session_state.user_id = "huzaifa_ejaz"
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # User ID input
        user_id = st.text_input(
            "User ID",
            value=st.session_state.user_id,
            help="Enter your user ID for personalized data"
        )
        st.session_state.user_id = user_id
        
        # API Health Check
        st.subheader("🔍 API Status")
        health_status, health_data = check_api_health()
        
        if health_status:
            st.success("✅ API is running")
            if health_data:
                with st.expander("API Details"):
                    st.json(health_data)
        else:
            st.error("❌ API is not responding")
            st.warning("Make sure your Flask app is running on http://localhost:5000")
        
        st.divider()
        
        # Quick Business Data Queries
        st.subheader("📊 Quick Queries")
        
        if st.button("💰 Business Insights"):
            if health_status:
                with st.spinner("Getting business insights..."):
                    success, data = get_business_data("insights", user_id)
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        if st.button("📈 Revenue Report"):
            if health_status:
                with st.spinner("Getting revenue report..."):
                    success, data = get_business_data("report", user_id, "revenue")
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        if st.button("💸 Expense Report"):
            if health_status:
                with st.spinner("Getting expense report..."):
                    success, data = get_business_data("report", user_id, "expenses")
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        if st.button("👥 Contact Report"):
            if health_status:
                with st.spinner("Getting contact report..."):
                    success, data = get_business_data("report", user_id, "contacts")
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        if st.button("📋 Invoice Report"):
            if health_status:
                with st.spinner("Getting invoice report..."):
                    success, data = get_business_data("report", user_id, "invoices")
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        if st.button("🔍 Raw Data"):
            if health_status:
                with st.spinner("Getting raw data..."):
                    success, data = get_business_data("raw", user_id)
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        st.divider()
        
        # Session Information
        st.subheader("📝 Session Info")
        if st.button("Show Sessions"):
            if health_status:
                with st.spinner("Getting session info..."):
                    success, data = get_sessions(user_id)
                    if success:
                        st.json(data)
                    else:
                        st.error(f"Error: {data.get('error', 'Unknown error')}")
        
        # Clear Chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Chat with your Business Agent")
    
    # Check API status for main interface
    if not health_status:
        st.error("⚠️ Cannot connect to the Business Agent API. Please ensure the Flask app is running.")
        st.info("To start the Flask app, run: `python main.py`")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show metadata for assistant messages
            if message["role"] == "assistant" and "metadata" in message:
                with st.expander("Message Details"):
                    st.json(message["metadata"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about your business..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                success, response_data = send_chat_message(prompt, user_id)
                
                if success:
                    response_text = response_data.get("response", "No response received")
                    st.markdown(response_text)
                    
                    # Add assistant message to chat history with metadata
                    assistant_message = {
                        "role": "assistant",
                        "content": response_text,
                        "metadata": {
                            "session_id": response_data.get("session_id"),
                            "tool_calls": response_data.get("tool_calls", 0),
                            "events_processed": response_data.get("events_processed", 0),
                            "timestamp": response_data.get("timestamp"),
                            "fallback": response_data.get("fallback", False)
                        }
                    }
                    st.session_state.messages.append(assistant_message)
                    
                    # Show response metadata
                    with st.expander("Response Details"):
                        st.json(response_data)
                        
                else:
                    error_message = f"❌ Error: {response_data.get('error', 'Unknown error')}"
                    st.error(error_message)
                    
                    # Add error message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })

    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "Show me all my contacts",
        "What are my unpaid invoices?", 
        "Generate a revenue report for all time",
        "Give me business insights and recommendations",
        "Create a new contact named 'Jane Doe' from 'ABC Corp' with email 'jane@abc.com'",
        "Log an expense of $200 for 'Office Supplies' with description 'Printer paper and ink'",
        "Schedule a meeting with John Smith titled 'Quarterly Review' for 2025-07-01 14:00:00",
        "Send an email to Sarah Johnson with subject 'Project Update'"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(sample_questions):
        with cols[i % 2]:
            if st.button(question, key=f"sample_{i}"):
                # Simulate clicking the question
                st.session_state.messages.append({"role": "user", "content": question})
                
                with st.chat_message("user"):
                    st.markdown(question)
                
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        success, response_data = send_chat_message(question, user_id)
                        
                        if success:
                            response_text = response_data.get("response", "No response received")
                            st.markdown(response_text)
                            
                            assistant_message = {
                                "role": "assistant",
                                "content": response_text,
                                "metadata": {
                                    "session_id": response_data.get("session_id"),
                                    "tool_calls": response_data.get("tool_calls", 0),
                                    "events_processed": response_data.get("events_processed", 0),
                                    "timestamp": response_data.get("timestamp"),
                                    "fallback": response_data.get("fallback", False)
                                }
                            }
                            st.session_state.messages.append(assistant_message)
                        else:
                            error_message = f"❌ Error: {response_data.get('error', 'Unknown error')}"
                            st.error(error_message)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error_message
                            })
                
                st.rerun()

if __name__ == "__main__":
    main()
