import os
from argparse import ArgumentParser
from importlib.metadata import version

DEFAULT_CONFIGS = [
    "/etc/cflare-ddns.json",
    "cflare-ddns.json",
]

# 15 minutes
DEFAULT_INTERVAL = 60 * 15


def check_config():
    for conf in DEFAULT_CONFIGS:
        if os.path.exists(conf):
            return conf
    return None


def init():
    args_parse = ArgumentParser()

    existing_config = check_config()
    default_config = os.environ.get(
        "CF_DDNS_CONFIG",
        default=existing_config,
    )
    args_parse.add_argument(
        "-c",
        "--config",
        default=default_config,
        dest="config_file",
        type=str,
        required=default_config is None,
        help=(
            "Path to your configuration file. "
            f"Default paths: {', '.join(DEFAULT_CONFIGS)}"
        ),
    )

    args_parse.add_argument(
        "-i",
        "--interval",
        default=os.environ.get("CF_DDNS_INTERVAL"),
        dest="interval",
        type=int,
        help=(
            "Number of seconds between each sync. "
            "This will make the program run forever."
            "Hit Ctrl-C to stop."
        ),
    )

    args_parse.add_argument(
        "-v",
        "--version",
        action="version",
        version=version("cflare-ddns"),
        help="App version",
    )
    return args_parse
