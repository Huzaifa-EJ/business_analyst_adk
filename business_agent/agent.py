from google.adk.agents import Agent
from business_agent.prompt import BUSINESS_AGENT_PROMPT
from .tools.database_tools import (
    create_user,
    create_contact,
    read_all_contacts,
    update_contact,
    find_contact_by_name,
    find_contact_by_email,
    find_contact_by_company,
    update_contact_by_name,
    create_invoice,
    read_invoice,
    update_invoice,
    mark_invoice_paid,
    create_invoice_by_contact_name,
    find_invoices_by_contact_name,
    find_invoices_by_status,
    create_revenue,
    create_expense,
    create_event,
    list_upcoming_events,
    log_interaction,
    read_interactions,
    log_interaction_by_contact_name,
    read_interactions_by_contact_name,
    generate_report,
    send_email,
    send_email_by_contact_name,
    get_business_insights,
)


root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='business_analyst_agent',
    description='Intelligent Business Analyst Assistant with comprehensive database access for CRM, financial management, and business analytics.',
    instruction=BUSINESS_AGENT_PROMPT,
    tools=[
        # User management
        create_user,
        get_business_insights,
        
        # Contact management (with name-based tools)
        create_contact,
        read_all_contacts,
        update_contact,
        find_contact_by_name,
        find_contact_by_email,
        find_contact_by_company,
        update_contact_by_name,
        
        # Invoice management (with name-based tools)
        create_invoice,
        read_invoice,
        update_invoice,
        mark_invoice_paid,
        create_invoice_by_contact_name,
        find_invoices_by_contact_name,
        find_invoices_by_status,
        
        # Financial management
        create_revenue,
        create_expense,
        
        # Event management
        create_event,
        list_upcoming_events,
        
        # Interaction management (with name-based tools)
        log_interaction,
        read_interactions,
        log_interaction_by_contact_name,
        read_interactions_by_contact_name,
        
        # Communication (with name-based tools)
        send_email,
        send_email_by_contact_name,
        
        # Reporting and analytics
        generate_report,
    ]
)
