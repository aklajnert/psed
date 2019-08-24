# -*- coding: utf-8 -*-

"""Console script for psed."""
import sys
import click

from .psed import Psed


@click.command()
@click.option(
    "-i", "--input", help="Path to the input file / directory.", required=True
)
@click.option("-f", "--find", help="String to find.", multiple=True)
@click.option("-r", "--replace", help="String to replace.")
@click.option(
    "--inplace", help="Modify the file(s) in place.", default=False, is_flag=True
)
def main(**kwargs):
    """Console script for psed."""
    psed = Psed(**kwargs)
    psed.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
