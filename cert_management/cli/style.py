from rich.console import Console
from rich.panel import Panel

console = Console()


def print_error(error) -> None:
    panel = Panel(error, title="[yellow]Error[/yellow]", style="bright_black")
    console.print(panel)


def print_main_help():
    message = """
     [#ffffff]
    There are 3 subcommands available for this application

    - [b]certificate-authority[/]: Interface for handle certificate authority
    - [b]private-key[/]: interface for handle private key


    [b]Para mais informações rápidas: [yellow]cert-management --help[/]

    [b]Para informações detalhadas: [blue][link=http://notas-musicais.readthedocs.io]acesse a documentação![/]
    [/]
    """
    panel = Panel(message, title="[yellow]Options[/]", style="bright_black")
    console.print(
        "[yellow]Usage[/yellow]: [b]cert_management [OPTIONS] COMMAND [ARGS]. [/]",
        panel,
    )
