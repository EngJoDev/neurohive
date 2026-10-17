"""
NeuroHive - CLI Interface.
"""

import click
from rich.console import Console
from neurohive import __version__
from neurohive.ui.banner import get_welcome_banner
from neurohive.ui.server import ThreadedHTTPServer, NeuroHiveHandler

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--version", "-v", is_flag=True, help="Show NeuroHive version.")
def main(ctx: click.Context, version: bool):
    """NeuroHive - Multi-Agent Swarm Orchestrator & Execution Sandbox."""
    if version or ctx.invoked_subcommand is None:
        console.print(get_welcome_banner())
        if ctx.invoked_subcommand is None:
            console.print("[dim]Use [bold cyan]neurohive start[/bold cyan] to launch the Swarm Web Studio.[/dim]\n")

@main.command()
@click.option("--port", "-p", default=9090, help="Web studio port (default: 9090)")
def start(port: int):
    """Start the NeuroHive Swarm Web Studio & API Server."""
    console.print(get_welcome_banner(port=port))
    server_address = ("0.0.0.0", port)
    httpd = ThreadedHTTPServer(server_address, NeuroHiveHandler)
    
    console.print(f"[bold green]✔ NeuroHive Engine running on http://0.0.0.0:{port}[/bold green]")
    console.print(f"[bold cyan]⚡ Swarm Web Studio: http://localhost:{port}[/bold cyan]")
    console.print("[dim]Press Ctrl+C to terminate the swarm studio.[/dim]\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]▲ Disconnecting Swarm agents safely...[/bold yellow]")
        httpd.server_close()
        console.print("[bold green]✔ NeuroHive terminated.[/bold green]")

if __name__ == "__main__":
    main()
