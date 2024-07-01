import glob
import logging
import os
from typing import Any

import toml


def load_config(file_path: str="pypelines.toml"):
    """Load the configuration file as a TOML object."""
    with open(file_path, "r") as config_file:
        config = toml.load(config_file)
    return config


def get_pipeline_file_paths(config: dict[str, Any]):
    """Retrieves a list of all pipeline files in the configured paths and sub-paths."""
    pipeline_files = set()
    if "files" in config.get("tool", {}).get("pypelines", {}):
        for path in config["tool"]["pypelines"]["files"]:
            # If the configured path is a directory, get all Python files inside of it.
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith(".py"):
                            pipeline_files.add(os.path.join(root, file))
            # If the path is a file pattern, iterate according to the pattern.
            elif "*" in path or "?" in path or "[" in path:
                for matched_file in glob.glob(path, recursive=True):
                    pipeline_files.add(matched_file)
            # If the path is a specific file, add it.
            elif os.path.isfile(path):
                pipeline_files.add(path)
            else:
                logging.warning(
                    f"[tool.pypelines.files] {path} is neither a valid directory, "
                    "file pattern, nor a specific file."
                )
    return list(pipeline_files)
