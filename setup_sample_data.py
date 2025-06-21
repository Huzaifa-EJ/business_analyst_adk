#!/usr/bin/env python3
"""
Setup sample data for the business agent database
This script uses a direct approach that works with the existing infrastructure
"""

import sqlite3
from datetime import date, timedelta

def setup_database():
    """Setup database with sample data."""
    print("🚀 Setting up sample data for business agent...")
    
    # Connect to database
    conn = sqlite3.connect('business_agent.db')
    cursor = conn.cursor()
    
    try:
        # Create business tables if they don't exist
        tables = [
            '''CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT,
                email TEXT,
                phone TEXT,
                company TEXT,
                notes TEXT,
                status TEXT DEFAULT 'lead'
            )''',
            '''CREATE TABLE IF NOT EXISTS invoice (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                contact_id INTEGER NOT NULL,
                issue_date TEXT,
                due_date TEXT,
                total_amount REAL,
                status TEXT DEFAULT 'unpaid',
                notes TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS expense (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                contact_id INTEGER,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                location TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS interaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                contact_id INTEGER NOT NULL,
                date TEXT,
                type TEXT,
                summary TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT
            )'''
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        print("✅ Database tables created")
        
        # Clear existing demo data
        user_id = 'huzaifa_ejaz'
        cursor.execute("DELETE FROM interaction WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM revenue WHERE invoice_id IN (SELECT id FROM invoice WHERE user_id = ?)", (user_id,))
        cursor.execute("DELETE FROM invoice WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM event WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM expense WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM contact WHERE user_id = ?", (user_id,))
        
        # Add sample contacts
        contacts = [
            (user_id, 'John Smith', 'john@techcorp.com', '+1-555-0123', 'TechCorp Inc', 'Key decision maker', 'client'),
            (user_id, 'Sarah Johnson', 'sarah@marketing.com', '+1-555-0234', 'Marketing Ltd', 'CMO prospect', 'lead'),
            (user_id, 'Michael Brown', 'mike@innovate.com', '+1-555-0345', 'Innovate Tech', 'CTO evaluation', 'prospect'),
            (user_id, 'Lisa Davis', 'lisa@global.com', '+1-555-0456', 'Global Corp', 'HR Director', 'client'),
            (user_id, 'Robert Wilson', 'rob@startup.com', '+1-555-0567', 'Startup Ventures', 'Founder', 'lead'),
            (user_id, 'David Miller', 'david@retail.com', '+1-555-0789', 'Retail Co', 'Operations Manager', 'client'),
        ]
        
        cursor.executemany('''
            INSERT INTO contact (user_id, name, email, phone, company, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', contacts)
        
        print(f"✅ Added {len(contacts)} contacts")
        
        # Get contact IDs
        cursor.execute("SELECT id FROM contact WHERE user_id = ? ORDER BY id", (user_id,))
        contact_ids = [row[0] for row in cursor.fetchall()]
        
        # Add sample invoices
        today = date.today()
        invoices = [
            (user_id, contact_ids[0], (today-timedelta(days=30)).isoformat(), today.isoformat(), 15000.00, 'paid', 'Premium package'),
            (user_id, contact_ids[3], (today-timedelta(days=45)).isoformat(), (today-timedelta(days=15)).isoformat(), 8500.00, 'paid', 'Collaboration tools'),
            (user_id, contact_ids[5], (today-timedelta(days=20)).isoformat(), (today+timedelta(days=10)).isoformat(), 12000.00, 'unpaid', 'Efficiency tools'),
            (user_id, contact_ids[1], (today-timedelta(days=10)).isoformat(), (today+timedelta(days=20)).isoformat(), 6500.00, 'unpaid', 'Marketing package'),
            (user_id, contact_ids[4], (today-timedelta(days=5)).isoformat(), (today+timedelta(days=25)).isoformat(), 9200.00, 'unpaid', 'Startup solution'),
            (user_id, contact_ids[2], (today-timedelta(days=60)).isoformat(), (today-timedelta(days=30)).isoformat(), 18500.00, 'paid', 'Tech implementation'),
        ]
        
        cursor.executemany('''
            INSERT INTO invoice (user_id, contact_id, issue_date, due_date, total_amount, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', invoices)
        
        print(f"✅ Added {len(invoices)} invoices")
        
        # Add revenue for paid invoices
        cursor.execute("SELECT id, total_amount FROM invoice WHERE user_id = ? AND status = 'paid'", (user_id,))
        paid_invoices = cursor.fetchall()
        
        revenue_data = [(invoice_id, amount, today.isoformat()) for invoice_id, amount in paid_invoices]
        cursor.executemany('''
            INSERT INTO revenue (invoice_id, amount, date)
            VALUES (?, ?, ?)
        ''', revenue_data)
        
        print(f"✅ Added {len(revenue_data)} revenue records")
        
        # Add sample expenses
        expenses = [
            (user_id, 500.00, 'Office Supplies', 'Monthly supplies', (today-timedelta(days=5)).isoformat()),
            (user_id, 1200.00, 'Software', 'License renewal', (today-timedelta(days=15)).isoformat()),
            (user_id, 800.00, 'Marketing', 'Ad campaign', (today-timedelta(days=10)).isoformat()),
            (user_id, 350.00, 'Travel', 'Client meetings', (today-timedelta(days=20)).isoformat()),
            (user_id, 2500.00, 'Equipment', 'New laptops', (today-timedelta(days=25)).isoformat()),
            (user_id, 450.00, 'Utilities', 'Office utilities', (today-timedelta(days=30)).isoformat()),
            (user_id, 1800.00, 'Training', 'Team development', (today-timedelta(days=35)).isoformat()),
            (user_id, 300.00, 'Communications', 'Phone & internet', (today-timedelta(days=40)).isoformat()),
        ]
        
        cursor.executemany('''
            INSERT INTO expense (user_id, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?)
        ''', expenses)
        
        print(f"✅ Added {len(expenses)} expenses")
        
        # Add sample events
        events = [
            (user_id, 'Client Meeting - TechCorp', (today+timedelta(days=3)).isoformat() + ' 14:00:00', contact_ids[0], 'Quarterly review', 'TechCorp Office'),
            (user_id, 'Demo - Marketing Solutions', (today+timedelta(days=7)).isoformat() + ' 10:00:00', contact_ids[1], 'Product demo', 'Online'),
            (user_id, 'Call - Innovate Tech', (today+timedelta(days=5)).isoformat() + ' 15:30:00', contact_ids[2], 'Tech discussion', 'Phone'),
            (user_id, 'Signing - Global Corp', (today+timedelta(days=10)).isoformat() + ' 11:00:00', contact_ids[3], 'Contract signing', 'Our Office'),
            (user_id, 'Team Meeting', (today+timedelta(days=1)).isoformat() + ' 09:00:00', None, 'Monthly planning', 'Conference Room'),
        ]
        
        cursor.executemany('''
            INSERT INTO event (user_id, title, date, contact_id, description, location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', events)
        
        print(f"✅ Added {len(events)} events")
        
        # Add sample interactions
        interactions = [
            (user_id, contact_ids[0], (today-timedelta(days=2)).isoformat(), 'call', 'Discussed quarterly metrics'),
            (user_id, contact_ids[1], (today-timedelta(days=5)).isoformat(), 'email', 'Sent detailed proposal'),
            (user_id, contact_ids[2], (today-timedelta(days=7)).isoformat(), 'meeting', 'Requirements gathering'),
            (user_id, contact_ids[3], (today-timedelta(days=3)).isoformat(), 'call', 'Contract negotiations'),
            (user_id, contact_ids[4], (today-timedelta(days=8)).isoformat(), 'email', 'Follow-up consultation'),
            (user_id, contact_ids[5], (today-timedelta(days=6)).isoformat(), 'call', 'Progress update'),
        ]
        
        cursor.executemany('''
            INSERT INTO interaction (user_id, contact_id, date, type, summary)
            VALUES (?, ?, ?, ?, ?)
        ''', interactions)
        
        print(f"✅ Added {len(interactions)} interactions")
        
        # Commit changes
        conn.commit()
        
        # Summary
        cursor.execute("SELECT COUNT(*) FROM contact WHERE user_id = ?", (user_id,))
        contact_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM invoice WHERE user_id = ?", (user_id,))
        invoice_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM expense WHERE user_id = ?", (user_id,))
        expense_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(total_amount) FROM invoice WHERE user_id = ? AND status = 'paid'", (user_id,))
        paid_total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(total_amount) FROM invoice WHERE user_id = ? AND status = 'unpaid'", (user_id,))
        unpaid_total = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(amount) FROM expense WHERE user_id = ?", (user_id,))
        expense_total = cursor.fetchone()[0] or 0
        
        print(f"\n🎉 Sample data setup complete!")
        print(f"📊 Summary:")
        print(f"   • {contact_count} contacts")
        print(f"   • {invoice_count} invoices")
        print(f"   • {expense_count} expenses")
        print(f"   • {len(events)} events")
        print(f"   • {len(interactions)} interactions")
        print(f"\n💰 Financial overview:")
        print(f"   • Paid invoices: ${paid_total:,.2f}")
        print(f"   • Unpaid invoices: ${unpaid_total:,.2f}")
        print(f"   • Total expenses: ${expense_total:,.2f}")
        print(f"   • Net profit: ${paid_total - expense_total:,.2f}")
        
        print(f"\n✅ Your business agent is ready to use!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    return True

if __name__ == "__main__":
    success = setup_database()
    if success:
        print("\n🚀 You can now test your business agent with realistic sample data!")
        print("Try asking questions like:")
        print("• 'Show me unpaid invoices'")
        print("• 'What's my revenue this month?'")
        print("• 'List my upcoming events'")
        print("• 'Show expense breakdown by category'")
    else:
        print("\n❌ Setup failed. Please check the error messages above.") 