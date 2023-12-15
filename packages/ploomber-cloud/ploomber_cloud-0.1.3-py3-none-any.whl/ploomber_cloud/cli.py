import click

from ploomber_cloud import api_key, deploy as deploy_, init as init_


@click.group()
def cli():
    pass


@cli.command()
@click.argument("key", type=str, required=True)
def key(key):
    """Set your API key"""
    api_key.set_api_key(key)


@cli.command()
@click.option(
    "--watch", is_flag=True, help="Track deployment status in the command line"
)
def deploy(watch):
    """Deploy your project to Ploomber Cloud"""
    deploy_.deploy(watch)


@cli.command()
@click.option(
    "--from-existing",
    "from_existing",
    is_flag=True,
    help="Choose an existing project to initialize from",
)
def init(from_existing):
    """Initialize a Ploomber Cloud project"""
    init_.init(from_existing)


if __name__ == "__main__":
    cli()
