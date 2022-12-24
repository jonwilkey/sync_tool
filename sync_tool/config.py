import json
from dataclasses import dataclass


@dataclass
class Config:
    local_to_s3_paths: dict[str, str]


def load_config(config_file: str) -> Config:
    with open(config_file, "r") as f:
        data = json.load(f)
    return Config(**data)
