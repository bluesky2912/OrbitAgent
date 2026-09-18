from enum import Enum
from typing import Dict, Any

class RiskLevel(Enum):
    SAFE = "SAFE"           # Auto-execute without asking
    REVIEW = "REVIEW"       # Pause, wait for 3 seconds or a quick 'y'
    CONFIRM = "CONFIRM"     # Require the user to explicitly type 'yes'
    BLOCK = "BLOCK"         # Reject the action completely

class SecurityGate:
    def __init__(self):
        # Define baseline risk profiles for our V1 tools
        self.tool_risks = {
            "system_info": RiskLevel.SAFE,
            "file_search": RiskLevel.SAFE,
            "file_read": RiskLevel.SAFE,
            "file_create": RiskLevel.REVIEW,
            "file_write": RiskLevel.REVIEW,
            "app_open": RiskLevel.REVIEW,
            "terminal_execute": RiskLevel.CONFIRM
        }

    def evaluate_action(self, tool_name: str, args: Dict[str, Any]) -> RiskLevel:
        # Default to BLOCK if the tool is unknown
        base_risk = self.tool_risks.get(tool_name, RiskLevel.BLOCK)
        
        # Contextual risk escalation: Block highly destructive terminal commands
        if tool_name == "terminal_execute":
            command = args.get("command", "").lower()
            # Catching common destructive commands on Windows and Linux
            dangerous_commands = ["rm -rf", "del /s /q", "format c:", "mkfs"]
            if any(cmd in command for cmd in dangerous_commands):
                return RiskLevel.BLOCK
                
        return base_risk

# Create a global instance we can import elsewhere
security_gate = SecurityGate()