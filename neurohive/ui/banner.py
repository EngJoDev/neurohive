"""
NeuroHive - Cyberpunk ASCII Branding & Terminal Banner.
"""

from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from neurohive import __version__

NEURO_LOGO = r"""
    _   __ ______ __  __ ____  ____   __  __ _____ _    __ ______
   / | / // ____// / / // __ \/ __ \ / / / //  _/| |  / // ____/
  /  |/ // __/  / / / // /_/ // / / // /_/ / / /  | | / // __/   
 / /|  // /___ / /_/ // _, _// /_/ // __  /_/ /   | |/ // /___   
/_/ |_//_____/ \____//_/ |_| \____//_/ /_//___/   |___//_____/   
"""

def get_welcome_banner(port: int = 9090) -> Panel:
    text = Text()
    text.append(NEURO_LOGO, style="bold cyan")
    text.append("\n  🧠 Autonomous Multi-Agent Swarm Orchestrator & Sandboxed Code Execution\n", style="bold magenta")
    text.append(f"  v{__version__} | Port: {port} | Swarm: Atlas • Cygnus • Vanguard • Sentinel\n", style="dim white")
    text.append("  [Multi-Agent ReAct] • [Isolated Sandbox] • [Web Canvas Active]\n", style="bold yellow")

    return Panel(
        Align.center(text),
        border_style="bright_magenta",
        padding=(0, 2),
        subtitle="[bold green]Swarm: SYNCHRONIZED[/bold green] • [bold cyan]Sandbox: SECURE[/bold cyan]",
        subtitle_align="right"
    )
