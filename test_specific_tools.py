from business_agent.tools.database_tools import log_interaction, read_interactions, send_email, generate_report
import inspect

tools = [log_interaction, read_interactions, send_email, generate_report]

for tool in tools:
    sig = inspect.signature(tool)
    has_defaults = any(param.default != param.empty for param in sig.parameters.values())
    if has_defaults:
        print(f'{tool.__name__}: HAS DEFAULTS')
        for name, param in sig.parameters.items():
            if param.default != param.empty:
                print(f'   {name}: {param.default}')
    else:
        print(f'{tool.__name__}: No defaults') 