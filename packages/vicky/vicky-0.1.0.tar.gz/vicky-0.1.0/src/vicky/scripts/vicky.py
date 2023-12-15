import click

from vicky.deployment import Deployment


@click.group()
def cli():
    pass


@click.command()
@click.argument("theme")
@click.argument("directory")
@click.option("--api-key", default=None, help="API key of a Vicky instance.")
@click.option(
    "--version",
    default=None,
    help="version to be set after a successful deployment of a theme.",
)
def deploy(theme, directory, api_key, version):
    """Deploy a theme to a Vicky instance."""
    deployment = Deployment(theme, directory, api_key=api_key, version=version)
    res = deployment.run()
    click.echo(res)


cli.add_command(deploy)


if __name__ == "__main__":
    cli()
