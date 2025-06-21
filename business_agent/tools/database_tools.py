from google.adk.tools import ToolContext
import sqlite3
from datetime import datetime

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

# USER TOOLS
def create_user(user_id: str, name: str, tool_context: ToolContext, email: str, 
               company: str, phone: str) -> dict:
    """Create a new user account.

    Args:
        user_id: Unique user identifier
        name: User's full name
        tool_context: Context for accessing session state
        email: User's email address
        company: User's company name
        phone: User's phone number

    Returns:
        Dictionary containing the result of creating the user
    """
    print(f"--- Tool: create_user called for: {name} ({user_id}) ---")
    
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            INSERT INTO user (id, name, email, company, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, email, company, phone))
        
        conn.commit()
        
        return {
            "action": "create_user",
            "status": "success",
            "user_id": user_id,
            "name": name,
            "email": email,
            "company": company,
            "phone": phone,
            "message": f"Successfully created user: {name}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "create_user",
            "status": "error",
            "error": str(e),
            "message": f"Failed to create user: {name}"
        }
    finally:
        if conn:
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

# CONTACT LOOKUP TOOLS
def find_contact_by_name(name: str, tool_context: ToolContext) -> dict:
    """Find contact by name (supports partial matching).

    Args:
        name: Contact's name (can be partial)
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing matching contacts
    """
    print(f"--- Tool: find_contact_by_name called for: {name} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Use LIKE for partial matching
        cursor.execute('''
            SELECT * FROM contact 
            WHERE user_id = ? AND name LIKE ?
            ORDER BY name
        ''', (user_id, f"%{name}%"))
        
        contacts = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "find_contact_by_name",
            "status": "success",
            "search_term": name,
            "matches_found": len(contacts),
            "contacts": contacts,
            "message": f"Found {len(contacts)} contacts matching '{name}'"
        }
        
    except Exception as e:
        return {
            "action": "find_contact_by_name",
            "status": "error",
            "error": str(e),
            "message": f"Failed to search for contact: {name}"
        }
    finally:
        if conn:
            conn.close()

