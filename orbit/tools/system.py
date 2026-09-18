import platform
import subprocess
from typing import Dict, Any

def get_system_info() -> Dict[str, Any]:
    """Returns basic information about the operating system."""
    return {
        "os": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine()
    }

def execute_terminal_command(command: str) -> str:
    """Executes a terminal command and returns the output."""
    try:
        # We use shell=True to allow normal terminal syntax.
        # This is normally very dangerous, but our Security Gate will protect us.
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30 # Prevent commands that hang forever
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Command Error: {result.stderr.strip()}"
            
    except Exception as e:
        return f"Execution Failed: {str(e)}"