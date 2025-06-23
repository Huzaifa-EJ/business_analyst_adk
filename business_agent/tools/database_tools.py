from google.adk.tools import ToolContext
import sqlite3
from datetime import datetime
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
import re

SESSIONS_DB = "sqlite:///./business_agent.db"

def initialize_business_database():
    """Initialize business tables in the same database and populate with sample data."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Create user table first (referenced by other tables)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT,
                company TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create business tables with proper foreign key constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                company TEXT,
                phone TEXT,
                notes TEXT,
                status TEXT DEFAULT 'lead',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                contact_id INTEGER,
                issue_date TEXT,
                due_date TEXT,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (contact_id) REFERENCES contact (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY,
                invoice_id INTEGER,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (invoice_id) REFERENCES invoice (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                contact_id INTEGER,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (contact_id) REFERENCES contact (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                contact_id INTEGER,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (contact_id) REFERENCES contact (id)
            )
        ''')
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] == 0:
            # Insert sample user first
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', ('huzaifa_ejaz', 'Huzaifa Ejaz', 'huzaifa@business.com', 'Business Analytics Co', '555-0100'))
            
            # Insert sample contacts
            contacts_data = [
                (1, 'huzaifa_ejaz', 'John Smith', 'john@techcorp.com', 'TechCorp', '555-0101', 'Potential client', 'lead'),
                (2, 'huzaifa_ejaz', 'Sarah Johnson', 'sarah@designstudio.com', 'Design Studio', '555-0102', 'Current client', 'client'),
                (3, 'huzaifa_ejaz', 'Mike Wilson', 'mike@consulting.com', 'Wilson Consulting', '555-0103', 'Hot prospect', 'prospect'),
            ]
            cursor.executemany(
                "INSERT INTO contact (id, user_id, name, email, company, phone, notes, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                contacts_data
            )
            
            # Insert sample invoices
            invoices_data = [
                (1, 'huzaifa_ejaz', 1, '2024-12-15', '2025-01-15', 2500.00, 'paid', 'Consulting services'),
                (2, 'huzaifa_ejaz', 2, '2024-12-20', '2025-01-20', 1800.00, 'unpaid', 'Design work'),
                (3, 'huzaifa_ejaz', 3, '2024-12-22', '2025-01-22', 3200.00, 'unpaid', 'Development project'),
                (4, 'huzaifa_ejaz', 1, '2024-12-10', '2025-01-10', 1500.00, 'paid', 'Additional consulting'),
            ]
            cursor.executemany(
                "INSERT INTO invoice (id, user_id, contact_id, issue_date, due_date, total_amount, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                invoices_data
            )
            
            # Insert sample revenue records
            revenue_data = [
                (1, 1, 2500.00, '2024-12-16'),
                (2, 4, 1500.00, '2024-12-11'),
            ]
            cursor.executemany(
                "INSERT INTO revenue (id, invoice_id, amount, date) VALUES (?, ?, ?, ?)",
                revenue_data
            )
            
            # Insert sample expenses
            expenses_data = [
                (1, 'huzaifa_ejaz', 250.00, 'Office Supplies', 'Printer paper and ink', '2024-12-18'),
                (2, 'huzaifa_ejaz', 1200.00, 'Software', 'Adobe Creative Suite license', '2024-12-01'),
                (3, 'huzaifa_ejaz', 450.00, 'Travel', 'Client meeting travel costs', '2024-12-15'),
                (4, 'huzaifa_ejaz', 300.00, 'Marketing', 'Social media advertising', '2024-12-20'),
            ]
            cursor.executemany(
                "INSERT INTO expense (id, user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?, ?)",
                expenses_data
            )
            
            # Insert sample events
            events_data = [
                (1, 'huzaifa_ejaz', 1, 'Client Meeting', '2024-12-28 14:00:00', 'Quarterly business review', 'TechCorp Office'),
                (2, 'huzaifa_ejaz', 2, 'Design Review', '2024-12-30 10:00:00', 'Review design mockups', 'Design Studio'),
                (3, 'huzaifa_ejaz', None, 'Team Planning', '2025-01-02 09:00:00', 'Q1 planning session', 'Our Office'),
            ]
            cursor.executemany(
                "INSERT INTO event (id, user_id, contact_id, title, date, description, location) VALUES (?, ?, ?, ?, ?, ?, ?)",
                events_data
            )
            
            # Insert sample interactions
            interactions_data = [
                (1, 'huzaifa_ejaz', 1, '2024-12-15', 'call', 'Discussed project requirements'),
                (2, 'huzaifa_ejaz', 2, '2024-12-18', 'email', 'Sent design proposals'),
                (3, 'huzaifa_ejaz', 3, '2024-12-20', 'meeting', 'In-person consultation'),
                (4, 'huzaifa_ejaz', 1, '2024-12-22', 'call', 'Follow-up on invoice payment'),
            ]
            cursor.executemany(
                "INSERT INTO interaction (id, user_id, contact_id, date, type, summary) VALUES (?, ?, ?, ?, ?, ?)",
                interactions_data
            )
            conn.commit()
            print("✅ Sample business data initialized in database")
        else:
            print("✅ Business data already exists in database")
            
    except Exception as e:
        print(f"❌ Error initializing business database: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_business_data_from_db(user_id='demo_user'):
    """Fetch business data from database for a specific user."""
    print(f"--- get_business_data_from_db called with user_id: {user_id} ---")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Fetch user info
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        user = dict(user_row) if user_row else None
        
        # Fetch contacts
        cursor.execute("SELECT * FROM contact WHERE user_id = ?", (user_id,))
        contacts = [dict(row) for row in cursor.fetchall()]
        
        # Fetch invoices
        cursor.execute("SELECT * FROM invoice WHERE user_id = ?", (user_id,))
        invoices = [dict(row) for row in cursor.fetchall()]
        
        # Fetch expenses
        cursor.execute("SELECT * FROM expense WHERE user_id = ?", (user_id,))
        expenses = [dict(row) for row in cursor.fetchall()]
        
        # Fetch events
        cursor.execute("SELECT * FROM event WHERE user_id = ?", (user_id,))
        events = [dict(row) for row in cursor.fetchall()]
        
        # Fetch interactions
        cursor.execute("SELECT * FROM interaction WHERE user_id = ?", (user_id,))
        interactions = [dict(row) for row in cursor.fetchall()]
        
        # Fetch revenue
        cursor.execute("SELECT * FROM revenue")
        revenue = [dict(row) for row in cursor.fetchall()]
        
        return {
            "user": user,
            "contacts": contacts,
            "invoices": invoices,
            "expenses": expenses,
            "events": events,
            "interactions": interactions,
            "revenue": revenue
        }
    except Exception as e:
        print(f"❌ Error fetching business data: {e}")
        return {"user": None, "contacts": [], "invoices": [], "expenses": [], "events": [], "interactions": [], "revenue": []}
    finally:
        conn.close()


def get_business_insights(tool_context: ToolContext) -> dict:
    """Generate comprehensive business insights from all available data.

    Args:
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing business insights and recommendations
    """
    print("--- Tool: get_business_insights called ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    business_data = get_business_data_from_db(user_id)
    
    # Calculate key metrics
    total_invoices = len(business_data["invoices"])
    paid_invoices = [inv for inv in business_data["invoices"] if inv["status"] == "paid"]
    unpaid_invoices = [inv for inv in business_data["invoices"] if inv["status"] == "unpaid"]
    
    total_revenue = sum(inv["total_amount"] for inv in paid_invoices)
    outstanding_amount = sum(inv["total_amount"] for inv in unpaid_invoices)
    total_expenses = sum(exp["amount"] for exp in business_data["expenses"])
    
    profit = total_revenue - total_expenses
    profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
    
    # Generate insights
    insights = []
    
    if outstanding_amount > 0 and total_revenue > 0 and (outstanding_amount / total_revenue) > 0.3:
        insights.append("⚠️ High outstanding invoices - consider following up on payments to improve cash flow.")
    
    if total_revenue > 0:
        if profit_margin > 20:
            insights.append("💰 Healthy profit margin - your business is performing well.")
        elif profit_margin < 10:
            insights.append("📉 Low profit margin - consider reviewing expenses or pricing strategies.")
    else:
        insights.append("ℹ️ No revenue recorded yet. Focus on securing your first paid invoice.")
        
    if len(unpaid_invoices) > len(paid_invoices):
        insights.append("🔔 You have more unpaid than paid invoices. It's time to focus on collections.")
    
    if not insights:
        insights.append("✅ Business vitals look stable. Keep up the great work!")

    return {
        "action": "get_business_insights",
        "status": "success",
        "key_metrics": {
            "total_revenue": f"${total_revenue:,.2f}",
            "outstanding_amount": f"${outstanding_amount:,.2f}",
            "total_expenses": f"${total_expenses:,.2f}",
            "profit": f"${profit:,.2f}",
            "profit_margin": f"{profit_margin:.2f}%",
            "total_invoices": total_invoices,
            "paid_invoices_count": len(paid_invoices),
            "unpaid_invoices_count": len(unpaid_invoices)
        },
        "insights": insights,
        "recommendations": [
            "Regularly follow up on overdue invoices to improve cash flow.",
            "Analyze expense categories to identify potential cost savings.",
            "Consider setting up automated invoice reminders for clients."
        ]
    }

# CONTACT TOOLS
def create_contact(name: str, tool_context: ToolContext, email: str, phone: str, company: str, 
                  notes: str, status: str) -> dict:
    """Add a new contact to the database.

    Args:
        name: Contact's full name
        email: Contact's email address
        phone: Contact's phone number
        company: Contact's company name
        notes: Additional notes about the contact
        status: Contact status (lead, prospect, client, inactive)
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of adding the contact
    """
    print(f"--- Tool: create_contact called for: {name} at {company} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    print(f"--- Using user_id: {user_id} ---")
    print(f"--- Tool context state: {tool_context.state} ---")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    # Validate status
    valid_statuses = ['lead', 'prospect', 'client', 'inactive']
    if status.lower() not in valid_statuses:
        status = 'lead'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if user exists, if not create them
        cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"User {user_id} doesn't exist, creating user entry...")
            # Create user entry with minimal required information
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_id.replace('_', ' ').title(), f"{user_id}@example.com", "Unknown Company", "000-000-0000"))
            print(f"Created user entry for {user_id}")
        
        cursor.execute('''
            INSERT INTO contact (user_id, name, email, phone, company, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name, email, phone, company, notes, status.lower()))
        
        contact_id = cursor.lastrowid
        conn.commit()
        
        return {
            "action": "create_contact",
            "status": "success",
            "contact_id": contact_id,
            "name": name,
            "email": email,
            "company": company,
            "phone": phone,
            "notes": notes,
            "contact_status": status.lower(),
            "message": f"Successfully added contact: {name}" + (f" from {company}" if company else "")
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_contact",
            "status": "error",
            "error": str(e),
            "message": f"Failed to add contact: {name}"
        }
    finally:
        if conn:
            conn.close()

def read_all_contacts(tool_context: ToolContext) -> dict:
    """Get a list of all contacts for the current user.

    Args:
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing list of contacts
    """
    print("--- Tool: read_all_contacts called ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    print(f"--- read_all_contacts using user_id: {user_id} ---")
    business_data = get_business_data_from_db(user_id)
    print(f"--- Fetched business data: contacts={len(business_data['contacts'])}, user={business_data['user']} ---")
    
    contacts = business_data["contacts"]
    
    return {
        "action": "read_all_contacts",
        "status": "success",
        "contacts_count": len(contacts),
        "contacts": contacts,
        "message": f"Retrieved {len(contacts)} contacts"
    }

def update_contact(contact_id: int, tool_context: ToolContext, name: str, email: str, phone: str,
                  company: str, notes: str, status: str) -> dict:
    """Update an existing contact.

    Args:
        contact_id: ID of the contact to update
        name: Updated contact name
        email: Updated email address
        phone: Updated phone number
        company: Updated company name
        notes: Updated notes
        status: Updated contact status
        tool_context: Context for accessing session state
    Returns:
        Dictionary containing the result of updating the contact
    """
    print(f"--- Tool: update_contact called for contact_id: {contact_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if contact exists
        cursor.execute("SELECT * FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        contact = cursor.fetchone()
        
        if not contact:
            return {
                "action": "update_contact",
                "status": "error",
                "error": f"Contact with ID {contact_id} not found",
                "message": f"Contact {contact_id} not found"
            }
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if name and name.strip():
            update_fields.append("name = ?")
            update_values.append(name)
        if email and email.strip():
            update_fields.append("email = ?")
            update_values.append(email)
        if phone and phone.strip():
            update_fields.append("phone = ?")
            update_values.append(phone)
        if company and company.strip():
            update_fields.append("company = ?")
            update_values.append(company)
        if notes and notes.strip():
            update_fields.append("notes = ?")
            update_values.append(notes)
        if status and status.strip():
            valid_statuses = ['lead', 'prospect', 'client', 'inactive']
            if status.lower() in valid_statuses:
                update_fields.append("status = ?")
                update_values.append(status.lower())
        
        if not update_fields:
            return {
                "action": "update_contact",
                "status": "warning",
                "message": "No fields provided to update"
            }
        
        update_values.extend([contact_id, user_id])
        update_query = f"UPDATE contact SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
        
        cursor.execute(update_query, update_values)
        conn.commit()
        
        # Fetch updated contact
        cursor.execute("SELECT * FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        updated_row = cursor.fetchone()
        updated_contact = dict(updated_row) if updated_row else {}
        
        return {
            "action": "update_contact",
            "status": "success",
            "contact_id": contact_id,
            "updated_contact": updated_contact,
            "message": f"Successfully updated contact: {updated_contact.get('name', 'Unknown')}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "update_contact",
            "status": "error",
            "error": str(e),
            "message": f"Failed to update contact {contact_id}"
        }
    finally:
        if conn:
            conn.close()


# INVOICE TOOLS
def create_invoice(contact_id: int, tool_context: ToolContext, issue_date: str, due_date: str, 
                  total_amount: float, status: str, notes: str) -> dict:
    """Create a new invoice for a contact.

    Args:
        contact_id: ID of the contact this invoice is for
        issue_date: Invoice issue date (YYYY-MM-DD format)
        due_date: Invoice due date (YYYY-MM-DD format)
        total_amount: Invoice total amount
        status: Invoice status (unpaid, paid, overdue, cancelled)
        notes: Additional notes for the invoice
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of creating the invoice
    """
    print(f"--- Tool: create_invoice called for contact_id: {contact_id}, amount: ${total_amount} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    # Set default dates
    if not issue_date or not issue_date.strip():
        issue_date = datetime.now().strftime("%Y-%m-%d")
    if not due_date or not due_date.strip():
        due_date = datetime.now().strftime("%Y-%m-%d")
    
    # Validate status
    valid_statuses = ['unpaid', 'paid', 'overdue', 'cancelled']
    if status.lower() not in valid_statuses:
        status = 'unpaid'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if user exists, if not create them
        cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"User {user_id} doesn't exist, creating user entry...")
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_id.replace('_', ' ').title(), f"{user_id}@example.com", "Unknown Company", "000-000-0000"))
            print(f"Created user entry for {user_id}")
        
        # Verify contact exists
        cursor.execute("SELECT name, company FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        contact_info = cursor.fetchone()
        
        if not contact_info:
            return {
                "action": "create_invoice",
                "status": "error",
                "error": f"Contact with ID {contact_id} not found",
                "message": f"Contact {contact_id} not found"
            }
        
        cursor.execute('''
            INSERT INTO invoice (user_id, contact_id, issue_date, due_date, total_amount, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, contact_id, issue_date, due_date, total_amount, status.lower(), notes))
        
        invoice_id = cursor.lastrowid
        conn.commit()
        
        return {
            "action": "create_invoice",
            "status": "success",
            "invoice_id": invoice_id,
            "contact_id": contact_id,
            "contact_name": contact_info[0],
            "company": contact_info[1],
            "total_amount": total_amount,
            "invoice_status": status.lower(),
            "issue_date": issue_date,
            "due_date": due_date,
            "notes": notes,
            "message": f"Successfully created ${total_amount} invoice for {contact_info[0]}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_invoice",
            "status": "error",
            "error": str(e),
            "message": f"Failed to create invoice for contact {contact_id}"
        }
    finally:
        if conn:
            conn.close()

def read_invoice(invoice_id: int, tool_context: ToolContext) -> dict:
    """Get detailed invoice information.

    Args:
        invoice_id: ID of the invoice to retrieve
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing invoice details
    """
    print(f"--- Tool: read_invoice called for invoice_id: {invoice_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT i.*, c.name as contact_name, c.company, c.email
            FROM invoice i
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.id = ? AND i.user_id = ?
        ''', (invoice_id, user_id))
        
        invoice = cursor.fetchone()
        
        if not invoice:
            return {
                "action": "read_invoice",
                "status": "error",
                "error": f"Invoice with ID {invoice_id} not found",
                "message": f"Invoice {invoice_id} not found"
            }
        
        invoice_dict = dict(invoice)
        
        return {
            "action": "read_invoice",
            "status": "success",
            "invoice": invoice_dict,
            "message": f"Retrieved invoice {invoice_id}"
        }
        
    except Exception as e:
        return {
            "action": "read_invoice",
            "status": "error",
            "error": str(e),
            "message": f"Failed to retrieve invoice {invoice_id}"
        }
    finally:
        if conn:
            conn.close()

def mark_invoice_paid(invoice_id: int, tool_context: ToolContext) -> dict:
    """Mark an invoice as paid and create revenue record.

    Args:
        invoice_id: ID of the invoice to mark as paid
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of marking invoice as paid
    """
    print(f"--- Tool: mark_invoice_paid called for invoice_id: {invoice_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Get invoice details
        cursor.execute("SELECT * FROM invoice WHERE id = ? AND user_id = ?", (invoice_id, user_id))
        invoice = cursor.fetchone()
        
        if not invoice:
            return {
                "action": "mark_invoice_paid",
                "status": "error",
                "error": f"Invoice with ID {invoice_id} not found",
                "message": f"Invoice {invoice_id} not found"
            }
        
        if invoice[6] == 'paid':  # status column
            return {
                "action": "mark_invoice_paid",
                "status": "warning",
                "message": f"Invoice {invoice_id} is already marked as paid"
            }
        
        # Update invoice status
        cursor.execute("UPDATE invoice SET status = 'paid' WHERE id = ?", (invoice_id,))
        
        # Check if revenue record exists
        cursor.execute("SELECT id FROM revenue WHERE invoice_id = ?", (invoice_id,))
        existing_revenue = cursor.fetchone()
        
        if not existing_revenue:
            # Create revenue record
            payment_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute('''
                INSERT INTO revenue (invoice_id, amount, date)
                VALUES (?, ?, ?)
            ''', (invoice_id, invoice[5], payment_date))  # total_amount column
        
        conn.commit()
        
        return {
            "action": "mark_invoice_paid",
            "status": "success",
            "invoice_id": invoice_id,
            "amount": invoice[5],
            "message": f"Successfully marked invoice {invoice_id} as paid (${invoice[5]})"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "mark_invoice_paid",
            "status": "error",
            "error": str(e),
            "message": f"Failed to mark invoice {invoice_id} as paid"
        }
    finally:
        if conn:
            conn.close()

def get_unpaid_invoices(tool_context: ToolContext) -> dict:
    """Get all unpaid invoices for the current user.

    Args:
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing all unpaid invoices with contact details
    """
    print("--- Tool: get_unpaid_invoices called ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Get all unpaid invoices with contact information
        cursor.execute('''
            SELECT i.*, c.name as contact_name, c.company, c.email, c.phone
            FROM invoice i
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ? AND i.status = 'unpaid'
            ORDER BY i.due_date ASC
        ''', (user_id,))
        
        unpaid_invoices = [dict(row) for row in cursor.fetchall()]
        
        # Calculate totals
        total_outstanding = sum(invoice['total_amount'] for invoice in unpaid_invoices)
        
        # Check for overdue invoices
        current_date = datetime.now().strftime("%Y-%m-%d")
        overdue_invoices = [inv for inv in unpaid_invoices if inv['due_date'] and inv['due_date'] < current_date]
        overdue_amount = sum(invoice['total_amount'] for invoice in overdue_invoices)
        
        return {
            "action": "get_unpaid_invoices",
            "status": "success",
            "unpaid_count": len(unpaid_invoices),
            "total_outstanding": total_outstanding,
            "overdue_count": len(overdue_invoices),
            "overdue_amount": overdue_amount,
            "unpaid_invoices": unpaid_invoices,
            "overdue_invoices": overdue_invoices,
            "message": f"Found {len(unpaid_invoices)} unpaid invoices totaling ${total_outstanding:,.2f}"
        }
        
    except Exception as e:
        return {
            "action": "get_unpaid_invoices",
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve unpaid invoices"
        }
    finally:
        if conn:
            conn.close()



# REVENUE TOOLS
def create_revenue(invoice_id: int, amount: float, tool_context: ToolContext, date: str) -> dict:
    """Record revenue entry for an invoice.

    Args:
        invoice_id: ID of the invoice this revenue is for
        amount: Revenue amount
        date: Date of revenue (YYYY-MM-DD format)
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of creating revenue record
    """
    print(f"--- Tool: create_revenue called for invoice_id: {invoice_id}, amount: ${amount} ---")
    
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Verify invoice exists
        cursor.execute("SELECT id FROM invoice WHERE id = ?", (invoice_id,))
        invoice = cursor.fetchone()
        
        if not invoice:
            return {
                "action": "create_revenue",
                "status": "error",
                "error": f"Invoice with ID {invoice_id} not found",
                "message": f"Invoice {invoice_id} not found"
            }
        
        # Check if revenue record already exists
        cursor.execute("SELECT id FROM revenue WHERE invoice_id = ?", (invoice_id,))
        existing_revenue = cursor.fetchone()
        
        if existing_revenue:
            return {
                "action": "create_revenue",
                "status": "warning",
                "message": f"Revenue record already exists for invoice {invoice_id}"
            }
        
        cursor.execute('''
            INSERT INTO revenue (invoice_id, amount, date)
            VALUES (?, ?, ?)
        ''', (invoice_id, amount, date))
        
        revenue_id = cursor.lastrowid
        conn.commit()
        
        return {
            "action": "create_revenue",
            "status": "success",
            "revenue_id": revenue_id,
            "invoice_id": invoice_id,
            "amount": amount,
            "date": date,
            "message": f"Successfully recorded ${amount} revenue for invoice {invoice_id}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_revenue",
            "status": "error",
            "error": str(e),
            "message": f"Failed to create revenue record for invoice {invoice_id}"
        }
    finally:
        if conn:
            conn.close()

# EXPENSE TOOLS
def create_expense(amount: float, category: str, tool_context: ToolContext, description: str, 
                  date: str) -> dict:
    """Record a new business expense.

    Args:
        amount: Expense amount
        category: Expense category
        tool_context: Context for accessing session state
        description: Description of the expense
        date: Date of expense (YYYY-MM-DD format)

    Returns:
        Dictionary containing the result of creating the expense
    """
    print(f"--- Tool: create_expense called for: {category} - ${amount} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if user exists, if not create them
        cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"User {user_id} doesn't exist, creating user entry...")
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_id.replace('_', ' ').title(), f"{user_id}@example.com", "Unknown Company", "000-000-0000"))
            print(f"Created user entry for {user_id}")
        
        cursor.execute('''
            INSERT INTO expense (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, category, description, date))
        
        expense_id = cursor.lastrowid
        conn.commit()
        
        return {
            "action": "create_expense",
            "status": "success",
            "expense_id": expense_id,
            "amount": amount,
            "category": category,
            "description": description,
            "date": date,
            "message": f"Successfully recorded ${amount} expense for {category}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_expense",
            "status": "error",
            "error": str(e),
            "message": f"Failed to create expense: {category}"
        }
    finally:
        if conn:
            conn.close()

# EVENT TOOLS
def create_event(title: str, tool_context: ToolContext, contact_id: int, date: str,
                description: str, location: str) -> dict:
    """Schedule a new event.

    Args:
        title: Event title
        tool_context: Context for accessing session state
        contact_id: ID of the contact this event is with (optional)
        date: Event date and time (YYYY-MM-DD HH:MM:SS format)
        description: Event description
        location: Event location

    Returns:
        Dictionary containing the result of creating the event
    """
    print(f"--- Tool: create_event called for: {title} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if user exists, if not create them
        cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"User {user_id} doesn't exist, creating user entry...")
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_id.replace('_', ' ').title(), f"{user_id}@example.com", "Unknown Company", "000-000-0000"))
            print(f"Created user entry for {user_id}")
        
        # Verify contact exists if provided
        if contact_id and contact_id > 0:
            cursor.execute("SELECT name FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
            contact = cursor.fetchone()
            
            if not contact:
                return {
                    "action": "create_event",
                    "status": "error",
                    "error": f"Contact with ID {contact_id} not found",
                    "message": f"Contact {contact_id} not found"
                }
        
        # Handle contact_id - if 0, set to None for database
        contact_id_for_db = contact_id if contact_id > 0 else None
        
        cursor.execute('''
            INSERT INTO event (user_id, contact_id, title, date, description, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, contact_id_for_db, title, date, description, location))
        
        event_id = cursor.lastrowid
        conn.commit()
        
        contact_name = None
        if contact_id and contact_id > 0:
            cursor.execute("SELECT name FROM contact WHERE id = ?", (contact_id,))
            contact_info = cursor.fetchone()
            contact_name = contact_info[0] if contact_info else "Unknown"
        
        return {
            "action": "create_event",
            "status": "success",
            "event_id": event_id,
            "title": title,
            "date": date,
            "contact_id": contact_id,
            "contact_name": contact_name,
            "location": location,
            "description": description,
            "message": f"Successfully created event: {title}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_event",
            "status": "error",
            "error": str(e),
            "message": f"Failed to create event: {title}"
        }
    finally:
        if conn:
            conn.close()

def list_upcoming_events(tool_context: ToolContext) -> dict:
    """Get list of upcoming events.

    Args:
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing upcoming events
    """
    print("--- Tool: list_upcoming_events called ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            SELECT e.*, c.name as contact_name, c.company
            FROM event e
            LEFT JOIN contact c ON e.contact_id = c.id
            WHERE e.user_id = ? AND e.date >= ?
            ORDER BY e.date
        ''', (user_id, current_date))
        
        events = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "list_upcoming_events",
            "status": "success",
            "events_count": len(events),
            "events": events,
            "message": f"Found {len(events)} upcoming events"
        }
        
    except Exception as e:
        return {
            "action": "list_upcoming_events",
            "status": "error",
            "error": str(e),
            "message": "Failed to retrieve upcoming events"
        }
    finally:
        if conn:
            conn.close()

# INTERACTION TOOLS
def log_interaction(contact_id: int, tool_context: ToolContext, date: str, 
                   interaction_type: str, summary: str) -> dict:
    """Log an interaction with a contact.

    Args:
        contact_id: ID of the contact
        tool_context: Context for accessing session state
        date: Date of interaction (YYYY-MM-DD format)
        interaction_type: Type of interaction (call, email, meeting, note)
        summary: Summary of the interaction

    Returns:
        Dictionary containing the result of logging the interaction
    """
    print(f"--- Tool: log_interaction called for contact_id: {contact_id}, type: {interaction_type} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Validate interaction type
    valid_types = ['call', 'email', 'meeting', 'note']
    if interaction_type.lower() not in valid_types:
        interaction_type = 'note'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if user exists, if not create them
        cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            print(f"User {user_id} doesn't exist, creating user entry...")
            cursor.execute('''
                INSERT INTO user (id, name, email, company, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, user_id.replace('_', ' ').title(), f"{user_id}@example.com", "Unknown Company", "000-000-0000"))
            print(f"Created user entry for {user_id}")
        
        # Verify contact exists
        cursor.execute("SELECT name FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        contact = cursor.fetchone()
        
        if not contact:
            return {
                "action": "log_interaction",
                "status": "error",
                "error": f"Contact with ID {contact_id} not found",
                "message": f"Contact {contact_id} not found"
            }
        
        cursor.execute('''
            INSERT INTO interaction (user_id, contact_id, date, type, summary)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, contact_id, date, interaction_type.lower(), summary))
        
        interaction_id = cursor.lastrowid
        conn.commit()
        
        return {
            "action": "log_interaction",
            "status": "success",
            "interaction_id": interaction_id,
            "contact_id": contact_id,
            "contact_name": contact[0],
            "date": date,
            "type": interaction_type.lower(),
            "summary": summary,
            "message": f"Successfully logged {interaction_type} interaction with {contact[0]}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "log_interaction",
            "status": "error",
            "error": str(e),
            "message": f"Failed to log interaction for contact {contact_id}"
        }
    finally:
        if conn:
            conn.close()

def read_interactions(contact_id: int, tool_context: ToolContext) -> dict:
    """View interaction history for a specific contact.

    Args:
        contact_id: ID of the contact
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing interaction history
    """
    print(f"--- Tool: read_interactions called for contact_id: {contact_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Verify contact exists
        cursor.execute("SELECT name FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        contact = cursor.fetchone()
        
        if not contact:
            return {
                "action": "read_interactions",
                "status": "error",
                "error": f"Contact with ID {contact_id} not found",
                "message": f"Contact {contact_id} not found"
            }
        
        cursor.execute('''
            SELECT * FROM interaction 
            WHERE contact_id = ? AND user_id = ?
            ORDER BY date DESC
        ''', (contact_id, user_id))
        
        interactions = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "read_interactions",
            "status": "success",
            "contact_id": contact_id,
            "contact_name": contact[0],
            "interactions_count": len(interactions),
            "interactions": interactions,
            "message": f"Found {len(interactions)} interactions with {contact[0]}"
        }
        
    except Exception as e:
        return {
            "action": "read_interactions",
            "status": "error",
            "error": str(e),
            "message": f"Failed to retrieve interactions for contact {contact_id}"
        }
    finally:
        if conn:
            conn.close()

# REPORTING TOOLS
def generate_report(report_type: str, tool_context: ToolContext, period: str) -> dict:
    """Generate business reports.

    Args:
        report_type: Type of report (revenue, expenses, contacts, invoices, interactions)
        tool_context: Context for accessing session state
        period: Time period (this_month, last_month, this_quarter, this_year, all_time)

    Returns:
        Dictionary containing the requested report
    """
    print(f"--- Tool: generate_report called for: {report_type} ({period}) ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    
    try:
        if report_type.lower() == "revenue":
            return _generate_revenue_report(user_id, period)
        elif report_type.lower() == "expenses":
            return _generate_expense_report(user_id, period)
        elif report_type.lower() == "contacts":
            return _generate_contact_report(user_id)
        elif report_type.lower() == "invoices":
            return _generate_invoice_report(user_id, period)
        elif report_type.lower() == "interactions":
            return _generate_interaction_report(user_id, period)
        else:
            return {
                "action": "generate_report",
                "status": "error",
                "error": f"Unknown report type: {report_type}",
                "message": f"Report type '{report_type}' not supported"
            }
            
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": f"Failed to generate {report_type} report"
        }

def _generate_revenue_report(user_id: str, period: str) -> dict:
    """Generate revenue report."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT r.*, i.contact_id, c.name as contact_name, c.company
            FROM revenue r
            JOIN invoice i ON r.invoice_id = i.id
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ?
        ''', (user_id,))
        
        revenues = [dict(row) for row in cursor.fetchall()]
        total_revenue = sum(rev['amount'] for rev in revenues)
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "revenue",
            "period": period,
            "total_revenue": total_revenue,
            "revenue_entries": len(revenues),
            "average_revenue": total_revenue / len(revenues) if revenues else 0,
            "revenue_details": revenues,
            "message": f"Revenue report generated: ${total_revenue:.2f} total"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate revenue report"
        }
    finally:
        if conn:
            conn.close()

def _generate_expense_report(user_id: str, period: str) -> dict:
    """Generate expense report."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute("SELECT * FROM expense WHERE user_id = ?", (user_id,))
        expenses = [dict(row) for row in cursor.fetchall()]
        
        total_expenses = sum(exp['amount'] for exp in expenses)
        
        # Group by category
        category_totals = {}
        for expense in expenses:
            category = expense['category']
            category_totals[category] = category_totals.get(category, 0) + expense['amount']
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "expenses",
            "period": period,
            "total_expenses": total_expenses,
            "expense_count": len(expenses),
            "categories": category_totals,
            "expense_details": expenses,
            "message": f"Expense report generated: ${total_expenses:.2f} total"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate expense report"
        }
    finally:
        if conn:
            conn.close()

def _generate_contact_report(user_id: str) -> dict:
    """Generate contact report."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute("SELECT * FROM contact WHERE user_id = ?", (user_id,))
        contacts = [dict(row) for row in cursor.fetchall()]
        
        status_counts = {}
        for contact in contacts:
            status = contact['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "contacts",
            "total_contacts": len(contacts),
            "status_breakdown": status_counts,
            "contact_details": contacts,
            "message": f"Contact report generated: {len(contacts)} total contacts"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate contact report"
        }
    finally:
        if conn:
            conn.close()

def _generate_invoice_report(user_id: str, period: str) -> dict:
    """Generate invoice report."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT i.*, c.name as contact_name, c.company
            FROM invoice i
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ?
        ''', (user_id,))
        
        invoices = [dict(row) for row in cursor.fetchall()]
        
        status_counts = {}
        status_amounts = {}
        
        for invoice in invoices:
            status = invoice['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            status_amounts[status] = status_amounts.get(status, 0) + invoice['total_amount']
        
        total_amount = sum(inv['total_amount'] for inv in invoices)
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "invoices",
            "period": period,
            "total_invoices": len(invoices),
            "total_amount": total_amount,
            "status_counts": status_counts,
            "status_amounts": status_amounts,
            "invoice_details": invoices,
            "message": f"Invoice report generated: {len(invoices)} invoices, ${total_amount:.2f} total"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate invoice report"
        }
    finally:
        if conn:
            conn.close()

