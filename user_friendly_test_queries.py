#!/usr/bin/env python3
"""
User-Friendly Test Queries for Business Analyst Agent

These test queries allow users to work with names, emails, and companies
instead of database IDs, making the system much more intuitive to use.
"""

# Contact Management (Name-based)
CONTACT_MANAGEMENT_QUERIES = [
    # Search and lookup
    "Find all contacts named John",
    "Search for contacts from TechCorp",
    "Find contact with email john@techcorp.com",
    "Show me contacts from companies containing 'Design'",
    "Find contacts with gmail email addresses",
    
    # Create contacts
    "Add a new contact named 'Alice Johnson' with email 'alice@techstartup.com', phone '555-2001', company 'Tech Startup Inc', notes 'Potential high-value client', status 'prospect'",
    "Create a contact for 'Bob Smith' from 'Marketing Solutions' with email 'bob@marketing.com' and phone '555-2002'",
    "Add 'Carol Williams' as a new lead with company 'Design Agency' and email 'carol@design.com'",
    
    # Update contacts by name
    "Update John Smith's status to client",
    "Change Sarah Johnson's company to New Design Studio",
    "Update Mike Wilson's email to mike.wilson@newcompany.com and status to prospect",
    "Change John Smith's phone number to 555-9999 and add notes 'VIP client'",
    
    # List contacts
    "Show me all my contacts",
    "List all contacts with their details",
    "Get all my contacts and their current status",
]

# Invoice Management (Name-based)
INVOICE_MANAGEMENT_QUERIES = [
    # Create invoices by contact name
    "Create a $2500 invoice for John Smith due in 30 days",
    "Generate a new invoice for Sarah Johnson with total amount $2200, due in 30 days, for 'Web design project'",
    "Create an invoice for $1800 for Mike Wilson with issue date today and due date in 15 days",
    "Bill Alice Johnson $3500 for consulting services due next month",
    
    # Find invoices by contact name
    "Show me all invoices for John Smith",
    "Find invoices for Sarah Johnson",
    "What invoices do I have for Mike Wilson?",
    
    # Find invoices by status
    "Show me all unpaid invoices",
    "Find all paid invoices",
    "List overdue invoices",
    "Show me cancelled invoices",
    
    # Mixed queries
    "Show me all unpaid invoices and their total amount",
    "Find all invoices over $2000",
    "What's the total amount of unpaid invoices?",
]

# Interaction Management (Name-based)
INTERACTION_MANAGEMENT_QUERIES = [
    # Log interactions by contact name
    "Log a call with John Smith about project discussion",
    "Record an email interaction with Sarah Johnson about design review",
    "Log a meeting with Mike Wilson yesterday about contract negotiations",
    "Add a note for Alice Johnson: 'Very interested in our premium package'",
    "Record a call interaction with John Smith today about payment follow-up",
    
    # Read interactions by contact name
    "Show me all interactions with John Smith",
    "Get interaction history for Sarah Johnson",
    "What interactions have I had with Mike Wilson?",
    "Display all communications with Alice Johnson",
]

# Communication (Name-based)
COMMUNICATION_QUERIES = [
    # Send emails by contact name
    "Send email to John Smith with subject 'Project Update' and message 'Hi John, project is on track for January deadline.'",
    "Email Sarah Johnson about the design review meeting",
    "Send an email to Mike Wilson with subject 'Contract Ready' and message 'Hi Mike, your contract is ready for signature.'",
    "Email Alice Johnson with subject 'Welcome' and message 'Welcome to our premium service!'",
]

# Event Management (Enhanced)
EVENT_MANAGEMENT_QUERIES = [
    # Create events
    "Schedule an event titled 'Strategic Planning Meeting' for '2025-01-15 10:00:00' at 'Conference Room A'",
    "Create a meeting 'Client Presentation' with John Smith for '2025-01-10 14:30:00' at 'Client Office'",
    "Schedule 'Quarterly Review' with Sarah Johnson for next Friday at 2 PM",
    "Add event 'Networking Conference' for '2025-02-05 09:00:00' at 'Convention Center'",
    
    # List events
    "Show me all upcoming events",
    "What events do I have scheduled?",
    "List my upcoming meetings and events",
]

# Expense Management
EXPENSE_MANAGEMENT_QUERIES = [
    # Create expenses
    "Log an expense of $150 for 'Office Supplies' with description 'Notebooks and pens'",
    "Record a $800 expense for 'Software' category with description 'Annual CRM subscription'",
    "Add an expense: $320 for 'Travel', description 'Client meeting transportation costs'",
    "Create expense entry for $450 in 'Marketing' category for 'Google Ads campaign'",
    "Log $120 expense for 'Utilities' with description 'Monthly internet bill'",
]

