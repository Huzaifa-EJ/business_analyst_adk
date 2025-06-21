import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
USER_ID = "huzaifa_ejaz"  # Use the user with sample data

def print_header(title):
    """Prints a formatted header."""
    print("\n" + "="*60)
    print(f"▶️  {title.upper()}")
    print("="*60)

def run_health_check():
    """Runs a health check on the Flask application."""
    print_header("HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        health_data = response.json()
        
        print("✅ Health check successful!")
        print(f"   App: {health_data.get('app')}")
        print(f"   Database: {health_data.get('database')}")
        print(f"   Tools Available: {health_data.get('tools_available')}")
        
        print("   Table Counts:")
        for table, count in health_data.get('business_data_counts', {}).items():
            print(f"     - {table}: {count} records")
            
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def send_chat_message(query: str):
    """Sends a message to the chat endpoint and prints the response."""
    print(f"\n💬 User Query: \"{query}\"")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": query, "user_id": USER_ID}
        )
        response.raise_for_status()
        chat_response = response.json().get('response', 'No response text found.')
        print(f"🤖 Agent Response: {chat_response}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error communicating with agent: {e}")

def test_contact_management():
    print_header("TESTING CONTACT MANAGEMENT")
    send_chat_message("Please add a new contact: Name is 'Test Client', Company is 'Test Corp Inc.', email is 'test@testcorp.com', and phone is '555-1234'.")
    send_chat_message("Can you list all of my contacts for me?")
    send_chat_message("Please update the contact 'Test Client' and set their status to 'prospect'.")

def test_invoice_management():
    print_header("TESTING INVOICE MANAGEMENT")
    send_chat_message("Create a new invoice for 'John Smith' for an amount of $2500. The due date is in 30 days. Add a note: 'Consulting services'.")
    send_chat_message("Can you show me the details for invoice ID 2?")
    send_chat_message("Please update invoice ID 2 and change the status to 'overdue'.")
    send_chat_message("I've received payment for invoice ID 3. Can you mark it as paid?")

def test_expense_management():
    print_header("TESTING EXPENSE MANAGEMENT")
    send_chat_message("Log a new expense of $150 for 'Marketing'. Description: 'Social media campaign'.")

def test_event_management():
    print_header("TESTING EVENT MANAGEMENT")
    next_tuesday = datetime.now() + timedelta(days=(1 - datetime.now().weekday() + 7) % 7)
    date_str = next_tuesday.strftime('%Y-%m-%d 14:00:00')
    send_chat_message(f"Schedule a meeting with 'Sarah Johnson' titled 'Project Sync'. It's on {date_str} at her office.")
    send_chat_message("What are my upcoming events?")

def test_interaction_logging():
    print_header("TESTING INTERACTION LOGGING")
    send_chat_message("Log an email interaction with 'Mike Wilson'. The summary is 'Sent proposal for Q3 projects'.")
    send_chat_message("Show me the interaction history for 'Mike Wilson'.")

def test_communication():
    print_header("TESTING COMMUNICATION (SIMULATED EMAIL)")
    send_chat_message("Send an email to 'John Smith' with the subject 'Invoice Reminder' and message 'Hi John, this is a friendly reminder that your invoice is due soon.'")

def test_reporting_and_insights():
    print_header("TESTING REPORTING AND INSIGHTS")
    send_chat_message("Generate a revenue report for all time.")
    send_chat_message("Generate an expense report.")
    send_chat_message("Can you give me a summary of my business performance? I'm looking for some key insights.")

if __name__ == "__main__":
    if run_health_check():
        test_contact_management()
        test_invoice_management()
        test_expense_management()
        test_event_management()
        test_interaction_logging()
        test_communication()
        test_reporting_and_insights()
    else:
        print("\nAborting tests due to health check failure.") 