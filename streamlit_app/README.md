# Business Analyst Agent - Streamlit Interface

This is a user-friendly chat interface for the Business Analyst Agent built with Streamlit.

## Quick Start

### 1. Start the Flask API Backend

First, make sure your Flask API is running:

```bash
python main.py
```

The API should be available at `http://localhost:5000`

### 2. Run the Streamlit App

From the project root directory, run:

```bash
streamlit run streamlit_app/app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## Features

### 🗣️ Chat Interface

- Natural language chat with your business agent
- Real-time responses with tool execution tracking
- Chat history with response metadata

### 📊 Quick Data Access (Sidebar)

- **Business Insights**: Get comprehensive business performance metrics
- **Revenue Report**: View all-time revenue breakdown
- **Expense Report**: Analyze expenses by category
- **Contact Report**: Overview of all contacts and their statuses
- **Invoice Report**: Invoice summary with status breakdown
- **Raw Data**: Direct access to database records

### 💡 Sample Questions

The app includes pre-built sample questions to get you started:

- "Show me all my contacts"
- "What are my unpaid invoices?"
- "Generate a revenue report for all time"
- "Give me business insights and recommendations"
- "Create a new contact named 'Jane Doe' from 'ABC Corp'"
- "Log an expense of $200 for 'Office Supplies'"
- "Schedule a meeting with John Smith titled 'Quarterly Review'"
- "Send an email to Sarah Johnson with subject 'Project Update'"

## Settings

### User ID

- Default user ID is `huzaifa_ejaz` (matches sample data)
- You can change this in the sidebar to access different user data
- The agent will automatically create new users if they don't exist

### API Health Check

- The sidebar shows real-time API connection status
- Displays API details including available tools and database counts
- Warns you if the Flask backend is not running

## Troubleshooting

### API Not Responding

If you see "❌ API is not responding":

1. Make sure Flask app is running: `python main.py`
2. Check that it's accessible at `http://localhost:5000/health`
3. Verify no firewall is blocking the connection

### No Data Showing

If queries return empty results:

1. Check that you're using the correct `user_id` (default: `huzaifa_ejaz`)
2. Verify the database has sample data by checking the health endpoint
3. Try the "Raw Data" button to see what's in the database

### Chat Not Working

If chat responses are failing:

1. Check the Flask logs for any errors
2. Try the simple question: "Show me all my contacts"
3. Check Response Details in the Streamlit app for debugging info

## Tips

- Use the **Response Details** expander to see tool call information
- The **Message Details** show metadata for each response
- Clear chat history with the "🗑️ Clear Chat" button
- Use the sidebar quick queries for instant data access
- Sample questions are great for testing functionality

Enjoy using your Business Analyst Agent! 🚀