# Reporting and Analytics
REPORTING_QUERIES = [
    # Revenue reports
    "Generate a revenue report for all time",
    "Show me revenue report for this year",
    "Create revenue analytics report",
    
    # Expense reports
    "Generate an expense report for all time",
    "Show me expense breakdown by category",
    "Create expenses analysis report",
    
    # Contact reports
    "Generate a contact report",
    "Show me contact analytics by status",
    "Create contacts summary report",
    
    # Invoice reports
    "Generate an invoice report for all time",
    "Show me invoice status breakdown",
    "Create invoices analytics report",
    
    # Interaction reports
    "Generate an interaction report for all time",
    "Show me interaction analytics by type",
    "Create interactions summary report",
    
    # Business insights
    "Show me my business insights and key metrics",
    "Generate comprehensive business insights with recommendations",
    "What's my business performance overview?",
]

# Complex Business Queries (Multi-step operations)
COMPLEX_BUSINESS_QUERIES = [
    # Multi-entity operations
    "Create a new contact 'Emma Davis' from 'Tech Solutions' with email 'emma@techsol.com', then create a $5000 invoice for her due in 30 days",
    "Find all prospects and show me their contact details and any existing invoices",
    "Show me all unpaid invoices and suggest which contacts I should follow up with first",
    
    # Analytics and insights
    "What's my total revenue vs expenses this year and what's my profit margin?",
    "Show me my top 5 clients by revenue and their contact information",
    "Which expense categories are costing me the most money?",
    "Who are my most valuable contacts based on invoice amounts?",
    
    # Workflow suggestions
    "Show me contacts I haven't interacted with in the last 30 days",
    "Find all overdue invoices and suggest follow-up actions",
    "Which clients should I prioritize for this week based on upcoming events and overdue invoices?",
]

# Natural Language Queries (Conversational)
NATURAL_LANGUAGE_QUERIES = [
    # Search queries
    "Who are my contacts from TechCorp?",
    "Show me all clients (status = client)",
    "What contacts do I have in the prospect stage?",
    "Find contacts with .com email addresses",
    "Who works at companies with 'Tech' in the name?",
    
    # Business questions
    "How much money am I owed?",
    "What's my biggest expense category?",
    "Who owes me the most money?",
    "What meetings do I have this week?",
    "Who should I follow up with today?",
    
    # Status questions
    "What's my business doing well?",
    "Where should I focus my attention?",
    "What needs immediate action?",
    "How is my cash flow looking?",
]

# Error Handling and Edge Cases
EDGE_CASE_QUERIES = [
    # Ambiguous names
    "Update John with new phone number 555-1234",  # Multiple Johns
    "Create invoice for Smith",  # Multiple Smiths
    "Send email to Mike about project",  # Multiple Mikes
    
    # Non-existent contacts
    "Find contact named 'Nonexistent Person'",
    "Create invoice for 'Unknown Client'",
    "Log interaction with 'Fake Contact'",
    
    # Invalid data
    "Create contact with invalid email 'not-an-email'",
    "Create invoice with negative amount",
    "Schedule event in the past",
]

# All test queries organized by category
ALL_USER_FRIENDLY_QUERIES = {
    "Contact Management": CONTACT_MANAGEMENT_QUERIES,
    "Invoice Management": INVOICE_MANAGEMENT_QUERIES,
    "Interaction Management": INTERACTION_MANAGEMENT_QUERIES,
    "Communication": COMMUNICATION_QUERIES,
    "Event Management": EVENT_MANAGEMENT_QUERIES,
    "Expense Management": EXPENSE_MANAGEMENT_QUERIES,
    "Reporting & Analytics": REPORTING_QUERIES,
    "Complex Business Operations": COMPLEX_BUSINESS_QUERIES,
    "Natural Language": NATURAL_LANGUAGE_QUERIES,
    "Edge Cases": EDGE_CASE_QUERIES,
}

# Quick test queries for immediate testing
QUICK_TEST_QUERIES = [
    "Find all contacts named John",
    "Show me all unpaid invoices", 
    "Create a $1500 invoice for John Smith due in 30 days",
    "Log a call with Sarah Johnson about project status",
    "Send email to Mike Wilson with subject 'Follow-up'",
    "Generate a business insights report",
    "Show me all interactions with John Smith",
    "Find contacts from TechCorp",
    "What's my total outstanding invoice amount?",
    "Create contact 'Test User' with email 'test@example.com'",
]

if __name__ == "__main__":
    print("=== User-Friendly Test Queries for Business Analyst Agent ===\n")
    
    print("## Contact Management")
    for i, query in enumerate(CONTACT_MANAGEMENT_QUERIES[:5], 1):
        print(f"{i}. {query}")
    print()
    
    print("## Invoice Management") 
    for i, query in enumerate(INVOICE_MANAGEMENT_QUERIES[:5], 1):
        print(f"{i}. {query}")
    print()
    
    print("## Quick Test Queries (Try these first!)") 
    for i, query in enumerate(QUICK_TEST_QUERIES, 1):
        print(f"{i}. {query}") 