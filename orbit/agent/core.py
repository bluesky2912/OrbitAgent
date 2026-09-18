import json
from litellm import completion
from orbit.security.gate import security_gate, RiskLevel
from orbit.tools.registry import AVAILABLE_TOOLS

# 1. Define the tools so the LLM knows they exist
LLM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Get basic information about the user's operating system.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminal_execute",
            "description": "Execute a terminal command on the user's system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The terminal command to run."
                    }
                },
                "required": ["command"]
            }
        }
    }
]

class OrbitAgent:
    def __init__(self, model_name="ollama/llama3"):
        # We prefix with "ollama/" so litellm knows where to route it
        self.model_name = model_name
        self.messages = [
            {
                "role": "system", 
                "content": "You are ORBIT, a local AI computer agent. You have tools to help the user. If you need system info or need to run a command, use the tools provided. Always be concise."
            }
        ]
        
    def chat(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        
        while True:
            # 2. Ask the LLM what to do next
            response = completion(
                model=self.model_name,
                messages=self.messages,
                tools=LLM_TOOLS,
                api_base="http://localhost:11434" # Default local Ollama port
            )
            
            message = response.choices[0].message
            
            # 3. Check if the LLM decided to use a tool
            if message.tool_calls:
                self.messages.append(message) # Save the AI's request to memory
                
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    # 4. INTERCEPT WITH SECURITY GATE
                    risk = security_gate.evaluate_action(tool_name, args)
                    
                    if risk == RiskLevel.BLOCK:
                        observation = "SYSTEM BLOCKED ACTION: Security violation."
                    elif risk in [RiskLevel.CONFIRM, RiskLevel.REVIEW]:
                        # Pause and ask the user in the terminal
                        print(f"\n⚠️  [SECURITY {risk.name}] ORBIT wants to run '{tool_name}' with arguments: {args}")
                        user_approval = input("Allow this action? (y/n): ")
                        
                        if user_approval.lower() != 'y':
                            observation = "USER CANCELLED ACTION."
                        else:
                            observation = AVAILABLE_TOOLS[tool_name](**args)
                    else:
                        # SAFE - execute automatically
                        observation = AVAILABLE_TOOLS[tool_name](**args)
                    
                    # 5. Feed the result back to the LLM
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(observation)
                    })
                # The loop restarts here, sending the observation back to the LLM
                
            else:
                # 6. No tools were called, meaning the AI has a final text answer
                final_text = message.content
                self.messages.append({"role": "assistant", "content": final_text})
                return final_text