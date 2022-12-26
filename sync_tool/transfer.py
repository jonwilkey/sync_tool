"""Module for functions that define and enact transfer plan."""

import os

from sync_tool.config import Config


def get_src_dst_map(config: Config):
    """Get source to destination filepath/key mapping (depending on transfer direction).

    :param config: Sync configuration
    :raises NotImplementedError: _description_
    :return: Source to destination filepath/key mapping
    """
    mapping: dict[str, str] = {}
    for path, prefix in config.local_to_s3_paths.items():
        if config.direction == "up":
            for root, _, files in os.walk(path):
                for name in files:
                    mapping[os.path.join(root, name)] = os.path.join(
                        prefix, root.removeprefix(path), name
                    )
        if config.direction == "down":
            raise NotImplementedError("TODO")
    return mapping
