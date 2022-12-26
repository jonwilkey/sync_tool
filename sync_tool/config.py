"""Module for parsing and load sync_tool's config."""

import json
from dataclasses import dataclass


@dataclass
class Config:
    """Dataclass for sync_tool config.

    :param local_to_s3_paths: Mapping of local to S3 filepaths/keys to sync
    :param s3_bucket: Name of S3 bucket to sync with
    :param direction: Direction to sync, either "up" or "down"
    """

    local_to_s3_paths: dict[str, str]
    s3_bucket: str
    direction: str

    def __post_init__(self) -> None:
        """Create :attr:`sync_plan` based on specified direction.

        :raises ValueError: If :attr:`self.direction` is not "up" or "down"
        """
        if self.direction == "up":
            self.sync_plan = {**self.local_to_s3_paths}
        elif self.direction == "down":
            self.sync_plan = {v: k for k, v in self.local_to_s3_paths.items()}
        else:
            raise ValueError(
                f"'{self.direction}' is not a valid value for the direction argument, "
                "please use either 'in' or 'out'"
            )


def load_config(config_file: str, direction: str) -> Config:
    """Load config from specified filepath and return as :py:class:`Config`.

    :param config_file: Path to config JSON file
    :param direction: Direction to sync, either "up" or "down"
    :return: Config object
    """
    with open(config_file, "r") as f:
        data = json.load(f)
    return Config(**data, direction=direction)
