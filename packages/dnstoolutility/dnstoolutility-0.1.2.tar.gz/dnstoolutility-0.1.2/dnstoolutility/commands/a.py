from operator import attrgetter
from rich.console import Console
from rich.table import Table

from dnstoolutility.utility import monochecker


def check_for_site(domain: str, printing=True) -> dict:
    data_list = {}

    response1 = sorted(
        monochecker(domain, "A"), key=attrgetter("value", "domain")
    )

    response2 = sorted(
        monochecker("www" + domain, "A"), key=attrgetter("value", "domain")
    )

    response = response1 + response2

    data_list["A"] = response
    table = Table(title=f"A of the domain {domain}")

    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("N", style="magenta")

    for e in response:
        table.add_row(e[0], e[1])

    console = Console()
    if printing:
        console.print(table)

    return data_list
