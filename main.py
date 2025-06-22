"""
Simple Daily Agent Demo - Uses ONE Database (Session DB) with proper ADK tools
Perfect for consultation demos and simple explanations.
"""

from flask import Flask, request, jsonify
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import ToolContext
from google.genai import types
import uuid
import os
import asyncio
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Import the agent from 1ess_agent module
from business_agent.agent import root_agent
from business_agent.tools.database_tools import (
    initialize_business_database,
    SESSIONS_DB,
    get_business_data_from_db,
    get_business_insights,
    generate_report,
)

# Load environment variables first - following ADK conventions
load_dotenv()

app = Flask(__name__)
app.secret_key = 'business-analyst-secret-key'

# Configure Google AI authentication following ADK documentation
# The API key should be set via environment variables, not hardcoded
# Environment variables will be loaded from .env file or system environment

# Verify required environment variables are set
if not os.getenv("GOOGLE_API_KEY") and not (os.getenv("GOOGLE_CLOUD_PROJECT") and os.getenv("GOOGLE_GENAI_USE_VERTEXAI")):
    print("❌ Missing required authentication configuration!")
    print("Please set either:")
    print("  - GOOGLE_API_KEY (for Google AI Studio)")
    print("  - Or GOOGLE_CLOUD_PROJECT + GOOGLE_GENAI_USE_VERTEXAI=true (for Vertex AI)")
    exit(1)

# Initialize database with business data
initialize_business_database()

# Setup database session service
try:
    session_service = DatabaseSessionService(db_url=SESSIONS_DB)
    print(f"✅ Database session service initialized")
    print(f"🔗 Database: {SESSIONS_DB}")
except Exception as e:
    print(f"❌ Error initializing database session service: {e}")
    exit(1)

# Initialize runner with both required arguments
runner = Runner(
    agent=root_agent, 
    session_service=session_service,
    app_name="business_agent"
)

async def get_or_create_session(user_id: str):
    """Get or create a session for the user and ensure business data is in state."""
    try:
        session_id = f"session_{user_id}"
        app_name = "business_agent"  # Match the app_name in Runner
        
        # Try to get existing session
        try:
            session = await session_service.get_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )
            print(f"Found existing session for user {user_id}")
            
            # Ensure user_id is in state for database queries
            if "user_id" not in session.state:
                session.state["user_id"] = user_id
                print("Added user_id to existing session")
            
            return session_id
            
        except Exception as e:
            # Create new session
            print(f"Creating new session for user {user_id}: {e}")
            initial_state = { "user_id": user_id, "user_name": user_id }
            
            await session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id,
                state=initial_state
            )
            print(f"Successfully created session {session_id}")
            return session_id
            
    except Exception as e:
        print(f"Session error: {e}")
        return f"fallback_{user_id}"