def find_contact_by_email(email: str, tool_context: ToolContext) -> dict:
    """Find contact by email address.

    Args:
        email: Contact's email address
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing matching contact
    """
    print(f"--- Tool: find_contact_by_email called for: {email} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT * FROM contact 
            WHERE user_id = ? AND email LIKE ?
        ''', (user_id, f"%{email}%"))
        
        contacts = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "find_contact_by_email",
            "status": "success",
            "search_email": email,
            "matches_found": len(contacts),
            "contacts": contacts,
            "message": f"Found {len(contacts)} contacts with email containing '{email}'"
        }
        
    except Exception as e:
        return {
            "action": "find_contact_by_email",
            "status": "error",
            "error": str(e),
            "message": f"Failed to search for email: {email}"
        }
    finally:
        if conn:
            conn.close()

def find_contact_by_company(company: str, tool_context: ToolContext) -> dict:
    """Find contacts by company name.

    Args:
        company: Company name (supports partial matching)
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing matching contacts
    """
    print(f"--- Tool: find_contact_by_company called for: {company} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        cursor.execute('''
            SELECT * FROM contact 
            WHERE user_id = ? AND company LIKE ?
            ORDER BY name
        ''', (user_id, f"%{company}%"))
        
        contacts = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "find_contact_by_company",
            "status": "success",
            "search_company": company,
            "matches_found": len(contacts),
            "contacts": contacts,
            "message": f"Found {len(contacts)} contacts from companies matching '{company}'"
        }
        
    except Exception as e:
        return {
            "action": "find_contact_by_company",
            "status": "error",
            "error": str(e),
            "message": f"Failed to search for company: {company}"
        }
    finally:
        if conn:
            conn.close()

def update_contact_by_name(name: str, tool_context: ToolContext, new_name: str, 
                          email: str, phone: str, company: str, 
                          notes: str, status: str) -> dict:
    """Update a contact by their name instead of ID.

    Args:
        name: Current name of the contact to update
        tool_context: Context for accessing session state
        new_name: New name for the contact
        email: Updated email address
        phone: Updated phone number
        company: Updated company name
        notes: Updated notes
        status: Updated contact status

    Returns:
        Dictionary containing the result of updating the contact
    """
    print(f"--- Tool: update_contact_by_name called for: {name} ---")
    
    # First find the contact
    find_result = find_contact_by_name(name, tool_context)
    
    if find_result["status"] != "success" or find_result["matches_found"] == 0:
        return {
            "action": "update_contact_by_name",
            "status": "error",
            "error": f"No contact found with name '{name}'",
            "message": f"Cannot find contact '{name}' to update"
        }
    
    if find_result["matches_found"] > 1:
        return {
            "action": "update_contact_by_name", 
            "status": "error",
            "error": f"Multiple contacts found with name '{name}'",
            "found_contacts": find_result["contacts"],
            "message": f"Found {find_result['matches_found']} contacts. Please be more specific or use contact ID."
        }
    
    # Get the contact ID and update
    contact = find_result["contacts"][0]
    contact_id = contact["id"]
    
    # Use new_name if provided, otherwise keep current name
    update_name = new_name if new_name and new_name.strip() else contact["name"]
    
    # Use existing values if new values are empty
    update_email = email if email and email.strip() else contact["email"]
    update_phone = phone if phone and phone.strip() else contact["phone"]  
    update_company = company if company and company.strip() else contact["company"]
    update_notes = notes if notes and notes.strip() else contact["notes"]
    update_status = status if status and status.strip() else contact["status"]
    
    result = update_contact(contact_id, tool_context, update_name, update_email, update_phone, update_company, update_notes, update_status)
    
    # Enhance the success message to be more explicit
    if result.get("status") == "success":
        result["message"] = f"✅ Successfully updated contact '{name}' to '{update_name}'"
        result["action"] = "update_contact_by_name"
    
    return result

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

def update_invoice(invoice_id: int, tool_context: ToolContext, issue_date: str, due_date: str,
                  total_amount: float, status: str, notes: str) -> dict:
    """Update an existing invoice.

    Args:
        invoice_id: ID of the invoice to update
        issue_date: Updated issue date (YYYY-MM-DD format)
        due_date: Updated due date (YYYY-MM-DD format)
        total_amount: Updated total amount
        status: Updated status
        notes: Updated notes
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of updating the invoice
    """
    print(f"--- Tool: update_invoice called for invoice_id: {invoice_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Check if invoice exists
        cursor.execute("SELECT * FROM invoice WHERE id = ? AND user_id = ?", (invoice_id, user_id))
        invoice = cursor.fetchone()
        
        if not invoice:
            return {
                "action": "update_invoice",
                "status": "error",
                "error": f"Invoice with ID {invoice_id} not found",
                "message": f"Invoice {invoice_id} not found"
            }
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if issue_date and issue_date.strip():
            update_fields.append("issue_date = ?")
            update_values.append(issue_date)
        if due_date and due_date.strip():
            update_fields.append("due_date = ?")
            update_values.append(due_date)
        if total_amount > 0:
            update_fields.append("total_amount = ?")
            update_values.append(total_amount)
        if status and status.strip():
            valid_statuses = ['unpaid', 'paid', 'overdue', 'cancelled']
            if status.lower() in valid_statuses:
                update_fields.append("status = ?")
                update_values.append(status.lower())
        if notes and notes.strip():
            update_fields.append("notes = ?")
            update_values.append(notes)
        
        if not update_fields:
            return {
                "action": "update_invoice",
                "status": "warning",
                "message": "No fields provided to update"
            }
        
        update_values.extend([invoice_id, user_id])
        update_query = f"UPDATE invoice SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
        
        cursor.execute(update_query, update_values)
        conn.commit()
        
        return {
            "action": "update_invoice",
            "status": "success",
            "invoice_id": invoice_id,
            "message": f"Successfully updated invoice {invoice_id}"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "update_invoice",
            "status": "error",
            "error": str(e),
            "message": f"Failed to update invoice {invoice_id}"
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



def find_invoices_by_contact_name(contact_name: str, tool_context: ToolContext) -> dict:
    """Find all invoices for a contact by name.

    Args:
        contact_name: Name of the contact
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing invoices for the contact
    """
    print(f"--- Tool: find_invoices_by_contact_name called for: {contact_name} ---")
    
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
            JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ? AND c.name LIKE ?
            ORDER BY i.issue_date DESC
        ''', (user_id, f"%{contact_name}%"))
        
        invoices = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "find_invoices_by_contact_name",
            "status": "success",
            "contact_name": contact_name,
            "invoices_found": len(invoices),
            "invoices": invoices,
            "message": f"Found {len(invoices)} invoices for contacts matching '{contact_name}'"
        }
        
    except Exception as e:
        return {
            "action": "find_invoices_by_contact_name",
            "status": "error",
            "error": str(e),
            "message": f"Failed to find invoices for: {contact_name}"
        }
    finally:
        if conn:
            conn.close()

