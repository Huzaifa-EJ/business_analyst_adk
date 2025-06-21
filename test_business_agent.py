#!/usr/bin/env python3
"""
Comprehensive Test Script for Business Analyst Agent

This script tests all the enhanced user-friendly tools and queries
without requiring database IDs, making the system more intuitive.
"""

import requests
import json
import time
import sys
from datetime import datetime
from user_friendly_test_queries import (
    CONTACT_MANAGEMENT_QUERIES,
    INVOICE_MANAGEMENT_QUERIES, 
    INTERACTION_MANAGEMENT_QUERIES,
    COMMUNICATION_QUERIES,
    EVENT_MANAGEMENT_QUERIES,
    EXPENSE_MANAGEMENT_QUERIES,
    REPORTING_QUERIES,
    COMPLEX_BUSINESS_QUERIES,
    NATURAL_LANGUAGE_QUERIES,
    EDGE_CASE_QUERIES,
    QUICK_TEST_QUERIES,
    ALL_USER_FRIENDLY_QUERIES
)

# Configuration
FLASK_API_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_agent"
DELAY_BETWEEN_TESTS = 1  # seconds

# Test queries from user_friendly_test_queries.py
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

CONTACT_MANAGEMENT_QUERIES = [
    "Find all contacts named John",
    "Search for contacts from TechCorp",
    "Find contact with email john@techcorp.com",
    "Add a new contact named 'Alice Johnson' with email 'alice@techstartup.com', phone '555-2001', company 'Tech Startup Inc', notes 'Potential high-value client', status 'prospect'",
    "Update John Smith's status to client",
    "Show me all my contacts",
]

INVOICE_MANAGEMENT_QUERIES = [
    "Create a $2500 invoice for John Smith due in 30 days",
    "Show me all invoices for John Smith",
    "Show me all unpaid invoices",
    "Find all paid invoices",
    "What's the total amount of unpaid invoices?",
]

INTERACTION_MANAGEMENT_QUERIES = [
    "Log a call with John Smith about project discussion",
    "Record an email interaction with Sarah Johnson about design review",
    "Show me all interactions with John Smith",
    "Add a note for Alice Johnson: 'Very interested in our premium package'",
]

COMMUNICATION_QUERIES = [
    "Send email to John Smith with subject 'Project Update' and message 'Hi John, project is on track for January deadline.'",
    "Email Sarah Johnson about the design review meeting",
]

EXPENSE_MANAGEMENT_QUERIES = [
    "Log an expense of $150 for 'Office Supplies' with description 'Notebooks and pens'",
    "Record a $800 expense for 'Software' category with description 'Annual CRM subscription'",
    "Create expense entry for $450 in 'Marketing' category for 'Google Ads campaign'",
]

REPORTING_QUERIES = [
    "Generate a business insights report",
    "Show me revenue report for all time",
    "Generate an expense report for all time",
    "Create a contact report",
    "Generate an invoice report for all time",
]