@app.route('/chat', methods=['POST'])
def chat():
    """Proper ADK agent chat endpoint with tools."""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'demo_user')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"Processing message: '{user_message}' for user: {user_id}")
        
        # Get session (using asyncio.run for async function in sync context)
        session_id = asyncio.run(get_or_create_session(user_id))
        print(f"Using session: {session_id}")
        
        # Run the proper ADK agent with tools
        content = types.Content(role='user', parts=[types.Part(text=user_message)])
        
        try:
            print("Running agent...")
            
            # Use asyncio.run to handle the async generator
            async def run_agent():
                events = []
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=content
                ):
                    events.append(event)
                return events
            
            event_list = asyncio.run(run_agent())
            
            print("Agent executed, processing events...")
            
            # Process events to get response
            agent_response = None
            tool_calls_count = 0
            all_text_parts = []
            
            print(f"Got {len(event_list)} events")
            
            for i, event in enumerate(event_list):
                print(f"Event {i}: {type(event).__name__}")
                
                # Look for any content in events
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            # Check for text content
                            if hasattr(part, 'text') and part.text and part.text.strip():
                                text = part.text.strip()
                                all_text_parts.append(text)
                                print(f"Found text: {text[:100]}...")
                            # Check for function calls
                            elif hasattr(part, 'function_call') and part.function_call:
                                tool_calls_count += 1
                                print(f"Found tool call: {part.function_call}")
            
            # Combine all text parts or use the last meaningful one
            if all_text_parts:
                # Use the last non-empty text part as the final response
                agent_response = all_text_parts[-1]
                print(f"Using final text response: {agent_response[:100]}...")
            
            # Return response
            if agent_response and agent_response.strip():
                return jsonify({
                    'response': agent_response,
                    'session_id': session_id,
                    'tool_calls': tool_calls_count,
                    'events_processed': len(event_list),
                    'timestamp': datetime.now().isoformat()
                })
            else:
                # Fallback response when no text response is found
                return jsonify({
                    'response': "Hello! I'm your business assistant. I can help you check unpaid invoices, manage contacts, create invoices, track expenses, and provide business insights. What would you like to know?",
                    'session_id': session_id,
                    'tool_calls': tool_calls_count,
                    'events_processed': len(event_list),
                    'fallback': True,
                    'timestamp': datetime.now().isoformat()
                })
            
                
        except Exception as e:
            print(f"Error running agent: {e}")
            return jsonify({'error': f'Agent execution error: {str(e)}'}), 500
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    """Direct endpoint to get business data from database."""
    query_type = request.args.get('type', 'insights')
    report_type = request.args.get('report_type', 'invoices')
    user_id = request.args.get('user_id', 'demo_user')
    
    class MockToolContext:
        state = {"user_id": user_id}

    mock_context = MockToolContext()
    
    try:
        if query_type == "insights":
            result = get_business_insights(mock_context)
        elif query_type == "report":
            result = generate_report(report_type, mock_context)
        elif query_type == "raw":
            result = get_business_data_from_db(user_id)
        else:
            result = {"error": f"Unknown query type: {query_type}. Use: insights, report, raw"}
        
        return jsonify(result)
    except Exception as e:
        print(f"❌ Data endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/sessions', methods=['GET'])
def list_sessions():
    """List sessions."""
    try:
        user_id = request.args.get('user_id', 'demo_user')
        session_id = f"session_{user_id}"
        
        async def get_session_info():
            try:
                session = await session_service.get_session(
                    app_name="business_agent",
                    user_id=user_id,
                    session_id=session_id
                )
                
                return [{
                    'session_id': session.id,
                    'user_id': session.user_id,
                    'state_keys': list(session.state.keys()),
                    'has_user_id': 'user_id' in session.state
                }]
                
            except Exception as e:
                print(f"Session not found: {e}")
                return []
        
        session_data = asyncio.run(get_session_info())
        
        return jsonify({
            'sessions': session_data,
            'count': len(session_data),
            'user_id_filter': user_id,
            'database': SESSIONS_DB,
            'note': 'Business data is now stored in database tables, not session state'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        # Check database connectivity and table status
        db_path = SESSIONS_DB.replace("sqlite:///", "")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Get counts for business tables
        table_counts = {}
        business_tables = ['user', 'contact', 'invoice', 'revenue', 'expense', 'event', 'interaction']
        for table in business_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'app': 'business_analyst_agent',
            'database': SESSIONS_DB,
            'tools_available': len(root_agent.tools),
            'database_tables': tables,
            'business_data_counts': table_counts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Business Analyst Agent...")
    print(f"🧠 Agent: {root_agent.name} | Model: {root_agent.model}")
    print(f"🛠️  Tools Available: {len(root_agent.tools)}")
    print(f"🗃️  Database: {SESSIONS_DB}")
    print("💬 Chat endpoint: POST http://localhost:5000/chat")
    print("📊 Data endpoint: GET http://localhost:5000/data?type=insights")
    print("📝 Sessions: GET /sessions?user_id=huzaifa_ejaz")
    print("🔍 Health check: GET http://localhost:5000/health")
    print("\n🌐 Starting Flask server...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