# ENHANCED INVOICE TOOLS
def create_invoice_by_contact_name(contact_name: str, total_amount: float, 
                                  tool_context: ToolContext, issue_date: str, 
                                  due_date: str, status: str, 
                                  notes: str) -> dict:
    """Create an invoice using contact name instead of ID.

    Args:
        contact_name: Name of the contact
        total_amount: Invoice total amount
        tool_context: Context for accessing session state
        issue_date: Invoice issue date
        due_date: Invoice due date
        status: Invoice status
        notes: Additional notes

    Returns:
        Dictionary containing the result of creating the invoice
    """
    print(f"--- Tool: create_invoice_by_contact_name called for: {contact_name} ---")
    
    # Find the contact first
    find_result = find_contact_by_name(contact_name, tool_context)
    
    if find_result["status"] != "success" or find_result["matches_found"] == 0:
        return {
            "action": "create_invoice_by_contact_name",
            "status": "error",
            "error": f"No contact found with name '{contact_name}'",
            "message": f"Cannot find contact '{contact_name}' to create invoice"
        }
    
    if find_result["matches_found"] > 1:
        return {
            "action": "create_invoice_by_contact_name",
            "status": "error", 
            "error": f"Multiple contacts found with name '{contact_name}'",
            "found_contacts": find_result["contacts"],
            "message": f"Found {find_result['matches_found']} contacts. Please be more specific."
        }
    
    # Get contact ID and create invoice
    contact = find_result["contacts"][0]
    contact_id = contact["id"]
    
    return create_invoice(contact_id, tool_context, issue_date, due_date, total_amount, status, notes)

