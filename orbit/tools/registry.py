from orbit.tools.system import get_system_info, execute_terminal_command

# This maps the tool name (which the AI uses) to the actual Python function
AVAILABLE_TOOLS = {
    "system_info": get_system_info,
    "terminal_execute": execute_terminal_command
}