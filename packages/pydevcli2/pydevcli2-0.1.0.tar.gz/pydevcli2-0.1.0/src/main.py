"""Main CLI to manage other scripts
"""
from typer import Typer

cli = Typer()


@cli.command()
def hello(name: str):
    """Say hello NAME

    Args:
        name (str): _description_
    """
    print(f"Hello {name}")


if __name__ == "__main__":
    cli()
