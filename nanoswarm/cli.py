import argparse
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
import os
import sys

from nanoswarm.core import NanoSwarm

console = Console()

async def run_swarm(topic: str, model: str = "gpt-4o-mini"):
    swarm = NanoSwarm(model=model)
    
    with console.status(f"[bold green]Casting experts for: '{topic}'...", spinner="dots"):
        await swarm._cast_agents(topic)
        
    console.print(Panel(Text("\n".join([f"• [bold cyan]{a.name}[/bold cyan]: {a.persona}" for a in swarm.agents])), title="[bold yellow]The Swarm[/bold yellow]", border_style="yellow"))
    
    with console.status("[bold magenta]The Swarm is debating...", spinner="aesthetic"):
        debate_log = await swarm.debate(topic)
        
    for name, thought in debate_log.items():
        console.print(Panel(Text(thought), title=f"[bold green]{name}[/bold green]", border_style="cyan"))
        
    with console.status("[bold red]Synthesizing final verdict...", spinner="bouncingBar"):
        verdict = await swarm.synthesize(topic, debate_log)
        
    console.print(Panel(Text(verdict), title="[bold red]Final Verdict[/bold red]", border_style="red"))

def main():
    parser = argparse.ArgumentParser(description="NanoSwarm CLI")
    parser.add_argument("topic", type=str, help="The decision, problem, or topic to debate")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="LiteLLM compatible model name")
    
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY") and args.model.startswith("gpt"):
        console.print("[bold red]Error: OPENAI_API_KEY environment variable not set[/bold red]")
        sys.exit(1)
        
    console.print(Panel(f"[bold blue]Welcome to NanoSwarm[/bold blue]\n[white]Topic:[/white] '{args.topic}'", border_style="blue"))
    asyncio.run(run_swarm(args.topic, args.model))

if __name__ == "__main__":
    main()
