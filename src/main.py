#!/usr/bin/env python3
"""
THE NERVE - A Cyberpunk Terminal RPG
Main Entry Point
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


def main():
    """Main entry point for THE NERVE"""
    console = Console()

    # Title screen with official logo
    title_art = """
████████╗██╗  ██╗███████╗
╚══██╔══╝██║  ██║██╔════╝
   ██║   ███████║█████╗
   ██║   ██╔══██║██╔══╝
   ██║   ██║  ██║███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝

███╗   ██╗███████╗██████╗ ██╗   ██╗███████╗
████╗  ██║██╔════╝██╔══██╗██║   ██║██╔════╝
██╔██╗ ██║█████╗  ██████╔╝██║   ██║█████╗
██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝
██║ ╚████║███████╗██║  ██║ ╚████╔╝ ███████╗
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝
    """

    title = Text(title_art, style="bold cyan", justify="center")
    tagline = Text("━━━ A Cyberpunk Terminal RPG ━━━", style="bold dim", justify="center")
    quote = Text('"Connect to THE NERVE. Feel everything."', style="italic cyan", justify="center")
    version = Text("Version 0.1.0 - Vertical Slice", style="dim", justify="center")

    console.print()
    console.print(Panel(
        Align.center(Text.assemble(title, "\n", tagline, "\n\n", quote, "\n", version)),
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()

    # Status message
    console.print("[yellow]🚧 Game in development - Vertical Slice Phase[/yellow]")
    console.print()
    console.print("[green]✅ Core systems implemented:[/green]")
    console.print("  • Game state management")
    console.print("  • Event system")
    console.print("  • Player entity with stats & skills")
    console.print("  • Dice rolling system (d20 + modifiers)")
    console.print("  • Save/load system")
    console.print("  • Data loading with JSON cache")
    console.print()
    console.print("[cyan]📍 Available content:[/cyan]")
    console.print("  • The Golden Drake (tavern location)")
    console.print("  • Bartender Tom (NPC with dialogue)")
    console.print("  • Ricky 'Fast Hands' Chen (tutorial enemy)")
    console.print("  • 6 unique items")
    console.print()
    console.print("[dim]To play the demo, run the test modules or wait for full game loop implementation.[/dim]")
    console.print()

    console.print("[bold cyan]⚡ THE NERVE pulses. Waiting for input...[/bold cyan]")
    input()


if __name__ == "__main__":
    main()
