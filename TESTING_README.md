# Testing Guide for Business Analyst Agent

## Quick Start

1. Start Flask API: `python main.py`
2. Run tests: `python run_tests.py`
3. Test in Streamlit: `streamlit run streamlit_app/app.py`

## Test Scripts

- `run_tests.py` - Interactive test runner
- `test_business_agent.py` - Comprehensive test suite
- `user_friendly_test_queries.py` - Collection of test queries

## User-Friendly Queries (No IDs Required!)

### Contact Management

- "Find all contacts named John"
- "Update John Smith's status to client"
- "Add contact 'Alice Johnson' with email 'alice@test.com'"

### Invoice Management

- "Create a $2500 invoice for John Smith due in 30 days"
- "Show me all unpaid invoices"
- "Find invoices for Sarah Johnson"

### Business Analytics

- "Generate business insights report"
- "What's my total outstanding amount?"
- "Show me revenue report"

## Running Tests

```bash
# Quick tests (5 min)
python test_business_agent.py --quick

# Full test suite (15 min)
python test_business_agent.py

# Interactive runner
python run_tests.py
```

Your agent now works with natural language instead of database IDs!
