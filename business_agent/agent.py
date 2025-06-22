from google.adk.agents import LlmAgent
from business_agent.prompt import BUSINESS_AGENT_PROMPT
from .tools.database_tools import (
    create_contact,
    read_all_contacts,
    create_invoice,
    read_invoice,
    mark_invoice_paid,
    get_unpaid_invoices,
    create_revenue,
    create_expense,
    create_event,
    list_upcoming_events,
    log_interaction,
    read_interactions,
    generate_report,
    get_business_insights,
    profit_loss_report,
    get_current_datetime,
)

root_agent = LlmAgent(
    model='gemini-2.0-flash-001',
    name='business_analyst_agent',
    description='Intelligent Business Analyst Assistant with comprehensive database access for CRM, financial management, and business analytics.',
    instruction=BUSINESS_AGENT_PROMPT,
    tools=[
        get_business_insights,
        create_contact,
        read_all_contacts,
        create_invoice,
        read_invoice,
        mark_invoice_paid,
        get_unpaid_invoices,
        create_revenue,
        create_expense,
        create_event,
        list_upcoming_events,
        log_interaction,
        read_interactions,
        generate_report,
        profit_loss_report,
        get_current_datetime,
    ]
)