def _generate_interaction_report(user_id: str, period: str) -> dict:
    """Generate interaction report."""
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT i.*, c.name as contact_name, c.company
            FROM interaction i
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ?
        ''', (user_id,))
        
        interactions = [dict(row) for row in cursor.fetchall()]
        
        type_counts = {}
        for interaction in interactions:
            interaction_type = interaction['type']
            type_counts[interaction_type] = type_counts.get(interaction_type, 0) + 1
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "interactions",
            "period": period,
            "total_interactions": len(interactions),
            "type_breakdown": type_counts,
            "interaction_details": interactions,
            "message": f"Interaction report generated: {len(interactions)} total interactions"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate interaction report"
        }
    finally:
        if conn:
            conn.close()

def profit_loss_report(period: str, tool_context: ToolContext) -> dict:
    """Generate profit and loss report.
    
    Args:
        period: Time period (this_month, last_month, this_quarter, this_year, all_time)
        tool_context: Context for accessing session state
    Returns:
        Dictionary containing the requested report
    """
    
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    user_id = tool_context.state.get("user_id", "demo_user")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Get all revenue data
        cursor.execute('''
            SELECT r.*, i.contact_id, c.name as contact_name, c.company
            FROM revenue r
            JOIN invoice i ON r.invoice_id = i.id
            LEFT JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ?
        ''', (user_id,))
        
        revenues = [dict(row) for row in cursor.fetchall()]
        total_revenue = sum(rev['amount'] for rev in revenues)
        
        # Get all expense data
        cursor.execute("SELECT * FROM expense WHERE user_id = ?", (user_id,))
        expenses = [dict(row) for row in cursor.fetchall()]
        total_expenses = sum(exp['amount'] for exp in expenses)
        
        # Calculate profit/loss
        net_profit_loss = total_revenue - total_expenses
        profit_margin = (net_profit_loss / total_revenue * 100) if total_revenue > 0 else 0
        
        # Group expenses by category for detailed breakdown
        expense_breakdown = {}
        for expense in expenses:
            category = expense['category']
            expense_breakdown[category] = expense_breakdown.get(category, 0) + expense['amount']
        
        # Determine financial status
        if net_profit_loss > 0:
            financial_status = "profitable"
            status_message = f"Business is profitable with ${net_profit_loss:.2f} net profit"
        elif net_profit_loss < 0:
            financial_status = "loss"
            status_message = f"Business has a loss of ${abs(net_profit_loss):.2f}"
        else:
            financial_status = "breakeven"
            status_message = "Business is at breakeven point"
        
        return {
            "action": "generate_report",
            "status": "success",
            "report_type": "profit_loss",
            "period": period,
            "financial_summary": {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "net_profit_loss": net_profit_loss,
                "profit_margin": profit_margin,
                "financial_status": financial_status
            },
            "revenue_details": {
                "revenue_count": len(revenues),
                "revenue_entries": revenues
            },
            "expense_details": {
                "expense_count": len(expenses),
                "expense_breakdown": expense_breakdown,
                "expense_entries": expenses
            },
            "insights": [
                status_message,
                f"Profit margin: {profit_margin:.2f}%",
                f"Revenue from {len(revenues)} transactions",
                f"Expenses across {len(expense_breakdown)} categories"
            ],
            "message": f"P&L report generated: {status_message}"
        }
        
    except Exception as e:
        return {
            "action": "generate_report",
            "status": "error",
            "error": str(e),
            "message": "Failed to generate profit and loss report"
        }
    finally:
        if conn:
            conn.close()
            
def parse_natural_date(date_text: str) -> dict:
    """Parse natural language date/time expressions into standard formats.
    
    Args:
        date_text: Natural language date/time string (e.g., "Thursday at 2pm", "next Friday at 11am", "tomorrow", "in 3 days")
        
    Returns:
        Dictionary containing parsed date information in multiple formats
    """
    print(f"--- Tool: parse_natural_date called with: '{date_text}' ---")
    
    try:
        # Get current date as reference point
        now = datetime.now()
        
        # Clean the input text
        date_text = date_text.strip().lower()
        
        # Handle special cases first
        if date_text in ['today', 'now']:
            parsed_date = now
        elif date_text in ['tomorrow']:
            parsed_date = now + relativedelta(days=1)
        elif date_text in ['yesterday']:
            parsed_date = now - relativedelta(days=1)
        elif 'next week' in date_text:
            parsed_date = now + relativedelta(weeks=1)
        elif 'next month' in date_text:
            parsed_date = now + relativedelta(months=1)
        else:
            # Handle relative expressions like "in 3 days", "in 2 weeks"
            relative_match = re.search(r'in (\d+) (day|days|week|weeks|month|months)', date_text)
            if relative_match:
                number = int(relative_match.group(1))
                unit = relative_match.group(2)
                
                if 'day' in unit:
                    parsed_date = now + relativedelta(days=number)
                elif 'week' in unit:
                    parsed_date = now + relativedelta(weeks=number)
                elif 'month' in unit:
                    parsed_date = now + relativedelta(months=number)
                else:
                    parsed_date = now
            else:
                # Try parsing with dateutil - it handles many natural language formats
                try:
                    parsed_date = date_parser.parse(date_text, default=now, fuzzy=True)
                except:
                    # If parsing fails, try with some preprocessing
                    # Handle day names with times
                    day_time_match = re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday).*?(\d{1,2})(am|pm)', date_text)
                    if day_time_match:
                        day_name = day_time_match.group(1)
                        hour = int(day_time_match.group(2))
                        ampm = day_time_match.group(3)
                        
                        if ampm == 'pm' and hour != 12:
                            hour += 12
                        elif ampm == 'am' and hour == 12:
                            hour = 0
                        
                        # Find next occurrence of the day
                        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                        target_day = days.index(day_name)
                        current_day = now.weekday()
                        
                        days_ahead = target_day - current_day
                        if days_ahead <= 0:  # Target day already happened this week
                            days_ahead += 7
                        
                        parsed_date = now + relativedelta(days=days_ahead)
                        parsed_date = parsed_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                    else:
                        # Final fallback - just parse what we can
                        parsed_date = date_parser.parse(date_text, default=now, fuzzy=True)
        
        # Format the parsed date in various useful formats
        return {
            "action": "parse_natural_date",
            "status": "success",
            "original_input": date_text,
            "parsed_datetime": parsed_date.isoformat(),
            "formatted_date": parsed_date.strftime("%Y-%m-%d"),
            "formatted_time": parsed_date.strftime("%H:%M:%S"),
            "formatted_datetime": parsed_date.strftime("%Y-%m-%d %H:%M:%S"),
            "formatted_display": parsed_date.strftime("%A, %B %d, %Y at %I:%M %p"),
            "day_of_week": parsed_date.strftime("%A"),
            "relative_description": _get_relative_description(parsed_date, now),
            "timestamp": parsed_date.timestamp(),
            "message": f"Parsed '{date_text}' as {parsed_date.strftime('%Y-%m-%d %H:%M:%S')}"
        }
        
    except Exception as e:
        return {
            "action": "parse_natural_date",
            "status": "error",
            "error": str(e),
            "original_input": date_text,
            "message": f"Failed to parse date: '{date_text}'. Please try a different format."
        }

def _get_relative_description(target_date: datetime, reference_date: datetime) -> str:
    """Generate a human-readable relative description of the date."""
    delta = target_date - reference_date
    
    if delta.days == 0:
        return "today"
    elif delta.days == 1:
        return "tomorrow"
    elif delta.days == -1:
        return "yesterday"
    elif 0 < delta.days < 7:
        return f"in {delta.days} days"
    elif delta.days < 0 and delta.days > -7:
        return f"{abs(delta.days)} days ago"
    elif delta.days >= 7:
        weeks = delta.days // 7
        if weeks == 1:
            return "next week"
        else:
            return f"in {weeks} weeks"
    else:
        weeks = abs(delta.days) // 7
        if weeks == 1:
            return "last week"
        else:
            return f"{weeks} weeks ago"

def get_current_datetime() -> dict:
    """Get the current date and time.

    Returns:
        Dictionary containing current date and time information
    """
    print("--- Tool: get_current_datetime called ---")
    
    try:
        from datetime import datetime
        
        now = datetime.now()
        
        return {
            "action": "get_current_datetime",
            "status": "success",
            "current_datetime": now.isoformat(),
            "formatted_date": now.strftime("%Y-%m-%d"),
            "formatted_time": now.strftime("%H:%M:%S"),
            "formatted_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month_name": now.strftime("%B"),
            "year": now.year,
            "message": f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
        }
        
    except Exception as e:
        return {
            "action": "get_current_datetime",
            "status": "error",
            "error": str(e),
            "message": "Failed to get current date and time"
        }

