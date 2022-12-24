import click
import logging
from sync_tool.config import load_config


log = logging.getLogger()


@click.command()
@click.option("--up", is_flag=True, help="Upload files from local to S3")
@click.option("--down", is_flag=True, help="Download files from S3 to local")
@click.option(
    "--config-file", default="config.json", help="Sync config.json file location"
)
def run(up: bool, down: bool, config_file: str) -> None:
    if up == down:
        if up:
            raise ValueError("Please specify either --up or --down, not both")
        else:
            raise ValueError("Please specify either --up or --down")
    load_config(config_file)
    log.info("Starting sync")


if __name__ == "__main__":  # pragma no cover
    run()
