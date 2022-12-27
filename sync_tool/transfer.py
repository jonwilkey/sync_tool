"""Module for functions that define and enact transfer plan."""

import os

from sync_tool.config import Config
from sync_tool.s3 import get_keys


def get_src_dst_map(config: Config) -> dict[str, str]:
    """Get source to destination filepath/key mapping (depending on transfer direction).

    :param config: Sync configuration
    :return: Source to destination filepath/key mapping
    """
    if config.direction == "up":
        mapping = {
            os.path.join(root, name): os.path.join(
                prefix, root.removeprefix(path), name
            )
            for path, prefix in config.local_to_s3_paths.items()
            for root, _, files in os.walk(path)
            for name in files
        }
    if config.direction == "down":
        mapping = {
            key: os.path.join(path.removesuffix(f"{prefix}/"), key)
            for path, prefix in config.local_to_s3_paths.items()
            for key in get_keys(bucket=config.s3_bucket, prefix=prefix)
        }
    return mapping
