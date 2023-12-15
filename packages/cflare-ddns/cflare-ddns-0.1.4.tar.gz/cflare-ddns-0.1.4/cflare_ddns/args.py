import os
from argparse import ArgumentParser

DEFAULT_CONFIG = "/etc/cflare-ddns.json"

# 15 minutes
DEFAULT_INTERVAL = 60 * 15


def init():
    args_parse = ArgumentParser()
    args_parse.add_argument(
        "-c",
        "--config",
        default=os.environ.get(
            "CF_DDNS_CONFIG",
            default=DEFAULT_CONFIG,
        ),
        dest="config_file",
        type=str,
        help="Path to your configuration file",
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
        ),
    )
    return args_parse
