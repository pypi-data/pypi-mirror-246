import whois

from rich.console import Console
from rich.table import Table


def is_registered(domain_name):
    """
    A function that returns a boolean indicating
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


def whois_query(domain_name: str):
    console = Console()
    table = Table(title=f"WHOIS of the domain {domain_name}")
    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("result", style="magenta")
    if is_registered(domain_name):
        whois_info = whois.whois(domain_name)
        table.add_row("Is registered?", "Yes")
        table.add_row("Domain registrar:", whois_info.registrar)
        table.add_row("WHOIS server:", whois_info.whois_server)
        table.add_row("Domain creation date:", whois_info.creation_date)
        table.add_row("Expiration date:", whois_info.expiration_date)
    else:
        table.add_row("Is registered?", "No")

    console.print(table)
