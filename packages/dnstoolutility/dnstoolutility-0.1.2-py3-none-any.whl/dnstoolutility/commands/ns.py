from operator import attrgetter
from rich.console import Console
from rich.table import Table

from dnstoolutility.utility import monochecker


def check_for_ns(domain: str, printing=True) -> dict:
    data_list = {}

    response = sorted(
        monochecker(domain, "NS"), key=attrgetter("value", "domain")
    )

    data_list["NS"] = response
    table = Table(title=f"NS of the domain {domain}")

    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("N", style="magenta")

    for e in response:
        table.add_row(e[0], e[1])

    console = Console()
    if printing:
        console.print(table)

    return data_list