class BusinessAgentTester:
    def __init__(self, api_url=FLASK_API_URL, user_id=TEST_USER_ID, delay=DELAY_BETWEEN_TESTS):
        self.api_url = api_url
        self.user_id = user_id
        self.delay = delay
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
    def print_header(self, title):
        """Print a formatted header for test sections."""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        
    def print_test(self, test_name, status="RUNNING"):
        """Print test status."""
        status_symbols = {
            'RUNNING': '⏳',
            'PASS': '✅', 
            'FAIL': '❌',
            'ERROR': '💥'
        }
        symbol = status_symbols.get(status, '❓')
        print(f"{symbol} {test_name}")
        
    def check_api_health(self):
        """Check if the Flask API is running."""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"API returned status {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def send_chat_message(self, message):
        """Send a chat message to the Flask API."""
        try:
            payload = {
                "message": message,
                "user_id": self.user_id
            }
            response = requests.post(
                f"{self.api_url}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"API returned status {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
    
    def run_test_query(self, query, expected_keywords=None, should_fail=False):
        """Run a single test query and validate the response."""
        self.print_test(f"Testing: {query[:50]}{'...' if len(query) > 50 else ''}", "RUNNING")
        
        try:
            success, response = self.send_chat_message(query)
            
            if not success:
                self.print_test("API call failed", "ERROR")
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Query failed: {query[:50]} - {response}")
                return False
            
            response_text = response.get("response", "")
            
            # Check if test should fail (for edge cases)
            if should_fail:
                if "error" in response_text.lower() or "not found" in response_text.lower():
                    self.print_test("Expected failure - PASS", "PASS")
                    self.test_results['passed'] += 1
                    return True
                else:
                    self.print_test("Expected failure but succeeded - FAIL", "FAIL")
                    self.test_results['failed'] += 1
                    return False
            
            # Check for expected keywords in successful responses
            if expected_keywords:
                for keyword in expected_keywords:
                    if keyword.lower() not in response_text.lower():
                        self.print_test(f"Missing keyword '{keyword}' - FAIL", "FAIL")
                        self.test_results['failed'] += 1
                        self.test_results['errors'].append(f"Missing keyword '{keyword}' in response to: {query[:50]}")
                        return False
            
            # Check for error indicators in response
            error_indicators = ["error", "failed", "cannot", "unable to"]
            has_error = False
            for indicator in error_indicators:
                if indicator in response_text.lower() and "success" not in response_text.lower():
                    has_error = True
                    break
            
            if has_error:
                self.print_test(f"Error detected in response - FAIL", "FAIL")
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Error in response: {response_text[:100]}")
                return False
            
            self.print_test("PASS", "PASS")
            self.test_results['passed'] += 1
            
            # Print response summary for important queries
            if any(word in query.lower() for word in ['create', 'add', 'update', 'generate']):
                print(f"   📝 Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
            
            return True
            
        except Exception as e:
            self.print_test(f"Exception: {str(e)} - ERROR", "ERROR")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"Exception in query: {query[:50]} - {str(e)}")
            return False
    
    def test_basic_functionality(self):
        """Test basic system functionality."""
        self.print_header("BASIC FUNCTIONALITY TESTS")
        
        # Test API health
        self.print_test("API Health Check", "RUNNING")
        health_status, health_data = self.check_api_health()
        if health_status:
            self.print_test("API is running", "PASS")
            self.test_results['passed'] += 1
        else:
            self.print_test(f"API health check failed: {health_data}", "FAIL")
            self.test_results['failed'] += 1
            return False
        
        # Test basic chat functionality
        basic_queries = [
            "Hello, can you help me with my business?",
            "What can you do for me?",
            "Show me my business insights"
        ]
        
        for query in basic_queries:
            self.run_test_query(query)
            time.sleep(self.delay)
        
        return True
    
    def test_contact_management(self):
        """Test contact management functionality."""
        self.print_header("CONTACT MANAGEMENT TESTS")
        
        # Create test contacts first
        setup_contacts = [
            "Add a new contact named 'Test Alice' with email 'alice@test.com', company 'Test Corp', status 'prospect'",
            "Create a contact for 'Test Bob' from 'Bob Industries' with email 'bob@test.com'",
            "Add 'Test Carol' as a new lead with company 'Carol LLC' and email 'carol@test.com'"
        ]
        
        for query in setup_contacts:
            self.run_test_query(query, expected_keywords=["successfully", "added", "created"])
            time.sleep(self.delay)
        
        # Test contact search and management
        contact_tests = [
            ("Find all contacts named Test", ["found", "contact"]),
            ("Search for contacts from Test Corp", ["found", "Test Corp"]),
            ("Show me all my contacts", ["contact"]),
            ("Update Test Alice's status to client", ["updated", "success"]),
            ("Find contact with email alice@test.com", ["alice", "test.com"])
        ]
        
        for query, keywords in contact_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_invoice_management(self):
        """Test invoice management functionality."""
        self.print_header("INVOICE MANAGEMENT TESTS")
        
        # Create invoices using contact names
        invoice_tests = [
            ("Create a $1500 invoice for Test Alice due in 30 days", ["invoice", "created", "Test Alice"]),
            ("Generate a new invoice for Test Bob with total amount $2200", ["invoice", "success", "Test Bob"]),
            ("Show me all invoices for Test Alice", ["invoice", "Test Alice"]),
            ("Show me all unpaid invoices", ["unpaid", "invoice"]),
            ("Find all paid invoices", ["paid", "invoice"])
        ]
        
        for query, keywords in invoice_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_interaction_management(self):
        """Test interaction logging and retrieval."""
        self.print_header("INTERACTION MANAGEMENT TESTS")
        
        interaction_tests = [
            ("Log a call with Test Alice about project discussion", ["interaction", "logged", "Test Alice"]),
            ("Record an email interaction with Test Bob about design review", ["interaction", "success", "Test Bob"]),
            ("Show me all interactions with Test Alice", ["interaction", "Test Alice"]),
            ("Add a note for Test Carol: 'Very interested in our services'", ["interaction", "note"])
        ]
        
        for query, keywords in interaction_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_communication(self):
        """Test communication functionality."""
        self.print_header("COMMUNICATION TESTS")
        
        communication_tests = [
            ("Send email to Test Alice with subject 'Project Update' and message 'Hi Alice, project on track'", ["email", "sent", "Test Alice"]),
            ("Email Test Bob about the meeting tomorrow", ["email", "Test Bob"])
        ]
        
        for query, keywords in communication_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_expense_management(self):
        """Test expense tracking."""
        self.print_header("EXPENSE MANAGEMENT TESTS")
        
        expense_tests = [
            ("Log an expense of $150 for 'Office Supplies' with description 'Test supplies'", ["expense", "success", "150"]),
            ("Record a $500 expense for 'Software' category", ["expense", "software", "500"]),
            ("Add an expense: $75 for 'Travel'", ["expense", "travel"])
        ]
        
        for query, keywords in expense_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_event_management(self):
        """Test event scheduling."""
        self.print_header("EVENT MANAGEMENT TESTS")
        
        event_tests = [
            ("Schedule an event titled 'Test Meeting' for '2025-06-15 10:00:00' at 'Office'", ["event", "created", "Test Meeting"]),
            ("Show me all upcoming events", ["event"]),
            ("List my upcoming meetings and events", ["event"])
        ]
        
        for query, keywords in event_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_reporting(self):
        """Test reporting functionality."""
        self.print_header("REPORTING TESTS")
        
        reporting_tests = [
            ("Generate a business insights report", ["insight", "business"]),
            ("Show me revenue report for all time", ["revenue", "report"]),
            ("Generate an expense report", ["expense", "report"]),
            ("Create a contact report", ["contact", "report"]),
            ("Generate an invoice report", ["invoice", "report"])
        ]
        
        for query, keywords in reporting_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_natural_language_queries(self):
        """Test natural language understanding."""
        self.print_header("NATURAL LANGUAGE TESTS")
        
        natural_tests = [
            ("Who are my contacts from Test Corp?", ["contact", "Test Corp"]),
            ("How much money am I owed?", ["money", "owed"]),
            ("What's my biggest expense category?", ["expense", "category"]),
            ("Show me all clients", ["client"]),
            ("What needs immediate action?", ["action"])
        ]
        
        for query, keywords in natural_tests:
            self.run_test_query(query, expected_keywords=keywords)
            time.sleep(self.delay)
    
    def test_edge_cases(self):
        """Test error handling and edge cases."""
        self.print_header("EDGE CASE TESTS")
        
        edge_tests = [
            ("Find contact named 'Nonexistent Person'", ["not found", "no contact"], True),
            ("Create invoice for 'Unknown Client'", ["not found", "cannot"], True),
            ("Update NonexistentUser with new phone number", ["not found", "cannot"], True)
        ]
        
        for query, keywords, should_fail in edge_tests:
            self.run_test_query(query, expected_keywords=keywords, should_fail=should_fail)
            time.sleep(self.delay)
    
    def test_quick_queries(self):
        """Test the quick test queries."""
        self.print_header("QUICK TEST QUERIES")
        
        for query in QUICK_TEST_QUERIES[:5]:  # Test first 5 quick queries
            self.run_test_query(query)
            time.sleep(self.delay)
    
    def run_comprehensive_test(self):
        """Run all test categories."""
        print("🚀 Starting Comprehensive Business Agent Test Suite")
        print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API URL: {self.api_url}")
        print(f"👤 Test User ID: {self.user_id}")
        
        start_time = time.time()
        
        # Run all test categories
        test_categories = [
            self.test_basic_functionality,
            self.test_contact_management,
            self.test_invoice_management,
            self.test_interaction_management,
            self.test_communication,
            self.test_expense_management,
            self.test_event_management,
            self.test_reporting,
            self.test_natural_language_queries,
            self.test_edge_cases,
            self.test_quick_queries
        ]
        
        for test_func in test_categories:
            try:
                test_func()
            except Exception as e:
                print(f"💥 Test category failed with exception: {str(e)}")
                self.test_results['failed'] += 1
                self.test_results['errors'].append(f"Category {test_func.__name__} failed: {str(e)}")
        
        # Print final results
        self.print_final_results(start_time)
    
    def print_final_results(self, start_time):
        """Print comprehensive test results."""
        end_time = time.time()
        duration = end_time - start_time
        
        self.print_header("TEST RESULTS SUMMARY")
        
        total_tests = self.test_results['passed'] + self.test_results['failed']
        pass_rate = (self.test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests Run: {total_tests}")
        print(f"✅ Tests Passed: {self.test_results['passed']}")
        print(f"❌ Tests Failed: {self.test_results['failed']}")
        print(f"📈 Pass Rate: {pass_rate:.1f}%")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        
        if self.test_results['errors']:
            print(f"\n🔍 Error Details:")
            for i, error in enumerate(self.test_results['errors'][:10], 1):  # Show first 10 errors
                print(f"   {i}. {error}")
            if len(self.test_results['errors']) > 10:
                print(f"   ... and {len(self.test_results['errors']) - 10} more errors")
        
        # Overall status
        if pass_rate >= 90:
            print(f"\n🎉 EXCELLENT! Your Business Agent is working great!")
        elif pass_rate >= 75:
            print(f"\n👍 GOOD! Your Business Agent is mostly working well.")
        elif pass_rate >= 50:
            print(f"\n⚠️  NEEDS WORK! Several issues found.")
        else:
            print(f"\n🚨 CRITICAL! Major issues detected.")
        
        print(f"\n📝 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def run_specific_test_category(category_name, delay=DELAY_BETWEEN_TESTS):
    """Run tests for a specific category."""
    tester = BusinessAgentTester(delay=delay)
    
    if not tester.check_api_health()[0]:
        print("❌ API is not running. Please start your Flask app first.")
        return
    
    category_map = {
        'contact': tester.test_contact_management,
        'invoice': tester.test_invoice_management,
        'interaction': tester.test_interaction_management,
        'communication': tester.test_communication,
        'expense': tester.test_expense_management,
        'event': tester.test_event_management,
        'reporting': tester.test_reporting,
        'natural': tester.test_natural_language_queries,
        'edge': tester.test_edge_cases,
        'quick': tester.test_quick_queries
    }
    
    if category_name.lower() in category_map:
        print(f"🎯 Running {category_name.upper()} tests only...")
        start_time = time.time()
        category_map[category_name.lower()]()
        tester.print_final_results(start_time)
    else:
        print(f"❌ Unknown category: {category_name}")
        print(f"Available categories: {', '.join(category_map.keys())}")

def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Business Analyst Agent')
    parser.add_argument('--category', '-c', type=str, help='Test specific category only')
    parser.add_argument('--api-url', type=str, default=FLASK_API_URL, help='Flask API URL')
    parser.add_argument('--user-id', type=str, default=TEST_USER_ID, help='Test user ID')
    parser.add_argument('--delay', type=float, default=DELAY_BETWEEN_TESTS, help='Delay between tests')
    parser.add_argument('--quick', action='store_true', help='Run only quick tests')
    
    args = parser.parse_args()
    
    if args.category:
        run_specific_test_category(args.category, args.delay)
    else:
        tester = BusinessAgentTester(args.api_url, args.user_id, args.delay)
        tester.run_comprehensive_test()

if __name__ == "__main__":
    main() 