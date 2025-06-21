from business_agent.tools.database_tools import *
import inspect

# Check all major tools
tools = [
    create_user, create_contact, read_all_contacts, update_contact,
    find_contact_by_name, find_contact_by_email, find_contact_by_company, update_contact_by_name,
    create_invoice, read_invoice, update_invoice, mark_invoice_paid,
    create_invoice_by_contact_name, find_invoices_by_contact_name, find_invoices_by_status,
    create_revenue, create_expense, create_event, list_upcoming_events,
    log_interaction, read_interactions, log_interaction_by_contact_name, read_interactions_by_contact_name,
    send_email, send_email_by_contact_name, generate_report, get_business_insights
]

print("Checking all tools for default values...")
has_any_defaults = False

for tool in tools:
    try:
        sig = inspect.signature(tool)
        has_defaults = any(param.default != param.empty for param in sig.parameters.values())
        if has_defaults:
            print(f"❌ {tool.__name__}: HAS DEFAULTS")
            for name, param in sig.parameters.items():
                if param.default != param.empty:
                    print(f"   {name}: {param.default}")
            has_any_defaults = True
        else:
            print(f"✅ {tool.__name__}: No defaults")
    except Exception as e:
        print(f"❓ {tool.__name__}: Error checking - {e}")

if has_any_defaults:
    print("\n❌ Some tools still have default values!")
else:
    print("\n✅ All tools are clean - no default values found!") 