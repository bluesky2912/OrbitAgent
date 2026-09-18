from orbit.tools.system import get_system_info, execute_terminal_command
from orbit.tools.filesystem import file_search, file_read, file_create, file_write

AVAILABLE_TOOLS = {
    "system_info": get_system_info,
    "terminal_execute": execute_terminal_command,
    "file_search": file_search,
    "file_read": file_read,
    "file_create": file_create,
    "file_write": file_write
}