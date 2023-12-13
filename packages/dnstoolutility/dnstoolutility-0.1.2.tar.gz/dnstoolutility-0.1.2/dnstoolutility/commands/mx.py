from operator import attrgetter
from rich.console import Console
from rich.table import Table

from dnstoolutility.utility import monochecker


def check_for_mail(domain: str, printing=True) -> dict:
    data_list = {}

    response = sorted(
        monochecker(domain, "MX"), key=attrgetter("value", "domain")
    )
    data_list["MX"] = response
    table = Table(title=f"MX of the domain {domain}")

    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("N", style="magenta")

    for e in response:
        table.add_row(e[0], e[1])

    console = Console()
    if printing:
        console.print(table)

    response = sorted(
        monochecker("pec." + domain, "MX"), key=attrgetter("value", "domain")
    )
    data_list["Pec"] = response

    table = Table(title=f"MX of the domain pec.{domain}")

    table.add_column("Value", justify="right", style="cyan", no_wrap=True)
    table.add_column("N", style="magenta")
    for e in response:
        table.add_row(e[0], e[1])

    if printing:
        console.print(table)
    return data_list