def find_invoices_by_contact_name(contact_name: str, tool_context: ToolContext) -> dict:
    """Find all invoices for a contact by name.

    Args:
        contact_name: Name of the contact
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing invoices for the contact
    """
    print(f"--- Tool: find_invoices_by_contact_name called for: {contact_name} ---")
    
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
            JOIN contact c ON i.contact_id = c.id
            WHERE i.user_id = ? AND c.name LIKE ?
            ORDER BY i.issue_date DESC
        ''', (user_id, f"%{contact_name}%"))
        
        invoices = [dict(row) for row in cursor.fetchall()]
        
        return {
            "action": "find_invoices_by_contact_name",
            "status": "success",
            "contact_name": contact_name,
            "invoices_found": len(invoices),
            "invoices": invoices,
            "message": f"Found {len(invoices)} invoices for contacts matching '{contact_name}'"
        }
        
    except Exception as e:
        return {
            "action": "find_invoices_by_contact_name",
            "status": "error",
            "error": str(e),
            "message": f"Failed to find invoices for: {contact_name}"
        }
    finally:
        if conn:
            conn.close()

def find_invoices_by_status(status: str, tool_context: ToolContext) -> dict:
    """Find all invoices by status.

    Args:
        status: Invoice status (paid, unpaid, overdue, cancelled)
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing invoices with the specified status
    """
    print(f"--- Tool: find_invoices_by_status called for status: {status} ---")
    
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
            WHERE i.user_id = ? AND i.status = ?
            ORDER BY i.due_date ASC
        ''', (user_id, status.lower()))
        
        invoices = [dict(row) for row in cursor.fetchall()]
        
        total_amount = sum(inv['total_amount'] for inv in invoices)
        
        return {
            "action": "find_invoices_by_status",
            "status": "success",
            "invoice_status": status.lower(),
            "invoices_found": len(invoices),
            "total_amount": total_amount,
            "invoices": invoices,
            "message": f"Found {len(invoices)} {status} invoices totaling ${total_amount:.2f}"
        }
        
    except Exception as e:
        return {
            "action": "find_invoices_by_status",
            "status": "error",
            "error": str(e),
            "message": f"Failed to find {status} invoices"
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

# ENHANCED INTERACTION TOOLS
def log_interaction_by_contact_name(contact_name: str, tool_context: ToolContext, 
                                   date: str, interaction_type: str, 
                                   summary: str) -> dict:
    """Log an interaction using contact name instead of ID.

    Args:
        contact_name: Name of the contact
        tool_context: Context for accessing session state
        date: Date of interaction
        interaction_type: Type of interaction
        summary: Summary of the interaction

    Returns:
        Dictionary containing the result of logging the interaction
    """
    print(f"--- Tool: log_interaction_by_contact_name called for: {contact_name} ---")
    
    # Find the contact first
    find_result = find_contact_by_name(contact_name, tool_context)
    
    if find_result["status"] != "success" or find_result["matches_found"] == 0:
        return {
            "action": "log_interaction_by_contact_name",
            "status": "error",
            "error": f"No contact found with name '{contact_name}'",
            "message": f"Cannot find contact '{contact_name}' to log interaction"
        }
    
    if find_result["matches_found"] > 1:
        return {
            "action": "log_interaction_by_contact_name",
            "status": "error",
            "error": f"Multiple contacts found with name '{contact_name}'",
            "found_contacts": find_result["contacts"],
            "message": f"Found {find_result['matches_found']} contacts. Please be more specific."
        }
    
    # Get contact ID and log interaction
    contact = find_result["contacts"][0]
    contact_id = contact["id"]
    
    return log_interaction(contact_id, tool_context, date, interaction_type, summary)

def read_interactions_by_contact_name(contact_name: str, tool_context: ToolContext) -> dict:
    """Read interactions using contact name instead of ID.

    Args:
        contact_name: Name of the contact
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing interaction history
    """
    print(f"--- Tool: read_interactions_by_contact_name called for: {contact_name} ---")
    
    # Find the contact first
    find_result = find_contact_by_name(contact_name, tool_context)
    
    if find_result["status"] != "success" or find_result["matches_found"] == 0:
        return {
            "action": "read_interactions_by_contact_name",
            "status": "error",
            "error": f"No contact found with name '{contact_name}'",
            "message": f"Cannot find contact '{contact_name}' to read interactions"
        }
    
    if find_result["matches_found"] > 1:
        return {
            "action": "read_interactions_by_contact_name",
            "status": "error",
            "error": f"Multiple contacts found with name '{contact_name}'",
            "found_contacts": find_result["contacts"],
            "message": f"Found {find_result['matches_found']} contacts. Please be more specific."
        }
    
    # Get contact ID and read interactions
    contact = find_result["contacts"][0]
    contact_id = contact["id"]
    
    return read_interactions(contact_id, tool_context)

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

# COMMUNICATION TOOLS
def send_email(contact_id: int, subject: str, message: str, tool_context: ToolContext) -> dict:
    """Send email to a contact (simulated).

    Args:
        contact_id: ID of the contact
        subject: Email subject
        message: Email message
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of sending email
    """
    print(f"--- Tool: send_email called for contact_id: {contact_id} ---")
    
    user_id = tool_context.state.get("user_id", "demo_user")
    db_path = SESSIONS_DB.replace("sqlite:///", "")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Verify contact exists and get email
        cursor.execute("SELECT name, email FROM contact WHERE id = ? AND user_id = ?", (contact_id, user_id))
        contact = cursor.fetchone()
        
        if not contact:
            return {
                "action": "send_email",
                "status": "error",
                "error": f"Contact with ID {contact_id} not found",
                "message": f"Contact {contact_id} not found"
            }
        
        if not contact[1]:  # email column
            return {
                "action": "send_email",
                "status": "error",
                "error": f"No email address found for {contact[0]}",
                "message": f"No email address for {contact[0]}"
            }
        
        # Log this as an interaction
        current_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO interaction (user_id, contact_id, date, type, summary)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, contact_id, current_date, 'email', f"Sent email: {subject}"))
        
        conn.commit()
        
        return {
            "action": "send_email",
            "status": "success",
            "contact_id": contact_id,
            "contact_name": contact[0],
            "email": contact[1],
            "subject": subject,
            "message": f"Email sent to {contact[0]} ({contact[1]})"
        }
        
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            "action": "send_email",
            "status": "error",
            "error": str(e),
            "message": f"Failed to send email to contact {contact_id}"
        }
    finally:
        if conn:
            conn.close()

def send_email_by_contact_name(contact_name: str, subject: str, message: str, 
                              tool_context: ToolContext) -> dict:
    """Send email using contact name instead of ID.

    Args:
        contact_name: Name of the contact
        subject: Email subject
        message: Email message
        tool_context: Context for accessing session state

    Returns:
        Dictionary containing the result of sending email
    """
    print(f"--- Tool: send_email_by_contact_name called for: {contact_name} ---")
    
    # Find the contact first
    find_result = find_contact_by_name(contact_name, tool_context)
    
    if find_result["status"] != "success" or find_result["matches_found"] == 0:
        return {
            "action": "send_email_by_contact_name",
            "status": "error",
            "error": f"No contact found with name '{contact_name}'",
            "message": f"Cannot find contact '{contact_name}' to send email"
        }
    
    if find_result["matches_found"] > 1:
        return {
            "action": "send_email_by_contact_name",
            "status": "error",
            "error": f"Multiple contacts found with name '{contact_name}'",
            "found_contacts": find_result["contacts"],
            "message": f"Found {find_result['matches_found']} contacts. Please be more specific."
        }
    
    # Get contact and send email
    contact = find_result["contacts"][0]
    contact_id = contact["id"]
    
    return send_email(contact_id, subject, message, tool_context)

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