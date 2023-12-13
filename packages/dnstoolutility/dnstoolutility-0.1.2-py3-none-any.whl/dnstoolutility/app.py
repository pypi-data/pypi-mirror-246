import click
from rich.console import Console
from rich.text import Text

from dnstoolutility.commands.a import check_for_site
from dnstoolutility.commands.mx import check_for_mail
from dnstoolutility.commands.ns import check_for_ns
from dnstoolutility.commands.whoisq import whois_query
from dnstoolutility.config import Config


@click.group()
@click.option(
    "--path", default="~/.config/dns-tool.json", help="Path off the config"
)
@click.pass_context
def cli(ctx, path: str):
    ctx.obj = Config(path)
    console = Console()
    text = Text("Hello, World!")
    text.stylize("bold magenta")
    console.print(text)


@cli.command()
@click.pass_obj
def update_config(config):
    console = Console()
    text = Text(f"Update the config\n")
    console.print(text)
    config.override_default()


@cli.command()
@click.option("--printing", default=True, help="Print the DNS results")
@click.argument("domain")
@click.pass_obj
def a(config, domain, printing):
    console = Console()
    text = Text(f"Searching info about A for the domain {domain}\n")
    console.print(text)
    check_for_site(domain, printing)


@cli.command()
@click.option("--printing", default=True, help="Print the DNS results")
@click.argument("domain")
@click.pass_obj
def mx(config, domain, printing):
    console = Console()
    text = Text(f"Searching info about MX for the domain {domain}\n")
    console.print(text)
    check_for_mail(domain, printing)


@cli.command()
@click.option("--printing", default=True, help="Print the DNS results")
@click.argument("domain")
@click.pass_obj
def ns(config, domain, printing):
    console = Console()
    text = Text(f"Searching info about NS for the domain {domain}\n")
    console.print(text)
    check_for_ns(domain, printing)


@cli.command()
@click.argument("domain")
@click.pass_obj
def update_config(config, domain):
    console = Console()
    text = Text(f"Search for the WHOIS of {domain}\n")
    console.print(text)
    whois_query(domain)
