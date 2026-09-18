from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from orbit.agent.core import OrbitAgent

console = Console()

def print_header():
    console.clear()
    header_text = Text("              ORBIT                   \n        LOCAL AI COMPUTER AGENT       ", style="bold cyan")
    console.print(Panel(header_text, border_style="cyan", expand=False))
    console.print("  [bold green]●[/bold green] SYSTEM READY")
    console.print("  [bold green]●[/bold green] MODEL: LOCAL (Ollama)")
    console.print("  [bold green]●[/bold green] TOOLS: 2")
    console.print("  [bold green]●[/bold green] MEMORY: ENABLED\n")

def main():
    print_header()
    agent = OrbitAgent() # Defaults to ollama/llama3
    
    while True:
        try:
            # The prompt
            user_input = console.input("[bold cyan]orbit >[/bold cyan] ")
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("[yellow]Shutting down ORBIT...[/yellow]")
                break
            if not user_input.strip():
                continue
                
            # Trigger the AI loop
            response = agent.chat(user_input)
            
            # Print the AI's final answer
            console.print(f"\n[bold magenta]ORBIT:[/bold magenta]\n{response}\n")
            
        except KeyboardInterrupt:
            # Handles Ctrl+C gracefully
            console.print("\n[yellow]Shutting down ORBIT...[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]System Error:[/bold red] {str(e)}\n")

if __name__ == "__main__":
    main()