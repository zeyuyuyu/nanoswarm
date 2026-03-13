import argparse
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
import os
import sys

from nanoswarm.core import NanoSwarm

console = Console()

async def run_swarm(topic: str, model: str = "gpt-4o-mini", enable_search: bool = False):
    swarm = NanoSwarm(model=model, enable_search=enable_search)
    
    if enable_search:
        with console.status(f"[bold green]Gathering recent web context for: '{topic}'...", spinner="point"):
            await swarm._gather_context(topic)
            if swarm.global_context:
                console.print(Panel(Text(f"{len(swarm.global_context)} chars loaded from web.", style="dim italic"), title="[bold blue]Data Ingestion[/bold blue]"))
    
    with console.status(f"[bold green]Casting experts for: '{topic}'...", spinner="dots"):
        await swarm._cast_agents(topic)
        
    console.print(Panel(Text("\n".join([f"• [{a.name}]: {a.persona}" for a in swarm.agents])), title="[bold yellow]The Swarm Roster[/bold yellow]", border_style="yellow"))
    
    with console.status("[bold magenta]The Swarm is debating...[/bold magenta]", spinner="aesthetic"):
        debate_log = await swarm.debate(topic)
        
    for name, thought in debate_log.items():
        console.print(Panel(Markdown(thought), title=f"[bold green]Expert: {name}[/bold green]", border_style="cyan"))
        
    with console.status("[bold red]Synthesizing final verdict...[/bold red]", spinner="bouncingBar"):
        verdict = await swarm.synthesize(topic, debate_log)
        
    console.print(Panel(Markdown(verdict), title="[bold red]Final Verdict[/bold red]", border_style="red"))

def main():
    parser = argparse.ArgumentParser(description="NanoSwarm CLI")
    parser.add_argument("topic", type=str, help="The decision, problem, or topic to debate")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="LiteLLM compatible model name")
    parser.add_argument("--search", action="store_true", help="Enable DuckDuckGo search integration to gather recent context before the debate.")
    
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY") and args.model.startswith("gpt"):
        console.print("[bold red]Error: OPENAI_API_KEY environment variable not set[/bold red]")
        sys.exit(1)
        
    console.print(Panel(f"[bold blue]Welcome to NanoSwarm[/bold blue]\n[white]Topic:[/white] '{args.topic}'\n[white]Search Enabled:[/white] {args.search}", border_style="blue"))
    asyncio.run(run_swarm(args.topic, args.model, args.search))

if __name__ == "__main__":
    main()
