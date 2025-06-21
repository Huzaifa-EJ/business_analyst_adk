#!/usr/bin/env python3
"""
Simple Test Runner for Business Analyst Agent

This script provides an easy way to run different types of tests
and includes manual testing prompts for interactive testing.
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

FLASK_API_URL = "http://localhost:5000"

def check_api_status():
    """Check if the Flask API is running."""
    try:
        response = requests.get(f"{FLASK_API_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_quick_tests():
    """Run quick tests to verify basic functionality."""
    print("🚀 Running Quick Tests...")
    subprocess.run([sys.executable, "test_business_agent.py", "--quick"])

def run_full_tests():
    """Run comprehensive tests."""
    print("🚀 Running Full Test Suite...")
    subprocess.run([sys.executable, "test_business_agent.py"])

def run_manual_tests():
    """Run manual interactive tests."""
    print_header("MANUAL TESTING MODE")
    print("📝 You can now test the agent manually with these sample queries:")
    print("   (Press Ctrl+C to exit manual testing)\n")
    
    sample_queries = [
        "Find all contacts named John",
        "Show me all unpaid invoices",
        "Create a $1500 invoice for John Smith due in 30 days",
        "Log a call with Sarah Johnson about project status", 
        "Generate a business insights report",
        "Add a new contact named 'Test Contact' with email 'test@example.com'",
        "Update John Smith's status to client",
        "Show me all interactions with John Smith",
        "Send email to Sarah Johnson with subject 'Test Email'",
        "What's my total outstanding invoice amount?"
    ]
    
    print("💡 Sample queries to try:")
    for i, query in enumerate(sample_queries, 1):
        print(f"   {i:2d}. {query}")
    
    print(f"\n🌐 Open your Streamlit app or use the Flask API directly")
    print(f"   Streamlit: streamlit run streamlit_app/app.py")
    print(f"   Flask API: {FLASK_API_URL}")
    
    try:
        input("\n📱 Press Enter when you're done with manual testing...")
    except KeyboardInterrupt:
        print("\n👋 Manual testing completed!")

def test_specific_queries():
    """Test specific user-friendly queries."""
    print_header("TESTING SPECIFIC USER-FRIENDLY QUERIES")
    
    # Import the test script functions
    from test_business_agent import BusinessAgentTester
    
    tester = BusinessAgentTester()
    
    # Check API first
    if not tester.check_api_health()[0]:
        print("❌ Flask API is not running!")
        print("   Please start it with: python main.py")
        return
    
    print("✅ API is running. Testing specific queries...\n")
    
    # Test specific user-friendly queries
    test_queries = [
        ("Find contacts named John", ["contact", "john"]),
        ("Show unpaid invoices", ["unpaid", "invoice"]),
        ("Create contact 'Quick Test' with email 'quick@test.com'", ["contact", "created", "success"]),
        ("Generate business insights", ["insight", "business"]),
        ("Show all my contacts", ["contact"])
    ]
    
    for query, expected_keywords in test_queries:
        print(f"🔍 Testing: {query}")
        result = tester.run_test_query(query, expected_keywords)
        time.sleep(1)
        print()
    
    # Print summary
    total = len(test_queries)
    passed = tester.test_results['passed']
    print(f"📊 Results: {passed}/{total} tests passed")

def main():
    """Main menu for test runner."""
    print_header("BUSINESS ANALYST AGENT TEST RUNNER")
    print("📅 " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Check API status
    api_running = check_api_status()
    if api_running:
        print("✅ Flask API is running")
    else:
        print("❌ Flask API is NOT running")
        print("   Start it with: python main.py")
    
    while True:
        print("\n🎯 Choose a testing option:")
        print("   1. Quick Tests (5 min) - Basic functionality")
        print("   2. Full Test Suite (15 min) - Comprehensive tests")
        print("   3. Manual Testing - Interactive testing with sample queries")
        print("   4. Test Specific Queries - Test key user-friendly queries")
        print("   5. Check API Status")
        print("   6. Exit")
        
        try:
            choice = input("\n👉 Enter your choice (1-6): ").strip()
            
            if choice == "1":
                if not api_running:
                    print("❌ Please start the Flask API first!")
                    continue
                run_quick_tests()
                
            elif choice == "2":
                if not api_running:
                    print("❌ Please start the Flask API first!")
                    continue
                run_full_tests()
                
            elif choice == "3":
                run_manual_tests()
                
            elif choice == "4":
                test_specific_queries()
                
            elif choice == "5":
                print("🔍 Checking API status...")
                api_running = check_api_status()
                if api_running:
                    print("✅ Flask API is running and healthy")
                else:
                    print("❌ Flask API is not responding")
                    print("   Start it with: python main.py")
                    
            elif choice == "6":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 