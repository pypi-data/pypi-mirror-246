"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Libtest22."""


if __name__ == "__main__":
    main(prog_name="ssb-libtest22")  # pragma: no cover
