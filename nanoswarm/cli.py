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

async def run_swarm(topic: str, model: str = "gpt-4o-mini", enable_search: bool = False, mode: str = "debate", rounds: int = 2):
    swarm = NanoSwarm(model=model, enable_search=enable_search)
    
    if enable_search:
        with console.status(f"[bold green]Gathering live intelligence for: '{topic}'...", spinner="point"):
            await swarm._gather_context(topic)
            if swarm.global_context:
                console.print(Panel(Text(f"[Found {len(swarm.global_context)} chars of live context]", style="dim italic"), title="[bold blue]Data Intelligence[/bold blue]"))
    
    with console.status(f"[bold green]Casting experts for: '{topic}'...", spinner="dots"):
        await swarm._cast_agents(topic)
        
    console.print(Panel(Text("\n".join([f"• [{a.name}]: {a.persona}" for a in swarm.agents])), title="[bold yellow]Swarm Roster[/bold yellow]", border_style="yellow"))
    
    if mode == "predict":
        with console.status("[bold magenta]The Swarm is predicting probabilities...[/bold magenta]", spinner="aesthetic"):
            predictions = await swarm.predict(topic)
            
        console.print(f"\n[bold white]Aggregate Swarm Probability:[/bold white] [bold red]{predictions['average_probability']}%[/bold red]\n")
        
        for name, p_data in predictions['breakdown'].items():
            content = f"[bold green]Probability: {p_data.get('probability', 'N/A')}%[/bold green]\n\n{p_data.get('reasoning', 'No reasoning provided.')}"
            console.print(Panel(content, title=f"Prediction: {name}", border_style="cyan"))
    else:    
        all_rounds = await swarm.debate(topic, rounds=rounds)
        for idx, round_data in enumerate(all_rounds):
            console.print(f"\n[bold underline white]Round {idx+1}[/bold underline white]\n")
            for name, thought in round_data.items():
                console.print(Panel(Markdown(thought), title=f"[bold green]{name}[/bold green]", border_style="cyan"))
            
        with console.status("[bold red]Synthesizing final verdict...[/bold red]", spinner="bouncingBar"):
            verdict = await swarm.synthesize(topic)
            
        console.print(Panel(Markdown(verdict), title="[bold red]Swarm Verdict[/bold red]", border_style="red"))

def main():
    parser = argparse.ArgumentParser(description="NanoSwarm CLI")
    parser.add_argument("topic", type=str, help="The decision, problem, or topic to simulate")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="LiteLLM compatible model name")
    parser.add_argument("--search", action="store_true", help="Enable DuckDuckGo search integration to gather recent context.")
    parser.add_argument("--mode", type=str, choices=["debate", "predict"], default="debate", help="Swarm behavior mode: debate decisions, or predict event probabilities (like MiroFish).")
    parser.add_argument("--rounds", type=int, default=1, help="Number of debate rounds (for 'debate' mode). Mutli-round allows them to argue.")
    
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY") and args.model.startswith("gpt"):
        console.print("[bold red]Error: OPENAI_API_KEY environment variable not set[/bold red]")
        sys.exit(1)
        
    console.print(Panel(f"[bold blue]Welcome to NanoSwarm[/bold blue]\n[white]Topic:[/white] '{args.topic}'\n[white]Mode:[/white] {args.mode.upper()}", border_style="blue"))
    asyncio.run(run_swarm(args.topic, args.model, args.search, args.mode, args.rounds))

if __name__ == "__main__":
    main()
